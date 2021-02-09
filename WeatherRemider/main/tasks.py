import os
from django.core.mail import send_mail
import requests

from .models import Subscribe
from WeatherRemider.celery import app

WEATHER_URL = 'https://api.weatherbit.io/v2.0/current?key='


@app.task(name='tasker')
def tasker(sub_id):
    el = Subscribe.objects.get(id=sub_id)
    if el.notification_period > 0 and el.follower and el.following:
        sub = requests.get(f'{WEATHER_URL}{os.environ.get("WEATHER_API_KEY")}&city={el.following}')
        send_mail('Weather forecast', f'Here is your periodic WeatherRemider:\n\n {sub.text}\n',
                  'callfutur@gmail.com', [str(el.follower.email)], fail_silently=False)
    return 'message sent'


