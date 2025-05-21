from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import json
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from insight_hub.models import Dashboard

# @csrf_exempt
@require_POST
def register_api(request):
    try:
        data = json.loads(request.body)
        fname = data.get("fname")
        lname = data.get("lname")
        email = data.get("email")
        password = data.get("password")
        username = data.get("username")
        dashboard_id=data.get('dashboard')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already taken."}, status=400)

        user = User.objects.create_user(username=username, password=password,
                                        first_name=fname, last_name=lname, email=email)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        if dashboard_id:
            try:
                dashboard_obj=Dashboard.objects.filter(id=dashboard_id).first()
                if dashboard_obj:
                    dashboard_obj.allowed_users.add(user)
                    messages.success(request, 'Allowed Dashboard viewer!')
                    messages.success(request, 'User registered successfully')
                    return JsonResponse({
                        "success": True,
                        "message":"Logged in successfully",
                        "redirect_url": f"/dashboard/{dashboard_obj.id}"
                    })
                else:
                    messages.error(request, 'Invalid dashboard ID')
            except Exception as e:
                    messages.error(request, 'Invalid dashboard ID')
        messages.success(request, 'User registered successfully')
        return JsonResponse({
            "success": True,
            "message":"User registered successfully",
            "redirect_url": reverse("index")
        })
    except Exception as e:
        print("HIIII")
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@require_POST
def login_api(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        dashboard_id=data.get('dashboard')

        if not username or not password:
            return JsonResponse({"success": False,'error': 'Username and password required'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if dashboard_id:
                try:
                    dashboard_obj=Dashboard.objects.filter(id=dashboard_id).first()
                    if dashboard_obj:
                        dashboard_obj.allowed_users.add(user)
                        messages.success(request, 'Allowed Dashboard viewer!')
                        messages.success(request, 'Logged in successfully')
                        return JsonResponse({
                            "success": True,
                            "message":"Logged in successfully",
                            "redirect_url": f"/dashboard/{dashboard_obj.id}"
                        })
                    else:
                        messages.error(request, 'Invalid dashboard ID')
                except Exception as e:
                        messages.error(request, 'Invalid dashboard ID')
            messages.success(request, 'Logged in successfully')
            return JsonResponse({
                "success": True,
                "message":"Logged in successfully",
                "redirect_url": reverse("index")
            })
        else:
            return JsonResponse({"success": False,'error': 'Invalid credentials'}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({"success": False,'error': 'Invalid JSON'}, status=400)
