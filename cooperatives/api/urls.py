from rest_framework.routers import DefaultRouter
from .views import CooperativeViewSet, MemberViewSet, TrainingViewSet, stats_summary
from django.urls import path, include

router = DefaultRouter()
router.register(r'cooperatives', CooperativeViewSet)
router.register(r'members', MemberViewSet)
router.register(r'trainings', TrainingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats-summary/', stats_summary, name='stats-summary'),
]