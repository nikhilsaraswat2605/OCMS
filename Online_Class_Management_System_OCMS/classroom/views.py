import datetime
from time import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import (DetailView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
from classroom.forms import UserForm, TeacherProfileForm, StudentProfileForm, MarksForm, MessageForm, NoticeForm, AssignmentForm, SubmitForm, TeacherProfileUpdateForm, StudentProfileUpdateForm, LiveClassForm, ClassTestForm, MaterialForm
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from classroom import models
from classroom.models import StudentsInClass, StudentMarks, ClassAssignment, SubmitAssignment, Student, Teacher, LiveClass, ClassTest, ClassMaterial
from django.contrib.auth.forms import PasswordChangeForm
from . import liveclass


# TODO Rename this here and in `TeacherSignUp`
def _extracted_from_TeacherSignUp_11(user_form, teacher_profile_form):
    user = user_form.save()
    user.is_teacher = True
    user.save()

    profile = teacher_profile_form.save(commit=False)
    profile.user = user
    profile.save()

    return True


# For Teacher Sign Up
def TeacherSignUp(request):
    user_type = 'teacher'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        teacher_profile_form = TeacherProfileForm(data=request.POST)

        if user_form.is_valid() and teacher_profile_form.is_valid():

            registered = _extracted_from_TeacherSignUp_11(
                user_form, teacher_profile_form)
        else:
            # messages.error(request, user_form.errors, teacher_profile_form.errors)
            print(user_form.errors, teacher_profile_form.errors)
    else:
        user_form = UserForm()
        teacher_profile_form = TeacherProfileForm()
    context = {'user_form': user_form, 'teacher_profile_form': teacher_profile_form,
               'registered': registered, 'user_type': user_type}
    template = "classroom/teacher_signup.html"
    return render(request, template, context)


# TODO Rename this here and in `StudentSignUp`
def _extracted_from_StudentSignUp_11(user_form, student_profile_form):
    user = user_form.save()
    user.is_student = True
    user.save()

    profile = student_profile_form.save(commit=False)
    profile.user = user
    profile.save()

    return True


# For Student Sign Up
def StudentSignUp(request):
    user_type = 'student'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        student_profile_form = StudentProfileForm(data=request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():

            registered = _extracted_from_StudentSignUp_11(
                user_form, student_profile_form)
        else:
            print(user_form.errors, student_profile_form.errors)
    else:
        user_form = UserForm()
        student_profile_form = StudentProfileForm()
    template = "classroom/student_signup.html"
    context = {'user_form': user_form, 'student_profile_form': student_profile_form,
               'registered': registered, 'user_type': user_type}
    return render(request, template, context)


# Sign Up page which will ask whether you are teacher or student.
def SignUp(request):
    return render(request, 'classroom/signup.html', {})


# logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


# login view.
def user_login(request):
    if request.method != "POST":
        return render(request, 'classroom/login.html', {})
    username = request.POST.get('username')
    password = request.POST.get('password')

    if user := authenticate(username=username, password=password):
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

        else:
            return HttpResponse("Account not active")

    else:
        messages.error(request, "Invalid Details")
        return redirect('classroom:login')


# User Profile of student.
class StudentDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "student"
    model = models.Student
    template_name = 'classroom/student_detail_page.html'


# User Profile for teacher.
class TeacherDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "teacher"
    model = models.Teacher
    template_name = 'classroom/teacher_detail_page.html'


# Profile update for students.
@login_required
def StudentUpdateView(request, pk):
    profile_updated = False
    student = get_object_or_404(models.Student, pk=pk)
    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST, instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'student_profile_pic' in request.FILES:
                profile.student_profile_pic = request.FILES['student_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = StudentProfileUpdateForm(request.POST or None, instance=student)
    template = "classroom/student_update_page.html"
    context = {'profile_updated': profile_updated, 'form': form}
    return render(request, template, context)


# Profile update for teachers.
@login_required
def TeacherUpdateView(request, pk):
    profile_updated = False
    teacher = get_object_or_404(models.Teacher, pk=pk)
    if request.method == "POST":
        form = TeacherProfileUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'teacher_profile_pic' in request.FILES:
                profile.teacher_profile_pic = request.FILES['teacher_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = TeacherProfileUpdateForm(request.POST or None, instance=teacher)
    template = "classroom/teacher_update_page.html"
    context = {'profile_updated': profile_updated, 'form': form}
    return render(request, template, context)


# List of all students that teacher has added in their class.
def class_students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
            Q(name__icontains=query)
        )
    qs_one = [x for x in qs if x in students_list]
    return render(request, "classroom/class_students_list.html", {
        "class_students_list": qs_one,
    })


class ClassStudentsListView(LoginRequiredMixin, DetailView):
    model = models.Teacher
    template_name = "classroom/class_students_list.html"
    context_object_name = "teacher"


# For Marks obtained by the student in all subjects.
class StudentAllMarksList(LoginRequiredMixin, DetailView):
    model = models.Student
    template_name = "classroom/student_allmarks_list.html"
    context_object_name = "student"


# To give marks to a student.
@login_required
def add_marks(request, pk):
    marks_given = False
    student = get_object_or_404(models.Student, pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.teacher = request.user.Teacher
            marks.save()
            messages.success(request, 'Marks uploaded successfully!')
            return redirect('classroom:submit_list')
    else:
        form = MarksForm()
    template = "classroom/add_marks.html"
    context = {'form': form, 'student': student, 'marks_given': marks_given}
    return render(request, template, context)


# For updating marks.
@login_required
def update_marks(request, pk):
    marks_updated = False
    obj = get_object_or_404(StudentMarks, pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST, instance=obj)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.save()
            marks_updated = True
    else:
        form = MarksForm(request.POST or None, instance=obj)
    template = "classroom/update_marks.html"
    context = {'form': form, 'marks_updated': marks_updated}
    return render(request, template, context)


# For writing notice which will be sent to all class students.
@login_required
def add_notice(request):  # sourcery skip: avoid-builtin-shadow
    template = "classroom/write_notice.html"
    notice_sent = False
    teacher = request.user.Teacher
    students = StudentsInClass.objects.filter(teacher=teacher)
    students_list = [x.student for x in students]

    if request.method != "POST":
        notice = NoticeForm()
    else:
        notice = NoticeForm(request.POST)
        if notice.is_valid():
            object = notice.save(commit=False)
            object.teacher = teacher
            object.save()
            object.students.add(*students_list)
            notice_sent = True
    context = {'notice': notice, 'notice_sent': notice_sent}
    return render(request, template, context)


# For student writing message to teacher.
@login_required
def write_message(request, pk):
    message_sent = False
    teacher = get_object_or_404(models.Teacher, pk=pk)

    if request.method != "POST":
        form = MessageForm()
    else:
        form = MessageForm(request.POST)
        if form.is_valid():
            mssg = form.save(commit=False)
            mssg.teacher = teacher
            mssg.student = request.user.Student
            mssg.save()
            message_sent = True

    context = {'form': form, 'teacher': teacher, 'message_sent': message_sent}
    template = "classroom/write_message.html"
    return render(request, template, context)


# For the list of all the messages teacher have received.
@login_required
def messages_list(request, pk):
    teacher = get_object_or_404(models.Teacher, pk=pk)
    template = "classroom/messages_list.html"
    context = {'teacher': teacher}
    return render(request, template, context)


# Student can see all notice given by their teacher.
@login_required
def class_notice(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    template = "classroom/class_notice_list.html"
    context = {'student': student}
    return render(request, template, context)


# To see the list of all the marks given by the techer to a specific student.
@login_required
def student_marks_list(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    teacher = request.user.Teacher
    given_marks = StudentMarks.objects.filter(teacher=teacher, student=student)
    template = "classroom/student_marks_list.html"
    context = {'student': student, 'given_marks': given_marks}
    return render(request, template, context)


# To add student in the class.
class add_student(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('classroom:students_list')

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(models.Student, pk=self.kwargs.get('pk'))

        try:
            StudentsInClass.objects.create(
                teacher=self.request.user.Teacher, student=student)
        except:
            messages.warning(
                self.request, 'warning, Student already in class!')
        else:
            messages.success(
                self.request, f'{student.name} successfully added!')

        return super().get(request, *args, **kwargs)


@login_required
def student_added(request):
    context = {}
    template = "classroom/student_added.html"
    return render(request, template, context)


# List of students which are not added by teacher in their class.
def students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
            Q(name__icontains=query)
        )
    qs_one = [x for x in qs if x not in students_list]

    return render(request, "classroom/students_list.html",  {
        "students_list": qs_one,
    })


# List of all the teacher present in the portal.
def teachers_list(request):
    query = request.GET.get("q", None)
    qs = Teacher.objects.all()
    if query is not None:
        qs = qs.filter(
            Q(name__icontains=query)
        )

    return render(request, "classroom/teachers_list.html", {
        "teachers_list": qs,
    })


####################################################

# Teacher uploading assignment.
@login_required
def upload_assignment(request):
    template = "classroom/upload_assignment.html"
    teacher = request.user.Teacher
    assignment_uploaded = False
    students = Student.objects.filter(
        user_student_name__teacher=request.user.Teacher)
    if request.method != 'POST':
        form = AssignmentForm()
    else:
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            students = Student.objects.filter(
                user_student_name__teacher=request.user.Teacher)
            upload.save()
            upload.student.add(*students)
            assignment_uploaded = True
    return render(request, template, {'form': form, 'assignment_uploaded': assignment_uploaded})


# Teacher uploading assignment.
@login_required
def upload_material(request):
    template = "classroom/upload_material.html"
    teacher = request.user.Teacher
    material_uploaded = False
    students = Student.objects.filter(
        user_student_name__teacher=request.user.Teacher)
    if request.method != 'POST':
        form = MaterialForm()
    else:
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            students = Student.objects.filter(
                user_student_name__teacher=request.user.Teacher)
            upload.save()
            upload.student.add(*students)
            material_uploaded = True
    return render(request, template, {'form': form, 'material_uploaded': material_uploaded})


# Teacher live class.
@login_required
def schedule_class(request):
    template = "classroom/live_class.html"
    teacher = request.user.Teacher
    class_scheduled = False
    students = Student.objects.filter(
        user_student_name__teacher=request.user.Teacher)
    if request.method != 'POST':
        form = LiveClassForm()
    else:
        form = LiveClassForm(request.POST, request.FILES)
        if form.is_valid():
            print(form['ClassName'].value())
            upload = form.save(commit=False)
            upload.Classlink = liveclass.createMeeting(
                meetingName=form['ClassName'].value(), Email=teacher.email)
            upload.teacher = teacher
            students = Student.objects.filter(
                user_student_name__teacher=request.user.Teacher)
            upload.save()
            upload.student.add(*students)
            class_scheduled = True

    return render(request, template, {'form': form, 'class_scheduled': class_scheduled})


# Teacher live class.
@login_required
def schedule_test(request):
    template = "classroom/class_test.html"
    teacher = request.user.Teacher
    test_scheduled = False
    students = Student.objects.filter(
        user_student_name__teacher=request.user.Teacher)
    if request.method != 'POST':
        form = ClassTestForm()
    else:
        form = ClassTestForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            students = Student.objects.filter(
                user_student_name__teacher=request.user.Teacher)
            upload.save()
            upload.student.add(*students)
            test_scheduled = True
    return render(request, template, {'form': form, 'test_scheduled': test_scheduled})

# Students getting the list of all the assignments uploaded by their teacher.


@login_required
def class_assignment(request):
    template = "classroom/class_assignment.html"
    currentDateTime = datetime.datetime.now()
    student = request.user.Student
    assignments = SubmitAssignment.objects.filter(student=student)
    assignment_list = [x.submitted_assignment for x in assignments]
    return render(request, template, {'student': student, 'assignment_list': assignment_list, 'currentDateTime': currentDateTime})

# Students getting the list of all the assignments uploaded by their teacher.


@login_required
def class_material(request):
    template = "classroom/class_material.html"
    currentDateTime = datetime.datetime.now()
    student = request.user.Student
    return render(request, template, {'student': student, 'currentDateTime': currentDateTime})

# Students getting the list of all the assignments uploaded by their teacher.


@login_required
def class_liveClass(request):
    currentDateTime = datetime.datetime.now()
    template = "classroom/class_liveClass.html"
    student = request.user.Student
    return render(request, template, {'student': student, 'currentDateTime': currentDateTime})


# Students getting the list of all the assignments uploaded by their teacher.
@login_required
def class_classTest(request):
    template = "classroom/class_classTest.html"
    currentDateTime = datetime.datetime.now()
    student = request.user.Student
    return render(request, template, {'student': student, 'currentDateTime': currentDateTime})

# List of all the assignments uploaded by the teacher himself.


@login_required
def assignment_list(request):
    template = "classroom/assignment_list.html"
    teacher = request.user.Teacher
    return render(request, template, {'teacher': teacher})

# List of all the assignments uploaded by the teacher himself.


@login_required
def material_list(request):
    template = "classroom/material_list.html"
    teacher = request.user.Teacher
    return render(request, template, {'teacher': teacher})


# List of all the assignments uploaded by the teacher himself.
@login_required
def liveClass_list(request):
    template = "classroom/liveClass_list.html"
    teacher = request.user.Teacher
    return render(request, template, {'teacher': teacher})


# List of all the assignments uploaded by the teacher himself.
@login_required
def classTest_list(request):
    template = "classroom/classTest_list.html"
    teacher = request.user.Teacher
    return render(request, template, {'teacher': teacher})


# For updating the assignments later.
@login_required
def update_assignment(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    form = AssignmentForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'assignment' in request.FILES:
            obj.assignment = request.FILES['assignment']
        obj.save()
        messages.success(
            request, "Updated Assignment".format(obj.assignment_name))
        return redirect('classroom:assignment_list')
    return render(request, "classroom/update_assignment.html", context)


# For updating the materials later.
@login_required
def update_material(request, id=None):
    obj = get_object_or_404(ClassMaterial, id=id)
    form = MaterialForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'material' in request.FILES:
            obj.material = request.FILES['material']
        obj.save()
        messages.success(
            request, "Updated Study Material/ Lectures".format(obj.material_name))
        return redirect('classroom:material_list')
    return render(request, "classroom/update_material.html", context)


# For deleting the assignment.
@login_required
def assignment_delete(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Assignment Removed")
        return redirect('classroom:assignment_list')
    context = {
        "object": obj,
    }
    return render(request, "classroom/assignment_delete.html", context)


# For deleting the material.
@login_required
def material_delete(request, id=None):
    obj = get_object_or_404(ClassMaterial, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Study Material/ Lectures Removed")
        return redirect('classroom:material_list')
    context = {
        "object": obj,
    }
    return render(request, "classroom/material_delete.html", context)


# For deleting the class test.
@login_required
def classTest_delete(request, id=None):
    obj = get_object_or_404(ClassTest, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Test deleted successfully")
        return redirect('classroom:classTest_list')

    context = {
        "object": obj,
    }
    return render(request, "classroom/classTest_delete.html", context)

# For deleting the live class.


@login_required
def liveClass_delete(request, id=None):
    obj = get_object_or_404(LiveClass, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Class deleted successfully")
        return redirect('classroom:liveClass_list')

    context = {
        "object": obj,
    }
    return render(request, "classroom/liveClass_delete.html", context)


# For students submitting their assignment.
@login_required
def submit_assignment(request, id=None):
    DeadlineExceeded = False
    assignment = get_object_or_404(ClassAssignment, id=id)
    teacher = assignment.teacher
    student = request.user.Student
    CurrentDate = str(datetime.datetime.now())
    ExpectedDate = str(assignment.Deadline)
    if ExpectedDate < CurrentDate:
        DeadlineExceeded = True
        return render(request, 'classroom/submit_assignment.html', {'DeadlineExceeded': DeadlineExceeded})
    if request.method != 'POST':
        form = SubmitForm()
    else:
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.student = student
            upload.submitted_assignment = assignment
            upload.save()
            return redirect('classroom:class_assignment')
    return render(request, 'classroom/submit_assignment.html', {'form': form, 'DeadlineExceeded': DeadlineExceeded})


# To see all the submissions done by the students.
@login_required
def submit_list(request):
    teacher = request.user.Teacher
    return render(request, 'classroom/submit_list.html', {'teacher': teacher})

##################################################################################################

# For changing password.


@login_required
def change_password(request):
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'classroom/change_password.html', args)
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if not form.is_valid():
            return redirect('classroom:change_password')
        form.save()
        messages.success(request, "Password changed")
        update_session_auth_hash(request, form.user)
        return redirect('home')
