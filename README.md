Hi guys, here is how to host this on your computer, you should run the following on your computer
clone the repository:
git clone https://github.com/your-username/treadsite.git

set up virtual enviornment:
python -m venv venv
mac/os: source venv/bin/activate
windows: venv\Scripts\activate

Migrate data:
python manage.py migrate

create a superuser(you):
python manage.py createsuperuser
run the server:
python manage.py runserver
