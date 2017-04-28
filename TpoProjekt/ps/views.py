from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import View
from django.views import generic
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.core.mail import EmailMessage
from django.conf import settings
from .middleware import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime
import sendgrid
from sendgrid.helpers.mail import *


from .forms import *
from .models import *

global stevec
stevec = 0
PREPOVED = ['123.123.123.123',]

#logika za izpis templata ob prijavi
class PrijavljenView(LoginRequiredMixin, generic.TemplateView):   #LOGIN required OK
    login_url = '/ps/'
    redirect_field_name = 'index'
    def dispatch(self, request, *args, **kwargs):
        return super(PrijavljenView, self).dispatch(request, *args, **kwargs)
    template_name = 'ps/prijavljen.html'


    def get_context_data(self, *args, **kwargs):
        context = super(PrijavljenView, self).get_context_data(*args, **kwargs)
        if self.request.user.username == 'admin':
            pass
        elif self.request.user.groups.all()[0].name == 'Pacient':
            racun = RacunPacient.objects.get(email=self.request.user.username)
            zadnja = racun.zadnjaPrijava
            context['zadnja'] = zadnja
        else:
            racun = RacunOsebje.objects.get(email=self.request.user.username)
            zadnja = racun.zadnjaPrijava
            context['zadnja'] = zadnja
        return context

#začetni view
class IndexView(generic.TemplateView):
    template_name = 'ps/index.html'

    def get(self, request, redirect_authenticated_user):   #DELA OK za prijavljene
        if request.user.is_authenticated():
            # If a user is logged in, redirect them to a page informing them of such
            return HttpResponseRedirect('/ps/prijavljen/')
        return render(request, self.template_name)

#view za prvi template ob "registraciji"...
class RacunPacientFormView(CreateView):
    model = RacunPacient
    form_class = RacunPacientForm
    # success_url = '/ps/registracija2/'
    def get_context_data(self, *args, **kwargs):
        context = super(RacunPacientFormView, self).get_context_data(*args, **kwargs)
        context['pacienti'] = RacunPacient.objects.filter()
        return context

    #preverjanje validacije forme in nato shranjevanje v bazo
    def form_valid(self, form):
        #hashiranje gesla
        form.instance.geslo = make_password(form.instance.geslo, hasher='unsalted_sha1')
        form.instance.geslo2 = make_password(form.instance.geslo2, hasher='unsalted_sha1')

        return super(RacunPacientFormView, self).form_valid(form)

    #po končanju prvega koraka gre na url pod "registracija2"
    def get_success_url(self):
        return reverse('ps:registracija2', args=(self.object.id,))

#view za drugi template ob registraciji
class PacientFormView(CreateView):
    model = Pacient
    form_class = PacientForm
    # success_url = '/ps/'
    #preverjanje validacije forme in nato shranjevanje v bazo
    def form_valid(self, form):
        #dobivanje ID za RacunPacient iz url naslova
        a = self.request.path
        a = a[:-1]
        a = a[17:]
        #shranjevanje pravega RacunPacient na Pacient
        form.instance.racun = RacunPacient.objects.get(pk=a)
        return super(PacientFormView, self).form_valid(form)

    #ob končanju gre na url pod "user", prenaša ID(a)
    def get_success_url(self):
        a = self.request.path
        a = a[:-1]
        a = a[17:]
        return reverse('ps:user', args=(a,))


# view za dodajanje pacienta v ze obstojec racun NOVO DODANO
class PacientFormViewExtra(CreateView):
    model = Pacient
    form_class = PacientFormExtra
    template_name = 'ps/pacient2_form.html'

    # success_url = '/ps/'
    # preverjanje validacije forme in nato shranjevanje v bazo
    def form_valid(self, form):
        # dobivanje ID za RacunPacient iz url naslova
        a = self.request.user
        racun = RacunPacient.objects.get(email=a.username)
        print(a)
        # shranjevanje pravega RacunPacient na Pacient
        form.instance.racun = racun
        return super(PacientFormViewExtra, self).form_valid(form)

    # ob končanju gre na url pod "user", prenaša ID(a)
    def get_success_url(self):
        return reverse('ps:pacientRacunList')


def PacientRacunList(request):
    #print(request.user.username)
    racun = RacunPacient.objects.get(email=request.user.username)
    pacienti = Pacient.objects.filter(racun=racun)#
    context = {
        'pacienti': pacienti,
    }
    return render(request, 'ps/pacientRacunList.html', context)
    # KONEC NOVO DODANO


#view za template ob dodajanju osebja
class RacunOsebjeFormView(CreateView):
    model = RacunOsebje
    form_class = RacunOsebjeForm

    #preverjanje validacije forme in nato shranjevanje v bazo
    def form_valid(self, form):
        #hashiranje gesla
        form.instance.geslo = make_password(form.instance.geslo, hasher='unsalted_sha1')
        form.instance.geslo2 = make_password(form.instance.geslo2, hasher='unsalted_sha1')
        return super(RacunOsebjeFormView, self).form_valid(form)
    #ob uspešnem dodajanju gre na url "userO", prenese se ID objekta
    def get_success_url(self):
        vloga = RacunOsebje.objects.get(pk=self.object.id).vloga
        if vloga == 'Medicinska sestra':
            return reverse('ps:okolis', args=(self.object.id,))
        else:
            return reverse('ps:userO', args=(self.object.id,))

class OkolisView (CreateView):
    model = Okolis
    form_class = OkolisForm

    def form_valid(self, form):
        a = self.request.path
        a = a[:-1]
        a = a[11:]
        print(a)
        form.instance.medicinskaSestra = RacunOsebje.objects.get(pk=a)
        return super(OkolisView, self).form_valid(form)
    def get_success_url(self):
        a = self.request.path
        a = a[:-1]
        a = a[11:]
        return reverse('ps:userO', args=(a,))

#view za shranjevanje pacienta v Users
class UserFormView(View):
    form_class = UserForm
    template_name = 'ps/user_form.html'
    # prikaz forme
    def get(self, request, pk):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # procesiranje podatkov iz forme
    def post(self, request, pk):
        # iz urlja dobimo pravega pacienta
        a = self.request.path
        a = a[:-1]
        a = a[9:]

        racun = RacunPacient.objects.get(pk=a)
        racun.casregistracije = datetime.datetime.now()
        racun.save()


        username = RacunPacient.objects.get(pk=a).email
        #create_user(uporabniško, email, geslo) - geslo na 'default', ker bi se drugače 2x hashiralo
        user = User.objects.create_user(username, username, 'default')
        user.is_active = False
        #shranjevanje gesla
        password = RacunPacient.objects.get(pk=a).geslo
        user.password = password
        user.save()

        # Pošiljanje registracijskega maila
        # install: pip install sendgrid
        sg = sendgrid.SendGridAPIClient(apikey=Key.objects.get(pk=1).key)
        from_email = Email("tpo.patronaza@gmail.com")
        subject = "Aktivacija računa za TPOPatronaza"
        to_email = Email(username)

        link = "http://127.0.0.1:8000/ps/aktivacija/" + a + "/"
        ctx = {'link': link}

        message = get_template('ps/email.html').render(Context(ctx))
        content = Content("text/html", message)

        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

        #dodajanje v skupino Pacient
        g = Group.objects.get(name='Pacient')
        g.user_set.add(user)
        return HttpResponseRedirect('/ps/prijavljen/')

#view za shranjevanje osebja v Users
class UserOFormView(View):
    form_class = UserForm
    template_name = 'ps/user_form.html'

    # prikaz forme
    def get(self, request, pk):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # procesiranje podatkov iz forme
    def post(self, request, pk):
        # iz urlja dobimo pravego osebje
        a = self.request.path
        a = a[:-1]
        a = a[10:]

        username = RacunOsebje.objects.get(pk=a).email
        # create_user(uporabniško, email, geslo) - geslo na 'default', ker bi se drugače 2x hashiralo
        user = User.objects.create_user(username, username, 'default')
        # shranjevanje gesla
        password = RacunOsebje.objects.get(pk=a).geslo
        user.password = password
        user.save()
        #dodajanje v skupino
        vloga = RacunOsebje.objects.get(pk=a).vloga
        print(vloga)
        g = Group.objects.get(name=vloga)
        g.user_set.add(user)

        return HttpResponseRedirect('/ps/prijavljen/')

class IsciDNView(generic.TemplateView):
    template_name = 'ps/isci.html'

#izpis seznama DN
class SeznamDNView(generic.ListView):
    template_name = 'ps/seznamDN.html'
    context_object_name = 'DN_list'

    def get_queryset(self):
        return DelavniNalog.objects.all()
    def get_context_data(self, *args, **kwargs):
        context = super(SeznamDNView, self).get_context_data(*args, **kwargs)

        oseba = RacunOsebje.objects.get(email=self.request.user.username)
        seznam = PacientDelovniNalog.objects.filter()
        vrsta = self.request.GET['vrsta']
        podvrsta = self.request.GET['podvrsta']
        casOd = self.request.GET['casOd']
        casDo = self.request.GET['casDo']
        if casOd != '':
            nalogi = DelavniNalog.objects.filter(datumVnosa__gte=casOd)
            seznam = seznam.filter(delavniNalog__in=nalogi)
        if casDo != '':
            nalogi = DelavniNalog.objects.filter(datumVnosa__lte=casDo)
            seznam = seznam.filter(delavniNalog__in=nalogi)

        if vrsta != 'vsi':
            nalogi = DelavniNalog.objects.filter(vrstaObiska=vrsta)
            seznam = seznam.filter(delavniNalog__in=nalogi)

        if podvrsta != 'vsi':
            nalogi = DelavniNalog.objects.filter(podVrstaObiska=podvrsta)
            seznam = seznam.filter(delavniNalog__in=nalogi)

        imeP = self.request.GET['imeP']
        priimekP = self.request.GET['priimekP']
        if imeP != '' or priimekP != '':
            pacienti = Pacient.objects.filter(ime__icontains=imeP).filter(priimek__icontains=priimekP)
            seznam = seznam.filter(pacient__in=pacienti)

        if oseba.vloga != 'Zdravnik':
            imeI = self.request.GET['imeI'] #I-izdajatelj
            priimekI = self.request.GET['priimekI']
            if imeI != '' or priimekI != '':
                zdravniki = RacunOsebje.objects.filter(ime__icontains=imeI).filter(priimek__icontains=priimekI).filter(
                    vloga='Zdravnik')
                dn = DelavniNalog.objects.filter(zdravnik__in=zdravniki)
                seznam = seznam.filter(delavniNalog__in=dn)

        if oseba.vloga != 'Medicinska sestra':
            imeZ = self.request.GET['imeZ'] #Z-zadolzena
            priimekZ = self.request.GET['priimekZ']
            if imeZ != '' or priimekZ != '':
                sestre = RacunOsebje.objects.filter(ime__icontains=imeZ).filter(priimek__icontains=priimekZ).filter(
                    vloga='Medicinska sestra')
                okolis = Okolis.objects.filter(medicinskaSestra__in=sestre)
                pacienti = Pacient.objects.filter(okolisID__in=okolis)
                seznam = seznam.filter(pacient__in=pacienti)

        if oseba.vloga == 'Medicinska sestra':
            okolis = Okolis.objects.get(medicinskaSestra=oseba)
            pacienti = Pacient.objects.filter(okolisID=okolis)
            context['pacientDN_list'] = seznam.filter(pacient__in=pacienti).distinct()
        elif oseba.vloga == 'Zdravnik':
            nalogi = DelavniNalog.objects.filter(zdravnik=oseba)
            context['pacientDN_list'] = seznam.filter(delavniNalog__in=nalogi)
        else:
            context['pacientDN_list'] = seznam.filter()
        #paginator = Paginator(context['pacientDN_list'], 3)
        print(context)
        return context

#izpis DN
class NalogView(generic.DetailView):
    model = DelavniNalog
    template_name = 'ps/nalog.html'


    def get_context_data(self, *args, **kwargs):
        context = super(NalogView, self).get_context_data(*args, **kwargs)
        pacienti = PacientDelovniNalog.objects.filter(delavniNalog=self.object)
        context['pacienti'] = pacienti
        context['prvi'] = pacienti.first()
        context['obiski'] = Obisk.objects.filter(delavniNalog=self.object)
        return context

#sprememba gesla
def get_geslo(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GesloForm(request.POST, user=request.user)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            geslo = form.cleaned_data.get('password')
            request.user.password =  make_password(geslo, hasher='unsalted_sha1')
            if RacunPacient.objects.filter(email=request.user.username).exists():
                print('je pacient')
                pacient = RacunPacient.objects.get(email=request.user.username)
                pacient.geslo = request.user.password
                pacient.geslo2 = request.user.password
                pacient.save()
            else:
                print('je osebje')
                osebje = RacunOsebje.objects.get(email=request.user.username)
                osebje.geslo = request.user.password
                osebje.geslo2 = request.user.password
                osebje.save()
            request.user.save()
            update_session_auth_hash(request, request.user)
            # redirect to a new URL:
            return HttpResponseRedirect('/ps/prijavljen/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GesloForm(user=request.user)

    return render(request, 'ps/geslo.html', {'form': form})


def inactive_view(request):
    if request.method == 'POST':
        print(request.user.email)

#login
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    inactive_user = User.objects.filter(email=username)
    if not inactive_user and username != 'admin':
        messages.info(request, 'Prijava ni bila uspešna. Poskusite ponovno.')
        ip = get_client_ip(request)
        global stevec
        stevec = stevec + 1
        print('ip c: ' + ip + ', stevec: ' + str(stevec))
        if stevec >= 3:
            blocked = settings.BLOCKED_IPS + [ip, ]
            settings.BLOCKED_IPS = blocked
            settings.BLOCKED_TIME = settings.BLOCKED_TIME + [datetime.datetime.now(), ]
            # settings.configure(default_settings=False, BLOCKED_IPS=blocked)
            stevec = 0
        return HttpResponseRedirect('/ps/')

    if (inactive_user is not None) and (username != 'admin'):
        print('username: ' + username)
        if (inactive_user[0].is_active == False):
            print(inactive_user[0].email)
            return render(request, 'ps/login_neaktiven.html', {'to_email': username})
            # return HttpResponseRedirect('/ps/inactive')


    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)

        if user.username == 'admin':
            pass
        elif user.groups.all()[0].name == 'Pacient':
            racun = RacunPacient.objects.get(email=user.username)
            racun.zadnjaPrijava = racun.trenutnaPrijava
            racun.trenutnaPrijava = datetime.datetime.now()
            racun.save()
        else:
            racun = RacunOsebje.objects.get(email=user.username)
            racun.zadnjaPrijava = racun.trenutnaPrijava
            racun.trenutnaPrijava = datetime.datetime.now()
            racun.save()

        global stevec
        stevec = 0
        return HttpResponseRedirect('/ps/prijavljen/')
    else:
        messages.info(request, 'Prijava ni bila uspešna. Poskusite ponovno.')
        ip = get_client_ip(request)
        global stevec
        stevec = stevec + 1
        print('ip c: ' + ip + ', stevec: ' + str(stevec))
        if stevec >= 3:
            blocked = settings.BLOCKED_IPS + [ip, ]
            settings.BLOCKED_IPS = blocked
            settings.BLOCKED_TIME = settings.BLOCKED_TIME + [datetime.datetime.now(), ]
            # settings.configure(default_settings=False, BLOCKED_IPS=blocked)
            stevec = 0
        return HttpResponseRedirect('/ps/')

#je prijavljen
def loggedin(request):

    return render_to_response('ps/prijavljen.html',
                              {'full_name':request.user.username})
#napačna prijava

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
#odjava
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/ps/')

#prikaz obiskov
#prikaz obiskov
def VisitView(request):
    pacient_delavniNalog = PacientDelovniNalog.objects.filter(pacient__okolisID__medicinskaSestra__email__exact=request.user)
    idDelavniNalogi = pacient_delavniNalog.values_list('delavniNalog_id', flat=True)
    delavniNalogi = DelavniNalog.objects.filter(id__in = idDelavniNalogi)
    obiski = Obisk.objects.filter(delavniNalog__in = delavniNalogi.values('id'), obiskOpravljen__exact = 'ne').order_by('predvidenDatumObiska')
    stDni = range(1, 32)
    stMes = range(1, 13)
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    stLet = range(today.year, today.year + 6)
    now = str(today)
    context = {
        'obiski': obiski,
        'stDni': stDni,
        'stMes': stMes,
        'stLet': stLet,
        'now': now,
        'tomorrow': tomorrow,
        'today': today
    }
    print(now)
    return render(request, 'ps/izbiraobiska.html', context)

#izdelava planov obiskov
def confirmVisit(request):
    if (request.POST.get('PotrdiPlan')):
        pacient_delavniNalog = PacientDelovniNalog.objects.filter(pacient__okolisID__medicinskaSestra__email__exact=request.user)
        idDelavniNalogi = pacient_delavniNalog.values_list('delavniNalog_id', flat=True)
        delavniNalogi = DelavniNalog.objects.filter(id__in=idDelavniNalogi)
        obiski = Obisk.objects.filter(delavniNalog__in=delavniNalogi.values('id'), obiskOpravljen__exact='ne').order_by('predvidenDatumObiska')
        for x in range(0, len(obiski)):
            action_name = 'menu' + str(x)
            if (request.POST.get(action_name) == 'Dodaj' or request.POST.get(action_name) == 'Spremeni'):
                datum_name = 'datum' + str(x)
                novDatum_s = request.POST.get(datum_name)
                plan_day = novDatum_s[8:]
                plan_month = novDatum_s[5:7]
                plan_year = novDatum_s[:4]
                if plan_day.isdigit() and plan_month.isdigit() and plan_year.isdigit():
                    novDatum = datetime.date(int(plan_year), int(plan_month), int(plan_day))
                    if (novDatum >= datetime.date.today()):
                        obisk = Obisk.objects.get(id__exact=obiski.values('id')[x]['id'])
                        obisk.zePlaniran = 'da'
                        obisk.planiranDatumObiska = novDatum
                        obisk.save()
            elif (request.POST.get(action_name) == 'Odstrani'):
                obisk = Obisk.objects.get(id__exact=obiski.values('id')[x]['id'])
                obisk.zePlaniran = 'ne'
                obisk.save()
    if (request.POST.get('RazveljaviPlan')):
        print("do nothing")
    return HttpResponseRedirect('/ps/planiranje/')


def aktivacijaLinka(request, pk):

    racun = RacunPacient.objects.get(pk=pk)

    # pretvorimo cas v sekunde
    reg_time = racun.casregistracije
    now = datetime.datetime.now()
    s1 = reg_time.second + reg_time.minute * 60 + reg_time.hour * 3600
    s2 = now.second + now.minute * 60 + now.hour * 3600

    # razlika casov mora biti manjsa od 180 sekund (3 min)
    s = s2 - s1
    if (s < 180):
        racun.aktiviran = True
        racun.save()

        user = User.objects.get(username=racun.email)
        user.is_active = True
        user.save()
    else:
        return render(request, 'ps/registracija_potekla.html')

    return HttpResponseRedirect('/ps/prijavljen')

#tocka 5
class DodajDelavniNalog(CreateView):
# class FormMixin(ContextMixin):
    # user = self.request.user
    # print(user.groups.all())
    model = DelavniNalog
    form_class = DelavniNalogForm
    success_url = '/ps/prijavljen'

    def form_valid(self, form):
        # v delavni nalog se avtomatsko shrani user in njegova ustanova
        racun = RacunOsebje.objects.filter(email=self.request.user.username)
        form.instance.zdravnik = racun[0]
        form.instance.izvajalecZdravstveneDejavnosti = racun[0].izvajalecZdravstveneDejavnosti

        return super(DodajDelavniNalog, self).form_valid(form)


def dodajDN(request):

    if request.method == 'POST':
        delavniNalog = DelavniNalogForm(request.POST)

        if delavniNalog.is_valid():
            dn = delavniNalog.save(commit=False)

def dodajDN(request):

    context = {'form': DelavniNalogForm,
               'pacientForm': PacientDelovniNalog,
               'obiskForm': ObiskForm,
               'zdravilaForm': ZdravilaDelovniNalog,
               'materialForm': MaterialDelovniNalog}

    if request.method == 'POST':
        delavniNalog = DelavniNalogForm(request.POST)
        pForm = PacientDelovniNalog(request.POST)
        if delavniNalog.is_valid() and pForm.is_valid():
            # shranimo delavni nalog
            dn = delavniNalog.save(commit=False)
            dn.zdravnik = RacunOsebje.objects.get(email=request.user.username)
            dn.izvajalecZdravstveneDejavnosti = RacunOsebje.objects.get(email=request.user.username).izvajalecZdravstveneDejavnosti
            dn.save()
            # povezovalna tabela pacient - delavni nalog
            pf = pForm.save(commit=False)
            pf.delavniNalog = dn
            pf.save()


            return HttpResponseRedirect('/ps/prijavljen')

    return render(request, 'ps/delavninalog_form.html', context)

#def resend_mail(request, email):
#    print('username:' + request.user.username)
#    return HttpResponseRedirect('/ps/')