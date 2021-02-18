import frappe
from frappe.utils.background_jobs import enqueue


def execute_price_list_update(doc_name):

    doc = frappe.get_doc("Price List", doc_name)

    item_group = doc.item_group

    for group in item_group:

        items = frappe.get_all(
            "Item", filters={"item_group": group.item_group}, fields=["name"])

        for item in items:
            item_price_list = frappe.get_all("Item Price", filters={
                                             "price_list": doc.name, "item_code": item.name}, fields=["name"])

            for item_price in item_price_list:
                item_price_doc = frappe.get_doc("Item Price", item_price.name)
                item_price_doc.db_set(
                    'price_list_rate',  group.price, update_modified=False)


@frappe.whitelist(allow_guest=True)
def price_list_update(doc_name):
    enqueue(execute_price_list_update, queue='long',
            job_name="Update Price List", timeout='3000', doc_name=doc_name, )
    return "SUCCESS"
