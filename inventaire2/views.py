import csv

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .models import Piece,Implantation
from .forms import inventaireLegacyForm, implantationForm

def csvToInventaire(f):
    with open(f, newline='') as csvfile:
        inventaire_orig = csv.reader(csvfile, delimiter=',')
        extraction_f = []
        for row in inventaire_orig:
            extraction_f.append(row)
        return extraction_f

def index(request):

    contexte = {}
    pT = Piece.objects.all()
    p = pT.order_by('-date_acquisition')[:40]
    implantations = Implantation.objects.all()
    # on fixe arbitrairement le périmètre «global» à 30
    contexte = {'piece': p, 'pT':pT,'implantations': implantations,
            'perimetre0': 30,}


    if request.method == "GET":
        form = implantationForm(request.GET)
        if form.is_valid():
            site_X = form.cleaned_data['implantationX']
            contexte['perimetre'] = site_X.id
            implantationX = Implantation.objects.get(pk=site_X.id)
            pX_T = Piece.objects.\
                filter(emplacement__site__id=site_X.id)
            if len(pX_T) == 0:
                message = 'Aucune information pour %s' % site_X.nom
                contexte['message'] = message
            else :
                pX = pX_T.order_by('-date_acquisition')[:40]
                contexte['pX_T'] = pX_T
                contexte['pX'] = pX
            contexte['implantationX'] = implantationX

    form = implantationForm()
    contexte['form']  = form

    return render(request,'inventaire2/index2.html', contexte)

def siteInfos(request,site_id):

    infos = Implantation.objects.get(pk=site_id)
    contexte = {'infos': infos }
    return render(request,'inventaire2/site.html', contexte)

def extraction(request,perimetre):

    fuseau = timezone.get_current_timezone()
    moment = datetime.now(fuseau)

    format_res = 'inventaire_'+ str(moment.year) +\
            str(moment.month) + str(moment.day) +\
            str(moment.hour) + str(moment.second)

    info_MIME = "attachment;filename=" + format_res

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = info_MIME
    
    writer = csv.writer(response)

    #TODO : laisser le choix à l'utilisateur
    entete = ['Site','Emplacement',
            "Catégorie",
            'Intitule',"Prix d'achat",
            "Devise",'Numéro de série',
            'Fonctionnel','Usage',
            "Date d'acquisition","Code d'inventaire",
            "Code document","Numéro CODA",
            "Valeur Commande CODA","Marque","Modèle",
            "Description","Commentaire",
            ]
    writer.writerow(entete)

    if perimetre == '30':
        piece_a_extraire = Piece.objects.all()
    else:
        piece_a_extraire = \
                Piece.objects.filter(emplacement__site__id=perimetre)

    for piece in piece_a_extraire:
        code_document = 'COM-' + \
        piece.commande_coda.section

        ligne_fichier = [
                piece.emplacement.site.nom,
                piece.emplacement.nom,
                piece.categorie,
                piece.intitule,
                piece.prix_achat,
                piece.devise.identifiant,
                piece.num_serie,
                piece.fonctionnel,
                piece.usage,
                piece.date_acquisition,
                piece.code_inventaire,
                code_document,
                piece.commande_coda.numero,
                piece.commande_coda.valeur,
                piece.modele.constructeur.nom,
                piece.modele.modele,
                piece.description,
                piece.commentaire,
                ]
        writer.writerow(ligne_fichier)

    return response

@login_required(login_url='/login/')
def importation(request):

    form = inventaireLegacyForm()
    contexte = {'form': form,}
    return render(request,'inventaire2/importation-csv.html',
            contexte)

def importationProcess(request):
    """Importation des données des autres sites

    Certaines informations seront fournies par défaut.
    Commande CODA: COM-INF 1
    valeur : 0 XAF
    """

    contexte = {}
    if request.method == 'POST':
        form = inventaireLegacyForm(request.POST,request.FILES)
        if form.is_valid():
            f = request.FILES['fichier']
            if f.content_type == 'text/csv':

                import_f = csvToInventaire(request.FILES['fichier'])
                premiere_ligne = True
                ligne = 0
                nbr_lignes_OK = 0
                lignes_Not_OK = []
                for colonne in import_f:
                    ligne +=1
                    if premiere_ligne :
                        premiere_ligne = False
                        continue
                    try:
                        implantation0 = Implantation.objects.get(\
                                nom__icontains=colonne[1])
                    except Implantation.DoesNotExist:
                        implantation0 = Implantation(nom=colonne[1])
                        implantation0.save()
                    try:
                        salle0 = implantation0.salle_set.get(\
                                nom__icontains=colonne[2])
                    except Salle.DoesNotExist:
                        salle0 = Salle(nom=colonne[2],site=implantation0)
                        salle0.save()

                    try:
                        marque0 = Marque.objects.get(nom__icontains=\
                                colonne[15])
                    except Marque.DoesNotExist:
                        marque0 = Marque(nom=colonne[15])
                        marque0.save()
                    try:
                        produit0 = marque0.produit_set.get(\
                                modele__icontains=colonne[16])
                    except Produit.MultipleObjectsReturned :
                        pass #TODO
                    except Produit.DoesNotExist:
                        produit0 = Produit(modele=colonne[16],
                                constructeur=marque0)
                        produit0.save()

                    try:
                        piece = Piece(intitule = colonne[4],
                                prix_achat = colonne[5],
                            devise = colonne[6],
                            date_acquisition = colonne[10],
                            code_inventaire = colonne[11],
                            emplacement = salle0,
                            #on rappelle qu'on se sert par défaut de
                            #la COM-INF 1
                            commande_coda = \
                                    Commande.objects.get(numero=1),
                            modele = produit0,
                            categorie = colonne[3],
                            )
                    except Piece.DoesNotExist:
                        piece.save()
                        nbr_lignes_OK += 1

                    else:
                        # cette pièce a déjà été inventoriée
                        lignes_Not_OK.append(ligne)

                contexte = {'lignes_Not_OK': lignes_Not_OK,
                        'nbr_lignes_OK': nbr_lignes_OK,
                        'total_lignes': ligne,
                        'f': f,
                        }

                return render(request,
                'inventaire2/importation-csv-report.html',
                contexte, status=302)

            else :
                form = inventaireLegacyForm()
                contexte = {'message': "votre fichier n'est pas au \
                        format CSV",
                        'form': form,
                        'f':f,
                        }
                return render(request, 'inventaire2/importation-csv.html',
                        contexte)
    else:
        form = inventaireLegacyForm()
        contexte = {'message': 'Veuillez recommencer svp',
                'form': form }
        return  render(request,'inventaire2/importation-csv.html',
                contexte)
