from django.db import models

# Create your models here.

def upload_location(instance, filename):
	return "%s" %(filename)

class SlideImage(models.Model):

	description = models.CharField(max_length=100)
	image = models.ImageField(upload_to=upload_location)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		  return "%s Posted on: %s" % (self.description,self.timestamp)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=225)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name
