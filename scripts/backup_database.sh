#!/bin/bash
# Script de backup para base de datos MySQL

echo "=== Iniciando backup de base de datos ==="

# Variables
DB_NAME="mycomparator_db"
DB_USER="mycomparator_user"
DB_PASS="tu-password-de-mysql"
BACKUP_DIR="/home/u123456789/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

echo "1. Creando backup de la base de datos..."
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/${DB_NAME}_backup_$DATE.sql.gz

echo "2. Verificando backup..."
if [ -s $BACKUP_DIR/${DB_NAME}_backup_$DATE.sql.gz ]; then
    echo "✅ Backup creado exitosamente: ${DB_NAME}_backup_$DATE.sql.gz"
else
    echo "❌ Error al crear backup"
    exit 1
fi

echo "3. Limpiando backups antiguos (más de $RETENTION_DAYS días)..."
find $BACKUP_DIR -name "${DB_NAME}_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "4. Mostrando backups actuales..."
ls -la $BACKUP_DIR/${DB_NAME}_backup_*.sql.gz

echo "=== Backup completado ==="
