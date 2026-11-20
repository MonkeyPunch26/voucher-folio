# pos_voucher_folio (Odoo 17 Community)

Exige el folio del voucher de la máquina de tarjetas (Transbank u otra) en cada pago con tarjeta
del POS, para poder cuadrar cada venta con su voucher sin integrar Odoo con Transbank.

## Qué hace
- En el método de pago marcado con **Exigir folio de voucher**, al validar la venta la caja pide
  el N° de operación del voucher. Sin folio no se puede terminar la venta.
- Si la máquina falló: botón **Sin folio…** → clave de autorización + motivo. La clave se verifica
  en el servidor y nunca se envía al navegador. El pago queda marcado "Autorizado sin folio".
- Pagos mixtos: solo se pide folio para la parte pagada con tarjeta.
- El folio se imprime en el ticket de Odoo.
- Backend: menú **Punto de Venta > Folios de voucher** (solo encargados) con los pagos con
  tarjeta; los autorizados sin folio salen en rojo hasta que alguien complete el folio en la misma
  lista. La marca "Autorizado sin folio" se conserva para auditoría. Búsqueda por folio en
  Pagos y columna de folio en la pestaña Pagos de cada pedido.
- Defensa en servidor: si llega un pago con tarjeta sin folio ni autorización, se registra igual
  (no se pierde la venta) pero queda marcado como pendiente.

## Configurar
1. Copiar la carpeta a los addons, actualizar lista de aplicaciones e instalar.
2. **Cerrar todas las sesiones del POS** (Odoo no deja modificar métodos de pago con cajas abiertas).
3. Punto de Venta > Configuración > Métodos de pago > Tarjeta: marcar **Exigir folio de voucher**.
4. Punto de Venta > Configuración > Ajustes > Pago: **Clave para pagos sin folio**.
   Sin clave configurada, nadie puede saltarse el folio.

## Tests
`odoo-bin -d <db> -u pos_voucher_folio --test-enable --test-tags /pos_voucher_folio --stop-after-init`
