from rest_framework.routers import DefaultRouter
from .views import CooperativeViewSet, MemberViewSet, TrainingViewSet, add_cooperative, add_member, search_member_by_id, stats_summary
from django.urls import path, include

router = DefaultRouter()
router.register(r'cooperatives', CooperativeViewSet)
router.register(r'members', MemberViewSet)
router.register(r'trainings', TrainingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats-summary/', stats_summary, name='stats-summary'),
    path('search-member/', search_member_by_id, name='search-member'),
    path('add-member/', add_member, name='add-member'),
    path('add-cooperative/', add_cooperative, name='add-cooperative'),
]