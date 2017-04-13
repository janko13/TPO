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
    datumRojstva = forms.DateField(label='Datum rojstva', widget=forms.DateInput(attrs={'type': 'date'}))
    spol = forms.ChoiceField(label='Spol', choices=GEN)
    naslov = forms.CharField(label='Naslov')
    posta = forms.ModelChoiceField(queryset=Posta.objects.all(), label='Pošta')
    okolisID = forms.ModelChoiceField(queryset=Okolis.objects.all(), label='Okoliš')

    def clean_zavarovanjeID(self):
        pacienti = list(Pacient.objects.all().values('zavarovanjeID'))
        zavarovanjeID = self.cleaned_data.get('zavarovanjeID')
        for d in pacienti:
            if zavarovanjeID == d['zavarovanjeID']:
                raise forms.ValidationError("Uporabnik s tem zavarovanjem že obstaja")
        return zavarovanjeID

    class Meta:
        model = Pacient
        fields = ['ime', 'priimek', 'datumRojstva', 'spol', 'zavarovanjeID', 'naslov', 'okolisID', 'posta']

#ZAČETEK DODAJANJA NOVEGA PACIENTA NA OBSTOJEČ RAČUN

class PacientFormExtra(forms.ModelForm):
    GEN = (
        ('M', 'moški'),
        ('Ž', 'ženska'),
    )
    SOR = (
        ('Mama', 'mama'),
        ('Oče', 'oče'),
        ('Brat', 'brat'),
        ('Sestra', 'sestra'),
        ('Žena', 'žena'),
        ('Mož', 'mož'),
        ('Sin', 'sin'),
        ('Hči', 'hči'),
        ('Drugo', 'drugo'),
    )
    ime = forms.CharField(label='Ime')
    priimek = forms.CharField(label='Priimek')
    zavarovanjeID = forms.CharField(label='Številka zdravstvenega zavarovanja')
    datumRojstva = forms.DateField(label='Datum rojstva', widget=forms.DateInput(attrs={'type': 'date'}))
    spol = forms.ChoiceField(label='Spol', choices=GEN)
    naslov = forms.CharField(label='Naslov')
    posta = forms.ModelChoiceField(queryset=Posta.objects.all(), label='Pošta')
    okolisID = forms.ModelChoiceField(queryset=Okolis.objects.all(), label='Okoliš')
    sorodstvoRacun = forms.ChoiceField(label='Sorodstvo', choices=SOR)

    def clean_zavarovanjeID(self):
        pacienti = list(Pacient.objects.all().values('zavarovanjeID'))
        zavarovanjeID = self.cleaned_data.get('zavarovanjeID')
        for d in pacienti:
            if zavarovanjeID == d['zavarovanjeID']:
                raise forms.ValidationError("Uporabnik s tem zavarovanjem že obstaja")
        return zavarovanjeID

    class Meta:
        model = Pacient
        fields = ['ime', 'priimek', 'datumRojstva', 'spol', 'zavarovanjeID', 'naslov', 'okolisID', 'posta', 'sorodstvoRacun']

#KONEC DODAJANJA NOVEGA PACIENTA NA OBSTOJEČ RAČUN

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

    def clean_osebaID(self):
        osebje = list(RacunOsebje.objects.all().values('osebaID'))
        osebaID = self.cleaned_data.get('osebaID')
        for d in osebje:
            if osebaID == d['osebaID']:
                raise forms.ValidationError("Uporabnik s tem ID-jem že obstaja")
        return osebaID

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


#delavni nalog forma
class DelavniNalogForm(forms.ModelForm):
    nujnost = (
        ('o', 'obvezn'),
        ('n', 'okvirn'),
    )

    moznostiZaVrstoObiska = (
        ('po', 'preventivni obisk'),
        ('ko', 'kurativni obisk'),
    )

    moznostiZaPodVrstoObiska = (
        ('on', 'obisk nosečnice'),
        ('oo', 'obisk otročičnice in novorojenčka'),
        ('ps', 'preventiva starostnika'),
        ('ai', 'aplikacija inekcije'),
        ('ok', 'odvzem krvi'),
        ('ks', 'kontrola zdravstvenega stanja'),
    )
    #dobi od uporabnika
    zdravnik = forms.ModelChoiceField(queryset=RacunOsebje.objects.all())
    bolezn = forms.ModelChoiceField(label='Bolezen', queryset=SifrantBolezn.objects.all(), required=False)
    datumPrvegaObiska = forms.DateField(label='Datum prvega obiska', widget=forms.DateInput(attrs={'type': 'date'}))
    nujnostObiska = forms.ChoiceField(label='Nujnost obiska', choices=nujnost)
    steviloObiskov = forms.IntegerField(label='Število obiskov')
    vrstaObiska = forms.ChoiceField(label='Vrsta obiska', choices=moznostiZaVrstoObiska)
    podVrstaObiska = forms.ChoiceField(label='Pod vrsta obiska', choices=moznostiZaPodVrstoObiska)
    # previri da je izpoljen eden od obeh
    casovniIntervalMedDvemaObiskoma = forms.CharField(label='Časovni interval med dvema obiskoma')
    casovnoObdobje = forms.CharField(label='Časovno obdobje')
    # dobi od uporabnika
    izvajalecZdravstveneDejavnosti = forms.ModelChoiceField(queryset=IzvajalecZdravstveneDejavnosti.objects.all())

    class Meta:
        model = DelavniNalog
        fields = ['zdravnik', 'bolezn', 'datumPrvegaObiska', 'nujnostObiska', 'steviloObiskov', 'vrstaObiska',
                  'podVrstaObiska', 'casovniIntervalMedDvemaObiskoma', 'casovnoObdobje',
                  'izvajalecZdravstveneDejavnosti']