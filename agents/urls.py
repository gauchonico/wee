from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.AgentListView.as_view(), name='agent-list'),
    path('<int:pk>/', views.AgentDetailView.as_view(), name='agent-detail'),
    path('create/', views.AgentCreateView.as_view(), name='agent-create'),
    path('<int:pk>/update/', views.AgentUpdateView.as_view(), name='agent-update'),
    path('<int:pk>/delete/', views.AgentDeleteView.as_view(), name='agent-delete'),
    path('bulk-upload/', views.AgentBulkUploadView.as_view(), name='agent-bulk-upload'),
] 