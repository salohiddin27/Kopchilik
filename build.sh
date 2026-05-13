pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.filter(username='salohiddin').exists() or User.objects.create_superuser('salohiddin', 'admin@gmail.com', '1')" | python manage.py shell
