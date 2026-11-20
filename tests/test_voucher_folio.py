from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@tagged("post_install", "-at_install")
class TestVoucherFolio(TestPoSCommon):

    def setUp(self):
        super().setUp()
        self.config = self.basic_config
        self.bank_pm1.require_voucher_ref = True
        self.product = self.create_product("Chaqueta", self.categ_basic, 10000)
        self.open_new_session()

    def _order(self, pm, **payment_extra):
        data = self.create_ui_order_data([(self.product, 1)], payments=[(pm, 10000)])
        data["data"]["statement_ids"][0][2].update(payment_extra)
        res = self.env["pos.order"].create_from_ui([data])
        return self.env["pos.order"].browse(res[0]["id"]).payment_ids

    # --- clave de autorización ---
    def test_pin_check(self):
        self.assertFalse(self.config.check_voucher_override_pin("1234"), "sin clave configurada nada pasa")
        self.config.voucher_override_pin = "1234"
        self.assertTrue(self.config.check_voucher_override_pin("1234"))
        self.assertFalse(self.config.check_voucher_override_pin("9999"))
        self.assertFalse(self.config.check_voucher_override_pin(""))

    def test_pin_never_sent_to_pos(self):
        self.config.voucher_override_pin = "1234"
        data = self.pos_session.load_pos_data()
        self.assertNotIn("voucher_override_pin", data["pos.config"])
        methods = {m["id"]: m for m in data["pos.payment.method"]}
        self.assertTrue(methods[self.bank_pm1.id]["require_voucher_ref"])
        self.assertFalse(methods[self.cash_pm1.id]["require_voucher_ref"])

    # --- registro de pagos ---
    def test_payment_with_folio(self):
        payment = self._order(self.bank_pm1, transaction_id="  98765 ")
        self.assertEqual(payment.transaction_id, "98765")
        self.assertFalse(payment.voucher_missing)
        self.assertFalse(payment.voucher_pending)

    def test_payment_authorized_without_folio_and_followup(self):
        payment = self._order(self.bank_pm1, voucher_missing=True, voucher_note="máquina trabada")
        self.assertTrue(payment.voucher_missing)
        self.assertEqual(payment.voucher_note, "máquina trabada")
        self.assertTrue(payment.voucher_pending)
        # Seguimiento: el encargado completa el folio después
        payment.transaction_id = "55555"
        self.assertFalse(payment.voucher_pending)
        self.assertTrue(payment.voucher_missing, "la marca de auditoría se conserva")

    def test_payment_without_folio_is_flagged_by_server(self):
        payment = self._order(self.bank_pm1)
        self.assertTrue(payment.voucher_missing)
        self.assertTrue(payment.voucher_pending)
        self.assertIn("sin folio", payment.voucher_note)

    def test_cash_not_affected(self):
        payment = self._order(self.cash_pm1)
        self.assertFalse(payment.voucher_missing)
        self.assertFalse(payment.transaction_id)
