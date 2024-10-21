from django.urls import path, include

from student_manage_system import views
urlpatterns  = [
    path("home/", views.showDemoPage, name="home" ),
    path('login/',views.login, name = "login"),
    path('signup/', views.signup, name="signup"),
    path('student_find_course/<int:id_student>/', views.student_find_course, name = "student_find_course"),
    path('page_student_join_course/<int:id_student>/', views.page_student_join_course, name = "page_student_join_course"),
    path('show_course_student/<int:id_student>/', views.show_course_student, name = "show_course_student"),
]