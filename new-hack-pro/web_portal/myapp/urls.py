from django.contrib import admin
from django.urls import path,include
from myapp import views
urlpatterns = [
   
    path('',views.home ,name='home' ),
    path('logout/',views.logout ,name='logout' ),
    path('mainhome',views.mainhome ,name='mainhome' ),
    path('register',views.register ,name='register' ),
    path('login1',views.login1 ,name='login1' ),
    path('loginuser',views.loginuser ,name='loginuser' ),
    path('registeruser',views.registeruser ,name='registeruser' ),
    path('findteacher',views.findteacher ,name='findteacher' ),
    path('findcourse',views.findcourse ,name='findcourse' ),
    path('findvideo',views.findvideo ,name='findvideo' ),
    path('indexprofile',views.indexprofile ,name='indexprofile' ),
    path('profile/', views.profilepage, name='profile')

    #path('loginuser',views.loginuser ,name='loginuser' ),
    
    
    
    #path('contact',views.contact ,name='contact' ),
    


]