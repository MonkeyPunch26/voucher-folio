from odoo import fields, models


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    require_voucher_ref = fields.Boolean(
        string="Exigir folio de voucher",
        help="Al pagar con este método, la caja exige el folio (N° de operación) del "
             "voucher de la máquina de tarjetas. Sin folio, solo se puede continuar con "
             "la clave de autorización.",
    )
