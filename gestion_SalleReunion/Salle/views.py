from django.shortcuts import render, redirect, get_object_or_404
from .forms import SalleForm
from API.models import Salle

def creer_salle(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('details_salle', salle_id=form.instance.pk)
    else:
        form = SalleForm()
    
    return render(request, 'creer.html', {'form': form})

def details_salle(request, salle_id):
    salle = get_object_or_404(Salle, pk=salle_id)
    return render(request, 'details_salle.html', {'Salle': salle})

def list_salles(request):
    salles = Salle.objects.all()
    # Par défaut, affichez tous les clients (supprimés et non supprimés)
    show_deleted = request.GET.get('show_deleted', False)

    if not show_deleted:
        # Si vous ne souhaitez pas afficher les clients supprimés, filtrez-les
        salles = salles.filter(isDeleted = False)

    return render(request, 'SalleList.html', {'salles': salles})

def modifier_salle(request, salle_id):
    salle = Salle.objects.get(id=salle_id)
    if request.method == 'POST':
        form = SalleForm(request.POST, instance=salle)
        if form.is_valid():
            form.save()
            return redirect("SalleList")
    else:
        form = SalleForm(instance=salle)
    return render(request, 'modifierSalle.html', {'form': form})

def supprimer_salle(request,salle_id):
    salle=Salle.objects.get(id=salle_id)
    if request.method == 'POST':
        
        #salle.delete()
        salle.isDeleted = True
        salle.save()
        return redirect('SalleList')
    else:
        return render(request, 'supprimerSalle.html', {'salle': Salle})