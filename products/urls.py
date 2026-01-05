from django.urls import path
from . import views
from .views import signup_view   # ← これが必要！

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),

    path('myreviews/', views.my_reviews, name='my_reviews'),
    path('review/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),

    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),

    path('home/', views.home, name='home'),

    # ★ ログイン・ログアウトはここに置かない（shopproject/urls.py で管理）
    # path('accounts/login/', views.login_view, name='login'),
    # path('accounts/logout/', views.logout_view, name='logout'),

    # ★ サインアップだけここで定義
    path('signup/', signup_view, name='signup'),
]