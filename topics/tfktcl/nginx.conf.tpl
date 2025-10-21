server {
  server_name tfktcl.de;
  location /tfktcl/newsletters/ { root /var/www; }
}
server {
  server_name api.tfktcl.de;
  location / { proxy_pass http://127.0.0.1:8000; }
}
