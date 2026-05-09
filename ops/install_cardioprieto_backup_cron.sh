#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/backup_cardioprieto_db.sh"
SCRIPT_DST="/usr/local/sbin/backup_cardioprieto_db.sh"
MYSQL_DEFAULTS_FILE="/root/.my.cnf.cardioprieto-backup"
CRON_FILE="/etc/cron.d/cardioprieto-db-backup"

if [[ "${EUID}" -ne 0 ]]; then
  echo "ERROR: ejecutar como root." >&2
  exit 1
fi

install -m 700 "${SCRIPT_SRC}" "${SCRIPT_DST}"

cat >"${MYSQL_DEFAULTS_FILE}" <<'EOF'
[client]
user=root
password=Corbis5
host=127.0.0.1
port=3307
EOF
chmod 600 "${MYSQL_DEFAULTS_FILE}"

cat >"${CRON_FILE}" <<EOF
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Los servidores estan en UTC. 06:00 UTC equivale a 03:00 America/Argentina/Buenos_Aires.
0 6 * * * root DB_NAME=cardioprieto DB_HOST=127.0.0.1 DB_PORT=3307 RETENTION_COUNT=3 MYSQL_DEFAULTS_FILE=${MYSQL_DEFAULTS_FILE} ${SCRIPT_DST}
EOF

chmod 644 "${CRON_FILE}"

echo "Backup instalado."
echo "Cron: ${CRON_FILE}"
echo "Script: ${SCRIPT_DST}"
echo "Credenciales MySQL: ${MYSQL_DEFAULTS_FILE}"
echo "Backups: /var/backups/cardioprieto-db"
echo "Log: /var/log/cardioprieto-db-backup.log"
