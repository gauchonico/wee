from django.http import JsonResponse
from .models import FarmerGroup

def get_farmer_groups(request):
    cooperative_id = request.GET.get('cooperative')
    if cooperative_id:
        farmer_groups = FarmerGroup.objects.filter(cooperative_id=cooperative_id).values('id', 'name')
        return JsonResponse(list(farmer_groups), safe=False)
    return JsonResponse([], safe=False) 