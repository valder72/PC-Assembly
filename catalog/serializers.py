from rest_framework import serializers
from .models import Category, Manufacturer, Part


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country']


class PartSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)

    class Meta:
        model = Part
        fields = [
            'id',
            'title',
            'category',
            'category_name',
            'manufacturer',
            'manufacturer_name',
            'price',
            'rating',
            'specs',
            'description',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Ціна не може бути від'ємною.")
        return value

    def validate_specs(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Характеристики повинні бути передані у форматі JSON-об'єкта.")
        return value
