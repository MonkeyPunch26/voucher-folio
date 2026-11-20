from odoo import _, api, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        vals = super()._payment_fields(order, ui_paymentline)
        folio = (ui_paymentline.get("transaction_id") or "").strip()
        vals["transaction_id"] = folio or False
        vals["voucher_missing"] = bool(ui_paymentline.get("voucher_missing"))
        vals["voucher_note"] = ui_paymentline.get("voucher_note") or False
        # Defensa en servidor: nunca se pierde una venta, pero si llega un pago con tarjeta
        # sin folio y sin autorización (p. ej. caja con código viejo), queda marcado.
        method = self.env["pos.payment.method"].browse(vals.get("payment_method_id"))
        if method.require_voucher_ref and vals.get("amount") and not folio and not vals["voucher_missing"]:
            vals["voucher_missing"] = True
            vals["voucher_note"] = _("Llegó sin folio ni autorización desde la caja")
        return vals
