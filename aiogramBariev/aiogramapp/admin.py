from django.contrib import admin

from .models import Product, Category, Subcategory, Tguser, Newsletter


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title', 'price', 'subcategory',
    list_display_links = 'pk', 'title'
    ordering = 'pk',


@admin.register(Tguser)
class TguserAdmin(admin.ModelAdmin):
    list_display = 'pk', 'tg_id',
    list_display_links = 'pk', 'tg_id'
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


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = 'pk', 'message',
    list_display_links = 'pk', 'message',
    ordering = 'pk',
