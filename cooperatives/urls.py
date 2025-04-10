from django.urls import path
from . import views
from . import api

app_name = 'cooperatives'

urlpatterns = [
    # District URLs
    path('districts/', views.DistrictListView.as_view(), name='district-list'),
    path('districts/<int:pk>/', views.DistrictDetailView.as_view(), name='district-detail'),
    path('districts/create/', views.DistrictCreateView.as_view(), name='district-create'),
    path('districts/<int:pk>/update/', views.DistrictUpdateView.as_view(), name='district-update'),
    path('districts/<int:pk>/delete/', views.DistrictDeleteView.as_view(), name='district-delete'),
    path('districts/bulk-upload/', views.DistrictBulkUploadView.as_view(), name='district-bulk-upload'),
    
    # County URLs
    path('counties/', views.CountyListView.as_view(), name='county-list'),
    path('counties/<int:pk>/', views.CountyDetailView.as_view(), name='county-detail'),
    path('counties/create/', views.CountyCreateView.as_view(), name='county-create'),
    path('counties/<int:pk>/update/', views.CountyUpdateView.as_view(), name='county-update'),
    path('counties/<int:pk>/delete/', views.CountyDeleteView.as_view(), name='county-delete'),
    path('counties/bulk-upload/', views.CountyBulkUploadView.as_view(), name='county-bulk-upload'),
    
    # SubCounty URLs
    path('sub-counties/', views.SubCountyListView.as_view(), name='subcounty-list'),
    path('sub-counties/<int:pk>/', views.SubCountyDetailView.as_view(), name='subcounty-detail'),
    path('sub-counties/create/', views.SubCountyCreateView.as_view(), name='subcounty-create'),
    path('sub-counties/<int:pk>/update/', views.SubCountyUpdateView.as_view(), name='subcounty-update'),
    path('sub-counties/<int:pk>/delete/', views.SubCountyDeleteView.as_view(), name='subcounty-delete'),
    path('sub-counties/bulk-upload/', views.SubCountyBulkUploadView.as_view(), name='subcounty-bulk-upload'),
    
    # Parish URLs
    path('parishes/', views.ParishListView.as_view(), name='parish-list'),
    path('parishes/<int:pk>/', views.ParishDetailView.as_view(), name='parish-detail'),
    path('parishes/create/', views.ParishCreateView.as_view(), name='parish-create'),
    path('parishes/<int:pk>/update/', views.ParishUpdateView.as_view(), name='parish-update'),
    path('parishes/<int:pk>/delete/', views.ParishDeleteView.as_view(), name='parish-delete'),
    path('parishes/bulk-upload/', views.ParishBulkUploadView.as_view(), name='parish-bulk-upload'),
    
    # Village URLs
    path('villages/', views.VillageListView.as_view(), name='village-list'),
    path('villages/<int:pk>/', views.VillageDetailView.as_view(), name='village-detail'),
    path('villages/create/', views.VillageCreateView.as_view(), name='village-create'),
    path('villages/<int:pk>/update/', views.VillageUpdateView.as_view(), name='village-update'),
    path('villages/<int:pk>/delete/', views.VillageDeleteView.as_view(), name='village-delete'),
    path('villages/bulk-upload/', views.VillageBulkUploadView.as_view(), name='village-bulk-upload'),
    
    # PaymentMode URLs
    path('payment-modes/', views.PaymentModeListView.as_view(), name='paymentmode-list'),
    path('payment-modes/<int:pk>/', views.PaymentModeDetailView.as_view(), name='paymentmode-detail'),
    path('payment-modes/create/', views.PaymentModeCreateView.as_view(), name='paymentmode-create'),
    path('payment-modes/<int:pk>/update/', views.PaymentModeUpdateView.as_view(), name='paymentmode-update'),
    path('payment-modes/<int:pk>/delete/', views.PaymentModeDeleteView.as_view(), name='paymentmode-delete'),
    
    # Cooperative URLs
    path('', views.CooperativeListView.as_view(), name='cooperative-list'),
    path('cooperatives/<int:pk>/', views.CooperativeDetailView.as_view(), name='cooperative-detail'),
    path('cooperatives/create/', views.CooperativeCreateView.as_view(), name='cooperative-create'),
    path('cooperatives/<int:pk>/update/', views.CooperativeUpdateView.as_view(), name='cooperative-update'),
    path('cooperatives/<int:pk>/delete/', views.CooperativeDeleteView.as_view(), name='cooperative-delete'),
    path('cooperatives/bulk-upload/', views.CooperativeBulkUploadView.as_view(), name='cooperative-bulk-upload'),
    
    # FarmerGroup URLs
    path('farmer-groups/', views.FarmerGroupListView.as_view(), name='farmer-group-list'),
    path('farmer-groups/<int:pk>/', views.FarmerGroupDetailView.as_view(), name='farmer-group-detail'),
    path('farmer-groups/create/', views.FarmerGroupCreateView.as_view(), name='farmer-group-create'),
    path('farmer-groups/<int:pk>/update/', views.FarmerGroupUpdateView.as_view(), name='farmer-group-update'),
    path('farmer-groups/<int:pk>/delete/', views.FarmerGroupDeleteView.as_view(), name='farmer-group-delete'),
    path('farmer-groups/bulk-upload/', views.FarmerGroupBulkUploadView.as_view(), name='farmer-group-bulk-upload'),
    
    # Member URLs
    path('members/', views.MemberListView.as_view(), name='member-list'),
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('members/create/', views.MemberCreateView.as_view(), name='member-create'),
    path('members/<int:pk>/update/', views.MemberUpdateView.as_view(), name='member-update'),
    path('members/<int:pk>/delete/', views.MemberDeleteView.as_view(), name='member-delete'),
    
    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),

    # Price URLs
    path('prices/', views.PriceListView.as_view(), name='price-list'),
    path('prices/<int:pk>/', views.PriceDetailView.as_view(), name='price-detail'),
    path('prices/create/', views.PriceCreateView.as_view(), name='price-create'),
    path('prices/<int:pk>/update/', views.PriceUpdateView.as_view(), name='price-update'),
    path('prices/<int:pk>/delete/', views.PriceDeleteView.as_view(), name='price-delete'),
    
    # Unit URLs
    path('units/', views.UnitListView.as_view(), name='unit-list'),
    path('units/<int:pk>/', views.UnitDetailView.as_view(), name='unit-detail'),
    path('units/create/', views.UnitCreateView.as_view(), name='unit-create'),
    path('units/<int:pk>/update/', views.UnitUpdateView.as_view(), name='unit-update'),
    path('units/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='unit-delete'),
    
    # API URLs
    path('api/farmer-groups/', api.get_farmer_groups, name='api-farmer-groups'),
] 