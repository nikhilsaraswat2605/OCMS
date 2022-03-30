from django.urls import reverse
import misaka
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='Student')
    phone = models.IntegerField()
    student_profile_pic = models.ImageField(
        upload_to="classroom/student_profile_pic", blank=True)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    roll_no = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('classroom:student_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no']


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='Teacher')
    teacher_profile_pic = models.ImageField(
        upload_to="classroom/teacher_profile_pic", blank=True)
    subject_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=250)
    class_students = models.ManyToManyField(Student, through="StudentsInClass")
    phone = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('classroom:teacher_detail', kwargs={'pk': self.pk})


class StudentMarks(models.Model):
    teacher = models.ForeignKey(
        Teacher, related_name='given_marks', on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    subject_name = models.CharField(max_length=250)
    maximum_marks = models.IntegerField()
    student = models.ForeignKey(
        Student, related_name="marks", on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name


class StudentsInClass(models.Model):
    student = models.ForeignKey(
        Student, related_name="user_student_name", on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher, related_name="class_teacher", on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name

    class Meta:
        unique_together = ('teacher', 'student')


class MessageToTeacher(models.Model):
    student = models.ForeignKey(
        Student, related_name='student', on_delete=models.CASCADE)
    message_html = models.TextField(editable=False)
    created_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(
        Teacher, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'message']


class ClassNotice(models.Model):
    teacher = models.ForeignKey(
        Teacher, related_name='teacher', on_delete=models.CASCADE)
    message_html = models.TextField(editable=False)
    created_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(Student, related_name='class_notice')
    message = models.TextField()

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message

    class Meta:
        unique_together = ['teacher', 'message']
        ordering = ['-created_at']


class ClassAssignment(models.Model):
    student = models.ManyToManyField(
        Student, related_name='student_assignment')
    Deadline = models.DateTimeField(auto_now=False, null=True)
    PublishedAt = models.DateTimeField(auto_now=False, null=True)
    assignment = models.FileField(upload_to='assignments')
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    teacher = models.ForeignKey(
        Teacher, related_name='teacher_assignment', on_delete=models.CASCADE)

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']


class ClassMaterial(models.Model):
    student = models.ManyToManyField(Student, related_name='student_material')
    material = models.FileField(upload_to='materials')
    material_name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(
        Teacher, related_name='teacher_material', on_delete=models.CASCADE)

    def __str__(self):
        return self.material_name

    class Meta:
        ordering = ['-created_at']


class LiveClass(models.Model):
    student = models.ManyToManyField(Student, related_name='student_liveClass')
    teacher = models.ForeignKey(
        Teacher, related_name='teacher_liveClass', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now=True)
    StartTime = models.DateTimeField(auto_now=False, null=True)
    Classlink = models.CharField(max_length=250)
    EndTime = models.DateTimeField(auto_now=False, null=True)
    ClassName = models.CharField(max_length=250)

    def __str__(self):
        return self.ClassName

    class Meta:
        ordering = ['-created_at']


class ClassTest(models.Model):
    student = models.ManyToManyField(Student, related_name='student_ClassTest')
    teacher = models.ForeignKey(
        Teacher, related_name='teacher_ClassTest', on_delete=models.CASCADE, default=None)
    Testlink = models.CharField(max_length=250)
    TestName = models.CharField(max_length=250)
    StartTime = models.DateTimeField(auto_now=False, null=True)
    EndTime = models.DateTimeField(auto_now=False, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.TestName

    class Meta:
        ordering = ['-created_at']


class SubmitAssignment(models.Model):
    student = models.ForeignKey(
        Student, related_name='student_submit', on_delete=models.CASCADE)
    submit = models.FileField(upload_to='Submission')
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(
        ClassAssignment, related_name='submission_for_assignment', on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher, related_name='teacher_submit', on_delete=models.CASCADE)

    def __str__(self):
        return f"Submitted{str(self.submitted_assignment.assignment_name)}"

    class Meta:
        ordering = ['-created_at']
