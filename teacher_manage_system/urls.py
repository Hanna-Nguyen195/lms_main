from django.urls import path, include

from teacher_manage_system import views
urlpatterns  = [
    path('home_teacher/<int:id_teacher>', views.home_teacher, name = "home_teacher"),
    path('teacher_signup/', views.teacher_signup, name = "teacher_signup"),
    path('teacher_login/', views.teacher_login, name = "teacher_login"),
    path("add_course/", views.add_course, name="add_course" ),
    path('add_student/<int:id_teacher>/<int:id_course>/',views.add_student, name = "add_student"),
    # path('show_student/<int:id_teacher>/<int:id_course>/', views.show_student, name = "show_student"),
   
#     
]