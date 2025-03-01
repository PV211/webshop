from cart.models import CartItem

def cart_count(request):
    uid = request.user.id
    cart_items = CartItem.objects.filter(user__id = uid)

    return {'cart_count': len(cart_items)}