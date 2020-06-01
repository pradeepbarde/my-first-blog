from django.contrib import admin
from blog.models import Topic, Entry, Fileupload

# Register your models here.

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Fileupload)
