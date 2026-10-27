from django.contrib import admin
from .models import Category, Manufacturer, Part


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'manufacturer', 'price')

