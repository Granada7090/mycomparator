.PHONY: deploy backup migrate collectstatic restart status

deploy:
	@echo "Iniciando deployment..."
	git pull origin main
	pip install -r requirements/production.txt
	python manage.py migrate --settings=config.settings.production
	python manage.py collectstatic --noinput --settings=config.settings.production
	sudo systemctl restart mycomparator.service
	@echo "Deployment completado"

backup:
	@echo "Creando backup de base de datos..."
	bash scripts/backup_database.sh

migrate:
	python manage.py migrate --settings=config.settings.production

collectstatic:
	python manage.py collectstatic --noinput --settings=config.settings.production

restart:
	sudo systemctl restart mycomparator.service

status:
	sudo systemctl status mycomparator.service

logs:
	tail -f logs/gunicorn_error.log

maintenance-on:
	@echo "Activando modo mantenimiento..."
	echo "MAINTENANCE_MODE=True" >> .env
	sudo systemctl restart mycomparator.service

maintenance-off:
	@echo "Desactivando modo mantenimiento..."
	sed -i '/MAINTENANCE_MODE=True/d' .env
	sudo systemctl restart mycomparator.service
