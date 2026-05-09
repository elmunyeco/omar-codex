# Backup diario de la base cardioprieto

Instalacion en el servidor:

```bash
cd /ruta/al/repo
sudo ops/install_cardioprieto_backup_cron.sh
```

Esto instala:

- Script: `/usr/local/sbin/backup_cardioprieto_db.sh`
- Cron diario: `/etc/cron.d/cardioprieto-db-backup`
- Horario: `03:00` de Argentina (`06:00 UTC` en servidores con timezone UTC)
- Backups: `/var/backups/cardioprieto-db`
- Log: `/var/log/cardioprieto-db-backup.log`
- Credenciales MySQL: `/root/.my.cnf.cardioprieto-backup`

Configuracion usada:

- Base: `cardioprieto`
- Usuario: `root`
- Host: `127.0.0.1`
- Puerto: `3307`
- Retencion: ultimos `3` backups

Prueba manual:

```bash
sudo /usr/local/sbin/backup_cardioprieto_db.sh
sudo ls -lh /var/backups/cardioprieto-db
sudo tail -n 50 /var/log/cardioprieto-db-backup.log
```

Si MySQL/MariaDB esta escuchando en otro puerto, editar:

```bash
sudo nano /etc/cron.d/cardioprieto-db-backup
sudo nano /root/.my.cnf.cardioprieto-backup
```
