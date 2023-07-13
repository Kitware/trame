# NGINX

Often a trame application might be put behind an NGINX either for standard routing or for providing SSL.
Either way, the default behavior of NGINX with WebSocket will make it so you get periodically disconnected.
You may want to adjust some of those parameters to allow un-interuption.

This guide aims to provide the proper settings to adjust in the websocket section.

```
# Default WS section
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
proxy_http_version 1.1;

# Trame add-on
proxy_socket_keepalive on;
proxy_connect_timeout 120;
proxy_send_timeout 360;
proxy_read_timeout 360;
```
