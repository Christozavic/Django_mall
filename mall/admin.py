from django.contrib import admin

# Register your models here.
from mall.forms import ProductAdminForm
from mall.models import Product, Classify, Tag
from utils.admin_actions import set_invalid, set_valid


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ 商品信息管理 """
    list_display = ('name', 'types', 'price', 'status', 'is_valid')
    list_per_page = 3  # 修改分页数据的大小
    list_filter = ('status',)
    # 排除某些字段，使之不可编辑，且在编辑界面不可见
    # exclude = ['remain_count']
    # 不可编辑，但是在界面上是可见的，只读状态
    readonly_fields = ['remain_count']
    actions = [set_valid, set_invalid]
    # 自定义的表单
    form = ProductAdminForm


# 方式 2：注册到后台管理
# admin.site.register(Product, ProductAdmin)

@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    """ 商品分类管理 """
    list_display = ['parent', 'name', 'code', 'is_valid']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ 商品标签管理 """
    list_display = ['name', 'code', 'is_valid']
