from django.contrib import admin

from . models import Sidebar,Link
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site

# Register your models here.

@admin.register(Sidebar,site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    pass

@admin.register(Link,site=custom_site)
class LinkBarAdmin(BaseOwnerAdmin):
    pass
