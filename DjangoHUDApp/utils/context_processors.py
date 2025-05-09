from django.urls import resolve

def mark_active_link(menu, current_path_name):
    for item in menu:
        item['is_active'] = item.get('name', '') == current_path_name

        if 'children' in item:
            item['children'] = mark_active_link(item['children'], current_path_name)

            if any(child.get('is_active', False) for child in item['children']):
                item['is_active'] = True

    return menu

def sidebar_menu(request):
	sidebar_menu = [{
		'text': 'Navigation',
		'is_header': 1
	},{
		'url': '/',
		'icon': 'bi bi-cpu',
		'text': 'Dashboard',
		'name': 'index'
	}, {
		'url': '/cooperatives/planting-analytics',
		'icon': 'bi bi-bar-chart',
		'text': 'Land Analytics',
		'name': 'planting-analytics'
	}, {
		'icon': 'bi bi-envelope',
		'text': 'Collections',
		'children': [{
			'url': '/cooperatives/collections/',
			'action': 'Collections',
			'text': 'Collections',
			'name': 'collection_list'
		}, {
			'url': '/cooperatives/collections/bulk-upload',
			'action': 'Compose',
			'text': 'Upload Collections',
			'name': 'collection_bulk_upload'
		}]
	},{
     
     	'icon': 'bi bi-columns-gap',
		'text': 'Loans',
  		'children': [{
			'url': '/cooperatives/loan-suppliers/',
			'icon': 'bi bi-columns-gap',
			'text': 'Loan Suppliers',
			'name': 'loan-supplier-list'
	},{
		'url': '/cooperatives/credit-managers/',
		'icon': 'bi bi-columns-gap',
		'text': 'Credit Managers',
		'name': 'credit-manager-list'
	},{
		'url': '/cooperatives/loans/',
		'icon': 'bi bi-columns-gap',
		'text': 'Loan Requests',
		'name': 'loan-list'
	},{
		'url':'/cooperatives/loans/dashboard',
		'icon': 'bi bi-columns-gap',
		'text': 'Loan Dashboard',
		'name': 'loan_dashboard'
	}]
 }, {
		'text': 'Cooperatives',
		'is_header': 1
	}, {
		'icon': 'bi bi-columns-gap',
		'text': 'Cooperatives',
		'children': [{
			'url': '/cooperatives/',
			'text': 'All Cooperatives',
			'name': 'cooperatives:cooperative-list'
		}, {
			'url': '/cooperatives/farmer-groups/',
			'text': 'Farmer Groups',
			'name': 'cooperatives:farmer-group-list'
		}, {
			'url': '/cooperatives/members/',
			'text': 'Members',
			'name': 'cooperatives:member-list'
		}]
	},
	{
		'text': 'Product Control Center',
		'is_header': 1
	}, {
		'icon': 'bi bi-columns-gap',
		'text': 'Products',
		'children': [{
			'url': '/cooperatives/products/',
			'text': 'All Products',
			'name': 'cooperatives:product-list'
		}, {
			'url': '/cooperatives/prices/',
			'text': 'Market Price',
			'name': 'cooperatives:price-list'
		}, {
			'url': '/cooperatives/units/',
			'text': 'Units Config',
			'name': 'cooperatives:unit-list'
		}]
	},{
		'icon':'bi bi-columns',
		'text':'Suppliers',
		'children':[{
			'url':'/cooperatives/suppliers/',
			'text':'All Suppliers',
			'name':'supplier_list'
		},{
			'url':'/cooperatives/supplier-products/',
			'text':'Supplier Product List',
			'name':'supplier_product_list'
      	}]
     },
	{
		'text': 'Geographical Location Center',
		'is_header': 1
	}, {
		'icon': 'bi bi-columns-gap',
		'text': 'Locations & Addresses',
		'children': [{
			'url': '/cooperatives/districts/',
			'text': 'Districts',
			'name': 'cooperatives:district-list'
		}, {
			'url': '/cooperatives/counties/',
			'text': 'Counties',
			'name': 'cooperatives:county-list'
		}, {
			'url': '/cooperatives/sub-counties/',
			'text': 'Sub-Counties',
			'name': 'cooperatives:subcounty-list'
		},
		{
			'url': '/cooperatives/parishes/',
			'text': 'Parishes',
			'name': 'cooperatives:parish-list'
		},
		{
			'url': '/cooperatives/villages/',
			'text': 'Villages',
			'name': 'cooperatives:village-list'
		}]
	},
	 {
		'is_divider': 1
	}, {
		'text': 'Agents',
		'is_header': 1
	}, {
		'url': '/agents/',
		'icon': 'bi bi-gear',
		'text': 'All Agents',
		'name': 'agent-list'
	},{
		'url': '/agents/global-incentive/',
		'icon': 'bi bi-gear',
		'text': 'Commission',
		'name': 'agents:global-incentive'
	}]
	
	resolved_path = resolve(request.path_info)

	current_path_name = resolved_path.url_name
	
	sidebar_menu = mark_active_link(sidebar_menu, current_path_name)

	return {'sidebar_menu': sidebar_menu}