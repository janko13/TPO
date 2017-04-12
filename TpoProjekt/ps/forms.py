from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import *

class RacunPacientForm(forms.ModelForm):
    imeKontaktna = forms.CharField(max_length=200, label='Ime kontaktne*', required=False)
    priimekKontaktna = forms.CharField(max_length=200, label='Priimek kontaktne*', required=False)
    naslovKontaktna = forms.CharField(max_length=200, label='Naslov kontaktne*', required=False)
    sorodstvoKontaktna = forms.CharField(max_length=200, label='Sorodstveno razmerje kontaktne*', required=False)
    geslo = forms.CharField(widget=forms.PasswordInput, label='Geslo')
    geslo2 = forms.CharField(widget=forms.PasswordInput, label='Ponovno vnesite geslo')
    email = forms.EmailField(label='Elektronski pošta')
    telefon = forms.CharField(label='Telefon')
    telefonKontaktna = forms.CharField(label='Telefon kontaktne*', required=False)

    def clean(self):
        cleaned_data = super(RacunPacientForm, self).clean()
        telefonK = self.cleaned_data.get('telefonKontaktna')
        imeK = self.cleaned_data.get('imeKontaktna')
        priimekK = self.cleaned_data.get('priimekKontaktna')
        naslovK = self.cleaned_data.get('naslovKontaktna')
        sorodstvoK = self.cleaned_data.get('sorodstvoKontaktna')
        if telefonK and imeK and priimekK and naslovK and sorodstvoK:
            print('JUHEJ')
            return cleaned_data

        print(priimekK)
        if telefonK or imeK or priimekK or naslovK or sorodstvoK:
            print(priimekK)
            raise forms.ValidationError("Izpolnite vsa polja o kontaktni osebi")

        return cleaned_data

    def clean_geslo(self):
        geslo = self.cleaned_data.get('geslo')

        if len(geslo) < 8:
            raise forms.ValidationError("Geslo je prekratko")
        if any(i.isdigit() for i in geslo) == False:
            raise forms.ValidationError("Geslo mora vsebovati vsaj eno cifro")
        return geslo

    def clean_email(self):
        pacienti = list(RacunPacient.objects.all().values('email'))
        osebje = list(RacunOsebje.objects.all().values('email'))
        mail = self.cleaned_data.get('email')
        for d in pacienti:
            if mail == d['email']:
                raise forms.ValidationError("Uporabnik s tem e-poštnim naslovom že obstaja")
        for d in osebje:
            if mail == d['email']:
                raise forms.ValidationError("Uporabnik s tem e-poštnim naslovom že obstaja")
        return mail


    def clean_geslo2(self):
        password1 = self.cleaned_data.get('geslo')
        password2 = self.cleaned_data.get('geslo2')

        if not password2:
            raise forms.ValidationError("Potrdite geslo")
        if password1 != password2:
            raise forms.ValidationError("Gesli se ne ujemata")
        return password2

    class Meta:
        model = RacunPacient
        fields = ['email', 'geslo', 'geslo2', 'telefon', 'imeKontaktna', 'priimekKontaktna', 'naslovKontaktna',
                  'telefonKontaktna', 'sorodstvoKontaktna']

class PacientForm(forms.ModelForm):
    GEN = (
        ('M', 'moški'),
        ('Ž', 'ženska'),
    )
    ime = forms.CharField(label='Ime')
    priimek = forms.CharField(label='Priimek')
    zavarovanjeID = forms.CharField(label='Številka zdravstvenega zavarovanja')
    datumRojstva = forms.DateField(label='Datum rojstva')
    spol = forms.ChoiceField(label='Spol', choices=GEN)
    naslov = forms.CharField(label='Naslov')
    posta = forms.ModelChoiceField(queryset=Posta.objects.all(), label='Pošta')
    okolisID = forms.ModelChoiceField(queryset=Okolis.objects.all(), label='Okoliš')

    class Meta:
        model = Pacient
        fields = ['ime', 'priimek', 'datumRojstva', 'spol', 'zavarovanjeID', 'naslov', 'okolisID', 'posta']

class RacunOsebjeForm(forms.ModelForm):
    GEN = (
        ('Zdravnik', 'Zdravnik'),
        ('Vodja PS', 'Vodja PS'),
        ('Medicinska sestra', ' Medicinska sestra'),
        ('Uslužbenec', 'Uslužbenec'),
    )

    ime = forms.CharField(max_length=200, label='Ime')
    priimek = forms.CharField(max_length=200, label='Priimek')
    geslo = forms.CharField(widget=forms.PasswordInput, label='Geslo')
    geslo2 = forms.CharField(widget=forms.PasswordInput, label='Ponovno vnesite geslo')
    email = forms.EmailField(label='Elektronski pošta')
    telefon = forms.CharField(label='Telefon')
    osebaID = forms.CharField(label='ID osebe')
    vloga = forms.ChoiceField(label='Vloga', choices=GEN)
    izvajalecZdravstveneDejavnosti = forms.ModelChoiceField(queryset=IzvajalecZdravstveneDejavnosti.objects.all(), label='Izvajalec zdravstvene dejavnosti')


    def clean_email(self):
        pacienti = list(RacunPacient.objects.all().values('email'))
        osebje = list(RacunOsebje.objects.all().values('email'))
        mail = self.cleaned_data.get('email')
        for d in pacienti:
            if mail == d['email']:
                raise forms.ValidationError("Uporabnik s tem e-poštnim naslovom že obstaja")
        for d in osebje:
            if mail == d['email']:
                raise forms.ValidationError("Uporabnik s tem e-poštnim naslovom že obstaja")
        return mail

    def clean_geslo(self):
        geslo = self.cleaned_data.get('geslo')

        if len(geslo) < 8:
            raise forms.ValidationError("Geslo je prekratko")
        if any(i.isdigit() for i in geslo) == False:
            raise forms.ValidationError("Geslo mora vsebovati vsaj eno cifro")
        return geslo

    def clean_geslo2(self):
        password1 = self.cleaned_data.get('geslo')
        password2 = self.cleaned_data.get('geslo2')

        if not password2:
            raise forms.ValidationError("Potrdite geslo")
        if password1 != password2:
            raise forms.ValidationError("Gesli se ne ujemata")
        return password2

    class Meta:
        model = RacunOsebje
        fields = [ 'ime', 'priimek', 'osebaID', 'email', 'geslo', 'geslo2', 'telefon', 'vloga', 'izvajalecZdravstveneDejavnosti',]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'password']

class GesloForm(forms.ModelForm):
    geslo = forms.CharField(widget=forms.PasswordInput, label='Staro geslo')
    password = forms.CharField(widget=forms.PasswordInput, label='Novo geslo')
    geslo2 = forms.CharField(widget=forms.PasswordInput, label='Ponovno vnesite novo geslo')

    def clean_password(self):
        geslo = self.cleaned_data.get('password')

        if len(geslo) < 8:
            raise forms.ValidationError("Geslo je prekratko")
        if any(i.isdigit() for i in geslo) == False:
            raise forms.ValidationError("Geslo mora vsebovati vsaj eno cifro")
        return geslo

    def clean_geslo(self):
        geslo = make_password(self.cleaned_data.get('geslo'), hasher='unsalted_sha1')
        staro = 'def'
        print(self.user.groups.all())
        if self.user.groups.filter(name__in=['Zdravnik', 'Medicinska sestra', 'Vodja PS', 'Uslužbenec']).exists():
            staro = RacunOsebje.objects.get(email=self.user.email).geslo
        elif self.user.groups.filter(name__in=['Pacient']).exists():
            staro = RacunPacient.objects.get(email=self.user.email).geslo

        if staro != geslo:
            raise forms.ValidationError("Staro geslo ni pravilno")
        return geslo

    def clean_geslo2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('geslo2')

        if not password2:
            raise forms.ValidationError("Potrdite geslo")
        if password1 != password2:
            raise forms.ValidationError("Gesli se ne ujemata")
        return password2

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.field_order = ['geslo', 'password', 'geslo2']
        super(GesloForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['password']