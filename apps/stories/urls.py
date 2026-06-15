from django.urls import path
from django.http import HttpResponse

app_name = 'stories'

def home(request):
    return HttpResponse("Universo Histórias")

urlpatterns = [
    path('', home, name='home'),
]