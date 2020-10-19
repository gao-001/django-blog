"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.generic import TemplateView
from .custom_site import custom_site
from .views import girl,login_view,logout_view
from blog.views import (IndexView,CategoryView,TagView,PostDatailView,SearchView,AuthorView,new_comment)
from django.views.decorators.cache import cache_page

from django.conf.urls.static import static
from django.conf import settings
from blog.apis import PostViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LastPostFeed
from blog.sitemap import PostSitemap

router = DefaultRouter()
router.register('post',PostViewSet,basename='api-post')




urlpatterns = [
    path('super_admin/', admin.site.urls,name='super-admin'),
    path('admin/', custom_site.urls,name='admin'),
    path('',IndexView.as_view(),name='index'),
    path('category/<int:category_id>/',CategoryView.as_view(),name='category-list'),
    path('tag/<int:tag_id>/',TagView.as_view(),name='tag-list'),
    path('post/<int:post_id>.html/',PostDatailView.as_view(),name='post-detail'),
    path('search/',SearchView.as_view(),name='search'),
    path('author/<int:owner_id>/',AuthorView.as_view(),name='author'),
    path('comment',new_comment,name='comment'),
    path('meizhi/<int:page_num>/',girl,name='girl'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('mdeditor/',include('mdeditor.urls')),
    path('api/',include(router.urls),name='api'),
    path('api/docs/',include_docs_urls(title='typeidea apis')),
    path('rss',LastPostFeed(),name='rss'),
    path('sitemap.xml',cache_page(60*20,key_prefix='sitemap_cache_')(sitemap_views.sitemap),{'sitemaps':{'posts':PostSitemap}}),
    path('project/',TemplateView.as_view(template_name='project.html'),name='project'),
    path('navigation/',TemplateView.as_view(template_name='navigation.html'),name='navigation'),
    path('about/',TemplateView.as_view(template_name='about.html'),name='about'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


