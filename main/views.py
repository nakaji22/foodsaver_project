from django.shortcuts import render, redirect
from .models import FoodItem
from .forms import FoodItemForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def home(request):
    # POST: フォームから新規登録
    if request.method == 'POST': #ユーザーがフォームを送信した時
        form = FoodItemForm(request.POST) #送信されたフォームのデータ
        if form.is_valid():
            food = form.save(commit=False) #問題なければインスタンス作成(まだDBには保存しない)
            food.author = request.user #現在ログイン中のユーザーを紐づける
            food.save() #DBに保存
            return redirect('home')
    else:
        form = FoodItemForm() #GETのとき(初回ログイン時など)は空のフォームを表示

    # 登録済み食材一覧を取得（ユーザーごとに）
    food_items = FoodItem.objects.filter(author=request.user).order_by('expiration_date') #消費期限の近い順に並べる

    return render(request, 'main/home.html', {
        'form': form,
        'food_items': food_items,
    })

@login_required
def food_detail(request, pk): # 該当ユーザーの食材から対象の1つを取得（なければ404）
    food = get_object_or_404(FoodItem, pk=pk, author=request.user) #DBから主キーpkを用いて対象の食材を取得
    return render(request, 'main/food_detail.html', {'food': food}) #食材の詳細ページを表示