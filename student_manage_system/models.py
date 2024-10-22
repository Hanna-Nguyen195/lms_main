from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
# model customeruser này dùng để quản lí đăng nhập, đki người dùng thay thế cho auth.user 
# model này có sẵn username passwword, email,... nhưng chưa có phone, address
class CustomerUser(AbstractUser):
    user_type_date = (( 1, "HOD"), (2, "Staff"),(3, "Student"))
    gender = models.CharField(max_length=255)
    user_type = models.CharField(default=1, choices=user_type_date, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    # mối quan hệ 1 1: 1 student lien kết với 1 bản ghi duy nhất trong bảng customeruser
    # 1 học sinh có 1 bản customeruser duy nhat
    admin = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)
    creater_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)
    # address = models.TextField()
    creater_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Courses( models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    course_name = models.CharField(max_length= 255)
    creater_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    creater_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)
    creater_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Enrollment(models.Model): 
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default="Register")
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    creater_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class JointCourse(models.Model):
    id_course = models.ForeignKey(Courses, on_delete= models.CASCADE)
    id_student = models.ForeignKey(Students, on_delete= models.CASCADE, null=True, blank=True)
    id_teacher = models.ForeignKey(Staffs, on_delete= models.CASCADE)
    objects = models.Manager()

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class SubmitAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    assignment_file = models.FileField(null=True, blank=True,upload_to='uploads/')
    marks = models.IntegerField(default=0)
    content = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Lession(models.Model):    
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    lession_name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    creater_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()



class LessionResource(models.Model):
    id = models.AutoField(primary_key=True)
    lession_id = models.ForeignKey(Lession, on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=255)
    resource_content = models.FileField(upload_to='uploads/')
    creater_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    creater_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class ExamAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_id = models.IntegerField()
    answer = models.CharField(max_length=255)
    objects = models.Manager()


@receiver( post_save, sender = CustomerUser)
def create_user_profile(sender, instance, created, **kwargs):
    if( created):
        if(instance.user_type == 1):
            AdminHOD.objects.create(admin = instance)
        if( instance.user_type == 2):
            Staffs.objects.create(admin = instance)
        if(instance.user_type ==3):
            Students.objects.create(admin = instance)
@receiver(post_save, sender = CustomerUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()













