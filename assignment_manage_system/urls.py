from django.urls import path, include

from assignment_manage_system import views

urlpatterns = [
    path('submit_assignment/<int:id_assignment>/<int:id_student>/', views.submit_assignment, name="submit_assignment"),
    path('create_assignment/<int:id_course>/', views.create_assignment, name="create_assignment"),
    path('show_all_assignment/<int:id_course>/', views.show_all_assignment, name="show_all_assignment"),
    path('teacher_delete_assignment/<int:id_assignment>/', views.teacher_delete_assignment, name="teacher_delete_assignment"),
    path('teacher_update_assignment/<int:id_assignment>/', views.teacher_update_assignment, name="teacher_update_assignment"),
    
]