frappe.ui.form.on("Vehicle Sale", {
	// ── On Load ──────────────────────────────────────────────────────────────

	refresh: function (frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Apply for Loan (DSA)"), function () {
				if (!frm.is_dirty()) {
					frappe.call({
						method: "auto_dealer.auto_dealer.api.loan_dsa.apply_for_loan",
						args: { vehicle_sale: frm.doc.name },
						callback: function (r) {
							if (r.message && r.message.success) {
								frappe.show_alert({
									message: __("Loan application submitted. App ID: {0}", [r.message.application_id]),
									indicator: "green",
								});
								frm.reload_doc();
							}
						},
					});
				} else {
					frappe.msgprint(__("Please save the form first before applying for a loan."));
				}
			}, __("Finance"));

			frm.add_custom_button(__("Push to Marketplace"), function () {
				frappe.call({
					method: "auto_dealer.auto_dealer.api.marketplace_sync.push_vehicle_to_marketplace",
					args: { vehicle: frm.doc.vehicle },
					callback: function (r) {
						if (r.message && r.message.status === "success") {
							frappe.show_alert({ message: __("Vehicle pushed to marketplace"), indicator: "green" });
						}
					},
				});
			}, __("Marketplace"));
		}
	},

	// ── EMI Calculation on field change ──────────────────────────────────────

	loan_amount: function (frm) { frm.trigger("_recalculate_emi"); },
	interest_rate: function (frm) { frm.trigger("_recalculate_emi"); },
	tenure_months: function (frm) { frm.trigger("_recalculate_emi"); },
	finance_type: function (frm) {
		let show = frm.doc.finance_type === "Loan";
		frm.toggle_display(["financier", "loan_amount", "down_payment", "tenure_months", "interest_rate", "emi_amount"], show);
		frm.trigger("_recalculate_emi");
	},

	_recalculate_emi: function (frm) {
		if (frm.doc.finance_type !== "Loan") {
			frm.set_value("emi_amount", 0);
			return;
		}
		const P = frm.doc.loan_amount;
		const r = frm.doc.interest_rate;
		const n = frm.doc.tenure_months;

		if (P && r && n) {
			const emi = auto_dealer.calculate_emi(P, r, n);
			frm.set_value("emi_amount", emi);
			frappe.show_alert({
				message: __("EMI calculated: ₹{0}/month", [format_number(emi, null, 2)]),
				indicator: "blue",
			});
		}
	},

	// ── Total Amount ─────────────────────────────────────────────────────────

	agreed_price: function (frm) { frm.trigger("_recalculate_total"); },
	discount_amount: function (frm) { frm.trigger("_recalculate_total"); },
	accessories_amount: function (frm) { frm.trigger("_recalculate_total"); },

	_recalculate_total: function (frm) {
		const total = (frm.doc.agreed_price || 0) - (frm.doc.discount_amount || 0) + (frm.doc.accessories_amount || 0);
		frm.set_value("total_amount", total);
	},

	// ── Fetch Vehicle details ─────────────────────────────────────────────────

	vehicle: function (frm) {
		if (!frm.doc.vehicle) return;
		frappe.call({
			method: "auto_dealer.auto_dealer.doctype.vehicle.vehicle.get_vehicle_details",
			args: { vin: frm.doc.vehicle },
			callback: function (r) {
				if (r.message) {
					const v = r.message;
					frm.set_value("agreed_price", v.on_road_price || v.ex_showroom_price);
					frappe.show_alert({
						message: __("Vehicle: {0} {1} {2} | Status: {3}", [v.make, v.model, v.variant || "", v.status]),
						indicator: v.status === "Available" ? "green" : "orange",
					});
					if (v.status !== "Available" && v.status !== "Booked") {
						frappe.msgprint(__("Warning: Vehicle {0} is currently {1}. Verify before proceeding.", [frm.doc.vehicle, v.status]));
					}
				}
			},
		});
	},
});
