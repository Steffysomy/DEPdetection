from django.shortcuts import render, redirect
from  .models import *
from django.contrib.auth import authenticate
from django.db.models import Q
# Create your views here.

def index(request):

    return render(request, 'index.html')    

def login(request):
    msg = ""
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        request.session['username'] = email
        if user is not None:
            if user.is_superuser:
                return redirect('/AdminHome')
            elif user.is_staff:
                ds = Counselor.objects.get(email=email)
                request.session['id'] = ds.id
                return redirect('/coHome')
            else:
                ds = Patient.objects.get(email=email)
                request.session['id'] = ds.id
                return redirect('/paHome')
            
        else:
            msg = "Invalid username or password"
    return render(request, 'login.html', {"msg": msg})


def paReg(request):
    msg = ""
    data = ""
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        file = request.FILES["file"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password == password2:
            try:
                usr = User.objects.create_user(
                    username=email, password=password, is_active=1)
                usr.save()
                col = Patient.objects.create(name=name, email=email, phone=phone, age=age, gender=gender, address=address, user=usr,idproof=file)
                col.save()
            except:
                msg = "Some Error Occured"
            else:
                msg = "Registartion Completed Successfully."
        else:
            msg = "Passwords not matching."
    return render(request, 'paReg.html', {"msg": msg})

def coReg(request):
    msg = ""
    data = ""
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        qual = request.POST["qual"]
        proof = request.FILES["proof"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password == password2:
            try:
                if User.objects.filter(username=email).exists():
                    msg = "Username already exists"
                else:
                    usr = User.objects.create_user(
                        username=email, password=password, is_active=0, is_staff=1)
                    usr.save()
                    col = Counselor.objects.create(name=name, email=email, phone=phone, qual=qual,address=address, proof=proof,user=usr)
                    col.save()
                    msg = "Registartion Completed Successfully."
                
            except:
                msg = "Some Error Occured"
        else:
            msg = "Passwords not matching."
    return render(request, 'coReg.html', {"msg": msg})


def AdminHome(request):
    return render(request, "AdminHome.html")


def adminPa(request):
    data = Patient.objects.all().order_by("-id")
    return render(request, "adminPa.html", {"data": data})

def adminCo(request):
    data = Counselor.objects.all().order_by("-id")
    return render(request, "adminCo.html", {"data": data})

def adminUpdateUsers(request):
    id = request.GET['id']
    status = request.GET['status']
    url = request.GET['url']
    usr = User.objects.get(id=id)
    usr.is_active = status
    usr.save()
    return redirect(f"/{url}")

def adminTests(request):
    msg = ''
    if request.POST:
        title = request.POST['title']
        content = request.POST['content']
        te = Tests.objects.create(title=title, content=content)
        te.save()
        msg = 'Test content added'
    data = Tests.objects.all().order_by("-id")
    return render(request, "adminTests.html", {"data": data, "msg":msg})

def adminUpdatetestStatus(request):
    id = request.GET['id']
    status = request.GET['status']
    url = request.GET['url']
    usr = Tests.objects.get(id=id)
    usr.status = status
    usr.save()
    return redirect(f"/{url}")

def paHome(request):
    return render(request, "paHome.html")

def paTests(request):
    data = Tests.objects.filter(status='Active')
    return render(request, "paTests.html", {"data":data})

def paAttendTest(request):
    uid = request.session['id']
    user = Patient.objects.get(id=uid)
    id = request.GET['id']
    data = Tests.objects.get(id=id)
    if request.POST:
        filename = request.FILES['filename']
        ins =Prediction.objects.create(test=data,patient=user,video=filename,status='Test Attended')
        ins.save()
        from prediction.emotions import main
        vid = f"D:/pro final/static/media/{ins.video}"
        print(vid)
        angry, disgust, fear, happy, neutral, sad, surprise = main(vid)
        dRes = int(angry) + int(fear) + int(sad) + int(int(neutral) /2) + int(int(disgust) /2)
        hRes = int(happy) + int(surprise) + int(int(neutral) / 4)
        if dRes > hRes:
            ins.prediction = "Depression detected"
        else:
            ins.prediction = "No Depression detected"
        ins.save()
        return redirect("/paTests")
    return render(request, "paAttendTest.html", {"data":data})

def paResults(request):
    uid = request.session['id']
    user = Patient.objects.get(id=uid)
    data = Prediction.objects.filter(patient=user).order_by("-id")
    return render(request, "paResults.html", {"data":data})

def paConsultCo(request):
    id = request.GET['id']
    uid = request.session['id']
    data = Counselor.objects.filter(user__is_active=1)
    return render(request, "paConsultCo.html", {"data":data, "id":id})

def paRequestCo(request):
    id = request.GET['id']
    pid = request.GET['pid']
    pre = Prediction.objects.get(id=pid)
    cou = Counselor.objects.get(id=id)
    con = Consultation.objects.create(counselor=cou,prediction=pre,status='Requested')
    con.save()
    return redirect("/paCounsultation")

def paCounsultation(request):
    uid = request.session['id']
    data = Consultation.objects.filter(prediction__patient=uid)
    return render(request, "paCounsultation.html", {"data":data})

def paReports(request):
    id = request.GET['id']
    data = Reports.objects.filter(consultation=id)
    con = Consultation.objects.get(id=id)
    cid = con.counselor.id
    cou = Counselor.objects.get(id=cid)
    return render(request, "paReports.html", {"data":data, "cou":cou})

def paChat(request):
    uid = request.session["id"]
    pat = Patient.objects.get(id=uid)
    cid = request.GET['id']
    url = request.GET['url']
    cou = Counselor.objects.get(id=cid)
    if request.method == "POST":
        msg = request.POST['msg']
        db = Message.objects.create(patient=pat, counselor=cou, message=msg, sendby='Patient')
        db.save()
    messages = Message.objects.filter(patient=pat, counselor=cou)
    return render(request, "paChat.html", {"messages": messages,"url":url})

def coHome(request):
    return render(request, "coHome.html")

def coConsultations(request):
    uid = request.session['id']
    data = Consultation.objects.filter(counselor=uid).exclude(status='Rejected')
    return render(request, "coConsultations.html", {"data":data})

def coChat(request):
    uid = request.session["id"]
    cou = Counselor.objects.get(id=uid)
    cid = request.GET['id']
    pat = Patient.objects.get(id=cid)
    url = request.GET['url']
    if request.method == "POST":
        msg = request.POST['msg']
        db = Message.objects.create(patient=pat, counselor=cou, message=msg, sendby='Counsellor')
        db.save()
    messages = Message.objects.filter(patient=pat, counselor=cou)
    return render(request, "coChat.html", {"messages": messages,"url":url})

def coReqStatus(request):
    id = request.GET['id']
    status = request.GET['status']
    con = Consultation.objects.get(id=id)
    con.status= status
    con.save()
    pid = con.prediction.id
    pre = Prediction.objects.get(id=pid)
    pre.status = "Consulted"
    pre.save()
    return redirect("/coConsultations")

def coReport(request):
    id = request.GET['id']
    con = Consultation.objects.get(id=id)
    pid = con.prediction.patient.id
    if request.POST:
        report = request.POST['report']
        document = request.FILES['document']
        rep = Reports.objects.create(consultation=con,report=report,document=document)
        rep.save()
    data = Reports.objects.filter(consultation__prediction__patient=pid)
    return render(request, "coReport.html", {"data": data,"id": id})

def coDeleteReport(request):
    cid = request.GET['cid']
    id = request.GET['id']
    rep = Reports.objects.get(id=id)
    rep.delete()
    return redirect(f"/coReport?id={cid}")



























































