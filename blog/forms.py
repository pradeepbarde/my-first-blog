from django import forms
from .models import Topic, Entry, Fileupload
from .validators import validate_topic, validate_char
# from django.core.validators import
from django.core.exceptions import ValidationError
from .forms import ValidationError


class TopicForm(forms.ModelForm):
    #text=forms.ModelChoiceField(label="Choice list",queryset=Topic.objects.all())  #<-----
    text=forms.CharField(label='Title', error_messages={"required":"Topic should be descriptive enough & unique, at least 3 words long!"}, validators=[validate_topic, validate_char],) #<---------
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

         

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
        
class FileuploadForm(forms.ModelForm):
    class Meta:
        model = Fileupload
        fields = ['upload']
        upload = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'}))
    # upload = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
