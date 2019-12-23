from django.shortcuts import render

from .models import Post, Tag, Category
from config.models import SideBar, Link
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from comment.forms import CommentForm
from comment.models import Comment


# Create your views here.


# 定义通用的侧边栏
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context

# index页面，遍历Post表的所有文档
class IndexView(CommonViewMixin, ListView):
    model = Post
    paginate_by = 2
    ordering = 'create_time' # 根据post表的create time字段进行排序
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

# 根据category id进行过滤出指定的post数据
class CategoryView(IndexView):

    # 在post表里过滤出category_id的数据，添加到context
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)

        # 过滤出category_id对应的类型名称，渲染到title
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    # 获取url中的category_id，在model中定义的表中过滤出指定category_id的数据
    def get_queryset(self):
        queryset = super().get_queryset()

        # 过滤获取categoryid的文章内容
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category=category_id)

# 根据tag id 进行过滤出指定的post数据
class TagView(IndexView):

    # 在post表里过滤出tag_id的数据，添加到context，用于渲染title
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    # 获取url中的tag_id，在model中定义的表中过滤出指定tag_id的数据，用于渲染post_list
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag=tag_id)

class UserView(IndexView):

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        username = get_object_or_404(User, pk=user_id)
        context.update({
            'username': username,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.kwargs.get('user_id')
        return queryset.filter(owner=user_id)

class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

class CommentViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path)
        })
        return context

class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'

# 显示文章内容
class PostDetailView(DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post_info'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    # # 获取comment_form用于渲染提交评论的表格，comment_list用于渲染现有文档的评论
    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context.update({
    #         'comment_form': CommentForm,
    #         'comment_list': Comment.get_by_target(self.request.path)
    #     })
    #     return context

# def post_detail(request, post_id=None):
#     if post_id:
#         post_info = Post.objects.get(id=post_id)
#
#     return render(request, 'blog/detail.html', context={'post_info': post_info})

