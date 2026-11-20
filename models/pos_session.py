from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _get_pos_ui_pos_config(self, params):
        config = super()._get_pos_ui_pos_config(params)
        # La clave nunca viaja al navegador (un encargado con acceso la tendría cargada).
        config.pop("voucher_override_pin", None)
        return config

    def _loader_params_pos_payment_method(self):
        params = super()._loader_params_pos_payment_method()
        params["search_params"]["fields"].append("require_voucher_ref")
        return params
