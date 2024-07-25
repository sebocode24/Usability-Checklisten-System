from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import pandas as pd
import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def index(request):
    user = request.user
    projekte = Project.objects.filter(user=user)
    return render(request, 'index.html', {'projekte': projekte})

@login_required
def new_projekt(request):
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            projekt = form.save()
            projekt.user.add(request.user)

            df = pd.read_excel('checkliste/static/Kriterienliste.xlsx')

            for _, row in df.iterrows():
                name = row['Kriterium']
                kategorie_name = row['Kategorie']
                subkategorie_name = row['Unterkategorie']

                category, _ = Category.objects.get_or_create(name=kategorie_name)

                if pd.notna(subkategorie_name):
                    subcategory, _ = SubCategory.objects.get_or_create(name=subkategorie_name, category=category)
                else:
                    subcategory = None

                Criterion.objects.create(
                    name=name,
                    projekt=projekt,
                    kategorie=category,
                    subkategorie=subcategory
                )

            return redirect('index')
    else:
        form = NewProjectForm()
    return render(request, 'neues-projekt.html', {'form': form})

@login_required
def projekt(request, pk):
    categories = Category.objects.all()
    projekt = Project.objects.get(id=pk)
    return render(request, 'projekt.html', {'categories': categories, 'projekt': projekt})

@login_required
def kategorie(request, pr_pk, kat_pk):
    projekt = Project.objects.get(id=pr_pk) 
    
    category = Category.objects.get(id=kat_pk)
    
    if request.method == 'POST':
        criteria = Criterion.objects.filter(projekt=projekt, kategorie=category)
        for criterion in criteria:
            form = RatingForm(request.POST, instance=criterion)
            if form.is_valid():
                form.save()
        return redirect('projekt', pk=pr_pk)
    else:
        criteria = Criterion.objects.filter(projekt=projekt, kategorie=category)
        formset = {'NoSubcategory': [RatingForm(instance=criterion) for criterion in criteria if criterion.subkategorie is None]}
        
        subcategories = SubCategory.objects.filter(category=category)
        for subcategory in subcategories:
            formset[subcategory] = [RatingForm(instance=criterion) for criterion in criteria if criterion.subkategorie == subcategory]
    
    return render(request, 'rating_list.html', {'formset': formset, 'category': category})

def auswertung(request, pk):
    projekt = Project.objects.get(id=pk)
    categories = Category.objects.all()
    return render(request, 'auswertung.html', {'projekt': projekt, 'categories': categories})


@login_required
def kategorie_auswertung(request, pr_pk, kat_pk):
    projekt = Project.objects.get(id=pr_pk)
    category = Category.objects.get(id=kat_pk)

    # Alle Kriterien ohne Subkategorie
    no_subcategory_criteria = Criterion.objects.filter(projekt=projekt, kategorie=category, subkategorie=None)
    
    # Kriterien pro Subkategorie
    subcategories = SubCategory.objects.filter(category=category)
    subcategory_criteria = {
        subcategory: Criterion.objects.filter(projekt=projekt, kategorie=category, subkategorie=subcategory)
        for subcategory in subcategories
    }

    # Daten für Chart.js vorbereiten
    labels = [criterion.name for criterion in no_subcategory_criteria]
    no_subcategory_data = [criterion.rating for criterion in no_subcategory_criteria]

    subcategory_data = {
        subcategory.name: [criterion.rating for criterion in criteria]
        for subcategory, criteria in subcategory_criteria.items()
    }
    
    return render(request, 'kategorie_auswertung.html', {
        'projekt': projekt,
        'category': category,
        'labels': json.dumps(labels, cls=DjangoJSONEncoder),
        'no_subcategory_data': json.dumps(no_subcategory_data, cls=DjangoJSONEncoder),
        'subcategory_data': json.dumps(subcategory_data, cls=DjangoJSONEncoder),
    })
def gesamt_auswertung(request, pk):
    pass