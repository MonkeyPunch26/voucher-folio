/** @odoo-module */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { onMounted, useRef, useState } from "@odoo/owl";

export const FOLIO_REGEX = /^[A-Za-z0-9-]{1,30}$/;

/**
 * Pide el folio del voucher. Payload al confirmar:
 *   { folio: "123456" }                      -> pago normal
 *   { override: true, reason: "..." }        -> autorizado sin folio (clave ya verificada)
 */
export class VoucherPopup extends AbstractAwaitablePopup {
    static template = "pos_voucher_folio.VoucherPopup";
    static defaultProps = {
        confirmKey: false, // Enter se maneja a mano según el modo
        cancelKey: "Escape",
        title: _t("Folio del voucher"),
        methodName: "",
        amount: "",
        configId: 0,
    };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({ mode: "folio", folio: "", pin: "", reason: "", error: "", busy: false });
        this.folioRef = useRef("folio");
        this.pinRef = useRef("pin");
        onMounted(() => this.folioRef.el?.focus());
    }

    get folioClean() {
        return this.state.folio.replace(/\s+/g, "");
    }
    get folioValid() {
        return FOLIO_REGEX.test(this.folioClean);
    }
    get canAuthorize() {
        return this.state.pin.trim() && this.state.reason.trim().length >= 3 && !this.state.busy;
    }

    _onWindowKeyup(event) {
        if (event.key === "Enter") {
            if (this.state.mode === "folio" && this.folioValid) {
                this.confirmFolio();
            } else if (this.state.mode === "auth" && this.canAuthorize) {
                this.authorize();
            }
            return;
        }
        super._onWindowKeyup(...arguments);
    }

    confirmFolio() {
        if (!this.folioValid) {
            this.state.error = _t("Folio inválido: solo letras, números o guion (máx. 30).");
            return;
        }
        this.props.close({ confirmed: true, payload: { folio: this.folioClean } });
    }

    goAuth() {
        this.state.mode = "auth";
        this.state.error = "";
        setTimeout(() => this.pinRef.el?.focus());
    }
    goBack() {
        this.state.mode = "folio";
        this.state.error = "";
        this.state.pin = "";
        setTimeout(() => this.folioRef.el?.focus());
    }

    async authorize() {
        if (!this.canAuthorize) {
            return;
        }
        this.state.busy = true;
        this.state.error = "";
        let ok = false;
        try {
            ok = await this.orm.call("pos.config", "check_voucher_override_pin", [
                [this.props.configId],
                this.state.pin,
            ]);
        } catch {
            this.state.error = _t(
                "No hay conexión con el servidor: la clave no se puede verificar. Reintente."
            );
            this.state.busy = false;
            return;
        }
        this.state.busy = false;
        if (!ok) {
            this.state.error = _t("Clave incorrecta.");
            this.state.pin = "";
            this.pinRef.el?.focus();
            return;
        }
        this.props.close({
            confirmed: true,
            payload: { override: true, reason: this.state.reason.trim() },
        });
    }
}
