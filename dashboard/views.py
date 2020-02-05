from django.shortcuts import render
from .models import InterestForm, ExperienceForm
import smtplib
import math
import random
from email.message import EmailMessage

# Create your views here.


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
            msg.set_content('Secret Key: ' + otp + "\nThis key is confidential do not share\nLink for Form 2:http://localhost:8000/interest/")
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
        print(interest_list)
        interest = ""
        experience = ""
        for i in range(len(interest_list)):
            interest += interest_list[i] + " "
        print(interest)
        for i in range(1, 8):
            experience = experience + " " + request.POST.get("exp" + str(i))
        experience_form = ExperienceForm(interest=interest, experience=experience)
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
