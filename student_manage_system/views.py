from multiprocessing import AuthenticationError
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .models import CustomerUser

# Create your views here.
def showDemoPage(request):
    return render(request, "home.html" )

def showLogin(request):
    return render(request, "login_page.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            return redirect('home')
        else:
            messages.success(request, ('There was an login'))
            return redirect('login')
    return render(request, 'login.html',{})
def signup(request):
    if(request.method == "POST"):
        fist_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        gender = request.POST['gender']
        user = CustomerUser.objects.create_user(username=username, password=password,first_name = fist_name, last_name = last_name, email=email, gender = gender,user_type = 3 )
        return redirect('login')
    return render(request,'signup.html',{})

#  ham tự động thêm sinh viên vào khóa học
def page_student_join_course(request, id_student):
    return render(request, 'student_join_course.html', {'id_student': id_student})
def student_find_course(request, id_student):
    if request.method == "POST":
        id_course = request.POST['course_id']   
        id_teacher = request.POST['teacher_id']
        teacher = Staffs.objects.get(id = id_teacher)
        courses = Courses.objects.get(id = id_course, staff_id = teacher)
        student = Students.objects.get(id = id_student)
        join = JointCourse.objects.filter(id_teacher = teacher, id_course = courses)
        if join:
            join = JointCourse(id_teacher = teacher, id_course = courses, id_student = student)
            join.save()
            messages.success(request, ('You have already joined this course'))
            # Can chinh sua lai de nó chuyen den trang chu cua khoa hoc
            return redirect('build_course', course_id = id_course, teacher_id = id_teacher)
        return render(request, 'student_join_course.html', {'id_student': id_student})
    


# def student_join_course(request, id_teacher, id_course):
#     join = JointCourse.objects.filter(id_teacher = id_teacher, id_course = id_course)


#  Trang show ra cac khoa học mà học sinh đã tham gia
def show_course_student(request, id_student):
    join = JointCourse.objects.filter(id_student = id_student)
    #  Do trong khoa hoc co luu giao vien roi, nen chi can loc ra cac khoa hoc ma sinh vien da tham gia
    context = []

    for x in join:
        course = x.id_course
        teacher1 = course.staff_id
        teacher = Staffs.objects.get(id=teacher1.id)
        
        # Sử dụng dictionary để lưu trữ từng cặp course và teacher
        context.append({
            'course': course,
            'teacher': teacher
        })
    return render(request, 'show_course_student.html', {'context': context, 'id_student': id_student})


def submit_homework(request, id_student):
    pass

def show_all_homework_submited(request, id_student):
    pass    

def submit_test(request, id_student):
    pass    

def show_grades_test(request, id_student):
    pass    

def show_all_grades_homework(request, id_student):
    pass

def show_all_grades_test(request, id_student):
    pass

# truy cap nội dung bài học, truy nhập lesson, bài tập, lí thuyết, điểm danh,, nộp bài tập


