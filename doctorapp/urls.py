from django.urls import path
from doctorapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('patient_register',views.patient_register,name='patient_register'),
    path('doctor_register',views.doctor_register,name='doctor_register'),
    path('logins',views.logins,name='logins'),
    path('patienthome',views.patienthome,name='patienthome'),
   
    path('adminhome',views.adminhome,name='adminhome'),
    path('patient_profile',views.patient_profile,name='patient_profile'),
    path('update_patient',views.update_patient,name='update_patient'),
    path('update_patients/<int:uid>',views.update_patients,name='update_patients'),
    path('book_appointment/<int:doctor_id>',views.book_appointment,name='book_appointment'),
    path('view_appointments',views.view_appointments,name='view_appointments'),
    #doctor
     path('doctorhome',views.doctorhome,name='doctorhome'),
    path('doctorprofile',views.doctorprofile,name='doctorprofile'),
    # path('doctor_view_profile',views.doctor_view_profile,name='doctor_view_profile'),
    path('doc_view_appointments',views.doc_view_appointments,name='doc_view_appointments'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('update_doctor',views.update_doctor,name='update_doctor'),
    path('updated_doctor/<int:uid>',views.updated_doctor,name='updated_doctor'),
    path('view_doctors',views.view_doctors,name='view_doctors'),
    path('view_patients',views.view_patients,name='view_patients'),
    path('view_all_appointments',views.view_all_appointments,name='view_all_appointments'),
    path('approve/<int:aid>',views.approve,name='approve'),
    path('delete_doctor/<int:did>',views.delete_doctor,name='delete_doctor'),
    path('delete_patient/<int:did>',views.delete_patient,name='delete_patient'),
    # path('approved_appointments',views.approved_appointments,name='approved_appointments'),   
]