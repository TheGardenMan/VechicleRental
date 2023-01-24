# setup
    1. create virtual env and activate it
    2. Navigate to folder where `manage.py` is locatef and run the following commands.
        `pip install -r requirements.txt`
        `python manage.py makemigrations`
        `python manage.py migrate`
    
# create admin user
    python manage.py createsuperuser

Then you can login using the above created credentials via `admin_login` API.


