from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.db import models
from cooperatives.models import Store, Collection, Sale

class Command(BaseCommand):
    help = 'Initialize store inventory from existing collections and sales'

    def handle(self, *args, **options):
        # Get all unique products from collections
        products = Collection.objects.values_list('product', flat=True).distinct()
        
        for product_id in products:
            # Get total collections for this product
            total_collections = Collection.objects.filter(product_id=product_id).aggregate(
                total=models.Sum('quantity'))['total'] or 0
            
            # Get total sales for this product
            total_sales = Sale.objects.filter(product_id=product_id).aggregate(
                total=models.Sum('quantity'))['total'] or 0
            
            # Calculate current inventory
            current_quantity = total_collections - total_sales
            
            # Create or update store record
            store, created = Store.objects.get_or_create(
                product_id=product_id,
                defaults={'quantity': current_quantity}
            )
            
            if not created:
                store.quantity = current_quantity
                store.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully initialized store for {store.product.name} with quantity {store.quantity}'
                )
            ) 