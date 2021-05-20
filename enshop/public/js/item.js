frappe.ui.form.on("Item", {
    validate: function(frm,cdt,cdn){
        frm.doc.show_in_website = 1
    }
})