/**
 * Auto Dealer — Global App JS
 * Included on every Frappe Desk page via hooks.py app_include_js
 */

frappe.provide("auto_dealer");

auto_dealer = {
	/**
	 * Format a VIN into the standard display format: XXXX-XXXXX-XXXXXXXX
	 */
	format_vin: function (vin) {
		if (!vin || vin.length !== 17) return vin || "";
		return `${vin.slice(0, 4)}-${vin.slice(4, 9)}-${vin.slice(9)}`;
	},

	/**
	 * Calculate EMI using the PMT formula (reducing-balance method)
	 * @param {number} principal - Loan amount
	 * @param {number} annual_rate - Annual interest rate in %
	 * @param {number} months - Tenure in months
	 * @returns {number} Monthly EMI amount
	 */
	calculate_emi: function (principal, annual_rate, months) {
		if (!principal || !annual_rate || !months) return 0;
		const r = annual_rate / 12 / 100;
		const emi = (principal * r * Math.pow(1 + r, months)) / (Math.pow(1 + r, months) - 1);
		return Math.round(emi * 100) / 100;
	},

	/**
	 * Show a loading indicator while an async call runs
	 * @param {string} msg - Message to show
	 */
	show_loading: function (msg) {
		frappe.show_progress(__("Please wait"), 0, 100, __(msg));
	},

	hide_loading: function () {
		frappe.hide_progress();
	},
};

// ── Dashboard KPI refresh ─────────────────────────────────────────────────────
$(document).on("page-change", function () {
	if (frappe.get_route_str() === "auto-dealer-dashboard") {
		auto_dealer.refresh_dashboard_kpis();
	}
});

auto_dealer.refresh_dashboard_kpis = function () {
	frappe.call({
		method: "auto_dealer.auto_dealer.utils.get_kpis",
		callback: function (r) {
			if (r.message) {
				console.log("[Auto Dealer KPIs]", r.message);
				// KPI cards update is handled by the Page's own script
			}
		},
	});
};
