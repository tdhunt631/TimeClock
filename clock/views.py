from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, UpdateView, CreateView, DeleteView, DetailView
from clock.models import Record, Project, UserStatus
from clock.forms import AddRecordForm, UpdateRecordForm, DateRangeForm, AddNoteForm
from django.utils import timezone
from django.views.generic.edit import BaseCreateView

#adds ability to decorate a class 
def class_view_decorator(decorator):
	def my_decorator(View):
		View.dispatch = method_decorator(decorator)(View.dispatch)
		return View
	return my_decorator


@class_view_decorator(login_required)
class AddNote(UpdateView):
	model = Record
	form_class=AddNoteForm
	template_name_suffix = '-note-form'

	def get_object(self):
		return get_object_or_404(Record, user=self.request.user, pk=self.kwargs['pk'])


@login_required
def clockOut(request, rec_id):
	u = get_object_or_404(User, id=request.user.id)
	u.userstatus.status = False
	record = get_object_or_404(Record, id=rec_id)
	record.endTime = timezone.now()
	record.save()
	return HttpResponseRedirect(reverse('clock:add-note', args=(rec_id,)))


@class_view_decorator(login_required)
class Punches(ListView):
	model = Record
	context_object_name = 'records'

	def get_context_data(self, **kwargs):
		u = User.objects.get(id=self.request.user.id) 
		status = u.userstatus.status 
		context = super(Punches, self).get_context_data(**kwargs)
		context['status'] = status
		return context

	def get_queryset(self):
		records = Record.objects.filter(user = self.request.user).order_by('-startTime')
		if self.request.GET.items():
			date_range = DateRangeForm(self.request.GET)
			if date_range.is_valid():
				cd = date_range.cleaned_data
				records = records.filter(start_time__range=[cd.get('from_date'), cd.get('to_date')])
		return records


@class_view_decorator(login_required)
class RecordUpdate(UpdateView):
	form_class=UpdateRecordForm

	def get_object(self):
		return get_object_or_404(Record, user=self.request.user, pk=self.kwargs['pk'])


@class_view_decorator(login_required)
class RecordAdd(CreateView):
	form_class=AddRecordForm
	template_name = 'record_add.html'

	def get(self,request,*args,**kwargs):
		u = User.objects.get(id=self.request.user.id) 
		if u.userstatus.status == True:
			return HttpResponseRedirect('/')
		else:
			self.object = None
		return super(BaseCreateView, self).get(request, *args, **kwargs)

	def get_form(self, form_class):
		form = super(RecordAdd, self).get_form(form_class)
		form.instance.user = self.request.user
		form.instance.startTime = timezone.now()
		return form	

	def form_valid(self, form):	
		u = User.objects.get(id=self.request.user.id) 
		u.userstatus.status = True
		return super(RecordAdd, self).form_valid(form)

