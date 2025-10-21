#!/usr/bin/env python3
import sys
import os
import json

if len(sys.argv) < 2:
    print("Usage: scripts/new_topic.py <slug>")
    sys.exit(1)

slug = sys.argv[1].strip()
tpath = f"topics/{slug}"
os.makedirs(tpath, exist_ok=True)

env = f"""TOPIC_SLUG={slug}
BRAND_NAME={slug.title()}
BRAND_TAGLINE=
BRAND_COLOR=#0F766E
PUBLIC_BASE_URL=
API_BASE_URL=
ARCHIVE_DIR=

DB_ENGINE=mysql
DB_HOST=
DB_PORT=3306
DB_USER=
DB_PASS=
DB_NAME={slug}_db

FROM_EMAIL=
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
SMTP_TLS=starttls
"""
with open(f"{tpath}/.env", "w") as f:
    f.write(env)

with open(f"{tpath}/brand.json", "w") as f:
    json.dump({"name": slug.title(), "tagline": "", "color": "#0F766E"}, f, indent=2)

with open(f"{tpath}/nginx.conf.tpl", "w") as f:
    f.write(
        """server {
  server_name ${PUBLIC_HOST};
  location /newsletters/ { root ${PUBLIC_ROOT}; }
}
server {
  server_name ${API_HOST};
  location / { proxy_pass http://127.0.0.1:8000; }
}
"""
    )

print(f"Topic scaffolded: {slug}")
