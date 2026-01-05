from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Article
from .forms import ReviewForm, ArticleForm

# 商品一覧
def product_list(request):
    category = request.GET.get('category')  # URLパラメータ ?category=xxx を取得

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    return render(request, 'products/product_list.html', {
        'products': products,
        'selected_category': category,
    })


# 商品詳細 + レビュー投稿
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })


# レビュー一覧（自分のレビュー管理ページ）
def my_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'products/my_reviews.html', {'reviews': reviews})


# レビュー編集
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('my_reviews')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'products/edit_review.html', {'form': form})


# レビュー削除
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('my_reviews')


# 記事一覧
def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'products/article_list.html', {'articles': articles})


# 記事詳細
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'products/article_detail.html', {'article': article})


# 記事作成
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'products/article_create.html', {'form': form})


# 記事編集
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'products/article_edit.html', {'form': form})


# 記事削除
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article_list')


# ホーム
def home(request):
    return render(request, 'products/home.html')

# --- 認証機能（ログイン・ログアウト・サインアップ） ---
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# ログイン
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'product_list')
            return redirect(next_url)
        else:
            return render(request, 'products/login.html', {'error': 'ログインに失敗しました'})

    return render(request, 'products/login.html')


# ログアウト
def logout_view(request):
    logout(request)
    return redirect('product_list')


# サインアップ
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'products/signup.html', {'error': 'このユーザー名は既に使われています'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('product_list')

    return render(request, 'products/signup.html')