# -*- coding:utf-8 -*- 
from django.db import models

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

class teacher(models.Model):
	t_id = models.PositiveIntegerField(default=0)
	name= models.CharField(max_length=20)
	birth = models.DateField()
	faculty = models.CharField(max_length=99)
	def __unicode__(self):
		return self.name

class event(models.Model):
	t_id = models.ForeignKey(teacher)
	Datadate = models.CharField(max_length = 10)
	Datatime = models.CharField(max_length = 5)
	Datatitle = models.CharField(max_length = 60)
	def __unicode__(self):
		return self.name

class appoint(models.Model):
	t_id = models.ForeignKey(teacher)
	appointID = models.IntegerField(primary_key=True, default = '1')
	Appointdate = models.CharField(max_length = 10)
	Appointtime = models.CharField(max_length = 5)
	Number = models.CharField(max_length = 10)
	State = models.CharField(max_length = 8, default = "N/D")
	Urgent = models.CharField(max_length = 40, default = u"无附加信息")