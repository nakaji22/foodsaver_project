# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), #URLパス,どのviewを呼び出すか,URLの名前(templatesの引数として使う)
    path('foods/<int:pk>/', views.food_detail, name='food_detail'), #<int:pkでモデルの主キーを受けとる>
    path('edit/<int:pk>/', views.food_edit, name='food_edit'),  # 編集
    path('delete/<int:pk>/', views.food_delete, name='food_delete'),  # 削除
    path('analysis/', views.monthly_analysis, name='monthly_analysis'),
]
