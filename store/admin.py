from django.contrib import admin

# Register your models here.

from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}