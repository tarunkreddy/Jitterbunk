# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from .forms import BunkForm
from .models import Bunk, UserProfile


def display_index(request, page_id=None):
    template_name = 'bunker/index.html'
    context_object_name = 'latest_bunks'
    num_bunks_per_page = 20
    if (page_id):
        start_index = int(page_id) * num_bunks_per_page
        end_index = start_index + num_bunks_per_page
        next_page = int(page_id) + 1
        prev_page = int(page_id) - 1

    else:
        start_index = 0
        end_index = num_bunks_per_page
        next_page = 1
        prev_page = -1
    numBunks = Bunk.objects.count()
    if (end_index + 1 > numBunks):
        next_page = -1

    bunks = Bunk.objects.filter(time__lte=timezone.now()).order_by('-time')[start_index:end_index]
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(userprofile=request.user.id)
    else:
        current_user = ""
    return render(request, 'bunker/index.html', {'current_user': current_user, 'latest_bunks': bunks, 'next_page': next_page, 'prev_page': prev_page})

class PersonalView(generic.DetailView):
    model = UserProfile
    template_name = 'bunker/personal.html'
    context_object_name = 'personal_info'
    def get_context_data(self, **kwargs):
        context = super(PersonalView, self).get_context_data(**kwargs)
        context['personal_bunks'] = Bunk.objects.filter(Q(from_user=context['personal_info']) | Q(to_user=context['personal_info'])).order_by('-time')
        return context

def send_bunk(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    if request.method == 'POST':
        form = BunkForm(request.POST)
        if form.is_valid():
            new_bunk = form.save(commit=False)
            new_bunk.from_user = user
            new_bunk.time = timezone.now()
            new_bunk.save()
            #return HttpResponseRedirect('/bunker/bunk-submitted')
            return HttpResponseRedirect(reverse('bunker:personal', args=(user.id,)))
        else:
            return HttpResponse("FAILURE!")
    else:
        form = BunkForm()

    return render(request, 'bunker/bunk.html', {'form': form})

def get_stats(request, user_id=None):
    if user_id:
        user = UserProfile.objects.get(id=user_id)
        num_bunks_sent = Bunk.objects.filter(from_user=user).count()
        num_bunks_rcvd = Bunk.objects.filter(to_user=user).count()
        usr_bunks_from = UserProfile.objects.filter(bunk__from_user=user).annotate(num_bunks_from=Count('bunk')).order_by('-num_bunks_from')
        usr_bunks_to = Bunk.objects.filter(to_user=user).values('from_user').annotate(num_bunks_to=Count('from_user')).order_by('-num_bunks_to')
        for bunk in usr_bunks_to:
            bunk['from_user'] = UserProfile.objects.get(id=bunk['from_user'])

    return render(request, 'bunker/stats.html', {'personal_info': user, 'num_bunks_sent': num_bunks_sent, 'num_bunks_rcvd': num_bunks_rcvd,
        'usr_bunks_from': usr_bunks_from, 'usr_bunks_to': usr_bunks_to})


