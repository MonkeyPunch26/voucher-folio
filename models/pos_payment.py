from odoo import api, fields, models


class PosPayment(models.Model):
    _inherit = "pos.payment"

    require_voucher_ref = fields.Boolean(related="payment_method_id.require_voucher_ref")
    voucher_missing = fields.Boolean(
        string="Autorizado sin folio",
        readonly=True,
        help="El pago se registró sin folio de voucher (con clave de autorización o por "
             "falta del dato). Queda marcado de forma permanente para auditoría.",
    )
    voucher_note = fields.Char(string="Motivo sin folio", readonly=True)
    voucher_pending = fields.Boolean(
        string="Folio pendiente",
        compute="_compute_voucher_pending",
        store=True,
    )

    @api.depends("voucher_missing", "transaction_id")
    def _compute_voucher_pending(self):
        for payment in self:
            payment.voucher_pending = payment.voucher_missing and not payment.transaction_id

    def _export_for_ui(self, payment):
        res = super()._export_for_ui(payment)
        res.update(
            transaction_id=payment.transaction_id,
            voucher_missing=payment.voucher_missing,
            voucher_note=payment.voucher_note,
        )
        return res
