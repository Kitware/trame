<VirtualHost *:80>
  DocumentRoot /deploy/server/www
  ErrorLog /deploy/server/logs/apache/error.log
  CustomLog /deploy/server/logs/apache/access.log combined

  Alias TRAME_URL_PREFIX /deploy/server/www/

  <Directory /deploy/server/www>
      Options Indexes FollowSymLinks
      AllowOverride None
      Require all granted
      FallbackResource /index.html
  </Directory>

  # Set CORS headers
  Header set Access-Control-Allow-Origin "*"

  # Handle launcher forwarding
  ProxyPass TRAME_URL_PREFIX/launcher http://localhost:9000/paraview
  ProxyPassReverse TRAME_URL_PREFIX/launcher http://localhost:9000/paraview

  # Handle paraview forwarding
  ProxyPass TRAME_URL_PREFIX/paraview http://localhost:9000/paraview
  ProxyPassReverse TRAME_URL_PREFIX/paraview http://localhost:9000/paraview

  # Handle WebSocket forwarding
  RewriteEngine On
  RewriteMap session-to-port txt:/opt/trame/proxy-mapping.txt
  RewriteCond %{QUERY_STRING} ^sessionId=(.*)&path=(.*)$ [NC]
  RewriteRule ^TRAME_URL_PREFIX/proxy.*$  ws://${session-to-port:%1}/%2  [P]

  # Handle API forwarding
  RewriteRule ^TRAME_URL_PREFIX/api/(.*)/(.*)$  http://${session-to-port:$1}/$2  [P,L]

</VirtualHost>
