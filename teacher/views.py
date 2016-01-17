#-*- coding: UTF-8 -*- 
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from .models import *

def table(request):
	if not request.user.is_authenticated():
		return render(request,'nopass.html')
	else:
		x = teacher.objects.all()
		return render(request,'teacherlist.html',{'teacher_list':x})

def detail(request,x):
	if not request.user.is_authenticated():
		return render(request,'nopass.html')
	else:
		try:
			x=int(x)
		except ValueError:
			raise Http404()
		detail = teacher.objects.get(id=x)

		TeacherID = teacher.objects.get(id=x).t_id
		Teacher = get_object_or_404(teacher, id=x)
		if request.method == "POST":
			teacher_add = teacher.objects.get(t_id=TeacherID)
			date_add = request.POST['Datadate']
			time_add = request.POST['Datatime']
			title_add = request.POST['Datatitle']
			urgent_add = request.POST['Urgent']
			appoint1 = appoint(t_id=teacher_add, Appointdate=date_add, Appointtime=time_add, Number=title_add, Urgent=urgent_add)
			appoint1.save()
			return render(request, 'detail.html', locals())
		else:
			teacherevent = event.objects.filter(t_id=x)
			context = {'teacherevent': teacherevent, }
			return render(request, 'detail.html', locals())

def main(request):
	if not request.user.is_authenticated():
		return render(request,'nopass.html')
	else:
		s=request.user
		return render_to_response('main.html',locals(),context_instance=RequestContext(request))


def search(request):
	if not request.user.is_authenticated():
		return render(request,'nopass.html')
	else:
		x = teacher.objects.filter(name=request.GET['q'])
		return render(request,'teacherlist.html',{'teacher_list':x})

@csrf_protect
def alogin(request):
	errors=[]
	account=None
	password=None
	if request.user.is_authenticated():
		if request.user.has_perm('auth.is_teacher'):
			return HttpResponseRedirect('/update')
		else:
			return HttpResponseRedirect('/main')
	else:
		if request.method == 'POST':
			if not request.POST.get('account'):
				errors.append('Please Enter account')
			else:
				account = request.POST.get('account')

			if not request.POST.get('password'):
				errors.append('Please Enter password')
			else:
				password = request.POST.get('password')

			if account is not None and password is not None:
				user = authenticate(username=account,password=password)
				if user is not None:
					if user.is_active :
						login(request,user)
						if user.has_perm('auth.is_teacher') :
							return HttpResponseRedirect('/update')
						else:
							return HttpResponseRedirect('/main')
					else:
						errors.append('disabled account')
				else:
					errors.append('invalid user')
		return render_to_response('account/login.html',{'errors':errors}, context_instance=RequestContext(request))

@csrf_protect
def student_register(request):  
	errors= []  
	account=None  
	password=None  
	password2=None  
	email=None  
	CompareFlag=False  
  
	if request.method == 'POST':  
		if not request.POST.get('account'):  
			errors.append('Please Enter account')  
		else:  
			account = request.POST.get('account')  
		if not request.POST.get('password'):  
			errors.append('Please Enter password')  
		else:  
			password = request.POST.get('password')
		if not request.POST.get('password2'):  
			errors.append('Please Enter password2')  
		else:  
			password2 = request.POST.get('password2')  
		if not request.POST.get('email'):  
			errors.append('Please Enter email')  
		else:  
			email = request.POST.get('email')
		if password is not None and password2 is not None:  
			if password == password2:  
				CompareFlag = True  
			else :  
				errors.append('password2 is diff password ')  
  
	if account is not None and password is not None and password2 is not None and email is not None and CompareFlag :  
		if User.objects.filter(username=account):
			errors.append('this account already exists, Please change another username')
		else:
			user=User.objects.create_user(account,email,password) 
			user.is_active=True
			permission=Permission.objects.get(name='student')
			user.user_permissions.add(permission)
			user.save()
			return HttpResponseRedirect('../../')
	return render_to_response('account/register.html', {'errors': errors}, context_instance=RequestContext(request))  
  
def alogout(request):  
	if not request.user.is_authenticated():
		return render(request,'nopass.html')
	else:
		logout(request)
		return HttpResponseRedirect('../../')

def recommend(request):
	if not request.user.is_authenticated():
		return render(request,'nopass.html')
	else:
		x=teacher.objects.filter(faculty=request.GET['falcuty'])
		return render(request,'teacherlist.html',{'teacher_list':x})

@csrf_protect
@permission_required('auth.is_teacher', login_url='../')
def update(request):
	name=None
	birth=None
	faculty=None
	detail = teacher.objects.get(t_id=request.user.id)
	
	if 'name' in request.GET:
		name = request.GET.get('name')
		birth = request.GET.get('birth')
		faculty = request.GET.get('faculty')
		detail.name = name 
		detail.birth = birth
		detail.faculty = faculty
		detail.save()
		detail = teacher.objects.get(t_id=request.user.id)
	return render_to_response('update.html', {'detail': detail}, context_instance=RequestContext(request))

@csrf_protect
@permission_required('auth.is_teacher', login_url='../')
def index(request):
	TeacherID = request.user.id
	Teacher = get_object_or_404(teacher, t_id=TeacherID)
	if request.method == "POST":
		teacher_add = teacher.objects.get(t_id=TeacherID)
		date_add = request.POST['Datadate']
		time_add = request.POST['Datatime']
		title_add = request.POST['Datatitle']
		urgent_add = request.POST['Urgent']
		appoint1 = appoint(t_id=teacher_add, Appointdate=date_add, Appointtime=time_add, Number=title_add, Urgent=urgent_add)
		appoint1.save()
		return render(request, "success.html", locals())
	else:
		teacherevent = event.objects.filter(t_id=teacher.objects.get(t_id=TeacherID).id)
		context = {'teacherevent': teacherevent, }
		return render(request, 'index.html', locals())

@csrf_protect
@permission_required('auth.is_teacher', login_url='../')
def aplist(request):
	TeacherID = request.user.id
	Teacher = get_object_or_404(teacher, t_id=TeacherID)

	teacherappointment = appoint.objects.filter(t_id=teacher.objects.get(t_id=TeacherID).id)
	template = loader.get_template('all.html')

	if request.method == "POST":
		teacher_add = teacher.objects.get(t_id=TeacherID)
		date_add = request.POST['Datadate']
		time_add = request.POST['Datatime']
		title_add = request.POST['Datatitle']
		appoint1 = event(t_id=teacher_add, Datadate=date_add, Datatime=time_add, Datatitle=title_add)
		appoint1.save()
		return HttpResponseRedirect("/index/")
	else:
		context = RequestContext(request, {'Teacher': Teacher, 'tappointment': teacherappointment, })
		return HttpResponse(template.render(context))

@csrf_protect
@permission_required('auth.is_teacher', login_url='../')
def ap_detail(request, appointID):
	TeacherID = request.user.id
	b = get_object_or_404(teacher, t_id=TeacherID)
	a = get_object_or_404(appoint, pk=appointID)

	template = loader.get_template('detail.html')
	context = RequestContext(request, { 'b': b, 'a': a, })

	if request.method == "POST":
		operate = request.POST['operate']
		if operate == u'接受预约':
			id_1 = a.t_id
			date_1 = a.Appointdate
			time_1 = a.Appointtime
			title_1 = a.Number
			a.save()
			event1 = event(t_id = id_1, Datadate = date_1, Datatime = time_1, Datatitle = title_1 + u" 预约")
			event1.save()
			a.delete()
			return HttpResponseRedirect("/all/")
		elif operate == u'取消预约':
			a = appoint.objects.get(appointID = appointID)
			a.delete()
			return HttpResponseRedirect("/all/")
	return render(request, 'appoint_detail.html', locals())