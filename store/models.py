from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = 'categories'  # plural name for the admin interface


    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='Unbranded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2)