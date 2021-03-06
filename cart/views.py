from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from cart.forms import AddToCartForm, DeleteCartItem
from cart.models import Cart, Item


# class CartPage(TemplateView):
#     template_name = 'cart.html'
#
#     def get_context_data(self, **kwargs):
#         user = self.request.user
#         context = super(CartPage, self).get_context_data(**kwargs)
#         cart = Cart.objects.filter(owner=user, is_paid=False).first()
#         context['cart'] = cart
#         return context


class CartView(LoginRequiredMixin, FormView):
    form_class = AddToCartForm
    template_name = 'cart.html'

    # def get_form(self, form_class=None):
    #     cart = Cart.objects.filter(owner=self.request.user, is_paid=False).first()
    #     cart = cart.cart_items.first()
    #     print(cart.quantity)
    #     # cart_item = Item.objects.filter(cart=cart).first()
    #     form = AddToCartForm(instance=cart, data=self.request.POST)
    #     print('-----------------form :-------------------\n',form)
    #     return form

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['update_form'] = context.get('form')
        cart = Cart.objects.filter(owner=self.request.user, is_paid=False).first()
        context['cart'] = cart
        return context

    def form_valid(self, form):
        form.save()
        return redirect('cart:cart')


# class AddToCart(FormView):
#     form_class = AddToCartForm
#     template_name = 'shop/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         print('============== YES ===========')
#         context = super(AddToCart, self).get_context_data(**kwargs)
#         context['add_to_cart_form'] = kwargs.pop('form')
#         return context

#     def form_valid(self, form):
#         slug = self.kwargs.get('slug')
#         user = self.request.user
#         product = Product.objects.filter(slug=slug).first()
#         form = form.save(commit=False)
#
#         cart = Cart.objects.filter(owner=user).first()
#         if cart is None or cart.is_paid is True:
#             Cart.objects.create(owner=user)
#
#         form.cart = cart
#         form.product = product
#         form.price = product.current_price
#         form.save()
#         messages.success(self.request, '?????????? ???? ???????????? ???? ?????? ???????? ?????????? ????')
#         return redirect('shop:product_detail', self=slug)


class RemoveCartItem(FormView):
    form_class = DeleteCartItem

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        cart_item = Item.objects.filter(pk=pk).first()
        print('-------------', cart_item)
        cart_item.delete()
        # if cart_item.cart.cart_items.count() == 1:
        #     cart_item.cart.delete()
        # # messages.success(self.request, '?????????????? ???? ???????????? ?????????? ????')
        return redirect('cart:cart')

    