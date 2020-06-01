import os
#import magic
from django.core.exceptions import ValidationError
from django import forms
# def validate_file_extension(upload):
#     valid_mime_types=['application/pdf']
#     file_mime_type= magic.from_buffer(upload.read(1024), mime=True)
#     if file_mime_type not in valid_mime_types:
#         raise ValidationError('Unsupported file extesion')
#         valid_extensions=['.pdf']
#         ext=os.path.splitext(upload.name)[1]
#         if ext.lower() not in valid_extensions:
#         raise ValidationError('Unacceptable file extension')

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions=['.pdf',]
    if ext.lower() not in valid_extensions:
       raise ValidationError('Unacceptable file extension-only pdf allowed')
       return value  

def validate_file_size(value):
    filesize=value.size
    # file size 1 MB=1000*1024=1024000
    if filesize > 1024000:
        raise ValidationError('Max. file size is 1 MB')
    else:
        return value


def validate_topic(value):
    #value=request.POST['text']
    count=len(value.split())
    # value_list= ['_']
    if count < 3 :
        raise ValidationError("Please provide at least a 3 word message,\
        %(count)s words is not descriptive enough")
    
def validate_char(value):
    num=list(range(0,9))
    value_list= ['_', '*',' ','!','@','#','$','%','^','(',')','=','-','/','.','&',num]
    if value in value_list:
        raise forms.ValidationError("Invalid Data!")
        return value
    # if not value.isalpha():
    #     raise ValueError("only characters please")
    #     return value