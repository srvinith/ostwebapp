from django.urls import path
from .import views

urlpatterns=[

    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('lightpage/',views.lightpage,name='lightpage'),
    path('get_state/',views.get_state,name='get_state'),
    path('change_state/',views.change_state,name='change_state'),
    path('roompage/',views.roompage,name='roompage')
]