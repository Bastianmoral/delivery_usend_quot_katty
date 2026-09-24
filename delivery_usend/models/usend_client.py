"""
Cliente HTTP puro para la API de Usend Chile.

Esta clase NO hereda de models.Model: no sabe nada de Odoo. Su única
responsabilidad es hablar con Usend (autenticación, armado del payload
atípico, y detección de errores de negocio dentro de respuestas HTTP 200).

Quien la use (por ejemplo delivery_carrier.py) es responsable de traducir
entre el mundo Odoo y los diccionarios que esta clase espera/devuelve.
"""

import requests


class UsendClient:

    # TODO: confirmar si conviene mover estas constantes a variables de
    # clase, a ir.config_parameter, o dejarlas como default de __init__.
    DEFAULT_BASE_URL = 'https://app.usend.cl/ws/ue'

    def __init__(self, user, password, base_url=None):
        """
        Args:
            user: credencial 'user' del header HTTP (WS_TEST en pruebas)
            password: credencial 'pass' del header HTTP
            base_url: por si alguna vez hay que apuntar a otro ambiente

        TODO: decidir el timeout por defecto acá (requests no tiene
        uno propio; sin timeout, un request colgado bloquea el worker de
        Odoo indefinidamente).
        """
        self.user = user
        self.password = password
        self.base_url = base_url or self.DEFAULT_BASE_URL
        # TODO: armar self._session = requests.Session() muy problablemente hagamos
        # conexiones entre varias llamadas seguidas.

    # ------------------------------------------------------------------
    # Métodos privados / genéricos (transporte)
    # ------------------------------------------------------------------

    def _build_payload(self, data: dict) -> dict:
        """
        Envuelve `data` en el formato atípico que espera Usend:
        application/x-www-form-urlencoded con un único campo 'json'
        que contiene el diccionario serializado como string JSON.

        TODO: tu lógica aquí (json.dumps + armar el dict de retorno
        {'json': ...})
        """
        raise NotImplementedError

    def _headers(self) -> dict:
        """
        TODO: tu lógica aquí — arma el dict de headers HTTP con
        'user' y 'pass'. Confirmar con las pruebas si Usend espera
        algún Content-Type explícito además del que pone requests
        automáticamente para x-www-form-urlencoded.
        """
        raise NotImplementedError

    def _check_business_error(self, response_json):
        """
        Usend puede devolver HTTP 200 con un error de negocio adentro,
        y el formato NO es consistente entre servicios:
          - a veces un objeto:  {"error": -1, "mensaje": "..."}
          - a veces un array:   [{"sql_error": "-1", "msg_error": "..."}]

        Esta función debe:
          1. Detectar cuál de los dos formatos vino.
          2. Levantar una excepción propia (ver TODO abajo) si hay error.
          3. No hacer nada (o retornar) si la respuesta es válida.

        TODO: tu lógica aquí. Sugerencia: definir una excepción
        `UsendApiError(Exception)` en este mismo archivo o en un
        `exceptions.py` aparte, para que delivery_carrier.py la pueda
        capturar específicamente en vez de un except genérico.
        """
        raise NotImplementedError

    def _post(self, endpoint: str, data: dict) -> dict:
        """
        Método genérico de POST, usado por cotizar_envio, crear_etiqueta
        y (más adelante) logistica_inversa.

        TODO: tu lógica aquí:
          1. payload = self._build_payload(data)
          2. response = requests.post(url, data=payload, headers=...)
          3. response.raise_for_status()  # solo cubre errores HTTP, no de negocio
          4. self._check_business_error(response.json())
          5. return response.json()
        """
        raise NotImplementedError

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """
        Método genérico de GET, usado por consultar_tracking.

        TODO: tu lógica aquí (fase Tracking, no prioritaria ahora).
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Métodos públicos por servicio
    # ------------------------------------------------------------------

    def cotizar_envio(self, origen, destino, peso, alto, largo, ancho,
                       tipo_empaque='PQ', seguro=None):
        """
        POST /cotizarenvio

        Payload esperado (confirmado): linea, id_orden, origen, destino,
        peso, alto, largo, ancho, tipo_empaque (default 'PQ'), seguro (opcional).

        TODO: tu lógica aquí:
          1. armar el dict `data` con los campos de arriba
          2. return self._post('cotizarenvio', data)
        """
        raise NotImplementedError

    def crear_etiqueta(self, **kwargs):
        """
        POST /ge/

        Payload esperado (grupos confirmados vía formulario de prueba):
        identificación, envío, receptor, dirección, producto, cedibles,
        despacho. Ver overview del proyecto para el detalle de cada grupo.

        TODO: tu lógica aquí. Sugerencia: no recibas 20 kwargs sueltos acá
        — pensar si conviene un dict estructurado por grupo, o construirlo
        del lado de delivery_carrier.py y pasar un solo `data` ya armado.
        """
        raise NotImplementedError

    def consultar_tracking(self, cod_rastreo):
        """
        GET /tracking/

        TODO: tu lógica aquí — fase posterior, no prioritaria ahora.
        """
        raise NotImplementedError

    def logistica_inversa(self, **kwargs):
        """
        POST /gli  (nota: sin TLS — http, no https)

        TODO: tu lógica aquí — fase posterior, payload sin confirmar
        aún con Usend. No es prioridad.
        """
        raise NotImplementedError
