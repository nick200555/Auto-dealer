frappe.ui.form.on("Service Job Card", {
	refresh: function (frm) {
		// Show "Send Ready Notification" button for completed jobs
		if (frm.doc.docstatus === 1 && frm.doc.status === "Completed" && frm.doc.mobile_no) {
			frm.add_custom_button(__("Send Ready SMS/WhatsApp"), function () {
				frappe.call({
					method: "auto_dealer.auto_dealer.api.whatsapp.send_whatsapp_message",
					args: {
						mobile_no: frm.doc.mobile_no,
						message: `Dear ${frm.doc.customer_name || frm.doc.customer}, your vehicle (VIN: ${frm.doc.vehicle}) is ready for pickup. Total: ₹${frm.doc.grand_total}. Thank you!`,
					},
					callback: function (r) {
						if (!r.exc) {
							frappe.show_alert({ message: __("Notification sent"), indicator: "green" });
						}
					},
				});
			}, __("Notify Customer"));
		}
	},

	// Auto-calculate line totals for parts
	service_items_on_form_rendered: function (frm) {
		frm.fields_dict.service_items.grid.on_row_add = function (row) {
			frappe.ui.form.on("Service Job Card Item", {
				qty: function (frm, cdt, cdn) {
					_calc_parts_row(frm, cdt, cdn);
				},
				rate: function (frm, cdt, cdn) {
					_calc_parts_row(frm, cdt, cdn);
				},
			});
		};
	},
});

function _calc_parts_row(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	const amount = (row.qty || 0) * (row.rate || 0);
	frappe.model.set_value(cdt, cdn, "amount", amount);
	frm.refresh_field("service_items");
}

frappe.ui.form.on("Service Job Card Item", {
	qty: function (frm, cdt, cdn) { _calc_parts_row(frm, cdt, cdn); },
	rate: function (frm, cdt, cdn) { _calc_parts_row(frm, cdt, cdn); },
});

frappe.ui.form.on("Service Job Card Labour", {
	hours: function (frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", (row.hours || 0) * (row.rate_per_hour || 0));
		frm.refresh_field("labour_items");
	},
	rate_per_hour: function (frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", (row.hours || 0) * (row.rate_per_hour || 0));
		frm.refresh_field("labour_items");
	},
});
