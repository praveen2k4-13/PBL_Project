import json
import requests

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .EmailBackend import EmailBackend
from .models import Attendance, Session, Subject


def login_page(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'user_type'):
            if request.user.user_type == '1':
                return redirect('admin_home')
            elif request.user.user_type == '2':
                return redirect('staff_home')
            else:
                return redirect('student_home')
    return render(request, 'main_app/login.html')


def do_login(request):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")

    # Google reCAPTCHA
    captcha_token = request.POST.get('g-recaptcha-response')
    captcha_url = "https://www.google.com/recaptcha/api/siteverify"
    captcha_key = "6LfTGD4qAAAAALtlli02bIM2MGi_V0cUYrmzGEGd"
    data = {'secret': captcha_key, 'response': captcha_token}

    try:
        captcha_response = requests.post(captcha_url, data=data)
        result = captcha_response.json()
        if not result.get('success'):
            messages.error(request, 'Invalid Captcha. Try Again')
            return redirect('login_page')
    except Exception:
        messages.error(request, 'Captcha could not be verified. Try Again')
        return redirect('login_page')

    # Authenticate using custom EmailBackend
    user = EmailBackend.authenticate(
        request,
        username=request.POST.get('email'),
        password=request.POST.get('password')
    )

    if user is not None:
        login(request, user)
        if hasattr(user, 'user_type'):
            if user.user_type == '1':
                return redirect('admin_home')
            elif user.user_type == '2':
                return redirect('staff_home')
            else:
                return redirect('student_home')
        else:
            messages.error(request, "User type not defined.")
            return redirect('login_page')
    else:
        messages.error(request, "Invalid login details")
        return redirect('login_page')


def logout_user(request):
    logout(request)
    return redirect('login_page')


@csrf_exempt
def get_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = Attendance.objects.filter(subject=subject, session=session)

        attendance_list = [
            {
                "id": attd.id,
                "attendance_date": str(attd.date),
                "session": attd.session.id
            }
            for attd in attendance
        ]
        return JsonResponse(attendance_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def show_firebase_data(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        session_id = request.POST.get('session')
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            session = get_object_or_404(Session, id=session_id)
            attendance_qs = Attendance.objects.filter(subject=subject, session=session)
            attendance_list = [
                {
                    "id": att.id,
                    "attendance_date": str(att.date),
                    "session": att.session.id
                }
                for att in attendance_qs
            ]
            return JsonResponse(attendance_list, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def show_firebase_js(request):
    data = """
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

firebase.initializeApp({
    apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
    authDomain: "sms-with-django.firebaseapp.com",
    projectId: "sms-with-django",
    storageBucket: "sms-with-django.appspot.com",
    messagingSenderId: "945324593139",
    appId: "1:945324593139:web:03fa99a8854bbd38420c86",
    measurementId: "G-2F2RXTL9GT"
});

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
    const notification = JSON.parse(payload);
    // Customize and show notification here
});
    """
    return HttpResponse(data, content_type="application/javascript")