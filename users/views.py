from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
#from django.contrib.auth.forms import UserCreationForm
#from .models import Topic, Entry
#from .forms import TopicForm, EntryForm
# Create your views here.

def loginreq(request):

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request = request,
                  template_name = "users/login.html",
                  context={"form":form})
    
    
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request, 'users/logged_out.html')
    #return HttpResponseRedirect("/")


def register(request):
    """Register a new user."""
    if request.method == "POST":
        # Process completed form.
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username=form.cleaned_data.get('username')
                            
        #     # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
            password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect('/')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
    form=UserCreationForm
    context = {'form': form}
    return render(request, 'users/register.html', context)