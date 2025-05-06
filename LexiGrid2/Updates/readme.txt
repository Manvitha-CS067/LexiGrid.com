
 ✅ Google OAuth Login in Django – Step by Step (Using `django allauth`)

Step 1: Create Google OAuth Credentials  

1. Go to: [https://console.cloud.google.com](https://console.cloud.google.com)
2. Create/select a project.
3. Navigate to   APIs & Services > Credentials  .
4. Click   Create Credentials > OAuth client ID  .
5. Choose   Web application  .
6. Under   Authorized redirect URIs  , add:
   http://localhost:8000/accounts/google/login/callback/
7. Click   Create  . Copy the:
       Client ID  
       Client Secret  

  

Step 2: Set Up Django Project  

django admin startproject Oauth_demo
cd Oauth_demo
django admin startapp app1


  

Step 3: Install Required Packages  

Install `django allauth`:
pip install django allauth


  
Step 4: Update `settings.py`  
Add to `INSTALLED_APPS`:


INSTALLED_APPS = [
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/index/'(any url) after login

SOCIALACCOUNT_LOGIN_ON_GET = True 
LOGOUT_REDIRECT_URL = '/'
   (Enables auto login via Google without clicking "Sign In")


Step 5: Apply Migrations  
python manage.py migrate


  

Step 6: Create Superuser  
python manage.py createsuperuser
Enter username, email, and password.

  

Step 7: Run Server and Open Admin Panel  

python manage.py runserver


Visit: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Login with the superuser credentials.

  



  

Step 8: Add Google OAuth Credentials in Admin  

1. Go to   Social Accounts > Social Applications > Add  .
2. Fill the form:

       Provider   → Google
       Name   → Google OAuth
       Client ID   → Paste from Google
       Secret Key   → Paste from Google
3. In the   Sites   section, select the site (localhost).
4. Click   Save  .

  

Step 9: Update URLs  

In `Oauth_demo/urls.py`:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),    required for allauth
    path('', include('app1.urls')),                your app URLs
]



Step 10: Create Views in `app1/views.py`  


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'app1/login.html')
def index(request):
    return render(request, 'app1/index.html')


  

Step 11: Add URLs in `app1/urls.py`  

Create `urls.py` in your app (`app1/urls.py`):


from django.urls import path
from .views import home, index

urlpatterns = [
    path('', home, name='home'),
    path('index/',index, name='index'),
]


Step 13: Create Templates  

    Folder structure:

```
templates/
└── app1/
    ├── login.html
    └── index.html
login.html
{% load social account %}
<h2>Login with Google</h2>
<a href="{% provider_login_url 'google' %}">Login using Google</a>


index.html
<h2>Welcome {{ user.first_name }}!</h2>
<p>This is your index page.</p>
<p><a href="{% url 'account_logout' %}">Logout</a></p>(To logout )



  
  

   ✅ Final Result

  Visiting `/` will show the Google login link.
  Once logged in via Google, you'll be redirected to `/index/`.
  No username/password signup form is needed (thanks to `SOCIALACCOUNT_LOGIN_ON_GET = True`).

  
