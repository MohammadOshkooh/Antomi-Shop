from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from shop.forms import ProductReviewForm, AddFavoriteItemForm, DeleteCommentForm
from shop.models import Product, Comment, ProductCategory, Favorite
from tag.models import Tag


class ProductList(ListView):
    model = Product
    template_name = 'shop/products_list.html'
    context_object_name = 'products'
    paginate_by = 16

    def __init__(self):
        super().__init__()
        self.max_range = None
        self.min_range = None

    def get_queryset(self):
        queryset = Product.objects.filter(availability=True)

        # search
        search = self.request.GET.get('search')
        select = self.request.GET.get('select')

        if search is not None:
            search.replace('+', ' ')
            queryset = Product.objects.filter(name__icontains=search)
            select.replace('+', ' ')
            if select == 'all':
                select = None

        # category filter
        category = self.request.GET.get('category')
        if category is not None or select is not None:
            if category is None:
                category = select
            new_queryset = []
            for product in queryset:
                if category in product.category.get_fullname():
                    new_queryset.append(product)
            queryset = new_queryset

        # tag filter
        tag = self.request.GET.get('tag')
        if tag is not None:
            queryset = queryset.filter(tag__title=tag)

        # filter price
        self.min_range = self.request.GET.get('price_min')
        self.max_range = self.request.GET.get('price_max')
        if self.min_range is not None:
            queryset = queryset.filter(current_price__range=[int(self.min_range), int(self.max_range)]).order_by(
                'current_price')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['tags'] = Tag.objects.all()

        if self.min_range is not None:
            context['min_range'] = self.min_range
            context['max_range'] = self.max_range
        else:
            context['min_range'] = 70000
            context['max_range'] = 100000

        return context


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, availability=True)
    comments = Comment.objects.filter(is_active=True, product=product)
    # related products
    related_products = []
    product_tags = product.tag.all()
    for pr in Product.objects.all():
        for tag in pr.tag.all():
            if tag in product_tags and pr not in related_products:
                related_products.append(pr)
    related_products.remove(product)

    if request.method == 'POST':
        user = request.user
        # product review
        product_review_form = ProductReviewForm(data=request.POST)
        if product_review_form.is_valid():
            if user.is_authenticated:
                product_review_form = product_review_form.save(commit=False)
                product_review_form.owner = user
                product_review_form.product = product
                product_review_form.save()
                messages.success(request, '?????? ?????? ???? ???????????? ?????? ????')
                return redirect(product.get_absolute_url(), product.slug)
            else:
                messages.error(request, '???????? ?????? ?????? ???????? ?????????? ????????')

        # update comment
        # try:
        #     comment_id = int(request.POST.get('comment_id'))
        # except:
        #     parent_id = None
        # if comment_id is not None:
        #     comment = Comment.objects.filter(id=comment_id).first()
        #     update_review_form = ProductReviewForm(instance=comment, data=request.POST)
        #     if update_review_form.is_valid():
        #         update_review_form = update_review_form.save()
        #         messages.success(request, '?????????????? ???? ???????????? ?????????? ????')
        #         return redirect(product.get_absolute_url(), product.slug)

        # delete comment
        delete_comment_form = DeleteCommentForm(request.POST)
        try:
            comment_id = int(request.POST.get('comment_id'))
        except:
            comment_id = None
        if comment_id is not None:
            comment = Comment.objects.filter(id=comment_id).first()
            comment.delete()
            messages.success(request, '?????????? ?????? ???? ???????????? ?????? ????')
            return redirect(product.get_absolute_url(), product.slug)

    # request.method is not 'POST':
    else:
        product_review_form = ProductReviewForm()
        delete_comment_form = DeleteCommentForm()

    context = {
        'product_review_form': product_review_form,
        'product': product,
        'comments': comments,
        'delete_comment_form': delete_comment_form,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


# class ProductDetail(DetailView, FormView):
#     model = Product
#     template_name = 'shop/product_detail.html'
#     queryset = Product.objects.filter(availability=True)
#     context_object_name = 'product'
#
#     form_class = ProductReviewForm
#
#     def form_valid(self, form):
#         user = self.request.user
#         product = self.queryset.first()
#         if user.is_authenticated:
#             review_form = form.save(commit=False)
#             review_form.owner = user
#             review_form.product = product
#             review_form.save()
#             messages.success(self.request, '?????? ?????? ???? ???????????? ?????? ????')
#             return HttpResponseRedirect(product.get_absolute_url(), product.slug)
#         else:
#             messages.error(self.request, '???????? ?????? ?????? ???????? ?????????? ????????')
#             return HttpResponseRedirect(reverse_lazy('account_login'))
#
#     def form_invalid(self, form):
#         return super(ProductDetail, self).form_invalid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetail, self).get_context_data()
#         product = kwargs['object']
#         context['comments'] = Comment.objects.filter(is_active=True, product=product)
#         return context


# ---- Favorite list ---- #

class FavoritesView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'favorite_list/favorites_list.html'
    context_object_name = 'favorite_items'

    def get_queryset(self):
        queryset = Favorite.objects.filter(owner=self.request.user)
        return queryset


class ClearFavoritesList(DeleteView):
    model = Favorite
    success_url = reverse_lazy('shop:favorites_list')


# def delete_favorite_item(request, slug):
#     instance = Favorite.objects.filter(owner=request.user).first()
#     product = get_object_or_404(Product, slug=slug)
#     if instance is not None:
#         if request.method == 'POST':
#             instance.product.remove(product)
#             messages.success(request, '???????? ???? ???????????? ???? ???????? ?????????? ???????? ???? ?????? ????')
#
#     return redirect('shop:favorites_list')

class DeleteFavoriteItem(LoginRequiredMixin, FormView):
    form_class = AddFavoriteItemForm

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        instance = Favorite.objects.filter(owner=self.request.user).first()
        product = get_object_or_404(Product, slug=slug)
        if product in instance.product.all():
            instance.product.remove(product)
            messages.success(self.request, '???????? ???? ???????????? ???? ???????? ?????????? ???????? ???? ?????? ????')
        return redirect('shop:favorites_list')


# def add_favorite_items(request, slug):
#     instance = Favorite.objects.filter(owner=request.user).first()
#     product = get_object_or_404(Product, slug=slug)
#     if instance is not None:
#         if request.method == 'POST':
#             if product in instance.product.all():
#                 messages.error(request, '?????? ???????? ???? ?????? ???? ???????? ?????????? ???????? ???? ???????? ????????')
#             else:
#                 add_form = AddFavoriteItemForm(instance=instance, data=request.POST)
#                 add_form = add_form.save()
#                 add_form.product.add(product)
#                 messages.success(request, '???????? ???? ???????????? ???? ???????? ?????????? ???????? ???? ?????????? ????')
#
#     else:  # instance in None -> favorite list not exist
#         if request.method == 'POST':
#             add_form = AddFavoriteItemForm()
#             # Favorite.objects.create(owner=request.user)
#             add_form = add_form.save(commit=False)
#             add_form.owner = request.user
#             add_form.save()
#             add_form.product.add(product)
#             messages.success(request, '???????? ???? ???????????? ???? ???????? ?????????? ???????? ???? ?????????? ????')
#
#     return redirect('shop:product_detail', slug=slug)


class AddFavoriteItems(LoginRequiredMixin, FormView):
    form_class = AddFavoriteItemForm
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AddFavoriteItems, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        product = Product.objects.filter(slug=slug).first()
        context['product'] = product
        return context

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        product = Product.objects.filter(slug=slug).first()
        return product.get_absolute_url()

    def get_form(self, form_class=None):
        instance = Favorite.objects.filter(owner=self.request.user).first()
        if instance is not None:
            return AddFavoriteItemForm(instance=instance, data=self.request.POST)
        else:
            return AddFavoriteItemForm(data=self.request.POST)

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        instance = Favorite.objects.filter(owner=self.request.user).first()
        if instance is not None:
            if self.request.method == 'POST':
                if product in instance.product.all():
                    messages.error(self.request, '?????? ???????? ???? ?????? ???? ???????? ?????????? ???????? ???? ???????? ????????')
                else:
                    form = form.save()
                    form.product.add(product)
                    messages.success(self.request, '???????? ???? ???????????? ???? ???????? ?????????? ???????? ???? ?????????? ????')

        else:  # instance in None -> favorite list not exist
            if self.request.method == 'POST':
                # Favorite.objects.create(owner=request.user)
                form = form.save(commit=False)
                form.owner = self.request.user
                form.save()
                form.product.add(product)
                messages.success(self.request, '???????? ???? ???????????? ???? ???????? ?????????? ???????? ???? ?????????? ????')

        return redirect('shop:product_detail', slug=slug)
