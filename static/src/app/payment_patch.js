/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Payment } from "@point_of_sale/app/store/models";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { VoucherPopup } from "./voucher_popup";

// --- Modelo: el pago transporta folio / autorización hasta el servidor ---
patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
        this.voucher_missing = this.voucher_missing || false;
        this.voucher_note = this.voucher_note || "";
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.transaction_id = json.transaction_id || "";
        this.voucher_missing = json.voucher_missing || false;
        this.voucher_note = json.voucher_note || "";
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.voucher_missing = this.voucher_missing;
        json.voucher_note = this.voucher_note;
        return json;
    },
    export_for_printing() {
        const res = super.export_for_printing(...arguments);
        res.voucher_folio = this.transaction_id || "";
        res.voucher_missing = this.voucher_missing;
        return res;
    },
    needsVoucherFolio() {
        return Boolean(
            this.payment_method?.require_voucher_ref &&
                !this.payment_method?.use_payment_terminal &&
                this.get_amount() !== 0 &&
                !this.transaction_id &&
                !this.voucher_missing
        );
    },
});

// --- Pantalla de pago: no se valida sin folio (o autorización) ---
patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        for (const line of this.paymentLines) {
            if (!line.needsVoucherFolio()) {
                continue;
            }
            const { confirmed, payload } = await this.popup.add(VoucherPopup, {
                methodName: line.payment_method.name,
                amount: this.env.utils.formatCurrency(line.get_amount()),
                configId: this.pos.config.id,
            });
            if (!confirmed || !payload) {
                return; // se queda en la pantalla de pago
            }
            if (payload.folio) {
                line.transaction_id = payload.folio;
            } else if (payload.override) {
                line.voucher_missing = true;
                line.voucher_note = payload.reason;
            }
        }
        return super.validateOrder(...arguments);
    },
});
