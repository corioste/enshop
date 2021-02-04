import frappe

def update_website_context(context):
    shipping_service = frappe.get_all("Shipping Service")
    context.shipping_service = shipping_service

    category_list = frappe.get_all("Sub Category")
    context.category_label = "Item Category"
    context.category_list = category_list
