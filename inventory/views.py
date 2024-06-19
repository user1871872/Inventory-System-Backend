from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Product,Purchase,SalesStatistic
from .serializers import ProductSerializer,PurchaseSerializer,SalesStatisticSerializer
from django.utils import timezone
from datetime import timedelta
import logging

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SaleStatisticViewSet(viewsets.ModelViewSet):
    queryset = SalesStatistic.objects.all()
    serializer_class = SalesStatisticSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

@api_view(['GET'])
def sales_statistics(request):
    today = timezone.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)

    daily_sales = SalesStatistic.objects.filter(sale_date__gte=start_of_day).aggregate(daily_sales=Sum('total_price'))
    weekly_sales = SalesStatistic.objects.filter(sale_date__gte=start_of_week).aggregate(weekly_sales=Sum('total_price'))
    monthly_sales = SalesStatistic.objects.filter(sale_date__gte=start_of_month).aggregate(monthly_sales=Sum('total_price'))

    return Response({
        "daily_sales": daily_sales['daily_sales'] or 0,
        "weekly_sales": weekly_sales['weekly_sales'] or 0,
        "monthly_sales": monthly_sales['monthly_sales'] or 0,
    })
@api_view(['POST'])
def purchase_product(request):
    try:
        for item in request.data:
            product = Product.objects.get(id=item['product_id'])
            if product.quantity >= item['quantity']:
                product.quantity -= item['quantity']
                product.save()
                
                purchase = Purchase(
                    product=product,
                    quantity=item['quantity'],
                    total_amount=item['total_amount']
                )
                purchase.save()

                # Update or create SalesStatistic for the current day
                date_today = timezone.now().date()
                sales_statistic, created = SalesStatistic.objects.get_or_create(date=date_today)
                sales_statistic.daily_total += item['total_amount']
                
                # Update weekly total
                start_of_week = date_today - timedelta(days=date_today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                weekly_statistics = SalesStatistic.objects.filter(date__range=(start_of_week, end_of_week))
                weekly_total = sum(stat.daily_total for stat in weekly_statistics)
                sales_statistic.weekly_total = weekly_total

                # Update monthly total
                start_of_month = date_today.replace(day=1)
                end_of_month = (date_today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                monthly_statistics = SalesStatistic.objects.filter(date__range=(start_of_month, end_of_month))
                monthly_total = sum(stat.daily_total for stat in monthly_statistics)
                sales_statistic.monthly_total = monthly_total
                
                sales_statistic.save()
            else:
                return Response({'error': f'Insufficient quantity for product: {product.name}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Purchase successful'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_sales_statistics(request):
    today = timezone.now().date()
    logger.info(f"Fetching sales statistics for date: {today}")
    sales_statistics = SalesStatistic.objects.filter(date=today).first()
    if not sales_statistics:
        logger.info(f"No sales statistics found for {today}. Returning default values.")
        sales_statistics = SalesStatistic(
            date=today,
            daily_total=0,
            weekly_total=0,
            monthly_total=0
        )
    logger.info(f"Sales statistics found: {sales_statistics}")
    serializer = SalesStatisticSerializer(sales_statistics)
    logger.info(f"Returning sales statistics: {serializer.data}")
    return Response(serializer.data)
    
@api_view(['GET'])
def list_purchases(request):
    purchases = Purchase.objects.all().order_by('-date')
    serializer = PurchaseSerializer(purchases, many=True)
    return Response(serializer.data)