from django.urls import path, include

from course_manage_system import views
urlpatterns  = [
#     path("home/", views.showDemoPage, name="home" ),
#     path('login/',views.login, name = "login"),
#    path('signup/', views.signup, name="signup"),
    path('build_course/<int:course_id>/', views.build_course, name="build_course"),
    path('create_lession/<int:id_course>/', views.create_lession, name="create_lession"),
    path('create_resource/<int:id_lession>/', views.create_resource, name="create_resource"),
    path('update_lession/<int:id_lession>/', views.update_lession, name="update_lession"),  
    path('update_resource/<int:id_resource>/', views.update_resource, name="update_resource"),  
    path('delete_lession/<int:id_lession>/', views.delete_lession, name="delete_lession"),
    path('delete_resource/<int:id_resource>/', views.delete_resource, name="delete_resource"),
    path('show_all_lession/<int:id_course>/', views.show_all_lession, name="show_all_lession"), 
]