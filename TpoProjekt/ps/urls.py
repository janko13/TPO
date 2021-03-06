from django.conf.urls import url
from . import views

app_name = 'ps'

urlpatterns = [
    #/ps/
    url(r'^$', views.IndexView.as_view(), name='index', kwargs={'redirect_authenticated_user': True}),
    url(r'^registracija/$', views.RacunPacientFormView.as_view(), name='registracija'),
    url(r'^registracija/(?P<pk>[0-9]+)/$', views.PacientFormView.as_view(), name='registracija2'),
    url(r'^dodajanjeOsebja/$', views.RacunOsebjeFormView.as_view(), name='dodajOsebje'),
    url(r'^dodajPacienta/$', views.PacientFormViewExtra.as_view(), name='dodajPacienta'),
    url(r'^pregledPacientovRacun/$', views.PacientRacunList, name='pacientRacunList'),  # dodano na novo
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserFormView.as_view(), name='user'),
    url(r'^userO/(?P<pk>[0-9]+)/$', views.UserOFormView.as_view(), name='userO'),
    url(r'^okolis/(?P<pk>[0-9]+)/$', views.OkolisView.as_view(), name='okolis'),
    url(r'^prijavljen/$', views.PrijavljenView.as_view(), name='userO'),
    url(r'^seznamDN/$', views.IsciDNView.as_view(), name='seznamDN'),
    url(r'^seznamDN/res/$', views.SeznamDNView.as_view(), name='seznamDNres'),
    url(r'^nalog/(?P<pk>[0-9]+)/$', views.NalogView.as_view(), name='nalog'),
    url(r'^spremeniGeslo/$', views.get_geslo, name='geslo'),
    url(r'^planiranje/$', views.VisitView, name='visit'),
    url(r'^izberiObiske/$', views.confirmVisit, name='confirmVisit'),

    # user auth urls
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout, name='odjava'),
    url(r'^loggedin/$', views.loggedin),
    url(r'^inactive/$', views.inactive_view, name='inactive'),
    #url(r'^inactive2/$', views.resend_mail, name='inactive2'),

    # link activation
    url(r'^aktivacija/(?P<pk>[0-9]+)/$', views.aktivacijaLinka, name='aktivacija-linka'),

    # dodajanje delovnega naloga
    #url(r'^dodajDelavniNalog/$', views.DodajDelavniNalog.as_view(), name='dodajDelavniNalog')
    url(r'^dodajDelavniNalog/$', views.dodajDN, name='dodajDelavniNalog')
]

