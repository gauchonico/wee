from django.urls import path
from . import views
from . import api
from django.urls import path, include

app_name = 'cooperatives'

urlpatterns = [
    
    # path('api/', include('cooperatives.api.urls')),
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
    path('cooperatives/<int:pk>/members/', views.CooperativeMemberListView.as_view(), name='cooperative-member-list'),
    
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
    path('members/bulk-upload/', views.MemberBulkUploadView.as_view(), name='member-bulk-upload'),
    path('members/system-id-bulk-upload/', views.MemberSystemIdBulkUploadView.as_view(), name='member-system-id-bulk-upload'),
    path('members/sunflower-acreage/bulk-upload/', views.SunflowerAcreageBulkUploadView.as_view(), name='sunflower-acreage-bulk-upload'),
    path('members/assign-products/', views.MemberProductAssignmentView.as_view(), name='member-product-assignment'),
    path('members/bulk-update/', views.MemberBulkUpdateView.as_view(), name='member-bulk-update'),
    
    # Planting Allocation URLs
    path('members/<int:member_pk>/planting/', views.MemberPlantingAllocationListView.as_view(), name='member-planting-list'),
    path('members/<int:member_pk>/planting/create/', views.MemberPlantingAllocationCreateView.as_view(), name='member-planting-create'),
    path('members/planting/<int:pk>/update/', views.MemberPlantingAllocationUpdateView.as_view(), name='member-planting-update'),
    
    # Collection URLs
    path('members/<int:member_pk>/collections/', views.MemberCollectionListView.as_view(), name='member-collection-list'),
    path('members/<int:member_pk>/collections/create/', views.MemberCollectionCreateView.as_view(), name='member-collection-create'),
    path('members/collections/<int:pk>/update/', views.MemberCollectionUpdateView.as_view(), name='member-collection-update'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-detail'),
    
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
    # path('api/farmer-groups/', api.get_farmer_groups, name='api-farmer-groups'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Supplier URLs
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),

    # Supplier Product URLs
    path('supplier-products/', views.SupplierProductListView.as_view(), name='supplier_product_list'),
    path('supplier-products/create/', views.SupplierProductCreateView.as_view(), name='supplier_product_create'),
    path('supplier-products/<int:pk>/update/', views.SupplierProductUpdateView.as_view(), name='supplier_product_update'),
    path('supplier-products/<int:pk>/delete/', views.SupplierProductDeleteView.as_view(), name='supplier_product_delete'),
    path('supplier-products/bulk-upload/', views.SupplierProductBulkUploadView.as_view(), name='supplier_product_bulk_upload'),

    path('planting-analytics/', views.PlantingAnalyticsView.as_view(), name='planting-analytics'),

    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('collections/bulk-upload/', views.CollectionBulkUploadView.as_view(), name='collection_bulk_upload'),

    # Loan Supplier URLs
    path('loan-suppliers/', views.LoanSupplierListView.as_view(), name='loan-supplier-list'),
    path('loan-suppliers/create/', views.LoanSupplierCreateView.as_view(), name='loan-supplier-create'),
    path('loan-suppliers/<int:pk>/update/', views.LoanSupplierUpdateView.as_view(), name='loan-supplier-update'),
    path('loan-suppliers/<int:pk>/delete/', views.LoanSupplierDeleteView.as_view(), name='loan-supplier-delete'),

    # Credit Manager URLs
    path('credit-managers/', views.CreditManagerListView.as_view(), name='credit-manager-list'),
    path('credit-managers/create/', views.CreditManagerCreateView.as_view(), name='credit-manager-create'),
    path('credit-managers/<int:pk>/update/', views.CreditManagerUpdateView.as_view(), name='credit-manager-update'),
    path('credit-managers/<int:pk>/delete/', views.CreditManagerDeleteView.as_view(), name='credit-manager-delete'),
    path('credit-managers/bulk-upload/', views.CreditManagerBulkUploadView.as_view(), name='credit-manager-bulk-upload'),

    # Loan URLs
    path('loans/', views.LoanListView.as_view(), name='loan-list'),
    path('loans/create/', views.LoanCreateView.as_view(), name='loan-create'),
    path('loans/<int:pk>/update/', views.LoanUpdateView.as_view(), name='loan-update'),
    path('loans/<int:pk>/approve/', views.LoanApprovalView.as_view(), name='loan-approval'),
    path('loans/<int:pk>/delete/', views.LoanDeleteView.as_view(), name='loan-delete'),
    path('loans/bulk-upload/', views.LoanBulkUploadView.as_view(), name='loan-bulk-upload'),
    path('loans/delete-all/', views.LoanDeleteAllView.as_view(), name='loan-delete-all'),
    path('members/<int:member_id>/loans/', views.MemberLoanListView.as_view(), name='member-loans'),
    path('loans/dashboard/', views.LoanDashboardView.as_view(), name='loan_dashboard'),

    # Offtaker URLs
    path('offtakers/', views.OfftakerListView.as_view(), name='offtaker-list'),
    path('offtakers/create/', views.OfftakerCreateView.as_view(), name='offtaker-create'),
    path('offtakers/<int:pk>/', views.OfftakerDetailView.as_view(), name='offtaker-detail'),
    path('offtakers/<int:pk>/update/', views.OfftakerUpdateView.as_view(), name='offtaker-update'),
    path('offtakers/<int:pk>/delete/', views.OfftakerDeleteView.as_view(), name='offtaker-delete'),

    # Sale URLs
    path('sales/', views.SaleListView.as_view(), name='sale-list'),
    path('sales/create/', views.SaleCreateView.as_view(), name='sale-create'),
    path('sales/<int:pk>/', views.SaleDetailView.as_view(), name='sale-detail'),
    path('sales/<int:pk>/update/', views.SaleUpdateView.as_view(), name='sale-update'),
    path('sales/<int:pk>/delete/', views.SaleDeleteView.as_view(), name='sale-delete'),

    # Store URLs
    path('store/', views.StoreListView.as_view(), name='store-list'),
    path('store/<int:pk>/', views.StoreDetailView.as_view(), name='store-detail'),

    # Thematic Area URLs
    path('thematic-areas/', views.ThematicAreaListView.as_view(), name='thematic-area-list'),
    path('thematic-areas/<int:pk>/', views.ThematicAreaDetailView.as_view(), name='thematic-area-detail'),
    path('thematic-areas/create/', views.ThematicAreaCreateView.as_view(), name='thematic-area-create'),
    path('thematic-areas/<int:pk>/update/', views.ThematicAreaUpdateView.as_view(), name='thematic-area-update'),
    path('thematic-areas/<int:pk>/delete/', views.ThematicAreaDeleteView.as_view(), name='thematic-area-delete'),

    # Training URLs
    path('trainings/', views.TrainingListView.as_view(), name='training-list'),
    path('trainings/<int:pk>/', views.TrainingDetailView.as_view(), name='training-detail'),
    path('trainings/create/', views.TrainingCreateView.as_view(), name='training-create'),
    path('trainings/<int:pk>/update/', views.TrainingUpdateView.as_view(), name='training-update'),
    path('trainings/<int:pk>/delete/', views.TrainingDeleteView.as_view(), name='training-delete'),
    path('trainings/dashboard/', views.TrainingDashboardView.as_view(), name='training-dashboard'),

    # API Endpoints
    path('api/cooperatives/<int:cooperative_id>/members/', views.get_cooperative_members, name='cooperative-members-api'),
] 