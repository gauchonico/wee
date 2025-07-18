from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ..models import Cooperative, Member, Training, Agent, Loan, Collection, District, County, SubCounty, Parish, Village, FarmerGroup, Product
from .serializers import CooperativeSerializer, MemberSerializer, TrainingSerializer, DistrictSerializer, CountySerializer, SubCountySerializer, ParishSerializer, VillageSerializer, FarmerGroupSerializer, ProductSerializer
from django.views.decorators.csrf import csrf_exempt

class CooperativeViewSet(viewsets.ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    
from .serializers import PlantingAllocationSerializer
from ..models import PlantingAllocation
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class PlantingAllocationViewSet(viewsets.ModelViewSet):
    queryset = PlantingAllocation.objects.all()
    serializer_class = PlantingAllocationSerializer
    permission_classes = [IsAuthenticated]

    # Optional: filter by member via query param
    def get_queryset(self):
        queryset = super().get_queryset()
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(member__id=member_id)
        return queryset

    # Optional: custom action to get allocations for a specific member
    @action(detail=False, methods=['get'], url_path='by-member/(?P<member_id>[^/.]+)')
    def by_member(self, request, member_id=None):
        allocations = self.get_queryset().filter(member__id=member_id)
        serializer = self.get_serializer(allocations, many=True)
        return Response(serializer.data)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer

class SubCountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCounty.objects.all()
    serializer_class = SubCountySerializer

class ParishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Parish.objects.all()
    serializer_class = ParishSerializer

class VillageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer

class FarmerGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FarmerGroup.objects.all()
    serializer_class = FarmerGroupSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['GET'])
def stats_summary(request):
    """Get summary statistics for the dashboard"""
    data = {
        'total_cooperatives': Cooperative.objects.count(),
        'total_members': Member.objects.count(),
        'total_loans': Loan.objects.count(),
        'total_collection': Collection.objects.count()
    }
    return Response(data)

@api_view(['GET'])
def search_member_by_id(request):
    """Search for a member by their member_id"""
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
    """Add a new cooperative"""
    serializer = CooperativeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_member(request):
    """Add a new member"""
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def member_choices(request):
    from ..models import Member
    return Response({
        'gender_choices': Member.GENDER_CHOICES,
        'role_choices': Member.ROLE_CHOICES,
        'id_type_choices': Member.ID_TYPE_CHOICES,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_user(request):
    """Verify if the current user is authenticated and return user info with agent details"""
    user = request.user
    
    # Check if user has an associated agent profile
    try:
        agent = Agent.objects.get(user=user)
        agent_data = {
            'agent_id': agent.agent_id,
            'first_name': agent.first_name,
            'last_name': agent.last_name,
            'phone_number': agent.phone_number,
            'is_credit_manager': agent.is_credit_manager,
            'farmers_profiled': agent.farmers_profiled,
            'is_active': agent.is_active,
        }
    except Agent.DoesNotExist:
        agent_data = None
    
    return Response({
        'is_authenticated': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
            'groups': list(user.groups.values_list('name', flat=True)),
        },
        'agent': agent_data
    })


@csrf_exempt
@api_view(['POST'])
def login_user(request):
    """Login endpoint that returns token and agent info"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user and user.is_active:
        # Check if user has an agent profile
        try:
            agent = Agent.objects.get(user=user)
            if not agent.is_active:
                return Response({'error': 'Agent account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_staff': user.is_staff,
                    'groups': list(user.groups.values_list('name', flat=True)),
                },
                'agent': {
                    'agent_id': agent.agent_id,
                    'first_name': agent.first_name,
                    'last_name': agent.last_name,
                    'phone_number': agent.phone_number,
                    'is_credit_manager': agent.is_credit_manager,
                    'farmers_profiled': agent.farmers_profiled,
                    'is_active': agent.is_active,
                }
            })
        except Agent.DoesNotExist:
            return Response({'error': 'User is not registered as an agent'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout endpoint that deletes the token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response({'error': 'No token found'}, status=status.HTTP_400_BAD_REQUEST)