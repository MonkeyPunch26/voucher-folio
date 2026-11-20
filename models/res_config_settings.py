from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_voucher_override_pin = fields.Char(
        related="pos_config_id.voucher_override_pin", readonly=False,
        groups="point_of_sale.group_pos_manager",
    )
