import requests
import os


def get_public_ipv4(token):
    url = "http://169.254.169.254/latest/meta-data/public-ipv4"
    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get(url, headers=headers)
    public_ipv4 = response.text
    return public_ipv4

def get_aws_token():
    url = "http://169.254.169.254/latest/api/token"
    headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
    response = requests.put(url, headers=headers)
    token = response.text
    return token

config_text = """
error_log /var/log/nginx/error.log;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {
  include mime.types;
  # fallback in case we can't determine a type
  default_type application/octet-stream;
  access_log /var/log/nginx/access.log combined;
  sendfile on;

  upstream app_server {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response

    # for UNIX domain socket setups
    server unix:/tmp/proxy.sock fail_timeout=0;

    # for a TCP configuration
    # server 192.168.0.7:8000 fail_timeout=0;
  }

  server {
    # if no Host match, close the connection to prevent host spoofing
    listen 80 default_server;
    return 444;
  }

  server {
    # use 'listen 80 deferred;' for Linux
    # use 'listen 80 accept_filter=httpready;' for FreeBSD
    listen 80;
    client_max_body_size 4G;

    # set the correct host(s) for your site
    server_name w.x.y.z;

    keepalive_timeout 5;

    # path for static files
    root /home/ubuntu/webdocs;

    location / {
      # checks for static file, if not found proxy to app
      try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Host $http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://app_server;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
      root /path/to/app/current/public;
    }
  }
}"""

# Fetch the public IP from EC2 metadata
token = get_aws_token()
public_ip = get_public_ipv4(token)

# Replace the placeholder with the actual public IP
config_text = config_text.replace('server_name w.x.y.z;', f'server_name {public_ip};')

# Write the updated configuration to the nginx configuration file
with open('/etc/nginx/nginx.conf', 'w') as file:
    file.write(config_text)
