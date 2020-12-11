# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bai Web and Mobile Lab and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class EnshopSettings(Document):
	def validate(self):
		pass

def _validate_cards(doc):
	if len(doc.most_popular_cards) != 3:
		frappe.throw(_('Please add 3 most popular cards'))
	if len(doc.featured_categories_cards) != 3:
		frappe.throw(_('Please add 3 featured categories cards'))


@frappe.whitelist()
def get_item_title(item_code=None):
	doc = ""
	if item_code:
		doc = frappe.get_doc("Item", item_code)
	

	return doc
		
