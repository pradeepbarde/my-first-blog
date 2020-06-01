from django.db import models
from django.contrib.auth.models import User
#from .models import Fileupload
from .validators import validate_file_size, validate_file_extension
# Create your models here.

class Topic(models.Model):
    """A topic the user is learning about"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        """Return a string representation of the model."""
        return self.text


class Entry(models.Model):
    """Something specific learned about a topic"""
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    # fileupload = models.ForeignKey(Fileupload, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
    def __str__(self):
        """Return a string representation of the model."""
        return self.text
    
    
    # model for file uploading
class Fileupload(models.Model):
    entry = models.ForeignKey(Entry, null=True, on_delete=models.PROTECT)
# file will be uploaded to MEDIA_ROOT/uploads
    upload = models.FileField(upload_to='uploads/', validators=[validate_file_size , validate_file_extension])
   
    def upload_link(self):
        if self.upload:
            return "<a href='%s'>download</a>" % (self.upload.url)
        else:
            return "No Attachment"
        upload_link.allow_tags = True
    
    