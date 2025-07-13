from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    CooperativeViewSet, MemberViewSet, TrainingViewSet,
    search_member_by_id, verify_user, login_user, logout_user,
    stats_summary, add_cooperative, add_member
)

router = DefaultRouter()
router.register(r'cooperatives', CooperativeViewSet)
router.register(r'members', MemberViewSet)
router.register(r'trainings', TrainingViewSet)

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
]