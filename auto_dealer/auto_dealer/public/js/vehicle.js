frappe.ui.form.on("Vehicle", {
	// Auto-uppercase VIN as user types
	vin: function (frm) {
		if (frm.doc.vin) {
			frm.set_value("vin", frm.doc.vin.toUpperCase());
		}
	},

	// Calculate on-road price on ex-showroom change (simple estimate)
	ex_showroom_price: function (frm) {
		if (frm.doc.ex_showroom_price && !frm.doc.on_road_price) {
			// Rough estimate: ex-showroom + 15% for taxes/registration
			let estimated = frm.doc.ex_showroom_price * 1.15;
			frm.set_value("on_road_price", Math.round(estimated));
			frappe.show_alert({
				message: __("On-Road Price estimated at 15% over Ex-Showroom."),
				indicator: "blue",
			});
		}
	},

	// Button: Update Status
	refresh: function (frm) {
		if (frm.doc.docstatus === 1 && frm.doc.status !== "Sold") {
			frm.add_custom_button(__("Mark as Demo"), function () {
				frappe.call({
					method: "auto_dealer.auto_dealer.doctype.vehicle.vehicle.update_vehicle_status",
					args: { vin: frm.doc.vin, status: "Demo" },
					callback: function (r) {
						if (!r.exc) {
							frappe.show_alert({ message: __("Status updated to Demo"), indicator: "green" });
							frm.reload_doc();
						}
					},
				});
			}, __("Actions"));

			frm.add_custom_button(__("Mark as Available"), function () {
				frappe.call({
					method: "auto_dealer.auto_dealer.doctype.vehicle.vehicle.update_vehicle_status",
					args: { vin: frm.doc.vin, status: "Available" },
					callback: function (r) {
						if (!r.exc) {
							frappe.show_alert({ message: __("Status updated to Available"), indicator: "green" });
							frm.reload_doc();
						}
					},
				});
			}, __("Actions"));
		}

		// Days-in-stock color indicator
		if (frm.doc.days_in_stock !== undefined) {
			let days = frm.doc.days_in_stock;
			let color = days > 90 ? "red" : days > 60 ? "orange" : "green";
			frm.get_field("days_in_stock").$wrapper.find(".control-value").css("color", color);
		}
	},
});
