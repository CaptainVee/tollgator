![Tollgator](https://socialify.git.ci/captainvee/Tollgator/image?description=1&descriptionEditable=Turn%20your%20youtube%20playlist%20into%20an%20online%20course&font=Source%20Code%20Pro&language=1&pattern=Brick%20Wall&theme=Dark)

# Tollgator

Tollgator is a web-applications that allow users to turn their youtube videos to become an online courses. Students can then take them serially and receive a certification on completion.

## Want to use this project?

1. Fork/Clone

   ```sh
   $ git clone https://github.com/CaptainVee/Tollgator.git
   ```

1. Cd into Tollgator
   ```sh
   $ cd Tollgator
   ```
1. Create and activate a virtual environment:

   ```sh
   $ python3 -m venv venv && source venv/bin/activate
   ```

1. Install the dependencies:

   ```sh
   (venv)$ pip install -r requirements.txt
   ```

1. Apply the migrations and run the Django development server:

   ```sh
   (venv)$ python manage.py makemigrations
   (venv)$ python manage.py migrate
   (venv)$ python manage.py runserver
   ```

1. Test at [http://localhost:8000/](http://localhost:8000/)

1. start the redis server in another terminal:

   ```sh
   $ redis-server
   ```

1. start the celery server in another terminal too:

   ```sh
   $ celery -A tollgator beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

   $ celery -A tollgator worker -l INFO
   ```

1. For runing test with pytest and coverage:

   ```sh
   $ coverage run -m pytest

   $ coverage report
   ```
