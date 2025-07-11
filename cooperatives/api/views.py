from rest_framework import viewsets, status
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

@api_view(['GET'])
def search_member_by_id(request):
    member_id = request.GET.get('member_id')
    if not member_id:
        return Response({'error': 'member_id parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        member = Member.objects.get(member_id=member_id)
        serializer = MemberSerializer(member)
        return Response(serializer.data)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['POST'])
def add_cooperative(request):
    serializer = CooperativeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_member(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)