import frappe
from frappe import _
from frappe.utils import cint
from erpnext.shopping_cart.cart import _get_cart_quotation
from erpnext.utilities.product import get_qty_in_stock


@frappe.whitelist()
def place_order(shipping_service, po_no):
	quotation = _get_cart_quotation()
	cart_settings = frappe.db.get_value("Shopping Cart Settings", None,
		["company", "allow_items_not_in_stock"], as_dict=1)
	quotation.company = cart_settings.company

	quotation.flags.ignore_permissions = True
	quotation.submit()

	if quotation.quotation_to == 'Lead' and quotation.party_name:
		# company used to create customer accounts
		frappe.defaults.set_user_default("company", quotation.company)

	if not (quotation.shipping_address_name or quotation.customer_address):
		frappe.throw(_("Set Shipping Address or Billing Address"))

	from erpnext.selling.doctype.quotation.quotation import _make_sales_order
	sales_order = frappe.get_doc(_make_sales_order(quotation.name, ignore_permissions=True))
	sales_order.payment_schedule = []
	sales_order.shipping_service = shipping_service
	sales_order.po_no = po_no

	if not cint(cart_settings.allow_items_not_in_stock):
		for item in sales_order.get("items"):
			item.reserved_warehouse, is_stock_item = frappe.db.get_value("Item",
				item.item_code, ["website_warehouse", "is_stock_item"])

			if is_stock_item:
				item_stock = get_qty_in_stock(item.item_code, "website_warehouse")
				if not cint(item_stock.in_stock):
					frappe.throw(_("{1} Not in Stock").format(item.item_code))
				if item.qty > item_stock.stock_qty[0][0]:
					frappe.throw(_("Only {0} in Stock for item {1}").format(item_stock.stock_qty[0][0], item.item_code))

	sales_order.flags.ignore_permissions = True
	sales_order.insert()
	sales_order.submit()

	if hasattr(frappe.local, "cookie_manager"):
		frappe.local.cookie_manager.delete_cookie("cart_count")

	return make_invoice("Sales Order", sales_order.name)



def make_invoice(ref_doc, ref_name):
		ref_doc = frappe.get_doc(ref_doc, ref_name)
		if (hasattr(ref_doc, "order_type") and getattr(ref_doc, "order_type") == "Shopping Cart"):
			from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
			si = make_sales_invoice(ref_name, ignore_permissions=True)
			si = si.insert(ignore_permissions=True)
			si.submit()

		return si.name
