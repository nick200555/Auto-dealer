frappe.ui.form.on("Test Drive", {
	refresh: function (frm) {
		if (frm.doc.docstatus === 1 && frm.doc.status === "Completed") {
			frm.add_custom_button(__("Create Vehicle Sale"), function () {
				frappe.new_doc("Vehicle Sale", {
					vehicle: frm.doc.vehicle,
					customer: frm.doc.customer,
					sales_executive: frm.doc.sales_executive,
				});
			}, __("Actions"));
		}
	},

	end_time: function (frm) {
		// Auto-calculate distance if odometer values are set
		if (frm.doc.odometer_start && frm.doc.odometer_end) {
			let distance = frm.doc.odometer_end - frm.doc.odometer_start;
			if (distance < 0) {
				frappe.msgprint(__("Odometer End cannot be less than Start."), __("Validation Error"));
				frm.set_value("odometer_end", frm.doc.odometer_start);
				return;
			}
			frm.set_value("distance_covered", distance);
			frappe.show_alert({
				message: __("Distance covered: {0} km", [distance]),
				indicator: "blue",
			});
		}
	},

	odometer_end: function (frm) {
		frm.trigger("end_time");
	},
});
