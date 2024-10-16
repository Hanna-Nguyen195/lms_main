from django.urls import path, include

from course_manage_system import views
urlpatterns  = [
#     path("home/", views.showDemoPage, name="home" ),
#     path('login/',views.login, name = "login"),
#    path('signup/', views.signup, name="signup"),
    path('build_course/<int:course_id>/<int:teacher_id>/', views.build_course, name="build_course"),

]