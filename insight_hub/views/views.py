from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from insight_hub.models import Dashboard, Chart, CSVFile
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        dashboards=Dashboard.objects.filter(user=request.user)
        return render(request,'insighthub/super_dashboard.html',{'all_dashboard':dashboards})
    else:
        return render(request,'insighthub/landing.html')

def dashboard(request, id):
    dashboard_obj = get_object_or_404(Dashboard, id=id)
    if dashboard_obj.is_public:
        chart_objs=Chart.objects.filter(dashboard=dashboard_obj)
        chart_data = []
        for chart in chart_objs:
            chart_data.append({
                "title": chart.title,
                "description": chart.description,
                "data": chart.get_chart_data(),
            })
        liked=False
        all_liked=dashboard_obj.likes
        if  all_liked.filter(id=request.user.id).first():
            liked=True
        return render(request,'insighthub/dashboard.html',{"dashboard":dashboard_obj,"combined":zip(chart_objs,chart_data),'is_liked':liked})
    elif request.user.is_authenticated:
        if request.user == dashboard_obj.user or request.user in dashboard_obj.allowed_users.all():
            chart_objs=Chart.objects.filter(dashboard=dashboard_obj)
            chart_data = []
            for chart in chart_objs:
                chart_data.append({
                    "title": chart.title,
                    "description": chart.description,
                    "data": chart.get_chart_data(),
                })
            liked=False
            all_liked=dashboard_obj.likes
            if  all_liked.filter(id=request.user.id).first():
                liked=True
            return render(request,'insighthub/dashboard.html',{"dashboard":dashboard_obj,"combined":zip(chart_objs,chart_data),'is_liked':liked})
        else:
            return HttpResponseForbidden("You're not allowed to view this private dashboard.")
    else:
        request.session['dashboard_id'] = str(dashboard_obj.id)
        login_url = reverse('login') + '?dashboard='+str(dashboard_obj.id)+'&'+ 'next=' + reverse('dashboard', args=[dashboard_obj.id])
        messages.error(request, 'This dashboard is private. Please login to view.')
        return redirect(login_url)

def delete_dashboard(request,id):
    if request.user.is_authenticated:
        try:
            dashboard_obj=Dashboard.objects.filter(id=id).first()
            if dashboard_obj.user==request.user:
                if dashboard_obj:
                    messages.success(request, 'Dashboard Deleted!')
                    dashboard_obj.delete()
                    return redirect("index")
                else:
                    messages.error(request, 'Invalid dashboard ID')
                    return redirect("index")
            else:
                messages.error(request, 'Only owner can delete dashboard')
                return redirect(f"/dashboard/{id}")
        except:
            messages.error(request, 'Invalid dashboard ID')
            return redirect("index")
    else:
        messages.error(request, 'User not authenticated')
        return redirect("login")

def update_dashboard(request,id):
    if request.user.is_authenticated:
        try:
            dashboard_obj=Dashboard.objects.filter(id=id)
            if dashboard_obj.exists():
                dashboard_obj=dashboard_obj.first()
                if dashboard_obj.user==request.user:
                    title=request.POST.get("title")
                    if title:
                        description=request.POST.get("description")
                        is_public=request.POST.get("is_public")
                        dashboard_obj.title=title
                        dashboard_obj.description=description
                        dashboard_obj.is_public=is_public
                        dashboard_obj.save()
                        messages.success(request, 'Dashboard Updated!')
                        return redirect(f"index")
                    else:
                        messages.error(request, "Title can't be empty")
                        return redirect(f"index")
                else:
                    messages.error(request, 'Only owner can update dashboard')
                    return redirect(f"index")
            else:
                messages.error(request, 'Invalid dashboard ID')
                return redirect("index")
        except Exception as e:
            print(e)
            messages.error(request, 'Invalid dashboard ID')
            return redirect("index")
    else:
        messages.error(request, 'User not authenticated')
        return redirect("login")

@require_POST
def create_chart(request,id):
    if request.user.is_authenticated:
        dashboard_obj=Dashboard.objects.filter(id=id)
        if dashboard_obj.exists():
            if dashboard_obj.first().user == request.user:
                csv_file=request.FILES.get("main_file")
                title=request.POST.get("title","")
                if csv_file and len("title") > 1 :
                    #FOR CHART MODEL
                    operation=request.POST.get("operation")
                    chart_type=request.POST.get("chart_type")
                    description=request.POST.get("description")
                    x_column=request.POST.get("x_column")
                    y_column=request.POST.get("y_column")
                    chart_obj=Chart.objects.create(operation=operation,dashboard=dashboard_obj.first(),chart_type=chart_type,title=title, description=description,x_column=x_column,y_column=y_column)
                    
                    csv_file = CSVFile.objects.create(chart=chart_obj, file_path=csv_file)

                    messages.success(request,"Chart created successfully!")
                    return redirect(f"/dashboard/{id}")
                else:
                    messages.error(request,"Invalid data provided")
                    return redirect("index")
            else:
                messages.error(request,"Only dashboard owner can create charts!")
                return redirect(f"/dashboard/{id}")
        else:
            messages.error(request,"Invalid Dashboard ID!")
            return redirect("index")
    messages.error(request, 'User not authenticated')
    return redirect("login")

@require_POST
def update_chart(request,id):
    if request.user.is_authenticated:
        dashboard_obj=Dashboard.objects.filter(id=id)
        chart_id=request.POST.get("chart_id")
        chart_obj=Chart.objects.filter(id=chart_id)
        if dashboard_obj.exists() and chart_obj.exists():
            if dashboard_obj.first().user == request.user:
                title=request.POST.get("title","")
                if len("title") > 1:
                    operation=request.POST.get("operation")
                    print(operation)
                    chart_type=request.POST.get("chart_type")
                    description=request.POST.get("description")
                    x_column=request.POST.get("x_column")
                    y_column=request.POST.get("y_column")
                    chart_obj.update(dashboard=dashboard_obj.first(),operation=operation,chart_type=chart_type,title=title, description=description,x_column=x_column,y_column=y_column)
                    messages.success(request,"Chart updated successfully!")
                    return redirect(f"/dashboard/{id}")
                else:
                    messages.error(request,"Title can't be empty")
                    return redirect("index")
            else:
                messages.error(request,"Only dashboard owner can update charts!")
                return redirect(f"/dashboard/{id}")
        else:
            messages.error(request,"Invalid Dashboard ID or Chart ID")
            return redirect("index")
    messages.error(request, 'User not authenticated')
    return redirect("login")

@require_POST
def delete_chart(request,id):
    if request.user.is_authenticated:
        chart_obj=Chart.objects.filter(id=id)
        dashboard_id=chart_obj.first().dashboard.id
        if chart_obj.exists():
            chart_obj.delete()
            messages.success(request,"Chart deleted!")
            return redirect(f"/dashboard/{dashboard_id}")
        else:
            messages.error(request,"Invalid Chart ID")
            return redirect("index")
    messages.error(request, 'User not authenticated')
    return redirect("login")

    