from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q,F

from .models import Post, Category, Tag
from comment.models import Comment
from comment.forms import CommentForm
from config.models import Sidebar
from datetime import date
from django.core.cache import cache


# Create your views here.

def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'tag': tag,
        'category': category,
        'post_list': post_list,
        'sidebars': Sidebar.get_all(),
    }
    context.update(Category.get_navs())

    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': Sidebar.get_all(),

    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


class CommonView:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': Sidebar.get_all(),
            'tags': Tag.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonView, ListView):
    queryset = Post.latest_posts()
    paginate_by = 6
    context_object_name = 'post_list'  # 如果不设置此项，在模板中需要使用object_list变量
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        '''重写queryset，根据分类过滤'''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context

    def get_queryset(self):
        '''重写queryset，根据标签过滤'''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class PostDatailView(CommonView, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super(PostDatailView, self).get_context_data()
        context.update({
            'comments': Comment.get_by_target(self.kwargs.get('post_id')),

            'comment_form': CommentForm
        })
        return context

    def get(self, request, *args, **kwargs):
        response = super(PostDatailView, self).get(request, *args, **kwargs)
        self.handle_visited()

        '''from django.db import connection
        print(connection.queries)'''
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)
        if increase_uv and increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv')+ 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv' + 1))


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword')
        })
        return context

    def get_queryset(self):
        query = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return query
        return query.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        query = super(AuthorView, self).get_queryset()
        owner_id = self.kwargs.get('owner_id')
        return query.filter(owner_id=owner_id)


def new_comment(request):
    if request.method == 'POST':
        post = Post.objects.get(pk=request.POST.get('post_id'))
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.target = post
            instance.save()
            return redirect(reverse('post-detail', kwargs={'post_id': post.id}))
