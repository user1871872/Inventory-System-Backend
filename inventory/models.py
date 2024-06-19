from django.db import models
from django.utils import timezone
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.product.name} - {self.quantity} - {self.date}'

class SalesStatistic(models.Model):
    date = models.DateField(default=timezone.now)
    daily_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weekly_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.date} - Daily: {self.daily_total} - Weekly: {self.weekly_total} - Monthly: {self.monthly_total}'