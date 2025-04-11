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
		'url': '/analytics',
		'icon': 'bi bi-bar-chart',
		'text': 'Analytics',
		'name': 'analytics'
	}, {
		'icon': 'bi bi-envelope',
		'text': 'Email',
		'children': [{
			'url': '/email/inbox',
			'action': 'Inbox',
			'text': 'Inbox',
			'name': 'emailInbox'
		}, {
			'url': '/email/compose',
			'action': 'Compose',
			'text': 'Compose',
			'name': 'emailCompose'
		}, {
			'url': '/email/detail',
			'action': 'Detail',
			'text': 'Detail',
			'name': 'emailDetail'
		}]
	}, {
		'is_divider': 1
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
		'text': 'Users',
		'is_header': 1
	}, {
		'url': '/settings',
		'icon': 'bi bi-gear',
		'text': 'Settings',
		'name': 'settings'
	}]
	
	resolved_path = resolve(request.path_info)

	current_path_name = resolved_path.url_name
	
	sidebar_menu = mark_active_link(sidebar_menu, current_path_name)

	return {'sidebar_menu': sidebar_menu}