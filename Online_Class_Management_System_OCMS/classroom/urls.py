from django.urls import path
from classroom import views

app_name = 'classroom'

urlpatterns =[
    path('signup/',views.SignUp,name="signup"),
    path('signup/student_signup/',views.StudentSignUp,name="StudentSignUp"),
    path('signup/teacher_signup/',views.TeacherSignUp,name="TeacherSignUp"),
    path('submit_assignment/<int:id>/',views.submit_assignment,name="submit_assignment"),
    path('submit_list/',views.submit_list,name="submit_list"),
    path('change_password/',views.change_password,name="change_password"),
    path('teacher/<int:pk>/',views.TeacherDetailView.as_view(),name="teacher_detail"),
    path('update/student/<int:pk>/',views.StudentUpdateView,name="student_update"),
    path('update/teacher/<int:pk>/',views.TeacherUpdateView,name="teacher_update"),
    path('student/<int:pk>/enter_marks',views.add_marks,name="enter_marks"),
    path('student/<int:pk>/marks_list',views.student_marks_list,name="student_marks_list"),
    path('marks/<int:pk>/update',views.update_marks,name="update_marks"),
    path('classTest_list/',views.classTest_list,name="classTest_list"),
    path('update_assignment/<int:id>/',views.update_assignment,name="update_assignment"),
    path('update_material/<int:id>/',views.update_material,name="update_material"),
    path('assignment_delete/<int:id>/',views.assignment_delete,name="assignment_delete"),
    path('material_delete/<int:id>/',views.material_delete,name="material_delete"),
    path('liveClass_delete/<int:id>/',views.liveClass_delete,name="liveClass_delete"),
    path('student/<int:pk>/add',views.add_student.as_view(),name="add_student"),
    path('students_list/',views.students_list,name="students_list"),
    path('teacher/write_notice',views.add_notice,name="write_notice"),
    path('student/<int:pk>/class_notice',views.class_notice,name="class_notice"),
    path('schedule_class/',views.schedule_class,name="schedule_class"),
    path('schedule_test/',views.schedule_test,name="schedule_test"),
    path('upload_assignment/',views.upload_assignment,name="upload_assignment"),
    path('upload_material/',views.upload_material,name="upload_material"),
    path('class_assignment/',views.class_assignment,name="class_assignment"),
    path('class_material/',views.class_material,name="class_material"),
    path('student_added/',views.student_added,name="student_added"),
    path('teachers_list/',views.teachers_list,name="teachers_list"),
    path('teacher/class_students_list',views.class_students_list,name="class_student_list"),
    path('student/<int:pk>/all_marks',views.StudentAllMarksList.as_view(),name="all_marks_list"),
    path('student/<int:pk>/message',views.write_message,name="write_message"),
    path('teacher/<int:pk>/messages_list',views.messages_list,name="messages_list"),
    path('class_liveClass/',views.class_liveClass,name="class_liveClass"),
    path('class_classTest/',views.class_classTest,name="class_classTest"),
    path('assignment_list/',views.assignment_list,name="assignment_list"),
    path('material_list/',views.material_list,name="material_list"),
    path('liveClass_list/',views.liveClass_list,name="liveClass_list"),
    path('classTest_delete/<int:id>/',views.classTest_delete,name="classTest_delete"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('student/<int:pk>/',views.StudentDetailView.as_view(),name="student_detail"),
]