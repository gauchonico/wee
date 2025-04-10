from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse

def index(request):
	return render(request, "pages/index.html")

def analytics(request):
	return render(request, "pages/analytics.html")

def emailInbox(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-3"
	}
	return render(request, "pages/email-inbox.html", context)

def emailDetail(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-3"
	}
	return render(request, "pages/email-detail.html", context)

def emailCompose(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-3"
	}
	return render(request, "pages/email-compose.html", context)

def widgets(request):
	return render(request, "pages/widgets.html")

def posCustomerOrder(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-customer-order.html", context)

def posKitchenOrder(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-kitchen-order.html", context)

def posCounterCheckout(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-counter-checkout.html", context)

def posTableBooking(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-table-booking.html", context)

def posMenuStock(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-menu-stock.html", context)

def uiBootstrap(request):
	return render(request, "pages/ui-bootstrap.html")

def uiButtons(request):
	return render(request, "pages/ui-buttons.html")

def uiCard(request):
	return render(request, "pages/ui-card.html")

def uiIcons(request):
	return render(request, "pages/ui-icons.html")

def uiModalNotifications(request):
	return render(request, "pages/ui-modal-notifications.html")

def uiTypography(request):
	return render(request, "pages/ui-typography.html")

def uiTabsAccordions(request):
	return render(request, "pages/ui-tabs-accordions.html")

def formElements(request):
	return render(request, "pages/form-elements.html")

def formPlugins(request):
	return render(request, "pages/form-plugins.html")

def formWizards(request):
	return render(request, "pages/form-wizards.html")

def tableElements(request):
	return render(request, "pages/table-elements.html")

def tablePlugins(request):
	return render(request, "pages/table-plugins.html")

def chartJs(request):
	return render(request, "pages/chart-js.html")

def chartApex(request):
	return render(request, "pages/chart-apex.html")

def map(request):
	return render(request, "pages/map.html")

def layoutStarter(request):
	return render(request, "pages/layout-starter.html")

def layoutFixedFooter(request):
	context = {
		"appFooter": 1
	}
	return render(request, "pages/layout-fixed-footer.html", context)

def layoutFullHeight(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-0"
	}
	return render(request, "pages/layout-full-height.html", context)

def layoutFullWidth(request):
	context = {
		"appContentFullWidth": 1,
		"appSidebarHide": 1
	}
	return render(request, "pages/layout-full-width.html", context)

def layoutBoxedLayout(request):
	context = {
		"appBoxedLayout": 1,
		"bodyClass": "pace-top"
	}
	return render(request, "pages/layout-boxed-layout.html", context)

def layoutCollapsedSidebar(request):
	context = {
		"appSidebarCollapsed": 1
	}
	return render(request, "pages/layout-collapsed-sidebar.html", context)

def layoutTopNav(request):
	context = {
		"appTopNav": 1,
		"appSidebarHide": 1
	}
	return render(request, "pages/layout-top-nav.html", context)

def layoutMixedNav(request):
	context = {
		"appTopNav": 1,
	}
	return render(request, "pages/layout-mixed-nav.html", context)

def layoutMixedNavBoxedLayout(request):
	context = {
		"appTopNav": 1,
		"appBoxedLayout": 1
	}
	return render(request, "pages/layout-mixed-nav-boxed-layout.html", context)

def pageScrumBoard(request):
	return render(request, "pages/page-scrum-board.html")

def pageProduct(request):
	return render(request, "pages/page-product.html")

def pageProductDetails(request):
	return render(request, "pages/page-product-details.html")

def pageOrder(request):
	return render(request, "pages/page-order.html")

def pageOrderDetails(request):
	return render(request, "pages/page-order-details.html")

def pageGallery(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": 'p-0',
		"appSidebarCollapsed": 1
	}
	return render(request, "pages/page-gallery.html", context)

def pageSearchResults(request):
	return render(request, "pages/page-search-results.html")

def pageComingSoon(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-coming-soon.html", context)

def pageError(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-error.html", context)

def pageLogin(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-login.html", context)

def pageRegister(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-register.html", context)

def pageMessenger(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": 'p-3'
	}
	return render(request, "pages/page-messenger.html", context)

def pageDataManagement(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": 'py-3'
	}
	return render(request, "pages/page-data-management.html", context)

def pageFileManager(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": 'd-flex flex-column'
	}
	return render(request, "pages/page-file-manager.html", context)

def pagePricing(request):
	return render(request, "pages/page-pricing.html")

def profile(request):
	return render(request, "pages/profile.html")

def calendar(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-0"
	}
	return render(request, "pages/calendar.html", context)

def settings(request):
	return render(request, "pages/settings.html")

def helper(request):
	return render(request, "pages/helper.html")
	
def error404(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-error.html", context)

def handler404(request, exception = None):
	return redirect('/404/')