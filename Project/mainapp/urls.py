from django.conf.urls import url
from django.urls import path

from mainapp import views

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),

    path('feedback/<int:pk>', views.FeedbackView.as_view(), name='feedback'),

    path('info/', views.InfoView.as_view(), name='info'),

    path('home/', views.HomeView.as_view(), name='home'),

    path('offer/<int:pk>', views.OfferView.as_view(), name='offer'),

    path('offer/<int:pk>/questions/', views.OfferQuestionsView.as_view(), name='question_list'),

    path('offer/<int:pk>/questions/create/', views.OfferQuestionCreate.as_view(), name='question_form'),

    path('response/<int:pk>', views.OfferResponseView.as_view(), name='response_detail'),

    url(r'^offer/response/(?P<pk>\d+)$', views.OfferResponseCreate, name='response_form'),

    path('employer/<int:pk>', views.OfferListByEmployerView.as_view(), name='offer_list_by_employer'),

    path('offer/<int:pk>/response/getall', views.ResponseListForOffer.as_view(), name='response_list_for_offer'),

    path('search/', views.OfferSearchListView.as_view(), name='offer_search_list_view'),

    url(r'^offer/delete/(?P<pk>\d+)$', views.offerDelete, name='offer_delete'),

    url(r'^offer/edit/(?P<pk>\d+)$', views.offerEdit, name='offer_edit'),

    url(r'^employer/edit/(?P<pk>\d+)$', views.employerEdit, name='employer_edit'),

    url(r'^question/delete/(?P<pk>\d+)$', views.questionDelete, name='question_delete'),

    url(r'^offer/new/$', views.NewOffer, name='newoffer'),

    url(r'^signin/$', views.UserFormView, name='signin'),

    url(r'^user/login$', views.LogIn, name='login'),

]
