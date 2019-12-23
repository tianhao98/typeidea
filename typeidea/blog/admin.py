from django.contrib import admin
from .models import Post, Tag, Category
from django.utils.html import format_html
from django.urls import reverse
from .adminforms import PostAdminForm
from typeidea.custom_site import costom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry
import mistune
# Register your models here.

class CategoryOwnerFilter(admin.SimpleListFilter):

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        id = self.value()
        if id:
            return queryset.filter(id=self.value())
        return queryset

@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'create_time', 'owner')
    fields = ('name', 'status', 'is_nav')

    list_filter = [CategoryOwnerFilter]

@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'create_time', 'owner',)
    fields = ('name', 'status')

    def post_count(self, obj):
        return obj.post_set.count()


    post_count.short_description = '文章数量'


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = [
        'title', 'category', 'status',
        'create_time', 'operator'
    ]

    form = PostAdminForm

    list_display_links = []

    list_filter = ['category']

    search_fields = ['title', 'category__name']

    action_on_to = True
    action_on_bottom = True

    save_on_to = True

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}"编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.content_html = mistune.markdown(obj.content)
        return super(PostAdmin, self).save_model(request, obj, form, change)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']