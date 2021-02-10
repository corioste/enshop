import frappe


@frappe.whitelist(allow_guest=True)
def get_doc(doc_type, doc_name):
    doc = frappe.get_doc(doc_type, doc_name)
    return doc


@frappe.whitelist(allow_guest=True)
def get_doc_single(doc_type):
    doc = frappe.get_doc(doc_type)
    return doc
