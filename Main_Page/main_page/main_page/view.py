from django.shortcuts import render
import shutil
import os


def show_main(request):

    context = {}
    return render(request, 'main.html', context)
