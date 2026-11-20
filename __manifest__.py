{
    "name": "POS: folio de voucher Transbank obligatorio",
    "summary": "Exige el folio del voucher de la máquina de tarjetas en cada pago con tarjeta. "
               "Permite continuar sin folio solo con clave de autorización y deja el pago "
               "marcado para seguimiento.",
    "version": "17.0.1.0.0",
    "category": "Point of Sale",
    "author": "Dros",
    "license": "LGPL-3",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_payment_method_views.xml",
        "views/pos_payment_views.xml",
        "views/pos_order_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_voucher_folio/static/src/app/voucher_popup.js",
            "pos_voucher_folio/static/src/app/voucher_popup.xml",
            "pos_voucher_folio/static/src/app/payment_patch.js",
            "pos_voucher_folio/static/src/app/receipt.xml",
        ],
    },
    "installable": True,
    "application": False,
}
