from django import forms
from API.models import Salle, TypeEquipement

class SalleForm(forms.ModelForm):
    ETAGE_CHOICES = [(i, str(i)) for i in range(11)]  # List of tuples representing choices for étage
    ZONE_CHOICES = [(i, str(i)) for i in range(1, 7)]  # List of tuples representing choices for zone

    # Choices for the 'etat' field
    ETAT_CHOICES = [
        ('Disponnible', 'Disponnible'),
        ('Non Disponnible', 'Non Disponnible'),
    ]

    # Choices for the 'typeSalle' field
    TYPESALLE_CHOICES = [
        ('Salle étranger', 'Salle étranger'),
        ('Salle de formation', 'Salle de formation'),
        ('Amphie', 'Amphie'),
        ('Salle réunion', 'Salle réunion'),
    ]

    # Choices for the 'securise' field
    SECURISE_CHOICES = [
        (True, 'Sécurisé'),
        (False, 'Non sécurisé'),
    ]

    étage = forms.ChoiceField(choices=ETAGE_CHOICES, label='Étage')
    zone = forms.ChoiceField(choices=ZONE_CHOICES, label='Zone')
    etat = forms.ChoiceField(choices=ETAT_CHOICES, initial='libre', label='État')
    typeSalle = forms.ChoiceField(choices=TYPESALLE_CHOICES, label='Type de salle')
    securise = forms.ChoiceField(choices=SECURISE_CHOICES, label='Sécurisé')
    equipements=forms.ModelMultipleChoiceField(
        queryset=TypeEquipement.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Salle
        fields = ['étage', 'zone', 'numero_de_salle','nom_salle', 'capacite', 'etat', 'typeSalle', 'securise']
        labels = {
            'numero_de_salle': 'Numéro de salle',
            'capacite': 'Capacité',
            'nom_salle':'Nom de salle'
        }

    def __init__(self, *args, **kwargs):
        super(SalleForm, self).__init__(*args, **kwargs)
        self.fields['equipements'].queryset = TypeEquipement.objects.all()

    def clean_numero_de_salle(self):
        numero_de_salle = self.cleaned_data.get('numero_de_salle')
        if Salle.objects.filter(numero_de_salle=numero_de_salle).exists():
            raise forms.ValidationError("une Salle avec Numero de Salle existe déjà.")
        return numero_de_salle