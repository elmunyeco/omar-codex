#!/usr/bin/env bash
set -Eeuo pipefail

umask 077

DB_NAME="${DB_NAME:-cardioprieto}"
DB_USER="${DB_USER:-root}"
DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-3307}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/cardioprieto-db}"
RETENTION_COUNT="${RETENTION_COUNT:-3}"
MYSQL_DEFAULTS_FILE="${MYSQL_DEFAULTS_FILE:-/root/.my.cnf.cardioprieto-backup}"
LOG_FILE="${LOG_FILE:-/var/log/cardioprieto-db-backup.log}"
LOCK_FILE="${LOCK_FILE:-/var/lock/cardioprieto-db-backup.lock}"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    log "ERROR: falta el comando requerido: $1"
    exit 1
  fi
}

mysql_auth_env=()
mysql_common_args=(
  "--host=${DB_HOST}"
  "--port=${DB_PORT}"
  "--user=${DB_USER}"
)

mysql_client_cmd=(mysql)
mysqldump_cmd=(mysqldump)

if [[ -r "${MYSQL_DEFAULTS_FILE}" ]]; then
  mysql_client_cmd+=("--defaults-extra-file=${MYSQL_DEFAULTS_FILE}")
  mysqldump_cmd+=("--defaults-extra-file=${MYSQL_DEFAULTS_FILE}")
elif [[ -n "${DB_PASSWORD:-}" ]]; then
  mysql_auth_env=("MYSQL_PWD=${DB_PASSWORD}")
else
  log "ERROR: no hay credenciales. Crear ${MYSQL_DEFAULTS_FILE} o ejecutar con DB_PASSWORD."
  exit 1
fi

main() {
  mkdir -p "$(dirname "${LOG_FILE}")" "${BACKUP_DIR}" "$(dirname "${LOCK_FILE}")"
  touch "${LOG_FILE}"
  chmod 600 "${LOG_FILE}"

  exec >>"${LOG_FILE}" 2>&1

  require_command mysql
  require_command mysqldump
  require_command gzip
  require_command flock
  require_command find

  exec 9>"${LOCK_FILE}"
  if ! flock -n 9; then
    log "Backup ya en ejecucion; saliendo."
    exit 0
  fi

  local timestamp output tmpfile
  timestamp="$(date '+%Y%m%d_%H%M%S')"
  output="${BACKUP_DIR}/${DB_NAME}_${timestamp}.sql.gz"
  tmpfile="${output}.tmp"

  log "Iniciando backup de ${DB_NAME} en ${DB_HOST}:${DB_PORT}"

  env "${mysql_auth_env[@]}" "${mysql_client_cmd[@]}" "${mysql_common_args[@]}" \
    --batch --skip-column-names --execute="SELECT 1" "${DB_NAME}" >/dev/null

  env "${mysql_auth_env[@]}" "${mysqldump_cmd[@]}" "${mysql_common_args[@]}" \
    --single-transaction \
    --quick \
    --routines \
    --triggers \
    --events \
    --hex-blob \
    --databases "${DB_NAME}" \
    | gzip -9 >"${tmpfile}"

  gzip -t "${tmpfile}"
  mv "${tmpfile}" "${output}"
  chmod 600 "${output}"

  mapfile -t backups_to_delete < <(
    find "${BACKUP_DIR}" -maxdepth 1 -type f -name "${DB_NAME}_*.sql.gz" -printf '%T@ %p\n' \
      | sort -rn \
      | awk -v keep="${RETENTION_COUNT}" 'NR > keep { sub(/^[^ ]+ /, ""); print }'
  )

  if (( ${#backups_to_delete[@]} > 0 )); then
    rm -f -- "${backups_to_delete[@]}"
    log "Rotacion OK: se mantienen los ultimos ${RETENTION_COUNT} backups."
  fi

  log "Backup OK: ${output}"
}

trap 'rm -f "${tmpfile:-}"' EXIT
main "$@"
