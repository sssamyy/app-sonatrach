from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    # path('login/',views.login,name='login'),
    path('planning',views.index_planning,name='index_planning'),
    path('planning/<int:pk>/',views.calendar_view,name='planning'),
    path('login',views.AuthenticationView.as_view(template_name='login.html'),name='authentification'),
    path('logout/', views.logout_view, name='logout'),
    path('page_accueil/',views.dashbord_user,name='dashbord_user'),
    path('page_accueil_ad/',views.dashbord_admin,name='dashbord_admin')
]