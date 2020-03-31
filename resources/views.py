from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
import requests
from bs4 import BeautifulSoup
import json
import projects.models as proj_models
from users.models import Profile

# Create your views here.
@login_required
def index(request):
    try:
        profile = Profile.objects.get(user=request.user)
        form = forms.ResourceForm(request.POST or None)
        if(request.method == "POST"):
            resource = form.save(commit=False)
            
            # extracting meta tags for the link posted
            link = resource.link
            data = requests.get(link).text
            soup = BeautifulSoup(data, "html.parser")

            # meta tags for og protocol
            title_og_tag = soup.find('meta', attrs={"property":"og:title"})
            description_og_tag = soup.find('meta', attrs={"property":"og:description"})
            img_og_tag = soup.find('meta', attrs={"property":"og:image"})
            
            # getting title from the given link
            if(title_og_tag):
                resource.title = title_og_tag['content']
            else:
                title_twitter_tag = soup.find('meta', attrs={'name': "twitter:title"})
                if(title_twitter_tag):
                    resource.title = title_twitter_tag['content']
                else:
                    title_tag = soup.find('meta', attrs={"name" : "title"})
                    if(title_tag):
                        resource.title = title_tag['content']
                    else:
                        resource.title = soup.title.string
            
            # getting description from the given link
            if(description_og_tag):
                resource.description = description_og_tag['content']
            else:
                description_twitter_tag = soup.find('meta', attrs={"name": "twitter:description"})
                if(description_twitter_tag):
                    resource.description = description_twitter_tag['content']
                else:
                    description_tag = soup.find('meta', attrs={"name" : "description"})
                    if(description_tag):
                        resource.description = description_tag['content']
                    else:
                        resource.description = "No Description Found"
            
            # getting img src for the given link
            if(img_og_tag):
                resource.img_src = img_og_tag['content']
            else:
                img_twitter_tag = soup.find('meta', attrs={"name": "twitter:image"})
                if(img_twitter_tag):
                    resource.img_src = img_twitter_tag['content']
                else:
                    resource.img_src = "null"
            resource.author = request.user
            resource.save()
            profile.resources_added.append(resource.id)
            profile.save()

        resources = models.Resource.objects.all()
        for resource in resources:
            resource.tag = str(resource.tag).split(",")

        user_created_projects = []
        if(len(profile.projects_created) > 0):
            temp_user_created_projects = proj_models.Project.objects.filter(id__in=profile.projects_created)
            for project_created in temp_user_created_projects:
                    user_created_projects.append([project_created.id, project_created.title])
        
        context = {
            'user_created_projects': user_created_projects,
            'form': form,
            'resources': resources,
            'user_levels': models.USER_LEVEL,
            'resources_bookmarked': profile.resources_bookmarked,
            'project_languages': proj_models.PROJECT_LANGUAGES
        }
        
        return render(request, 'resources/index.html', context=context)
    except:
        return redirect('/users/profile/')


@login_required
def resource_exp_filter(request, level):
    resources = models.Resource.objects.filter(user_level = level)
    for resource in resources:
        resource.tag = str(resource.tag).split(",")
    form = forms.ResourceForm()

    context = {
        'form': form,
        'resources': resources,
        'user_levels': models.USER_LEVEL,
        'project_languages': proj_models.PROJECT_LANGUAGES
    }

    return render(request, 'resources/index.html', context=context)

@login_required
def resource_lang_filter(request, lang):
    for key, value in proj_models.PROJECT_LANGUAGES:
        if(value==lang.strip()):
            lang = key
    resources = models.Resource.objects.filter(tag__contains=lang)
    for resource in resources:
        resource.tag = str(resource.tag).split(",")

    form = forms.ResourceForm()

    context = {
        'form': form,
        'resources': resources,
        'user_levels': models.USER_LEVEL,
        'project_languages': proj_models.PROJECT_LANGUAGES
    }

    return render(request, 'resources/index.html', context=context)

@login_required
def bookmark_resource(request):
    try:
        profile = Profile.objects.get(user=request.user)
        resource_id = int(request.GET.get('resource_id'))
        if(resource_id in profile.resources_bookmarked):
            profile.resources_bookmarked.remove(resource_id)
            profile.save()
            return HttpResponse('resource-removed')
        else:
            profile.resources_bookmarked.append(resource_id)
            profile.save()
            return HttpResponse('resource-added')
    except:
        return HttpResponse('redirect')
 
@login_required
def user_resources_bookmarked(request, id):
    profile = Profile.objects.get(user__id=id)
    resources = models.Resource.objects.filter(id__in=profile.resources_bookmarked)
    for resource in resources:
        resource.tag = str(resource.tag).split(',')
    resource_form = forms.ResourceForm()
    context = {
        'form': resource_form,
        'resources': resources,
        'resources_bookmarked': profile.resources_bookmarked,
        'user_levels': models.USER_LEVEL,
        'project_languages': proj_models.PROJECT_LANGUAGES
    }

    return render(request, 'resources/index.html', context=context)

@login_required
def resources_added(request, id):
    profile = Profile.objects.get(user__id=id)
    resources = models.Resource.objects.filter(id__in=profile.resources_added)
    for resource in resources:
        resource.tag = str(resource.tag).split(',')
    resource_form = forms.ResourceForm()
    context = {
        'form': resource_form,
        'resources': resources,
        'resources_bookmarked': profile.resources_bookmarked,
        'user_levels': models.USER_LEVEL,
        'project_languages': proj_models.PROJECT_LANGUAGES
    }

    return render(request, 'resources/index.html', context=context)

@login_required
def add_resource_to_project(request):
    project_id = int(request.GET.get('project_id'))
    resource_id = int(request.GET.get('resource_id'))
    project = proj_models.Project.objects.get(id=project_id)
    if request.user == project.author:
        if(resource_id in project.project_resources):
            return HttpResponse('resource already exists')
        else:
            project.project_resources.append(resource_id)
            project.save()
            return HttpResponse('resource added successfully to ' + project.title)

@login_required
def remove_resource_from_project(request):
    project_id = int(request.GET.get('project_id'))
    resource_id = int(request.GET.get('resource_id'))
    project = proj_models.Project.objects.get(id=project_id)
    if(resource_id in project.project_resources):
        project.project_resources.remove(resource_id)
        project.save()
        return HttpResponse('removed')
    else:
        return HttpResponse(0)

@login_required
def project_resources(request, id):
    project = proj_models.Project.objects.get(id=id)
    resources = models.Resource.objects.filter(id__in=project.project_resources)
    profile = Profile.objects.get(user=request.user)

    for resource in resources:
        resource.tag = str(resource.tag).split(',')

    context = {
        'project_id': project.id,
        'is_project_resources': True,
        'resources': resources,
        'resources_bookmarked': profile.resources_bookmarked,
        'user_levels': models.USER_LEVEL,
        'project_languages': proj_models.PROJECT_LANGUAGES
    }

    request_user = [str(request.user.id), request.user.username]
    if(request_user in project.developers_list):
        context['is_developer'] = True

    return render(request, 'resources/index.html', context=context)