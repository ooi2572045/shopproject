from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem
from products.models import Product


# 商品をカートに追加
def add_to_cart(request, product_id):

    # ★ ログインしていない場合は HOME に戻す
    if not request.user.is_authenticated:
        messages.error(request, "まだログインしていないので買えません。")
        return redirect('/')

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# カートページ
def cart_page(request):

    if not request.user.is_authenticated:
        messages.error(request, "ログインしていません。")
        return redirect('/')

    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


# 数量増やす
def increase_quantity(request, item_id):

    if not request.user.is_authenticated:
        messages.error(request, "ログインしていません。")
        return redirect('/')

    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')


# 数量減らす
def decrease_quantity(request, item_id):

    if not request.user.is_authenticated:
        messages.error(request, "ログインしていません。")
        return redirect('/')

    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


# 削除
def remove_item(request, item_id):

    if not request.user.is_authenticated:
        messages.error(request, "ログインしていません。")
        return redirect('/')

    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')


# チェックアウト
def checkout_page(request):

    if not request.user.is_authenticated:
        messages.error(request, "ログインしていません。")
        return redirect('/')

    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


# 注文完了
def order_complete(request):

    if not request.user.is_authenticated:
        messages.error(request, "ログインしていません。")
        return redirect('/')

    cart_items = CartItem.objects.filter(user=request.user)

    items_to_show = []
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        items_to_show.append(item)

    cart_items.delete()

    return render(request, 'cart/complete.html', {
        'items': items_to_show
    })