#!/bin/bash
# Script de deployment para Hostinger

echo "=== Iniciando deployment en Hostinger ==="

# Variables
PROJECT_DIR="/home/u123456789/domains/mycomparator.net/public_html"
BACKUP_DIR="/home/u123456789/backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "1. Creando backup de la base de datos actual..."
mysqldump -u mycomparator_user -p mycomparator_db > $BACKUP_DIR/mycomparator_db_backup_$DATE.sql

echo "2. Deteniendo aplicación..."
pkill -f gunicorn

echo "3. Actualizando código..."
cd $PROJECT_DIR
git pull origin main

echo "4. Activando entorno virtual..."
source venv/bin/activate

echo "5. Instalando dependencias..."
pip install -r requirements/production.txt

echo "6. Aplicando migraciones..."
python manage.py migrate --settings=config.settings.production

echo "7. Colectando archivos estáticos..."
python manage.py collectstatic --noinput --settings=config.settings.production

echo "8. Iniciando aplicación..."
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3 --daemon

echo "9. Limpiando cache..."
python manage.py clear_cache --settings=config.settings.production

echo "=== Deployment completado ==="
echo "Aplicación disponible en: https://mycomparator.net"
