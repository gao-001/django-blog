from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Tag, Post, Category
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


# Register your models here.

class PostInline(admin.TabularInline):  # StackedInline样式不同
    fields = ('title','desc')
    extra = 1
    model = Post

@admin.register(Category,site=custom_site)
class CategoryAdmin(admin.ModelAdmin):

    inlines = [PostInline,]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count','owner')
    fields = ('name', 'status', 'is_nav','owner')

    def post_count(self, obj):
        return obj.post_set.count()

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request,obj,form,change)

    post_count.short_description = '文章数量'


@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status',)




class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户'''
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = ('title', 'category', 'status', 'created_time', 'owner', 'operator')
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    filter_horizontal = ('tag',)

    actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True

    # 省略其他代码
    exclude = ('owner',)

    '''fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )'''

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc', 'content'
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'



    class Media:
        css = {
            'all': ("https://cdn.staticfile.org/twitter-bootstrap/4.5.0/css/bootstrap-grid.min.css")
        }
        js = (
            "https://cdn.staticfile.org/popper.js/0.2.0/popper.min.js",
            "https://cdn.staticfile.org/twitter-bootstrap/4.5.0/js/bootstrap.min.js")



@admin.register(LogEntry,site=custom_site)
class LogRntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']


