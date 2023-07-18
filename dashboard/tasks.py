# tasks.py
from celery import shared_task
import time
from admin_config.celery import app

@app.task
def assign_lead(instance_id):
    print("STARTING")
    from .models import CustomUser, Lead
    instance = Lead.objects.get(pk=instance_id)
    users = CustomUser.objects.filter(is_superuser=False).order_by('-id')
    for user in users:
        instance.handlers.add(user)
        instance.save()
        print("DONE first",user.email)
        time.sleep(5)
    return "Done"

@app.task
def add(self,a,b):
    return a+b


@app.task
def count():
    for i in range(10):
        print(i)
    return "DONE"