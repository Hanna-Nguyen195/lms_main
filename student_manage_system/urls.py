from django.urls import path, include

from student_manage_system import views
urlpatterns  = [
    path("home/", views.showDemoPage, name="home" ),
    path('login/',views.login, name = "login"),
   path('signup/', views.signup, name="signup"),
]