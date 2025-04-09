.PHONY: build dev clean

# Comando para desarrollo
dev:
	python manage.py runserver

# Comando para build (producción)
build:
	pip install -r requirements.txt
	python manage.py collectstatic --noinput
	python manage.py migrate

# Limpiar archivos generados
clean:
	rm -rf staticfiles/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete