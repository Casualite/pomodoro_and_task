echo "starting celery beat scheduler" 
celery -A main.celery beat --max-interval 1 -l info 