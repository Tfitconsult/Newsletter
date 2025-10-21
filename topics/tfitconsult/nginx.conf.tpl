server {
  server_name tfitconsult.de;
  location /consulting/newsletters/ { root /var/www; }
}
server {
  server_name api.tfitconsult.de;
  location / { proxy_pass http://127.0.0.1:8000; }
}
