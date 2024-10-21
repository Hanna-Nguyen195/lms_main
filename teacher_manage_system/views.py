from multiprocessing import AuthenticationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from student_manage_system.models import Lession, Staffs, CustomerUser, Courses,JointCourse, Students

def home_teacher(request, id_teacher):
    teacher_inf = Staffs.objects.get(id = id_teacher)
    teacher = teacher_inf.admin
    joint = JointCourse.objects.filter(id_teacher = id_teacher)
    students = []
    courses = []
    if(joint.exists()):
        for join in joint:
            # Neu student none thi khong truy cap duoc admin  student.append(joint.id_student.admin)
            if join.id_student is not None:
                students.append(join.id_student)
        else:
            students.append(join.id_student)
            courses.append(join.id_course)
    return render(request, "home_teacher.html", {'teacher' : teacher, 'courses' :courses, 'students': students, 'teacher_id': id_teacher})

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
        gender = request.POST['gender']
        user = CustomerUser.objects.create_user(username=username, password=password,first_name = fist_name, last_name = last_name, email=email, gender = gender,user_type = 2 )
        return redirect('teacher_login')
    return render(request,'signup_teacher.html',{})


#  Them khoa hoc
def add_course(request, id_teacher):
    if request.method == "POST":
        name_course = request.POST['course_name']
        try:
            teacher = Staffs.objects.get(id=id_teacher)
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
    return render(request, "add_course.html" , {'id_teacher' : id_teacher})

def page_show_student(request, id_teacher, id_course):
    teacher = Staffs.objects.get(id = id_teacher)
    courses = Courses.objects.get(id = id_course, staff_id = teacher)
    joint=JointCourse.objects.filter(id_course = courses,id_teacher = teacher)
    students=[]
    for x in joint:
                students.append(x.id_student)
    return render(request, "show_student.html",{'students' : students})

def page_add_student(request, id_teacher):
    return render(request, 'add_student.html', {'id_teacher' : id_teacher}) 

def add_student(request, id_teacher):
    if(request.method == "POST"):
            fist_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            gender = request.POST['gender']
            id_course = request.POST['id_course']
            user = authenticate(request, username = username, password = password)
            if( authenticate(request, username = username, password = password) is None):
                user = CustomerUser.objects.create_user(username=username, password=password,first_name = fist_name, last_name = last_name, email=email,user_type = 3 )
                print(user)
            # student_pro = Students.objects.create(admin = user, gender = gender)
            teacher = Staffs.objects.get(id = id_teacher)
            courses = Courses.objects.get(id = id_course, staff_id = teacher)
            student1 = Students.objects.get(admin = user)
            join = JointCourse(id_course = courses, id_teacher = teacher, id_student = student1)
            join.save()
            joint=JointCourse.objects.filter(id_teacher = teacher, id_course = courses)
            students=[]
            for x in joint:
                students.append(x.id_student)
            messages.success(request, "Add Student successfully")
            return redirect('page_show_student', id_teacher = id_teacher, id_course = id_course)
    #  neu khong vao ham if thi no se hien ra trang de add_studetnt
    # kieu nhu neu khong xay dung 1 ham rieng thi phai lam nhu nay de nó hien trang
    
    return render(request,'add_student.html', {'id_teacher' : id_teacher})

def teacher_add_student_into_course(request, id_course):
    if(request.method == "POST"):
        fist_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST

#  Loc ra cac hoc sinh trong khoa hoc cua 1 giao vien
# def show_student(request, course_id, teacher_id):
#     #  Loc ra cai khoa hoc da 
#     join_all = JointCourse.objects.get(id_course = course_id, id_teacher = teacher_id)
#     students = join_all.id_student
#     teachers = join_all.id_teacher
#     courses = join_all.id_course
#     return render(request, "show_student.html",{'students':students,'teachers' :teachers, "courses":courses})

# Ham cham diem cho hoc sinh
def mark_assignment(request, id_teacher):
    pass


#  Ham hien thi diem cua tat ca hoc sinh trong 1 khoa hoc cua 1 bai ktra or 1 bai tap
def show_all_grade_assignment(request, id_teacher):
    pass    

# Xep hang diem bai ktra cho sinh vien
def rank_grade_assignment(request, id_teacher):
    pass    

def rank_test(request, id_teacher):
    pass    



# Cham diem va luu vao bang submission


# Them lession and li thuyet, bai tập, kiểm tra, điểm danh = Tạo bài học, tạo bài tập
def teacher_add_lession(request, id_teacher, id_course):
    if(request.method == "POST"):
        name_lession = request.POST['name_lession']
        #  content coi nhu la phan mo ta
        content = request.POST.get('content')
        try:
            lession = Lession(lession_name = name_lession, content = content, course_id = id_course)
            lession.save()
            
            # truyen vao teacher phai la 1 instance t
        except Exception as e:
            messages.error(request, "Failed to add lession: " + str(e))
    






