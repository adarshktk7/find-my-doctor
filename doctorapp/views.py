from django.shortcuts import render , redirect,HttpResponse,get_object_or_404
from .models import User,Patient , Doctor,Appointment
from django.contrib.auth import authenticate , login,logout


# Create your views here.
def index(request):
    return render(request,'index.html')

def patient_register(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        place = request.POST['place']
        gender = request.POST['gender']
        age = request.POST['age']
        user=User.objects.create_user(username=username, password=password,usertype='patient')
        Patient.objects.create(
            pat=user,
            name=name,
            place=place,
            gender=gender,
            age=age)
        return  redirect(logins)
    else:
        return render(request,'patient_register.html')
    
def doctor_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        specilization = request.POST['specilization']
        location = request.POST['location']
        hospital = request.POST['hospital']
        qualification=request.POST['qualification']
        user = User.objects.create_user(username=username,password=password,usertype='doctor')
        Doctor.objects.create(
            doc=user,
            name=name, 
            specilization=specilization, 
            location=location, 
            hospital=hospital,
            qualification=qualification)
        return  redirect(logins)
    else:
        return render(request,'doctor_register.html')
    
def logins(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        User=authenticate(request,username=username,password=password)
        if User is not None and User.is_superuser==1:
            return redirect(adminhome)
        elif User is not None and User.usertype=="doctor":
            login(request,User)
            request.session['doc']=User.id
            return redirect(doctorhome)
        elif User is not None and User.usertype=="patient" and User.is_active==1:
            login(request,User)
            request.session['pat']=User.id
            return redirect(patienthome)
        return HttpResponse("not valid")
    else:
        return render(request,'logins.html')
    
#patient


def patienthome(request):
    doctors=[]
    if request.method=="POST":
        specilization = request.POST.get('specilization')
        location = request.POST.get('location')
        doctors=Doctor.objects.filter(specilization__icontains=specilization,location__icontains=location)
    return render(request,'patienthome.html',{'doctors':doctors})



def view_patients(request):
    x=Patient.objects.all()
    return render(request,'view_patients.html',{'x1':x})

def adminhome(request):
    alldoc=Doctor.objects.all
    total_doctors=Doctor.objects.count()
    total_patients=Patient.objects.count()
    total_appointments=Appointment.objects.count()
    recent_appointments = Appointment.objects.order_by('-date')[:5]

    return render(request, 'adminhome.html',{
        'total_doctors':total_doctors,
        'total_patients':total_patients,
        'total_appointments':total_appointments,
        'alldoc':alldoc,
        'recent_appointments': recent_appointments

    })

def patient_profile(request):
    patient = Patient.objects.filter(pat=request.user).first()
    return render(request, 'patient_profile.html',{ 'patient':patient})

def update_patient(request):
    patient=request.session.get('pat')
    patients=Patient.objects.get(pat_id=patient)
    user=User.objects.get(id=patient)
    return render(request,'update_patient.html',{'view':patients,'data':user})

def update_patients(request,uid):
    if request.method=="POST":
        patient=Patient.objects.get(id=uid)
        pat=patient.pat_id
        user=User.objects.get(id=pat)
        user.username=request.POST['username']
        user.save()
        patient.name=request.POST['name']
        patient.place=request.POST['place']
        patient.age=request.POST['age']
        patient.gender=request.POST['gender']
        patient.save()
        return HttpResponse("success")
    
def book_appointment(request,doctor_id):
    doctor=Doctor.objects.get(id=doctor_id)
    patient=Patient.objects.get(pat=request.user)
    if request.method=='POST':
        patient_name=request.POST.get('patient_name')
        date=request.POST.get('date')
        time=request.POST.get('time')
        symptoms=request.POST.get('symptoms')
        Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            patient_name=patient_name,
            date=date,
            time=time,
            symptoms=symptoms
        )
        return render (request, 'appointment_success.html',{'doctor':doctor})
    else:
        return render(request,'book_appointment.html',{'doctor':doctor})
    
def view_appointments(request):
    patient=Patient.objects.get(pat=request.user)
    appointment=Appointment.objects.filter(patient=patient)
    return render(request,'view_appointments.html',{'appointment':appointment})

def lgout(request):
    logout(request)
    return redirect (logins)

#doctor

def doctorhome(request):
    doctor=Doctor.objects.get(doc=request.user)
    appointments=Appointment.objects.filter(doctor=doctor)
    approved_appointments = Appointment.objects.filter(doctor=doctor, status='Approved')

    return render(request,'doctorhome.html',{'doctor':doctor,'appointments':approved_appointments})

def doctorprofile(request):
    doctor=Doctor.objects.filter(doc=request.user).first()
    return render (request,'doctorprofile.html',{'doctor':doctor})

# def doctor_view_profile(request,doctor_id):
#     doctor= get_object_or_404 (Doctor,id=doctor_id)
#     return render(request,'doctor_view_profile.html',{'doctor':doctor})

def doc_view_appointments(request):
    doctor=Doctor.objects.get(doc=request.user)
    appointments=Appointment.objects.filter(doctor=doctor)
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')  # "approve" or "reject"
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

        if action == 'approve':
            appointment.status = 'Approved'
        elif action == 'reject':
            appointment.status = 'Rejected'

        appointment.save()
        return redirect('doc_view_appointments')
    return render(request,'doc_view_appointments.html',{'appointments':appointments})

def update_doctor(request):
    doctor=request.session.get('doc')
    doctors=Doctor.objects.get(doc_id=doctor)
    user=User.objects.get(id=doctor)
    return render(request,'update_doctor.html',{'view':doctors,'data':user})

def updated_doctor(request,uid):
    if request.method=='POST':
        doctor=Doctor.objects.get(id=uid)
        doc=doctor.doc_id
        user=User.objects.get(id=doc)
        user.username=request.POST['username']
        user.save()
        doctor.name=request.POST['name']
        doctor.specilization=request.POST['specilization']
        doctor.location=request.POST['location']
        doctor.hospital=request.POST['hospital']
        doctor.qualification=request.POST['qualification']
        doctor.save()
        return HttpResponse('success')
    
def view_doctors(request):
    x=Doctor.objects.all()
    return render(request,'view_doctor.html',{'x1':x})

def view_all_appointments(request):
    appointments=Appointment.objects.all().order_by('-date', '-time')
    return render (request,'view_all_appointments.html',{'appointments':appointments})

def approve(request,aid):
    doctor=Doctor.objects.get(id=aid)
    doctor.doc.is_active = True
    doctor.doc.save()
    return HttpResponse('approved')

def delete_doctor(request,did):
    doctor=User.objects.get(id=did)
    doctor.delete()
    return redirect(view_doctors)

def delete_patient(request,did):
    patient=User.objects.get(id=did)
    patient.delete()
    return redirect(view_patients)


# def approved_appointments(request):
#     x=User.objects.filter(is_active=1,usertype='patient')
#     return render(request,'approved_appointments.html',{'x':x})







    

