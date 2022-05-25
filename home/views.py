from django.shortcuts import render
from .models import Orders


def index(request):
    dates_bd = Orders.objects.all()


    dates = {'dates': dates_bd}

    return render(request, 'home/index.html', dates)
