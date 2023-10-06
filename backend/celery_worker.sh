echo "starting celery worker" 
celery -A main.celery worker -l info -n worker1