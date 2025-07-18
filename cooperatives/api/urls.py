from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    CooperativeViewSet, MemberViewSet, TrainingViewSet, member_choices,
    search_member_by_id, verify_user, login_user, logout_user,
    stats_summary, add_cooperative, add_member,
    DistrictViewSet, CountyViewSet, SubCountyViewSet, ParishViewSet, VillageViewSet, FarmerGroupViewSet, ProductViewSet
)

router = DefaultRouter()
router.register(r'cooperatives', CooperativeViewSet)
router.register(r'members', MemberViewSet)
router.register(r'trainings', TrainingViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'counties', CountyViewSet)
router.register(r'subcounties', SubCountyViewSet)
router.register(r'parishes', ParishViewSet)
router.register(r'villages', VillageViewSet)
router.register(r'farmergroups', FarmerGroupViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = router.urls + [
    # Dashboard/Stats endpoints
    path('stats-summary/', stats_summary, name='stats-summary'),
    
    # Authentication endpoints
    path('login/', login_user, name='login'),
    path('verify-user/', verify_user, name='verify-user'),
    path('logout/', logout_user, name='logout'),
    
    # Search endpoints
    path('search-member/', search_member_by_id, name='search-member'),
    
    # Add endpoints
    path('add-member/', add_member, name='add-member'),
    path('add-cooperative/', add_cooperative, name='add-cooperative'),
    path('member-choices/', member_choices, name='member-choices'),
]