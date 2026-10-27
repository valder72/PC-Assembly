from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.name


class Part(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='parts'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name='parts'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    specs = models.JSONField()
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title