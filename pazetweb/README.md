# ELIMINAR ARCHIVOS *.PYC
    - find . -name "*.pyc" -exec rm -f {} \;

# CONFIGURAR CACHE PARA DJANGO
    - sudo apt-get install redis-server 
    - p

# INSPECCIONAR BASE DE DATOS
    - python manage.py inspectdb > models.py 