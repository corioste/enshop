import frappe

@frappe.whitelist()
def remove_item_image():
    items = frappe.get_all("Item")
    for item in items:
        item_doc = frappe.get_doc("Item", item.name)
        item_doc.image = ""
        item_doc.save()
        frappe.db.commit()

    print("DONE")