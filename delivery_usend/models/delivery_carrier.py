"""
Puente entre Odoo (delivery.carrier) y UsendClient.

Sigue el mismo patrón que los conectores oficiales de Odoo para DHL/FedEx/UPS:
se agrega 'usend' como opción del campo selection `delivery_type`, y se
implementan los métodos que el framework de delivery.carrier espera
(rate_shipment, send_shipping, get_tracking_link, cancel_shipment).

Las credenciales (WS_TEST) NO van como campo de este modelo — se leen desde
Ajustes > Técnico > Parámetros del Sistema (ir.config_parameter), tal como
quedó acordado. Este archivo solo debe LEER esos parámetros, nunca
hardcodearlos.
"""

from odoo import models, fields, api
from .usend_client import UsendClient


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    # TODO: agregar 'usend' como opción de este selection. Ojo: hay que
    # extender el selection existente, no reemplazarlo — revisar cómo lo
    # hacen los módulos delivery_dhl / delivery_fedex como referencia.
    delivery_type = fields.Selection(
        selection_add=[
            # ('usend', 'Usend'),  # TODO: descomentar y completar
        ],
        ondelete={'usend': 'set default'},
    )

    # ------------------------------------------------------------------
    # Helper interno
    # ------------------------------------------------------------------

    def _usend_get_client(self):
        """
        Construye un UsendClient leyendo credenciales desde
        ir.config_parameter.

        TODO: tu lógica aquí:
          1. ICP = self.env['ir.config_parameter'].sudo()
          2. user = ICP.get_param('delivery_usend.ws_user')
          3. password = ICP.get_param('delivery_usend.ws_pass')
          4. return UsendClient(user=user, password=password)

        TODO: decidir qué pasa si los parámetros no están seteados
        (¿UserError? ¿log + return None?).
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Métodos que el framework delivery.carrier espera encontrar
    # ------------------------------------------------------------------

    def usend_rate_shipment(self, order):
        """
        Cotización. Odoo llama a este método (o uno con este patrón de
        nombre, confirmar convención exacta en delivery_dhl como
        referencia) cuando el delivery_type es 'usend'.

        Debe devolver un dict con al menos:
          {'success': True/False, 'price': float, 'error_message': str or False,
           'warning_message': str or False}

        TODO: tu lógica aquí:
          1. client = self._usend_get_client()
          2. mapear los datos de `order` (origen, destino, peso, dimensiones)
             a los argumentos de client.cotizar_envio(...)
          3. llamar y armar el dict de retorno esperado por Odoo
          4. capturar UsendApiError y traducirlo a success=False
        """
        raise NotImplementedError

    def usend_send_shipping(self, pickings):
        """
        Genera la etiqueta/OT para cada picking. Debe devolver una lista
        de dicts, uno por picking, con al menos:
          {'exact_price': float, 'tracking_number': str}

        TODO: tu lógica aquí:
          1. client = self._usend_get_client()
          2. por cada picking, mapear los datos (partner, productos,
             dirección, ubi_direc = código INE de comuna) a los grupos
             que espera client.crear_etiqueta(...)
          3. llamar y guardar el resultado (número de guía, cod_barra, etc.)
        """
        raise NotImplementedError

    def usend_get_tracking_link(self, picking):
        """
        TODO: tu lógica aquí — fase posterior (depende de
        consultar_tracking, no prioritario ahora).
        """
        raise NotImplementedError

    def usend_cancel_shipment(self, pickings):
        """
        TODO: tu lógica aquí. Confirmar con la documentación de Usend si
        existe un endpoint de anulación explícita, o si basta con que
        las OTs de prueba se anulen solas a las 24h (como ya sabemos que
        pasa en el ambiente de pruebas).
        """
        raise NotImplementedError
