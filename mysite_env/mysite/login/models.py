from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class registry(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)

class ticket(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    src=models.CharField(max_length=100)
    det=models.CharField(max_length=100)
    date=models.DateField(max_length=100)
    soft=models.IntegerField()
    softprice = models.CharField(max_length=100)
    hard = models.IntegerField()
    hardprice = models.CharField(max_length=100)
    hardseat = models.IntegerField()
    hardseatprice = models.CharField(max_length=100)

class bought_ticket(models.Model):
    id = models.AutoField(primary_key=True)
    tid = models.IntegerField()
    tname=models.CharField(max_length=100)
    tsrc=models.CharField(max_length=100)
    tdet=models.CharField(max_length=100)
    tdate=models.DateField(max_length=100)
    type = models.CharField(max_length=100)
    num = models.IntegerField()
    name = models.CharField(max_length=100)
    realname = models.CharField(max_length=100)
    idnum = models.CharField(max_length=100)
    buytime=models.DateTimeField(default=datetime.now)

class admincode(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    realname = models.CharField(max_length=100)
    idnum = models.CharField(max_length=100)
    check=models.CharField(max_length=100)


class modify(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tid = models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    modifytime=models.DateTimeField(default=datetime.now)