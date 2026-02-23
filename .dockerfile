FROM python:3.14.2
WORKDIR /Django-Webhook_Catcher
RUN ["python", "manage.py", "runserver"]
