from multiprocessing import AuthenticationError
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from student_manage_system.models import Staffs, CustomerUser, Courses,JointCourse, Students

def home_teacher(request, id_teacher):
    teacher_inf = Staffs.objects.get(id = id_teacher)
    teacher = teacher_inf.admin
    courses = Courses.objects.filter(staff_id = id_teacher)
    return render(request, "home_teacher.html", {'teacher' : teacher, 'courses' :courses})

# Create your views here.
def teacher_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        staff = Staffs.objects.get(admin = user )
        
        if user is not None:
            return redirect("home_teacher",id_teacher = staff.id)
        else:
            messages.success(request, ('There was an login'))
            return redirect('teacher_login')
    return render(request,'login_teacher.html')


def teacher_signup( request):
    if(request.method == "POST"):
        fist_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = CustomerUser.objects.create_user(username=username, password=password,user_type = 2 )
        return redirect('teacher_login')
    return render(request,'signup_teacher.html',{})

# def add_course(request):
#     if(request.method == "POST"):
#         name_course = request.POST['course_name']
#         staff = request.user.staff_id
#         try:
#             course = Courses(course_name = name_course, staff_id = staff)
#             course.save()
#             return redirect('home')
#         except:
#             messages.error(request, "Faild to Add course")
#             return redirect('home')
#     return redirect('add_course')



def add_course(request):
    if request.method == "POST":
        name_course = request.POST['course_name']
        staff_id = request.POST['staff_id']
        try:
            teacher = Staffs.objects.get(id=staff_id)
            # truyen vao teacher phai la 1 instance tuc la 1 nguoi
            course = Courses(course_name=name_course,staff_id = teacher)
            if Courses.objects.filter(course_name=name_course, staff_id=teacher).exists():
                messages.error(request, 'Khóa học đã tồn tại.')
                print(messages)
                # redirect('add_course')
            else: 
                course1 = JointCourse(id_course = course, id_teacher = teacher)
                course.save()
                course1.save()
                messages.success(request, "Course added successfully!")
                courses = Courses.objects.filter(staff_id = teacher)
                return render(request, "show_all_course.html", {"courses" : courses, "teacher": teacher})  # Chuyển hướng về trang chủ khi thành công
        except Exception as e:
            messages.error(request, "Failed to add course: " + str(e))  # Thêm thông báo lỗi
            return render(request, 'show_error.html', {'messages': messages.get_messages(request)})  # Render lại trang với thông báo
    
    # Hiển thị trang thêm khóa học (nếu là GET request)
    return render(request, "add_course.html")



def add_student(request, id_teacher, id_course):
    if(request.method == "POST"):
            fist_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            gender = request.POST['gender']
            user = CustomerUser.objects.create_user(username=username, password=password,user_type = 3 )
            students = Students.objects.get(admin = user)
            join = JointCourse(id_course = id_course, id_teacher = id_teacher, id_student = students.id)
            join.save()
            messages.success(request, "Add Student successfully")
            return render(request, "show_student.html", { "messages":messages, "students" :students})
    #  neu khong vao ham if thi no se hien ra trang de add_studetnt
    # kieu nhu neu khong xay dung 1 ham rieng thi phai lam nhu nay de nó hien trang
    return render(request, "add_student.html")
#  Loc ra cac hoc sinh trong khoa hoc cua 1 giao vien
# def show_student(request, course_id, teacher_id):
#     #  Loc ra cai khoa hoc da 
#     join_all = JointCourse.objects.get(id_course = course_id, id_teacher = teacher_id)
#     students = join_all.id_student
#     teachers = join_all.id_teacher
#     courses = join_all.id_course
#     return render(request, "show_student.html",{'students':students,'teachers' :teachers, "courses":courses})



        




