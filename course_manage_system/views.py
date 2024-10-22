from multiprocessing import AuthenticationError
from pyexpat.errors import messages
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from student_manage_system import models
from django.core.files.storage import FileSystemStorage
# Create your views here.
# Function get a course by id
#  Course cua teacher and course cua student

#  ham show ra cac thong tin chi tiet khoa hoc cua teacher
def build_course(request, course_id):
    # Lấy khóa học với id tương ứng
    courses = get_object_or_404(models.Courses, id = course_id)
    teacher = courses.staff_id
    # students = []
    # for x in course_all:
    #     if x.id_student is not None:
    #         students.append(x)
    return render(request, "course_default.html",{'course':courses, 'teacher':teacher})


# def student_join_course(request, student_id, course_id,teacher_id):
#     join_all_course = models.JointCourse.objects.get(id_course = course_id, id_student = student_id, id_teacher = teacher_id)
#     if(join_all_course.exit() ):
#         course = join_all_course.id_course
#         student = join_all_course.id_student
#         teacher = join_all_course.id_teacher


def create_lession(request, id_course):
    if(request.method == "POST"):
        name_lession = request.POST['name_lession']
        #  content coi nhu la phan mo ta
        content = request.POST.get('content')
        course = models.Courses.objects.get(id = id_course)
        teacher = course.staff_id
        try:
            name = models.Lession.objects.all().values_list('lession_name', flat=True)
            cont = models.Lession.objects.all().values_list('content', flat=True)
            if( name_lession in name ):
                messages.error(request, "Lession already exists")
                return redirect('create_lession', id_course = id_course)
            lession = models.Lession(lession_name = name_lession, content = content, course_id = course)
            lession.save()
            lessions = models.Lession.objects.filter(course_id = course)
            return render(request, 'show_all_lession.html', {'lessions': lessions})
            # truyen vao teacher phai la 1 instance t
        except Exception as e:
            messages.error(request, "Failed to add lession: " + str(e))
            return render(request, 'show_error.html', {'messages': messages.get_messages(request)})
    return render(request, 'create_lession.html', {'id_course': id_course})


def create_resource(request, id_lession):
    if(request.method == "POST"):
            name = request.POST.get('name')  # Lấy dữ liệu từ input title
            content = request.FILES['content']  # Lấy file từ input file
            try:
                lession = models.Lession.objects.get(id = id_lession)
                
                lessionresource = models.LessionResource(lession_id = lession, resource_name = name, resource_content = content)
                name_resource = models.LessionResource.objects.all().values_list('resource_name', flat=True)
                #  Doan nay mai bo sung them in ra HTML la khoa hoc da ton tai
                if( name in name_resource ):
                    messages.error(request, "Resource already exists")
                    return redirect('create_resource', id_lession = id_lession)
                lessionresource.save()
                resources = models.LessionResource.objects.filter(lession_id = lession)
                return render(request, 'show_all_resource.html', {'resources': resources})

            except Exception as e:
                messages.error(request, "Failed to add resource: " + str(e))
                return render(request, 'show_error.html')
            
    return render(request, 'create_resource.html', {'id_lession': id_lession})



