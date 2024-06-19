from rest_framework import serializers
from .models import Product,Purchase, SalesStatistic

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class SalesStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesStatistic
        fields = ['date', 'daily_total', 'weekly_total', 'monthly_total'] 
