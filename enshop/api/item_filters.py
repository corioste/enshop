import frappe


@frappe.whitelist(allow_guest=True)
def get_categories_from_group(group_name):

    final_category_list = []

    params = ""

    sql_group_child = get_sql_parent_child_group(group_name)

    group_child_list = frappe.db.sql(sql_group_child, as_dict=1)

    for child_list in group_child_list:
        child_name = child_list.name
        params = params + 'ti.item_group = "'+child_name+'"'
        if(group_child_list[-1] != child_list):
            params = params + " || "

    categories = get_categories_from_group_parent(params)

    categories_list = frappe.db.sql(categories, as_dict=1)

    all_categories = _get_featured_cards("featured_categories_cards")

    for category_x in all_categories:
        for category_y in categories_list:
            if category_x.label == category_y.category_name:
                final_category_list.append(category_x)

    html = frappe.render_template('enshop/www/filter-categories/categories-row.html', {
                                  "featured_categories_cards": final_category_list})

    return html


@frappe.whitelist(allow_guest=True)
def get_products_html_for_website_by_category_name(category_name):

    sql_query = get_sql_query(category_name)

    items = frappe.db.sql(sql_query, as_dict=1)

    html = ''.join(get_html_for_items(items))

    if not items:
        html = frappe.render_template(
            'erpnext/www/all-products/not_found.html', {})

    return html


@frappe.whitelist(allow_guest=True)
def get_products_html_for_website_by_category_name_and_group(category_name, group_name):
    category_name = category_name.replace("&amp;", "&")

    params = ""

    sql_group_child = get_sql_parent_child_group(group_name)

    group_child_list = frappe.db.sql(sql_group_child, as_dict=1)

    for child_list in group_child_list:
        child_name = child_list.name
        params = params + 'ti.item_group = "'+child_name+'"'
        if(group_child_list[-1] != child_list):
            params = params + " || "

    sql_query = get_sql_query_group(category_name, params)

    items = frappe.db.sql(sql_query, as_dict=1)

    html = ''.join(get_html_for_items(items))

    if not items:
        html = frappe.render_template(
            'erpnext/www/all-products/not_found.html', {})

    return html


def get_html_for_items(items):
    html = []
    for item in items:
        html.append(frappe.render_template('enshop/www/all-products/item_col.html', {
            'item': item
        }))
    return html


def get_sql_query(category_name):
    return '''SELECT 
					ti.name, 
					ti.item_name, 
					ti.website_image, 
					ti.image, 
					ti.web_long_description , 
					ti.description , 
					ti.route  
				FROM  tabItem AS ti 
				INNER JOIN `tabSub Category Child` AS tcc 
				ON ti.name = tcc.parent 
				WHERE tcc.category_name = "{0}"'''.format(category_name)


def get_sql_query_group(category_name, params):
    return '''SELECT 
					ti.name, 
					ti.item_name, 
					ti.website_image, 
					ti.image, 	
					ti.web_long_description , 
					ti.description , 
					ti.route  
				FROM  tabItem AS ti 
				INNER JOIN `tabSub Category Child` AS tcc 
				ON ti.name = tcc.parent 
				WHERE {0}
				AND tcc.category_name = "{1}"
		'''.format(params, category_name)


def get_sql_parent_child_group(parent_name):
    return '''SELECT name FROM `tabItem Group` where parent_item_group = "{0}"'''.format(parent_name)


def get_categories_from_group_parent(group_names):
    return '''SELECT  DISTINCT tcc.category_name  
		FROM  tabItem AS ti 
		INNER JOIN `tabSub Category Child` AS tcc 
		ON ti.name = tcc.parent 
		WHERE {0}'''.format(group_names)


def _get_featured_cards(parentfield):
    return frappe.get_all(
        "Enshop Settings Card",
        fields=["label", "imageurl"],
        filters={"parentfield": parentfield}
    )
