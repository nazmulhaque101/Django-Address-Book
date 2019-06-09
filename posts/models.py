from django.conf import settings
from django.db import models



def upload_location(instance, filename):
	return "blog%s_%s" %(instance.id,filename)

	
class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

	fullname = models.CharField(max_length=120, default="N/A")
	nickname = models.CharField(max_length=120, default="N/A")
	email =  models.CharField(max_length=120, default="N/A")
	phone = models.CharField(max_length=20, default="N/A")
	address = models.TextField(default="N/A")

	image = models.ImageField(
		upload_to=upload_location,
		null=True,
		blank=True)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	class Meta:
		ordering  = ["fullname"]
# 		order by reverse id,timestamp,updated