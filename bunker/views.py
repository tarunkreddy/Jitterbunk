# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from .forms import BunkForm
from .models import Bunk, UserProfile


class IndexView(generic.ListView):
    template_name = 'bunker/index.html'
    context_object_name = 'latest_bunks'

    def get_queryset(self):
        return Bunk.objects.filter(time__lte=timezone.now()).order_by('-time')[:20]

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

def bunk_submitted(request):
    return HttpResponse("Success!")


