from django.http import HttpResponse
from django.shortcuts import redirect, render
from student_manage_system import models
from django.contrib import messages
# Create your views here.
# Ham nop bai tap cua hoc sinh
def submit_assignment(request, id_assignment,id_student):
    if(request.method == "POST"):
        content = request.POST.get('content')
        assignment_file = request.FILES.get('assignment_file')
        try:
            if assignment_file or content:
                assignment = models.Assignment.objects.get(id = id_assignment)
                student = models.Students.objects.get(id = id_student)
                submit = models.SubmitAssignment(assignment_id = assignment, student_id = student, content = content, assignment_file = assignment_file)
                submit.save()
                messages.success(request, "Submit assignment successfully")
                return HttpResponse("Submit assignment successfully")
            else:
                message = messages.error(request, "Please fill in the form")
                return render(request, 'submit_assignment.html',{"id_assignment": id_assignment, "id_student": id_student, "messages": message})
        except Exception as e:
            messages.error(request, "Failed to submit assignment: " + str(e))
            return render(request, 'show_error.html', {'messages': messages.get_messages(request)})
    return render(request, 'submit_assignment.html',{"id_assignment": id_assignment, "id_student": id_student})



#  Ham teacher up assignment len
def create_assignment(request, id_course):
    if( request.method == "POST"):
        title = request.POST.get('title')
        description = request.POST.get('description')
        course = models.Courses.objects.get(id = id_course)
        try:
            name = models.Assignment.objects.all().values_list('title', flat=True)
            if( title in name ):
                messages.error(request, "Assignment already exists")
                return redirect('create_assignment', id_course = id_course)
            assignment = models.Assignment(course_id = course, title = title, description = description)
            assignment.save()
            assignments = models.Assignment.objects.filter(course_id = course)
            #  Sau nay co the doi cho nay thanh thong bao them khoa hoc thanh cong
            #  va tao 1 url show toan bo assignment
            return render(request, 'show_all_assignment.html', {'assignments': assignments})
        except Exception as e:
            messages.error(request, "Failed to add assignment: " + str(e))
            return render(request, 'show_error.html', {'messages': messages.get_messages(request)})
    return render(request, 'create_assignment.html', {'id_course': id_course})

def show_all_assignment(request, id_course):
    course = models.Courses.objects.get(id = id_course)
    assignments = models.Assignment.objects.filter(course_id = course)
    return render(request, 'show_all_assignment.html', {'assignments': assignments})

def teacher_delete_assignment(request, id_assignment):
    assignment = models.Assignment.objects.get(id = id_assignment)
    course = assignment.course_id
    assignment.delete()
    assignments = models.Assignment.objects.filter(course_id = course)
    return render(request, 'show_all_assignment.html', {'assignments': assignments})



def teacher_update_assignment(request, id_assignment):
    assignment = models.Assignment.objects.get(id = id_assignment)
    if(request.method == "POST"):
        title = request.POST.get('title')
        description = request.POST.get('description')
        try:
            assignment.title = title
            assignment.description = description
            assignment.save()
            # Sau do show tat ca assignment
            course = assignment.course_id
            assignments = models.Assignment.objects.filter(course_id = course)
            return render(request, 'show_all_assignment.html', {'assignments': assignments})
        except Exception as e:
            messages = messages.error(request,"Failed to update assignment: " + str(e))
            return render(request, 'show_error.html', {'messages': messages})
    return render(request, 'teacher_update_assignment.html', {'id_assignment': id_assignment})








