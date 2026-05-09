# HTTPS con Let's Encrypt y Nginx

Guia para dejar un subdominio atendiendo por HTTPS con certificado de Let's Encrypt usando Nginx y Certbot.

Dominio usado en los ejemplos:

```text
hc.dromarprieto.com
```

Si el dominio final es otro, reemplazarlo en todos los comandos y archivos.

## 1. Validaciones previas

El registro DNS debe apuntar al servidor correcto y no debe estar proxied por Cloudflare.

```bash
dig +short hc.dromarprieto.com
```

Debe devolver la IP publica del servidor.

Los puertos `80` y `443` deben estar abiertos:

```bash
ufw status
```

Si UFW esta activo:

```bash
ufw allow 'Nginx Full'
ufw status
```

Verificar que Nginx este instalado y activo:

```bash
nginx -v
systemctl status nginx
```

Si no esta instalado:

```bash
apt update
apt install -y nginx
systemctl enable --now nginx
```

## 2. Crear configuracion Nginx inicial por HTTP

Crear el archivo:

```bash
nano /etc/nginx/sites-available/hc.dromarprieto.com
```

Contenido:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name hc.dromarprieto.com;

    client_max_body_size 25m;

    location /static/ {
        alias /root/omar-codex/hhcc/staticfiles/;
        access_log off;
        expires 30d;
    }

    location /media/ {
        alias /root/omar-codex/hhcc/media/;
        access_log off;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_redirect off;
    }
}
```

Notas:

- Ajustar `/root/omar-codex/hhcc/staticfiles/` y `/root/omar-codex/hhcc/media/` si el proyecto vive en otra ruta.
- Si Django/Gunicorn escucha en otro puerto o socket, cambiar `proxy_pass`.
- Si no hay `staticfiles` o `media`, se pueden dejar igual; Nginx solo servira esas rutas si existen.

Activar el sitio:

```bash
ln -sf /etc/nginx/sites-available/hc.dromarprieto.com /etc/nginx/sites-enabled/hc.dromarprieto.com
nginx -t
systemctl reload nginx
```

Probar HTTP:

```bash
curl -I http://hc.dromarprieto.com
```

## 3. Instalar Certbot

Metodo recomendado por Certbot para Ubuntu: snap.

Si habia una version vieja instalada por `apt`, removerla antes:

```bash
apt remove -y certbot python3-certbot-nginx || true
```

```bash
apt update
apt install -y snapd
snap install core
snap refresh core
snap install --classic certbot
ln -sf /snap/bin/certbot /usr/bin/certbot
```

## 4. Emitir el certificado y configurar HTTPS

Ejecutar:

```bash
certbot --nginx -d hc.dromarprieto.com
```

Cuando pregunte:

- Email: usar un email administrable.
- Terms of Service: aceptar.
- Compartir email con EFF: opcional.
- Redireccion HTTP a HTTPS: elegir redireccionar si ofrece la opcion.

Certbot va a editar la configuracion de Nginx y agregar los certificados en:

```text
/etc/letsencrypt/live/hc.dromarprieto.com/fullchain.pem
/etc/letsencrypt/live/hc.dromarprieto.com/privkey.pem
```

Validar:

```bash
nginx -t
systemctl reload nginx
curl -I https://hc.dromarprieto.com
```

## 5. Renovacion automatica

Certbot instalado por snap deja renovacion automatica mediante systemd timer.

Verificar:

```bash
systemctl list-timers | grep certbot
```

Probar renovacion sin tocar certificados reales:

```bash
certbot renew --dry-run
```

Si el dry-run termina sin errores, la renovacion automatica esta bien.

## 6. Comandos utiles

Ver certificados emitidos:

```bash
certbot certificates
```

Ver configuracion activa de Nginx:

```bash
nginx -T | less
```

Ver logs:

```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
journalctl -u nginx -n 100 --no-pager
```

Reintentar emision si hubo error:

```bash
certbot --nginx -d hc.dromarprieto.com
```

## 7. Errores comunes

Si Certbot falla por validacion HTTP:

- Revisar que `hc.dromarprieto.com` apunte a la IP correcta.
- Revisar que el registro en Cloudflare este en `DNS only`, no `Proxied`.
- Revisar que el puerto `80` este abierto.
- Revisar que Nginx responda por HTTP antes de correr Certbot.

Si Nginx devuelve 502:

- La app no esta escuchando en `127.0.0.1:8000`, o el `proxy_pass` apunta mal.
- Verificar con:

```bash
curl -I http://127.0.0.1:8000
systemctl status gunicorn
docker ps
```

Si Django arma URLs HTTP estando en HTTPS:

- Confirmar que Nginx pase:

```nginx
proxy_set_header X-Forwarded-Proto $scheme;
```

- En Django puede hacer falta configurar:

```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

## Referencias oficiales

- Let's Encrypt Getting Started: https://letsencrypt.org/getting-started/
- Certbot para Ubuntu + Nginx: https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal
- Certbot snap en Ubuntu: https://snapcraft.io/install/certbot/ubuntu
- Nginx reverse proxy: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
- Gunicorn deploy behind Nginx: https://docs.gunicorn.org/en/stable/deploy.html
