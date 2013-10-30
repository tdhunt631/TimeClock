from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse


class UserStatus(models.Model):
	user = models.OneToOneField(User)
	_status = models.BooleanField(default=False, db_column='status')
	
	@property
	def status(self):
		return self._status 

	@status.setter
	def status(self, value):
		self._status = value
		self.save()	

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserStatus.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)

class Project(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('clock:index')	


class Record(models.Model):
	user = models.ForeignKey(User, editable=True)
	project = models.ForeignKey(Project, null=True, blank=True, default=None)
	startTime = models.DateTimeField()
	endTime = models.DateTimeField(null=True, blank=True)
	note = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.note

	def get_absolute_url(self):
		return reverse('clock:index')	


