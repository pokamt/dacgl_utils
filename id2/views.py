#-*- coding: utf-8 -*-

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

from id2.forms import InscriptionForm

def index(request):
    
    contexte = {}

    return render(request,'id2/index.html',contexte)

def entree(request):
    return render(request,'id2/entree.html')

def entreeVerification(request):
    
    if request.method == 'POST':
        usern = request.POST['identifiant']
        passwd = request.POST['password']
        user = authenticate(username=usern, password = passwd)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/ident/inscription/')
            else :
                # compte désactivé
                return HttpResponseForbidden('/ident/')

    return HttpResponseRedirect('/ident/login/')

def inscription(request):
    """
    Saisie des informations relatives au passage d'un usager
    """

    form = InscriptionForm()

    return render(request,'id2/inscription.html',{'form':form})
