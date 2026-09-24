# Notas del esqueleto — delivery_usend

Este módulo es un ESQUELETO. Ningún método tiene lógica resuelta a propósito:
todos levantan `NotImplementedError` o tienen un `# TODO: tu lógica aquí`.
La idea es que tu entiendas cada línea que se vaya generando, no que copie/pegue algo ya armado.

## Orden sugerido para completarlo

1. `usend_client.py` → `_build_payload` y `_headers` (lo más mecánico,
   buen punto de entrada).
2. `usend_client.py` → `_check_business_error` (acá está la parte
   más delicada: dos formatos de error distintos).
3. `usend_client.py` → `_post` (junta los tres anteriores).
4. `usend_client.py` → `cotizar_envio` (el servicio más simple de los
   cuatro — buen primer método completo end-to-end).
5. Probar `cotizar_envio` con un script suelto (fuera de Odoo, con
   `python3` directo) antes de tocar `delivery_carrier.py` — así se
   valida la clase sin la complejidad de levantar Odoo encima.
6. `delivery_carrier.py` → `_usend_get_client` y `usend_rate_shipment`,
   una vez que `cotizar_envio` ya esté probado.
7. Etiquetas (`crear_etiqueta` + `usend_send_shipping`) es más grande
   porque el payload tiene más grupos de campos — dejarlo para el final.

Tracking y Logística Inversa quedan deliberadamente sin desarrollar en
este esqueleto: son fase posterior según lo acordado.

## Security

`security/ir.model.access.csv` está vacío a propósito: como
`delivery.carrier` ya existe y ya tiene sus permisos, este módulo no
necesita reglas de acceso propias mientras no se agregue un modelo nuevo
(por ejemplo, un log de llamadas a Usend). Si en algún momento agregan
un modelo nuevo, ahí sí hay que llenar este CSV.

## No lo antes de empezar

Cargar las credenciales `WS_TEST` en Ajustes > Técnico > Parámetros del
Sistema con las claves:
- `delivery_usend.ws_user`
- `delivery_usend.ws_pass`

(o los nombres de clave que prefieran — están hardcodeados como sugerencia
en el comentario de `_usend_get_client`, hay que decidirlos y ser
consistentes).
