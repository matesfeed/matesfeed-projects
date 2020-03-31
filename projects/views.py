from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms
from . import models
from users.models import Profile
    
# Create your views here.
@login_required
def index(request):
    project_form = forms.ProjectForm(request.POST or None)
    try:
        profile = Profile.objects.get(user=request.user)
        if(request.method == "POST"):
            project = project_form.save(commit=False)
            project.author = request.user
            project.developers_list.append([str(request.user.id), request.user.username])
            project.save()
            profile.projects_created.append(project.id)
            profile.projects_working.append(project.id)
            profile.save()
            
        projects = models.Project.objects.all()
        for project in projects:
            project.language = str(project.language).split(',') 
            
        project_form = forms.ProjectForm()
        context = {
            'project_form': project_form,
            'projects': projects,
            'projects_bookmarked': profile.projects_bookmarked
        }
        return render(request, 'projects/index.html', context=context)
    except:
        return redirect('/users/profile/')

@login_required
def project(request, id):
    
    profile = Profile.objects.get(user=request.user)

    projects_bookmarked = profile.projects_bookmarked
    
    project = models.Project.objects.get(id=id)
    
    project.language = str(project.language).split(',')
    
    project_developers_list = project.developers_list

    requests_users_id_list = []
    for pending_request in project.requests_list:
        requests_users_id_list.append(int(pending_request[0]))

    rejected_users_id_list = []
    for rejected_request in project.rejected_list:
        rejected_users_id_list.append(int(rejected_request[0]))

    ignored_users_id_list = []
    for ignored_request in project.ignored_list:
        ignored_users_id_list.append(int(ignored_request[0]))

    developers_users_id_list = []
    for developer in project.developers_list:
        developers_users_id_list.append(int(developer[0]))

    developers_len = len(project_developers_list)
    
    dev_requests_sent = [str(dev) for dev in profile.dev_requests_sent]
    dev_requests_inbox = [str(dev) for dev in profile.dev_requests_inbox]
    devs_connected = [str(dev) for dev in profile.devs_connected]

    context = {
        'project': project,
        'projects_bookmarked': projects_bookmarked,
        'developers_len': developers_len,
        'requests_users_id_test': requests_users_id_list,
        'rejected_users_id_list': rejected_users_id_list,
        'ignored_users_id_list': ignored_users_id_list,
        'developers_users_id_list': developers_users_id_list,
        'issue_form': forms.IssueForm,
        'dev_requests_sent': dev_requests_sent,
        'dev_requests_inbox': dev_requests_inbox,
        'devs_connected': devs_connected,
        'str_user_id': str(request.user.id)
    }        

    if((request.user == project.author) or (request.user.id in developers_users_id_list)):

        issues = models.Issue.objects.filter(project_id=id)

        new_issues = []
        left_issues = []
        working_issues = []
        completed_issues = []

        for issue in issues:
            if(issue.status == 0):
                new_issues.append(issue)
            elif(issue.status == 1):
                working_issues.append(issue)
            elif(issue.status == 2):
                completed_issues.append(issue)
            elif(issue.status == 10):
                left_issues.append(issue)

        context['is_project_developer'] = (request.user.id in developers_users_id_list or request.user == project.author)
        context['issues_exist'] = (len(issues) > 0)
        context['new_issues'] = new_issues
        context['new_issues_count'] = len(new_issues)
        context['left_issues'] = left_issues
        context['left_issues_count'] = len(left_issues)
        context['working_issues'] = working_issues
        context['working_issues_count'] = len(working_issues)
        context['completed_issues'] = completed_issues
        context['completed_issues_count'] = len(completed_issues)

        # project invite status
        context['invites_pending'] = Profile.objects.filter(user__id__in=project.developers_requested)
        context['invites_accepted'] = Profile.objects.filter(user__id__in=project.developers_request_accepted)
        context['invites_rejected'] = Profile.objects.filter(user__id__in=project.developers_request_rejected)

    if(request.user == project.author):
        requests_list = project.requests_list
        context['requests_list'] = requests_list
    return render(request, 'projects/project.html', context=context)

@login_required
def addIssue(request, id):
    if(request.method == "POST"):
        issue_form = forms.IssueForm(request.POST)
        issue = issue_form.save(commit=False)
        issue.status = 0
        issue.project_id = id
        issue.developers_list.append(request.user.id)
        issue.save()

    return redirect('/projects/'+ str(id))

@login_required
def changeIssueStatus(request, project_id, issue_id, status):
    issue = models.Issue.objects.get(id=issue_id)
    issue.status = status
    issue.save()
    return redirect('/projects/' + str(project_id))

@login_required
def bookmark_project(request):
    try:
        project_id = int(request.GET['project_id'])
        profile = Profile.objects.get(user=request.user)
        if(project_id in profile.projects_bookmarked):
            profile.projects_bookmarked.remove(project_id)
            profile.save()
            return HttpResponse('project-removed')
        else:
            profile.projects_bookmarked.append(project_id)
            profile.save()
            return HttpResponse('project-added')
    except:
        return HttpResponse('redirect')


# project acceptance request

@login_required
def handle_project_request(request):
    user_id = int(request.GET.get('user_id'))
    profile = Profile.objects.get(user__id=user_id)
    project_id = int(request.GET.get('project_id'))
    project = models.Project.objects.get(id=project_id)
    user_details = [str(user_id), profile.user.username]
    
    if(user_id in project.requests_list):
        profile.projects_requested.remove(project_id)
        profile.save()
        project.requests_list.remove(user_details)
        project.save()
        return HttpResponse("removed")
    elif(user_id in project.ignored_list):
        profile.projects_requested.remove(project_id)
        profile.save()
        project.ignored_list.remove(user_details)
        project.save()
        return HttpResponse("removed")
    else:
        profile.projects_requested.append(project_id)
        profile.save()
        project.requests_list.append(user_details)
        project.save()
        return HttpResponse("added")
        
@login_required
def handle_pending_project_requests(request):
    user_id = int(request.GET.get('user_id'))
    project_id = int(request.GET.get('project_id'))
    request_code = request.GET.get('request_code')
    profile = Profile.objects.get(user__id=user_id)
    project = models.Project.objects.get(id=project_id)

    user_details = [str(user_id), (User.objects.get(id=user_id)).username]
    if(request_code == "accept"):
        profile.projects_working.append(project_id)
        profile.projects_requested.remove(project_id)
        profile.save()
        project.developers_list.append(user_details)
        project.requests_list.remove(user_details)
        project.save()
        return HttpResponse(1)
    elif(request_code == "reject"):
        profile.projects_rejected.append(project_id)
        profile.save()
        project.requests_list.remove(user_details)
        project.save()
        return HttpResponse(1)
    elif(request_code == "ignore"):
        project.request_list.remove(user_details)
        project.save()
        return HttpResponse(1)
    
@login_required
def leave_project_request(request):
    user_id = int(request.GET.get('user_id'))
    project_id = int(request.GET.get('project_id'))
    project = models.Project.objects.get(id=project_id)
    profile = Profile.objects.get(user__id = user_id)
    user_details = [str(user_id), (User.objects.get(id=user_id)).username]
    
    if project.is_active:
        project.developers_list.remove(user_details);
        if user_id in project.developers_requested:
            project.develoers_requested.remove(user_id)
        if user_id in project.developers_request_accepted:
            project.developers_request_accepted.remove(user_id)
        if project_id in profile.projects_working:
            profile.projects_working.remove(project_id)
        profile.save()
        project.save()
    return HttpResponse(1)

@login_required
def end_project(request, id):
    project = models.Project.objects.get(id=int(id))

    devs_id_list = []
    for dev_id in project.developers_list:
        devs_id_list.append(dev_id[0])
    devs_id_list.append(request.user.id)

    devs_profile = Profile.objects.filter(id__in=devs_id_list)
    
    # mark project filed completed
    project.is_active = False
    project.save()

    # mark develpers field complete
    for dev_profile in devs_profile:
        dev_profile.projects_completed.append(int(id))
        dev_profile.projects_working.remove(int(id))
        dev_profile.save()

    return redirect("/projects/" + str(id) + "/")

@login_required
def restart_project(request, id):
    project = models.Project.objects.get(id=int(id))

    devs_id_list = []
    for dev_id in project.developers_list:
        devs_id_list.append(dev_id[0])
    devs_id_list.append(request.user.id)

    devs_profile = Profile.objects.filter(id__in=devs_id_list)
    
    # mark project filed completed
    project.is_active = True
    project.save()

    # mark develpers field complete
    for dev_profile in devs_profile:
        dev_profile.projects_completed.remove(int(id))
        dev_profile.projects_restarted.append(int(id))
        dev_profile.projects_working.append(int(id))
        dev_profile.save()

    return redirect("/projects/" + str(id) + "/")

@login_required
def user_projects_bookmarked(request, id):
    try:
        profile = Profile.objects.get(user__id=id)
        projects = models.Project.objects.filter(id__in=profile.projects_bookmarked)
        for project in projects:
            project.language = str(project.language).split(',')
        project_form = forms.ProjectForm()
        context = {
            'project_form': project_form,
            'projects': projects,
            'projects_bookmarked': profile.projects_bookmarked
        }
        return render(request, 'projects/index.html', context=context)
    except:
        return redirect("/users/profile/")

@login_required
def user_working_projects(request, id):
    try:
        profile = Profile.objects.get(user__id=id)
        projects = models.Project.objects.filter(id__in=profile.projects_working)
        for project in projects:
            project.language = str(project.language).split(',')
        project_form = forms.ProjectForm()
        context = {
            'project_form': project_form,
            'projects': projects,
            'projects_bookmarked': profile.projects_bookmarked
        }
        return render(request, 'projects/index.html', context=context)
    except:
        return redirect("/users/profile/")

@login_required
def user_requested_projects(request, id):
    try:
        profile = Profile.objects.get(user__id=id)
        projects = models.Project.objects.filter(id__in=profile.projects_requested)

        for project in projects:
            project.language = str(project.language).split(',')
        project_form = forms.ProjectForm()
        context = {
            'project_form': project_form,
            'projects': projects,
            'projects_bookmarked': profile.projects_bookmarked
        }
        return render(request, 'projects/index.html', context=context)
    except:
        return redirect("/users/profile/")

@login_required
def user_requests_rejected(request, id):
    try:
        profile = Profile.objects.get(user__id=id)
        projects = models.Project.objects.filter(id__in=profile.projects_rejected)

        for project in projects:
            project.language = str(project.language).split(',')
        project_form = forms.ProjectForm()
        context = {
            'project_form': project_form,
            'projects': projects,
            'projects_bookmarked': profile.projects_bookmarked
        }
        return render(request, 'projects/index.html', context=context)
    except:
        return redirect("/users/profile/")

@login_required
def projects_created(request, id):
    try:
        profile = Profile.objects.get(user__id=id)
        projects = models.Project.objects.filter(id__in=profile.projects_created)

        for project in projects:
            project.language = str(project.language).split(',')

        project_form = forms.ProjectForm()
        context = {
            'project_form': project_form,
            'projects': projects,
            'projects_bookmarked': profile.projects_bookmarked
        }
        return render(request, 'projects/index.html', context=context)
    except:
        return redirect('/users/profile/')

@login_required
def projects_completed(request, id):
    try:
        profile = Profile.objects.get(user__id=id)
        projects = models.Project.objects.filter(id__in=profile.projects_completed)

        for project in projects:
            project.language = str(project.language).split(',')

        project_form = forms.ProjectForm()
        context = {
            'project_form': project_form,
            'projects': projects,
            'projects_bookmarked': profile.projects_bookmarked
        }
        return render(request, 'projects/index.html', context=context)
    except:
        return redirect('/users/profile/')
    
@login_required
def kick_out_dev(request):
    dev_id = int(request.GET.get('dev_id'))
    project_id = int(request.GET.get('project_id'))
    dev_name = request.GET.get('dev_name')

    project = models.Project.objects.get(id=project_id)
    dev_details = [str(dev_id), dev_name]
    if dev_details in project.developers_list:
        project.developers_list.remove(dev_details)
        project.save()

        profile = Profile.objects.get(user__id=dev_id)
        profile.projects_working.remove(project_id)
        if project_id in profile.projects_completed:
            profile.projects_completed.remove(project_id)
        profile.save()
        return HttpResponse('removed')


@login_required
def invite_devs(request):
    dev_id = int(request.GET.get('dev_id'))
    project_id = int(request.GET.get('project_id'))

    project = models.Project.objects.get(id=project_id)
    profile = Profile.objects.get(user__id=dev_id)
    if not dev_id in project.developers_request_accepted and not dev_id in project.developers_request_rejected:
        if not dev_id in project.developers_requested and not project_id in profile.project_requests_inbox:
            profile.project_requests_inbox.append(project_id)
            profile.save()
            project.developers_requested.append(dev_id)
            project.save()
            return HttpResponse(profile.user.username + ' Invited')

        return HttpResponse(profile.user.username + ' Already Invited')
        
    elif dev_id in project.developers_request_rejected:
            profile.project_requests_inbox.append(project_id)
            profile.save()
            project.developers_requested.append(dev_id)
            project.save()
            return HttpResponse(profile.user.username + 'is invited again')

    elif dev_id in project.developers_request_accepted:
        return HttpResponse('Is already a developer')
    
    elif [str(dev_id), profile.user.username] in project.developers_list:
        return HttpResponse('Is already a developer')

@login_required
def cancel_invite(request):
    user_id = int(request.GET.get('user_id'))
    project_id = int(request.GET.get('project_id'))

    project =  models.Project.objects.get(id=project_id)
    profile = Profile.objects.get(user__id=user_id)

    if user_id in project.developers_requested:
        project.developers_requested.remove(user_id)
        project.save()

    if project_id in profile.project_requests_inbox:
        profile.project_requests_inbox.remove(project_id)
        profile.save()
    
    return HttpResponse('cancelled')