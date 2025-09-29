from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.
def about(request):
    return HttpResponse(" Application Bonnes Lectures, développée en TP de Framework Web, Université d’Orléans, 2024")

def welcome(request):
    return render(request, "bonnes_lectures/welcome.html")