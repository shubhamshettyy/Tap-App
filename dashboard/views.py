from django.shortcuts import render, redirect
from .models import InterestForm, ExperienceForm, PhoneInterview
import smtplib
import math
import random
from email.message import EmailMessage
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def induction(request, pk):
    EMAIL_ADDRESS = 'tapapplication2020@gmail.com'
    EMAIL_PASSWORD = 'Testing321'
    acceptance_msg = EmailMessage()
    acceptance_msg['Subject'] = 'Accepted for induction'
    acceptance_msg['From'] = EMAIL_ADDRESS
    acceptance_msg['To'] = pk
    acceptance_msg.set_content("You are selected for the induction program.")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(acceptance_msg)
    messages.success(request, f'Sent induction email !')
    return redirect('phone-interview')


@login_required
def phone_interview_detail(request, pk):
    if request.method == "POST":
        obj = PhoneInterview.objects.filter(email=pk).first()
        a = request.POST.get('1', '')
        a = int(a)
        if a >= 3:
            obj.accepted = True
        else:
            obj.accepted = False
        obj.grade = request.POST.get('1', '')
        obj.save()
        return redirect('phone-interview')
    return render(request, 'phone_interview_detail.html', context={'object': InterestForm.objects.filter(email=pk).first(), 'eobject': ExperienceForm.objects.filter(email=pk).first()})


@login_required
def phone_interview(request):
    context = {
        'interests': InterestForm.objects.all(),
        'experiences': ExperienceForm.objects.filter(shortlisted=True),
        'interviews': PhoneInterview.objects.all()

    }
    if request.method == "POST":
        selected_interest = request.POST.get('property', "")
        selected_exp = request.POST.get('exp', "")
        if selected_interest != 'all':
            context = {
                'interests': InterestForm.objects.all(),
                'experiences': ExperienceForm.objects.filter(interest__icontains=selected_interest),
                'interviews': PhoneInterview.objects.all()
            }
        return render(request, 'phone_interview.html', context)
    context = {
        'interests': InterestForm.objects.all(),
        'experiences': ExperienceForm.objects.filter(shortlisted=True),
        'interviews': PhoneInterview.objects.all()
    }
    print(context)
    return render(request, 'phone_interview.html', context)


def interview_timing(request, pk):
    if request.method == "POST":
        time = request.POST.get('time', "")
        name = request.POST.get('name', "")
        obj = PhoneInterview(name=name, timing=time, email=pk)
        obj.save()
        return render(request, 'thankyou.html')

    return render(request, 'interview_timing.html', {'email': pk})


@login_required
def shortlist_email(request):
    EMAIL_ADDRESS = 'tapapplication2020@gmail.com'
    EMAIL_PASSWORD = 'Testing321'
    expTrue = ExperienceForm.objects.filter(shortlisted=True)
    expFalse = ExperienceForm.objects.filter(shortlisted=False)
    true_mail = []
    false_mail = []
    for exp in expTrue:
        true_mail.append(exp.email)
    for exp in expFalse:
        false_mail.append(exp.email)

    for email in true_mail:
        acceptance_msg = EmailMessage()
        acceptance_msg['Subject'] = 'Accepted for phone interview'
        acceptance_msg['From'] = EMAIL_ADDRESS
        acceptance_msg['To'] = email
        acceptance_msg.set_content("Please enter phone interview timings:http://localhost:8000/interview/" + email)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(acceptance_msg)
    rejection_msg = EmailMessage()
    rejection_msg['Subject'] = 'Result of Shortlisting'
    rejection_msg['From'] = EMAIL_ADDRESS
    rejection_msg['To'] = false_mail
    rejection_msg.set_content("ThankYou for applying.Better luck next time.")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(rejection_msg)
    messages.success(request, f'Email Sent!')
    return redirect('shortlist')


@login_required
def shortlist(request):
    print("hello")
    context = {
        'interests': InterestForm.objects.all(),
        'experiences': ExperienceForm.objects.filter(shortlisted=True),

    }
    if request.method == "POST":
        selected_interest = request.POST.get('property', "")
        selected_exp = request.POST.get('exp', "")
        if selected_interest != 'all':
            context = {
                'interests': InterestForm.objects.all(),
                'experiences': ExperienceForm.objects.filter(interest__icontains=selected_interest),
            }
        return render(request, 'shortlist.html', context)
    context = {
        'interests': InterestForm.objects.all(),
        'experiences': ExperienceForm.objects.filter(shortlisted=True),
    }
    print(context)
    return render(request, 'shortlist.html', context)


@login_required
def dashboard(request):

    if request.method == "POST":
        selected_interest = request.POST.get('property', "")
        selected_exp = request.POST.get('exp', "")
        if selected_interest != 'all':
            context = {
                'interests': InterestForm.objects.all(),
                'experiences': ExperienceForm.objects.filter(interest__icontains=selected_interest),
            }
            messages.success(request, f'Filter applied: {selected_interest}!')
            return render(request, 'index.html', context)

    context = {
        'interests': InterestForm.objects.all(),
        'experiences': ExperienceForm.objects.all()
    }

    return render(request, 'index.html', context)


def detailview(request, pk):
    if request.method == "POST":
        obj = ExperienceForm.objects.filter(email=pk).first()
        a = request.POST.get('1', '')
        print(a)
        a = int(a)
        if a >= 3:
            obj.shortlisted = True
        else:
            obj.shortlisted = False
        obj.grade = request.POST.get('1', '')
        obj.save()
        return redirect('dashboard')
    return render(request, 'detailview.html', context={'object': InterestForm.objects.filter(email=pk).first(), 'eobject': ExperienceForm.objects.filter(email=pk).first()})


# def grade(request):
#     if request.method == "POST":


def home(request):

    return render(request, 'index.html')


def interest(request):
    EMAIL_ADDRESS = 'tapapplication2020@gmail.com'
    EMAIL_PASSWORD = 'Testing321'

    if request.method == "POST":
        string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lent = len(string)
        otp = ""
        for i in range(15):
            otp += string[math.floor(random.random() * lent)]

        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        phno = request.POST.get('phno', '')
        city = request.POST.get('city', "").lower()
        pincode = request.POST.get('pincode', '')

  #       email_body = """<pre>
        # Congratulations! We've successfully created account.
        # Go to the page: <a href="https://www.google.com/">click here</a>
        # Thanks,
        # XYZ Team.
        # </pre>"""

        # msg = MIMEText(email_body ,'html')

        print(otp, city)
        if city == "mumbai" or city == "pune":
            msg = EmailMessage()
            msg['Subject'] = 'Approval for Form 2 submission'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            msg.set_content('Secret Key: ' + otp + "\nThis key is confidential do not share\nLink for Form 2:http://localhost:8000/experience/")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            inst = InterestForm(name=name, phone_number=phno, email=email, city=city, secret_key=otp, pincode=pincode)
            inst.save()
        else:
            inst = InterestForm(name=name, phone_number=phno, email=email, city=city, pincode=pincode)
            inst.save()

        return render(request, 'adminusers/logout.html')

    return render(request, 'form1.html')


# def sk_validation(request, sk):
#     render(request,)


def form2_post(request):
    if request.method == "POST":
        interest_list = request.POST.getlist('checkbox[]', '')
        email = request.POST.get('email', "")
        desc = request.POST.get('desc', "")
        print(interest_list, email)
        interest = ""
        experience = ""
        for i in range(len(interest_list)):
            interest += interest_list[i] + " "
        print(interest)
        for i in range(1, 8):
            experience = experience + " " + request.POST.get("exp" + str(i))
        experience_form = ExperienceForm(email=email, interest=interest, experience=experience, description=desc)
        print(experience_form)
        experience_form.save()
        return render(request, 'failure.html')


def experience(request):

    if request.method == 'POST':
        sk = request.POST.get('sk', "")
        if len(InterestForm.objects.filter(secret_key=sk)) != 0:
            return render(request, 'form2.html', {'object': InterestForm.objects.filter(secret_key=sk).first()})
        else:
            return render(request, 'failure.html')

    return render(request, 'sk_validation.html')
