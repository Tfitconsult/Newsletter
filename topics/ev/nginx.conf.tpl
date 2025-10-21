server {
  server_name cancanary.de;
  location /ev/newsletters/ { root /var/www; }
}
server {
  server_name api.cancanary.de;
  location / { proxy_pass http://127.0.0.1:8000; }
}
