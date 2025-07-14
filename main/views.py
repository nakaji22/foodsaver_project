from django.shortcuts import render, redirect
from .models import FoodItem, CATEGORY_CHOICES
from .forms import FoodItemForm, FoodSearchForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.db.models import Sum
from django.http import HttpResponse
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
import io
import base64


def home(request):
    # 登録フォーム処理
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.author = request.user
            food.save()
            return redirect('home')
    else:
        form = FoodItemForm()

    # 検索フォームの処理
    search_form = FoodSearchForm(request.GET) #FoodSearchFormを入力した場合のみ
    food_items = FoodItem.objects.filter(author=request.user)

    if search_form.is_valid(): # 検索フォームが有効な場合検索条件に基づいてフィルタリング
        name = search_form.cleaned_data.get('name')
        category = search_form.cleaned_data.get('category')
        max_days_left = search_form.cleaned_data.get('max_days_left')
        max_price = search_form.cleaned_data.get('max_price')

        if name:
            food_items = food_items.filter(name__icontains=name)
        if category:
            food_items = food_items.filter(category=category)
        if max_days_left is not None:
            today = timezone.now().date()
            deadline = today + timedelta(days=max_days_left)
            food_items = food_items.filter(expiration_date__range=(today, deadline))
        if max_price is not None:
            food_items = food_items.filter(price__lte=max_price)

    today = timezone.now()

    return render(request, 'main/home.html', {
        'form': form,
        'search_form': search_form,
        'food_items': food_items,
        'month': today.strftime('%Y年%m月'),
    })


@login_required
def food_detail(request, pk): # 該当ユーザーの食材から対象の1つを取得（なければ404）
    food = get_object_or_404(FoodItem, pk=pk, author=request.user) #DBから主キーpkを用いて対象の食材を取得
    return render(request, 'main/food_detail.html', {'food': food}) #食材の詳細ページを表示

@login_required
def food_edit(request, pk):
    food = get_object_or_404(FoodItem, pk=pk, author=request.user)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FoodItemForm(instance=food)
    return render(request, 'main/food_edit.html', {'form': form})

@login_required
def food_delete(request, pk):
    food = get_object_or_404(FoodItem, pk=pk, author=request.user)
    if request.method == 'POST':
        food.delete()
        return redirect('home')
    return render(request, 'main/food_confirm_delete.html', {'food': food})

@login_required
def monthly_analysis(request):
    user = request.user
    today = timezone.now().date()
    month_start = today.replace(day=1)
    next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)

    items = FoodItem.objects.filter(
        author=user,
        purchase_date__gte=month_start,
        purchase_date__lt=next_month
    )

    font_path = 'NotoSansCJKjp-Regular.otf'
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

    # カテゴリ別合計金額
    category_sums = items.values('category').annotate(total=Sum('price'))

    # 合計金額
    total_price = items.aggregate(total=Sum('price'))['total'] or 0

    # 円グラフ描画
    labels = [dict(CATEGORY_CHOICES)[c['category']] for c in category_sums]
    sizes = [c['total'] for c in category_sums]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', textprops={'fontproperties': font_prop})
    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return render(request, 'main/analysis.html', {
        'category_sums': category_sums,
        'total_price': total_price,
        'chart': img_base64,
        'month': today.strftime('%Y年%m月'),
    })