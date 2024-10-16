from multiprocessing import AuthenticationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from student_manage_system import models
# Create your views here.
# Function get a course by id
#  Course cua teacher and course cua student

#  ham show ra cac khoa hoc cua teacher
def build_course(request, course_id, teacher_id):
    # Lấy khóa học với id tương ứng
    course_all = models.JointCourse.objects.get(id_course = course_id, id_teacher = teacher_id)
    course = course_all.id_course
    teacher_inf = course_all.id_teacher
    teacher = teacher_inf.admin
    students_inf = course_all.id_student
    students = students_inf.admin
    return render(request, "course_default.html",{'course':course, 'teacher':teacher, "students":students})


def student_join_course(request, student_id, course_id,teacher_id):
    join_all_course = models.JointCourse.objects.get(id_course = course_id, id_student = student_id, id_teacher = teacher_id)
    if(join_all_course.exit() ):
        course = join_all_course.id_course
        student = join_all_course.id_student
        teacher = join_all_course.id_teacher



