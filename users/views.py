from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms 
from . import models
from projects.models import PROJECT_LANGUAGES, Project

@login_required
def developers(request):
    user_profile = models.Profile.objects.get(user=request.user)
    dev_profiles = models.Profile.objects.order_by("projects_created").reverse()[:10]
    context = {
        'dev_profiles': dev_profiles,
        'user_profile': user_profile
    }
    
    # inviting devs
    project_id = request.GET.get('id')
    if project_id:
        project_id = int(project_id)
        project = Project.objects.get(id=project_id)
        if (request.user == project.author):
            context['project_id'] = project_id
            context['project'] = project

    return render(request, 'users/developers.html', context=context)

@login_required
def profile(request):
    
    redirect_url = request.GET.get("next", '/projects/')
    context = {}
        
    try:
        profile = models.Profile.objects.get(user=request.user)
        form = forms.ProfileForm(request.POST or None, instance=profile)
        profile_exist = True
        context['email'] = profile.user.email
        if(request.method == "POST"):
            if(form.is_valid()):
                form.save()
                return redirect(redirect_url)
        else:
            context['profile'] = profile
    except:
        profile_exist = False
        form = forms.ProfileForm(request.POST or None)
        if request.method == "POST":
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect(redirect_url)
    context['form'] = form
    context['profile_exist'] = profile_exist
    context['request_user_id'] = request.user.id
        
    return render(request, 'users/profile.html', context=context)

@login_required
def show_profile(request, id):
    try:
        profile = models.Profile.objects.get(user__id=id)
        form = forms.ProfileForm(instance=profile)
        profile.interests = str(profile.interests).split(',')
        context = {
            'profile': profile,
            'email': profile.user.email,
        }
    except:
        message = "User didn't created profile yet"
        context = {
            'message': message
        }
    return render(request, 'users/show_profile.html', context=context)
    
@login_required
def search_users(request):
    keyword = request.POST.get('keyword')
    devs = models.Profile.objects.filter(user__username__contains=keyword)
    profile = models.Profile.objects.get(user = request.user)
    context = {
        'devs': devs,
        'keyword': keyword,
        'profile': profile
    }

    # inviting devs
    project_id = request.GET.get('id')
    if project_id:
        project_id = int(project_id)
        project = Project.objects.get(id=project_id)
        context['project_id'] = project_id
        context['project'] = project
    return render(request, 'users/search_users.html', context=context)

@login_required
def send_dev_request(request, id):
    profile = models.Profile.objects.get(user=request.user)
    dev = User.objects.get(id=id)
    dev_profile = models.Profile.objects.get(user=dev)

    if not (id in profile.dev_requests_sent and request.user.id in dev_profile.dev_requests_sent):
        profile.dev_requests_sent.append(id)
        profile.save()
        
        dev_profile.dev_requests_inbox.append(request.user.id)
        dev_profile.save()

    return HttpResponse("send")

@login_required
def cancel_dev_request(request, id):
    profile = models.Profile.objects.get(user=request.user)
    dev = User.objects.get(id=id)
    dev_profile = models.Profile.objects.get(user=dev)

    if (id in profile.dev_requests_sent and request.user.id in dev_profile.dev_requests_inbox):
        profile.dev_requests_sent.remove(id)
        profile.save()
        
        dev_profile.dev_requests_inbox.remove(request.user.id)
        dev_profile.save()

    return HttpResponse("cancelled")

@login_required
def accept_dev_request(request, id):
    profile = models.Profile.objects.get(user=request.user)
    dev = User.objects.get(id=id)
    dev_profile = models.Profile.objects.get(user=dev)

    if (id in profile.dev_requests_inbox and request.user.id in dev_profile.dev_requests_sent):
        if id in profile.dev_requests_sent:
            profile.dev_requests_sent.remove(id)
        profile.dev_requests_inbox.remove(id)
        profile.devs_connected.append(id)
        profile.save()
        
        if request.user.id in dev_profile.dev_requests_inbox:
            dev_profile.dev_requests_inbox.remove(request.user.id)
        dev_profile.dev_requests_sent.remove(request.user.id)
        dev_profile.devs_connected.append(request.user.id)
        dev_profile.save()

    return HttpResponse("accepted")

@login_required
def reject_dev_request(request, id):
    profile = models.Profile.objects.get(user=request.user)
    dev = User.objects.get(id=id)
    dev_profile = models.Profile.objects.get(user=dev)

    if (id in profile.dev_requests_inbox and request.user.id in dev_profile.dev_requests_sent):
        profile.dev_requests_inbox.remove(id)
        profile.save()
        
        dev_profile.dev_requests_sent.remove(request.user.id)
        dev_profile.save()

    return HttpResponse("rejected")

@login_required
def break_connection(request, id):
    profile = models.Profile.objects.get(user=request.user)
    dev = User.objects.get(id=id)
    dev_profile = models.Profile.objects.get(user=dev)

    if (id in profile.devs_connected and request.user.id in dev_profile.devs_connected):
        profile.devs_connected.remove(id)
        profile.save()
        
        dev_profile.devs_connected.remove(request.user.id)
        dev_profile.save()

    return HttpResponse("broke")

@login_required
def dev_requests_inbox(request):
    profile = models.Profile.objects.get(user=request.user)
    devs_list = User.objects.filter(id__in=profile.dev_requests_inbox)
    context = {
        'devs_list' : devs_list,
        'requests_type': "inbox"
    }
    return render(request, 'users/dev.html', context=context)

@login_required
def dev_requests_sent(request):
    profile = models.Profile.objects.get(user=request.user)
    devs_list = User.objects.filter(id__in=profile.dev_requests_sent)
    context = {
        'devs_list' : devs_list,
        'requests_type': "sent"
    }
    return render(request, 'users/dev.html', context=context)

@login_required
def devs_connected(request):
    profile = models.Profile.objects.get(user=request.user)
    devs_list = User.objects.filter(id__in=profile.devs_connected)
    context = {
        'devs_list' : devs_list,
        'requests_type': 'connected'
    }
    return render(request, 'users/dev.html', context=context)

# create a field for project requests in user models.py
@login_required
def projects_invited(request):
    profile = models.Profile.objects.get(user=request.user)
    projects = Project.objects.filter(id__in=profile.project_requests_inbox)

    context = {
        'projects': projects
    }
    return render(request,'users/project_invites.html', context=context)

@login_required
def handle_project_invite(request):
    project_id = int(request.GET.get('project_id'))
    user_id = int(request.GET.get('user_id'))
    invite_action = request.GET.get('invite_action')

    project = Project.objects.get(id=project_id)
    profile = models.Profile.objects.get(user__id=user_id)

    if invite_action == "accept":
        if project.is_active:
            if project_id in profile.project_requests_inbox:
                profile.project_requests_inbox.remove(project_id)
                profile.projects_working.append(project_id)
                profile.save()

                project.developers_requested.remove(user_id)
                project.developers_list.append([str(user_id), profile.user.username])
                project.developers_request_accepted.append(user_id)

                if user_id in project.developers_request_rejected:
                    project.developers_request_rejected.remove(user_id)
                project.save()

                return HttpResponse('You now are a developer in ' + project.title)
            else:
                return HttpResponse('Nice try Dude')

    elif invite_action == "reject":
        if project.is_active:
            if project_id in profile.project_requests_inbox:
                profile.project_requests_inbox.remove(project_id)
                profile.save()
                
                project.developers_requested.remove(user_id)
                if not user_id in project.developers_request_rejected:
                    project.developers_request_rejected.append(user_id)
                project.save()

                return HttpResponse("request sucessfully rejected")
            else:
                return HttpResponse('Nice try Dude')

