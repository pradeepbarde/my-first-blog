from __future__ import unicode_literals
from django.shortcuts import render , get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
#from django.core.urlresolver import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry, Fileupload
from .forms import TopicForm, EntryForm, FileuploadForm 
#from .forms import ModelFormWithFileField
from django.conf import settings
from django.contrib import messages
# for download
import os
from django.http import FileResponse
from django.template import RequestContext
#from django.conf.urls.static import static
from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your views here.

def index(request):
    """The home page for Learning Log"""
    return render(request, 'index.html')

#@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    
    # Restricting Topics Access to Appropriate Users
    #topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'topics.html', context)

#@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    #---------------------------------------------
    entry, created = Entry.objects.get_or_create(topic_id=(topic.id), text='Hi!-default entry, to upload file click add new entry' )
    entry_id=entry.id
    fileupload, created = Fileupload.objects.get_or_create(entry_id=(entry.id), upload='uploads/About_us.pdf')   #<--'/media/uploads/Application.pdf'
    #-----------------------------------------------
    # try:
    #     entry=Entry.objects.get(id=topic_id)
    #     entry_id=entry.id 
        
    # #     # show Fileupload objects
    # except Entry.DoesNotExist:
    #     entry = Entry(topic_id=(topic.id), text='Hi!-default entry, to upload file click add new entry' )
    #     entry.save()  
    #     entry_id=entry.id   #<-------
    # try:
    #   fileupload=Fileupload.objects.get(id=entry_id)S
    # except Fileupload.DoesNotExist:
    #     fileupload=Fileupload(entry_id=(entry.id), upload='/media/uploads/Application.pdf' )   #<------
    #     fileupload.save()      
    #---------------------------------------------
    #entry = Entry.objects.create(topic_id=(topic.id), text='Hi' )
    #----------------------------------------------      
    #fileupload=Entry.objects.get(id=topic_id) 
    # Protecting a User’s Topics
    #if topic.owner != request.user:
        #raise Http404("Invalid user")
    
    entries = topic.entry_set.order_by('-date_added')
    #ufiles=fileupload.upload_link()  
    ufiles = entry.fileupload_set.order_by('id')
    
    context = {'topic': topic, 'entries': entries,'ufiles': ufiles}
    return render(request, 'topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    topic = Topic.objects.all()
    form=TopicForm(request.POST)
    if request.method=='POST':
        #------------------
        if form.is_valid():
            text= form.cleaned_data.get("text")
            if form.cleaned_data["text"]:
                topic=topic.filter(text__icontains=form.cleaned_data["text"])
                if not(topic): #<----
                    new_topic = form.save(commit=False)
                    new_topic.owner = request.user
                    new_topic.text=text.title()  #<-------
                    new_topic.save()
                    
                else:
                    
                    raise Http404("Topic already exist: Title should be unique!")
                    
            form.save()
        else:
            raise Http404("Invalid Data: Title must begin with alphabets & should be descriptive enough!")
        return HttpResponseRedirect('/Topics')
        #------------------
        select_topic=get_object_or_404(Topic,pk=request.POST.get('topic_id'))
        topic.text=select_topic
        topic.save()
    #return render_to_response('new_topic.html', {'topic':topic}, context_instance = RequestContext(request))
    context = { 'form': form ,'topic':topic }
    return render(request, 'new_topic.html', context)
    
    # topic = Topic.objects.all()
    # if (request.method) != 'POST':
    # #     # No data submitted; create a blank form.
    #     form = TopicForm() #-------
        
    # else:
         
    #     form = TopicForm(request.POST)
    #     if form.is_valid():
    #          #----------------------------
    #         text= form.cleaned_data.get("text")
    #         if form.cleaned_data["text"]:
    #             topic=topic.filter(text__icontains=form.cleaned_data["text"])
    #          #----------------------------                   
    #         #text= form.cleaned_data.get('text')
               
    #         # Associating New Topics with the Current User
    #         #topic = Topic.objects.filter(text=request.POST['text'])
            
    #             if not(topic): #<----
    #                 new_topic = form.save(commit=False)
    #                 new_topic.owner = request.user
    #                 new_topic.save()
    #             else:
    
    #                 raise Http404("Topic already exist")
    
    #     form.save()
    #     return HttpResponseRedirect('/Topics')
                   
    # context = { 'form': form ,'topic':topic }
    # return render(request, 'new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    #<------------------------------------
    entry=Entry.objects.get(id=topic_id)  #<--------
    
    #topic=entry.topic
    #fileupload=Fileupload.objects.get(id=entry_id)
    
    #<-------------------------------------
    # prevent unauthorised entry
    if topic.owner != request.user:
        raise Http404("Invalid user,you are not authhorised user")
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
        # File upload blank form
        form_up=FileuploadForm()  #<-------
    else:
       # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        # upload form
        form_up=FileuploadForm(data=request.POST, files=request.FILES)   #<---------
        if (form.is_valid() and form_up.is_valid()): 
             
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            form.save()
            #-----------------------------------------------
        #if form_up.is_valid():
            new_file=form_up.save(commit=False)
            new_file.entry=entry
            new_file.save()
            form_up.save()
            #-----------------------------------------------
                       
            return HttpResponseRedirect('/Topics')
                                       
    context = {'topic': topic, 'form': form, 'form_up': form_up}
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    #fileupload=Fileupload.objects.all() #<---here change
    topic = entry.topic
    #Protecting the edit_entry Page
    if topic.owner != request.user:
        raise Http404("Invalid user,you are not authhorised user")

    if request.method != 'POST':
    #     # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
        # form_up=FileuploadForm(fileupload) #<---here change
    else:
        # POST data submitted; process data.
    
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            #edit_entry.save()
            return HttpResponseRedirect('/Topics')

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'edit_entry.html', context)

# Function for download

@login_required
def download_file(request, fileupload_id):
    fileupload = get_object_or_404(Fileupload, pk=fileupload_id)  #<------

    file_name, file_extension = os.path.splitext(fileupload.upload.file.name)
    file_extension = file_extension[1:] # remove the dot
    response = FileResponse(fileupload.upload.file, content_type="file/%s" % file_extension)
    response["Content-Disposition"] = "attachment;" \
        "filename=%s.%s" % (fileupload.upload.name[:50] , file_extension[:50])
    return response

