import frappe


@frappe.whitelist(allow_guest=True)
def get_categories_from_group(group_name):

    final_category_list = []

    params = ""

    sql_group_child = get_sql_parent_child_group(group_name)

    group_child_list = frappe.db.sql(sql_group_child, as_dict=1)
    print(group_child_list)
    for child_list in group_child_list:
        child_name = child_list.name
        params = params + 'ti.item_group = "'+child_name+'"'
        if(group_child_list[-1] != child_list):
            params = params + " || "

    categories = get_categories_from_group_parent(params)

    categories_list = frappe.db.sql(categories, as_dict=1)

    all_categories = _get_featured_cards()

    for category_x in all_categories:
        for category_y in categories_list:
            if category_x.category_name == category_y.category_name:
                if category_x.show_in_website == 1:
                    final_category_list.append(category_x)

    return final_category_list


@frappe.whitelist(allow_guest=True)
def get_products_html_for_website_by_category_name(category_name):

    sql_query = get_sql_query(category_name)

    items = frappe.db.sql(sql_query, as_dict=1)

    html = ''.join(get_html_for_items(items))

    if not items:
        html = frappe.render_template(
            'enshop/www/shop/not_found.html', {})

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

    print("JS")
    print(items)
    if not items:
        html = frappe.render_template(
            'enshop/www/shop/not_found.html', {})

    return html


@frappe.whitelist(allow_guest=True)
def get_products_items_by_category_name_and_group(category_name, group_name):
    category_name = category_name.replace("&amp;", "&")

    params = ""

    sql_group_child = get_sql_parent_child_group(group_name)

    group_child_list = frappe.db.sql(sql_group_child, as_dict=1)

    for child_list in group_child_list:
        child_name = child_list.name
        params = params + 'ti.item_group = "'+child_name+'"'
        if(group_child_list[-1] != child_list):
            params = params + " || "

    sql_query = get_sql_query_group_with_page(category_name, params)

    items = frappe.db.sql(sql_query, as_dict=1)

    return items


def get_html_for_items(items):
    html = []
    for item in items:
        html.append(frappe.render_template('enshop/www/shop/item_col.html', {
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


def get_sql_query_group_with_page(category_name, params):
    start = frappe.form_dict.start or 0
    products_settings = get_product_settings()
    page_length = products_settings.products_per_page
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
				WHERE ({0})
				AND tcc.category_name = "{1}"
                LIMIT {2}
                OFFSET {3}
		'''.format(params, category_name, page_length, start)


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
				WHERE ({0})
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


def _get_featured_cards():
    return frappe.get_all(
        "Sub Category",
        fields=["show_in_website", "category_name", "attach_image_3"]
    )


def get_product_settings():
    doc = frappe.get_cached_doc('Products Settings')
    doc.products_per_page = doc.products_per_page or 20
    return doc
