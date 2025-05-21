from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json, tempfile, os
from django.views.decorators.http import require_POST
from insight_hub.models import Dashboard
from django.contrib import messages
from insight_hub.utils.for_qr import generate_dashboard_qr
from insight_hub.utils.csv_analyzer import analyze_csv
from django.urls import reverse
from urllib.parse import urljoin

@require_POST
def upload_csv(request):
    if request.user.is_authenticated:
        file=request.FILES.get("main_file")
        if file:
            if not file.name.lower().endswith('.csv'):
                return JsonResponse({"success": False, "message": "Only .csv files are allowed!"})
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                for chunk in file.chunks():
                    tmp_file.write(chunk)
                temp_file_path = tmp_file.name

            analysis_result = analyze_csv(temp_file_path)
            os.unlink(temp_file_path)
            return  JsonResponse({"success":True,"data":analysis_result})
        else:
            return  JsonResponse({"success":False,"message":"File not uploaded!"})
    else:
        return  JsonResponse({"success":False})

@require_POST
def create_dashboard(request):
    if request.user.is_authenticated:
        user=request.user
        data = json.loads(request.body)
        title=data.get("title")
        if title:
            description=data.get("description")
            is_public=data.get("is_public")
            dashboard_obj=Dashboard.objects.create(user=user,title=title,description=description,is_public=is_public)
            base_url = f"{request.scheme}://{request.get_host()}"
            generate_dashboard_qr(full_url=urljoin(base_url, f"dashboard/{dashboard_obj.id}"), dash_id=dashboard_obj.id)
            messages.success(request, 'Dashboard created successfully!')
            return JsonResponse({"success":True,"message":"Dashboard created successfully","redirect_url" : reverse("index") })
        else:
            return JsonResponse({"success":False,"error":"Title can't be empty!"})
    else:
        return JsonResponse({"success":False,"error":"User not authenticated!"})

@require_POST
def like_dashboard(request):
    data = json.loads(request.body)
    dashboard_id=data.get("dashboard_id")
    dashboard_obj = Dashboard.objects.filter(id=dashboard_id).first()
    if dashboard_obj.likes.filter(id=request.user.id).exists():
        dashboard_obj.likes.remove(request.user)
        new_number_of_likes=dashboard_obj.number_of_likes()
        response={'success':True,'new_number_of_likes':new_number_of_likes,"is_liked":False}
    else:
        dashboard_obj.likes.add(request.user)
        new_number_of_likes=dashboard_obj.number_of_likes()
        response={'success':True,'new_number_of_likes':new_number_of_likes,"is_liked":True}
    return JsonResponse(response)