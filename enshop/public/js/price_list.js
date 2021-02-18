frappe.ui.form.on("Price List", {
    validate: function(frm,cdt,cdn){

        frappe.call({
            method: "enshop.enshop.doc_events.price_list.price_list_update",
            args: {
                doc_name: frm.doc.name
            },
            callback: function(r){
                console.log(r.message)
            }
        })
    }
})