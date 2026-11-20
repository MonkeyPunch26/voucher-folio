import logging

from odoo import _, fields, models
from odoo.tools import consteq

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = "pos.config"

    voucher_override_pin = fields.Char(
        string="Clave para pagos sin folio",
        groups="point_of_sale.group_pos_manager",
        copy=False,
        help="Clave que permite validar un pago con tarjeta sin folio de voucher "
             "(p. ej. si la máquina se trabó). Nunca se envía a la caja: se verifica en el servidor.",
    )

    def check_voucher_override_pin(self, pin):
        """Verifica la clave en el servidor. Devuelve True/False."""
        self.ensure_one()
        stored = self.sudo().voucher_override_pin or ""
        ok = bool(stored) and bool(pin) and consteq(str(pin), stored)
        _logger.info(
            "POS %s: autorización sin folio %s (usuario %s)",
            self.name, "ACEPTADA" if ok else "RECHAZADA", self.env.user.login,
        )
        return ok
