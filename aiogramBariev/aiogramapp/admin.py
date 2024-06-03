from django.contrib import admin

from .models import Product, Category, Subcategory


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title', 'price', 'subcategory',
    list_display_links = 'pk', 'title'
    ordering = 'pk',


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title'
    list_display_links = 'pk', 'title'
    ordering = 'pk',


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title', 'parent'
    list_display_links = 'pk', 'title',
    ordering = 'pk',

