from django.contrib.auth.models import User, Group
from django.db import models
from django import forms
import datetime

# Create your models here.
from django.utils import timezone

class Key(models.Model):
    opis = models.CharField(max_length=250)
    key = models.CharField(max_length=250)

class SifrantMateriala (models.Model):
    GEN = (
        ('rd', 'rdeča'),
        ('mo', 'modra'),
        ('ru', 'rumena'),
        ('ze', 'zelena'),
    )

    barvaEpruvet = models.CharField(max_length=2, choices=GEN)

    def __str__(self):
        return self.barvaEpruvet


class SifrantZdravil (models.Model):
    imeZdravila = models.CharField(max_length=250)
    sifraZdravila = models.CharField(max_length=25)

    def __str__(self):
        return self.imeZdravila + ' ' + self.sifraZdravila


class SifrantBolezn(models.Model):
    imeBolezni = models.CharField(max_length=250)
    sifraBolezni = models.CharField(max_length=25)

    def __str__(self):
        return self.imeBolezni + ' ' + self.sifraBolezni


class Posta(models.Model):
    imePosta = models.CharField(max_length=250)
    sifraPosta = models.CharField(max_length=25)

    def __str__(self):
        return self.imePosta + ' ' + self.sifraPosta


class IzvajalecZdravstveneDejavnosti (models.Model):
    posta = models.ForeignKey(Posta)
    imeIzvajalecZdravstveneDejavnosti = models.CharField(max_length=250)
    sifraIzvajalecZdravstveneDejavnosti = models.CharField(max_length=25)
    naslovIzvajalecZdravstveneDejavnosti = models.CharField(max_length=250, default='string')

    def __str__(self):
        return self.imeIzvajalecZdravstveneDejavnosti + ' ' + self.sifraIzvajalecZdravstveneDejavnosti \
              + ' ' + self.naslovIzvajalecZdravstveneDejavnosti


class RacunOsebje(models.Model):
    GEN = (
        ('Zdravnik', 'Zdravnik'),
        ('Vodja PS', 'Vodja PS'),
        ('Medicinska sestra', 'Medicinska sestra'),
        ('Uslužbenec', 'Uslužbenec'),
    )

    izvajalecZdravstveneDejavnosti = models.ForeignKey(IzvajalecZdravstveneDejavnosti)
    osebaID = models.CharField(max_length=5)
    geslo = models.CharField(max_length=50, default='blablabla')
    geslo2 = models.CharField(max_length=50, default='blablabla')
    priimek = models.CharField(max_length=250)
    ime = models.CharField(max_length=250)
    email = models.EmailField()
    telefon = models.CharField(max_length=25)
    vloga = models.CharField(max_length=40, choices=GEN, default='Zdravnik')
    neuspesenVnos = models.IntegerField(default=0)

    def __str__(self):
        return self.ime + ' ' + self.priimek + ' ' + self.vloga

class Okolis (models.Model):
    imeOkolisa = models.CharField(max_length=250)
    sifraOkolisa = models.CharField(max_length=25)
    medicinskaSestra = models.ForeignKey(RacunOsebje)

    def __str__(self):
        return self.imeOkolisa + ' ' + self.sifraOkolisa


class RacunPacient(models.Model):
    telefon = models.CharField(max_length=25)
    email = models.EmailField()
    geslo = models.CharField(max_length=50, default='blablabla')
    geslo2 = models.CharField(max_length=50, default='blablabla')
    aktiviran = models.BooleanField(default=False)
    imeKontaktna = models.CharField(max_length=250, blank=True, null=True)
    priimekKontaktna = models.CharField(max_length=250, blank=True, null=True)
    naslovKontaktna = models.CharField(max_length=250, blank=True, null=True)
    telefonKontaktna = models.CharField(max_length=25, blank=True, null=True)
    sorodstvoKontaktna = models.CharField(max_length=250, blank=True, null=True)
    neuspesenVnos = models.IntegerField(default=0)
    casregistracije = models.DateTimeField(default=datetime.datetime.now(), null=True)


    def __str__(self):
        return self.email


class Pacient(models.Model):
    GEN = (
        ('M', 'moški'),
        ('Ž', 'ženska'),
    )
    ime = models.CharField(max_length=250)
    priimek = models.CharField(max_length=250)
    zavarovanjeID = models.CharField(max_length=20)
    datumRojstva = models.DateField()
    spol = models.CharField(choices=GEN, max_length=1)
    naslov = models.CharField(max_length=250)
    posta = models.ForeignKey(Posta)
    okolisID = models.ForeignKey(Okolis)
    sorodstvoRacun = models.CharField(max_length=250, default='lasten')
    racun = models.ForeignKey(RacunPacient)

    def __str__(self):
        return self.ime + ' ' + self.priimek + ' ' + self.sorodstvoRacun


class DelavniNalog(models.Model):
    nujnost = (
        ('obvezen', 'obvezen'),
        ('okviren', 'okviren'),
    )

    moznostiZaVrstoObiska = (
        ('preventivni obisk', 'preventivni obisk'),
        ('kurativni obisk', 'kurativni obisk'),
    )

    moznostiZaPodVrstoObiska = (
        ('obisk nosečnice', 'obisk nosečnice'),
        ('obisk otročičnice in novorojenčka', 'obisk otročičnice in novorojenčka'),
        ('preventiva starostnika', 'preventiva starostnika'),
        ('aplikacija inekcije', 'aplikacija inekcije'),
        ('odvzem krvi', 'odvzem krvi'),
        ('kontrola zdravstvenega stanja', 'kontrola zdravstvenega stanja'),
    )

    zdravnik = models.ForeignKey(RacunOsebje)
    bolezn = models.ForeignKey(SifrantBolezn, null=True, blank=True)
    datumPrvegaObiska = models.DateField()
    nujnostObiska = models.CharField(max_length=19, choices=nujnost)
    steviloObiskov = models.IntegerField()
    vrstaObiska = models.CharField(max_length=29, choices=moznostiZaVrstoObiska)
    podVrstaObiska = models.CharField(max_length=29, choices=moznostiZaPodVrstoObiska)
    casovniIntervalMedDvemaObiskoma = models.CharField(max_length=25, blank=True, null=True)
    casovnoObdobje = models.CharField(max_length=25, blank=True, null=True)
    izvajalecZdravstveneDejavnosti = models.ForeignKey(IzvajalecZdravstveneDejavnosti)
    datumVnosa = models.DateField(editable=False, default=timezone.now) #dodano

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.datumVnosa = timezone.now()
        return super(DelavniNalog, self).save(*args, **kwargs)


class Obisk(models.Model):
    opravljen = (
        ('ne', 'ne'),
        ('da', 'da'),
    )
    delavniNalog = models.ForeignKey(DelavniNalog)
    predvidenDatumObiska = models.DateField()  # spremenjeno iz datumObiska
    dejanskiDatumObiska = models.DateField(default=timezone.now)  # dodano
    planiranDatumObiska = models.DateField(default=timezone.now)
    zaporednoSteviloObiska = models.IntegerField(default=0)
    obiskOpravljen = models.CharField(max_length=2, choices=opravljen, default='ne')
    zePlaniran = models.CharField(max_length=2, choices=opravljen, default='ne')


class PacientDelovniNalog(models.Model):
    delavniNalog = models.ForeignKey(DelavniNalog)
    pacient = models.ForeignKey(Pacient)


class ZdravilaDelovniNalog (models.Model):
    delavniNalog = models.ForeignKey(DelavniNalog)
    zdravial = models.ForeignKey(SifrantZdravil)
    stevilo = models.IntegerField()


class MaterialDelovniNalog (models.Model):
    delavniNalog = models.ForeignKey(DelavniNalog)
    material = models.ForeignKey(SifrantMateriala)
    stevilo = models.IntegerField()