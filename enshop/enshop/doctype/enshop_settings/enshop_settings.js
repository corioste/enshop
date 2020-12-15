// Copyright (c) 2020, Bai Web and Mobile Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Enshop Settings', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Enshop Settings Card Most Popular', {
	item_code: function (frm,cdt,cdn) {
		const hostname = "https://"+window.location.hostname
		const child_doc = frappe.get_doc(cdt,cdn);
		const current_index = child_doc.idx - 1
		frm.call({
			method: "get_item_title",
			args: {
				"item_code": frm.doc.most_popular_cards[current_index].item_code
			},
			callback: function (r) {
				const item_doc = r.message
				frappe.model.set_value(cdt, cdn, "label", item_doc.item_name)
				frappe.model.set_value(cdt, cdn, "hyperlink", hostname+'/'+item_doc.route)
				frappe.model.set_value(cdt, cdn, "imageurl", hostname+'/'+item_doc.image)
				console.log(item_doc)
			}
		});
	}
});

frappe.ui.form.on('Enshop Settings Card', {
	label: function (frm,cdt,cdn) {
		frappe.model.set_value(cdt, cdn, "imageurl", "https://via.placeholder.com/400x250")
	},
	image_file: function(frm,cdt,cdn){
		const child_doc = frappe.get_doc(cdt,cdn);
		const current_index = child_doc.idx - 1
		const file_name = frm.doc.featured_categories_cards[current_index].image_file
		frappe.model.set_value(cdt, cdn, "imageurl", file_name)
	}
});

frappe.ui.form.on('Enshop Group Card', {
	item_group: function (frm,cdt,cdn) {

		const child_doc = frappe.get_doc(cdt,cdn);
		
		const current_index = child_doc.idx - 1
		const item_group = frm.doc.featured_item_group[current_index].item_group

		frappe.model.set_value(cdt, cdn, "label", item_group)
		frappe.model.set_value(cdt, cdn, "imageurl", "https://via.placeholder.com/400x250")
		
		
	}
});