from multiprocessing import AuthenticationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from student_manage_system import models
# Create your views here.
# Function get a course by id
#  Course cua teacher and course cua student

#  ham show ra cac thong tin chi tiet khoa hoc cua teacher
def build_course(request, course_id, teacher_id):
    # Lấy khóa học với id tương ứng
    course_all = models.JointCourse.objects.filter(id_course = course_id, id_teacher = teacher_id)
    course = course_all.first().id_course
    teacher = course_all.first().id_teacher
    students = []
    for x in course_all:
        if x.id_student is not None:
            students.append(x)
    return render(request, "course_default.html",{'course':course, 'teacher':teacher, "students":students})


def student_join_course(request, student_id, course_id,teacher_id):
    join_all_course = models.JointCourse.objects.get(id_course = course_id, id_student = student_id, id_teacher = teacher_id)
    if(join_all_course.exit() ):
        course = join_all_course.id_course
        student = join_all_course.id_student
        teacher = join_all_course.id_teacher



