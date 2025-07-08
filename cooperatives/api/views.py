from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated  # Optional: use if you want to restrict access
from rest_framework.response import Response
from ..models import Cooperative, Member, Training, Loan, Collection
from .serializers import CooperativeSerializer, MemberSerializer, TrainingSerializer

class CooperativeViewSet(viewsets.ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Uncomment if you want authentication
def stats_summary(request):
    data = {
        'total_cooperatives': Cooperative.objects.count(),
        'total_members': Member.objects.count(),
        'total_loans': Loan.objects.count(),
        'total_collection': Collection.objects.count()
        
    }
    return Response(data)