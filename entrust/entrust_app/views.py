from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import password_reset, password_reset_confirm
from datetime import datetime
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from entrust_app.models import *
from entrust_app.models import *
from django.core.mail import send_mail
from forms import *
from entrust_app.models import *
from django.conf import settings
from django.contrib import auth
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
from django.utils.http import base36_to_int, is_safe_url
from django.shortcuts import resolve_url

def home(request):
	return render (request, 'entrust_app/landing.html')

def resources(request):
	return render (request, 'entrust_app/resources.html')


def signup(request):
	
	if request.method=='POST':
		form=signupform(request.POST)
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
        		lastname = form.cleaned_data['lastname']
        		email = form.cleaned_data['email']
        		nickname = form.cleaned_data['nickname']
        		password= form.cleaned_data['password']
			password1= form.cleaned_data['password1']
			doorno = form.cleaned_data['doorno']
        		street = form.cleaned_data['street']
        		city = form.cleaned_data['city']
        		state = form.cleaned_data['state']
        		country = form.cleaned_data['country']
        		pincode = form.cleaned_data['pincode']
        		phoneno = form.cleaned_data['phoneno']
        		dateofbirth = form.cleaned_data['dateofbirth']
	
			user = User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=nickname,password=password)
			user.is_active=False
			user.save()

			user_info = User_information.objects.create(user=user,phone_number=phoneno,dob=dateofbirth,door_number=doorno,street=street,city=city,state=state,country=country,pincode=pincode)
			user_info.save()
		
			token = default_token_generator.make_token(user)
			email_body = """
Entrust welcomes you..Please click the link below to
verify your email address and complete the registration of your account. If you think you received this mail by mistake , Kindly ignore it:
http://%s%s
""" % (request.get_host(),
       reverse('confirm', args=(user.username, token)))
			send_mail( subject = "Entrust - Please verify your email account", message = email_body, from_email = settings.EMAIL_HOST_USER, recipient_list = [email])
			message = "Registration successfull! Check your mail!" 
			# return redirect('/entrust-app/')
			return render(request,'entrust_app/login.html',{'message': message})
		else:
			return render(request,'entrust_app/signup.html',{'form':form})

		#save to the other model the rest of the fields
	else:
		form = signupform()
		return render(request,'entrust_app/signup.html',{'form':form})

def loginuser(request):
	
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request,user)
			user_req = User.objects.get(username=request.user.username)
			usertasks=Service.objects.exclude(user_ordering=user_req)
			return redirect('/entrust-app/home/?id=1')
	#		return render (request, 'entrust_app/homepage.html',{'tasks_name':usertasks})

		#	return render(request,'entrust_app/homepage.html')
		else:
			return render(request,'entrust_app/login.html',{'registration_message':"Username and Password do not match"})
				
	else:
		return render(request,'entrust_app/login.html')

def confirmemail(request, username, token):
        user = get_object_or_404(User, username=username)

        # Send 404 error if token is invalid
        if not default_token_generator.check_token(user, token):
                raise Http404

        # Otherwise token was valid, activate the user.
        user.is_active = True
        user.save()
	return redirect('/entrust-app/')
	# return homepage for that user after logging him in

@login_required
def homepage(request):
	

	if request.GET.get('id'):
		id_home = request.GET.get('id')
		if id_home == "1":
			user_req  = User.objects.get(username=request.user.username)
			user_address = User_information.objects.get(user=request.user)
			usertasks=Service.objects.exclude(user_ordering=user_req).filter(pincode=user_address.pincode)
			search_area="Neighbourhood"
			return render (request, 'entrust_app/homepage.html',{'tasks_name':usertasks, 'user_info' : user_req,'search_area':search_area})
		if id_home == "2":
			user_req  = User.objects.get(username=request.user.username)
			user_address = User_information.objects.get(user=request.user)
			usertasks=Service.objects.exclude(user_ordering=user_req).filter(city=user_address.city)
			search_area="Intracity"
			return render (request, 'entrust_app/homepage.html',{'tasks_name':usertasks, 'user_info' : user_req,'search_area':search_area})
		if id_home == "3":
			user_req  = User.objects.get(username=request.user.username)
			user_address = User_information.objects.get(user=request.user)
			usertasks=Service.objects.exclude(user_ordering=user_req).filter(country=user_address.country)
			search_area="Intercity"
			return render (request, 'entrust_app/homepage.html',{'tasks_name':usertasks, 'user_info' : user_req,'search_area':search_area})

@login_required
def update(request):
	

	if request.GET.get('id'):
		id_home = request.GET.get('id')
		if id_home == "1":
			user_req  = User.objects.get(username=request.user.username)
			user_address = User_information.objects.get(user=request.user)
			usertasks=Service.objects.exclude(user_ordering=user_req).filter(pincode=user_address.pincode)
			return render (request, 'entrust_app/update.xml',{'tasks_name':usertasks},content_type='application/xml')
		if id_home == "2":
			user_req  = User.objects.get(username=request.user.username)
			user_address = User_information.objects.get(user=request.user)
			usertasks=Service.objects.exclude(user_ordering=user_req).filter(city=user_address.city)
			return render (request, 'entrust_app/update.xml',{'tasks_name':usertasks},content_type='application/xml')
		if id_home == "3":
			user_req  = User.objects.get(username=request.user.username)
			user_address = User_information.objects.get(user=request.user)
			usertasks=Service.objects.exclude(user_ordering=user_req).filter(country=user_address.country)
			return render (request, 'entrust_app/update.xml',{'tasks_name':usertasks},content_type='application/xml')




@login_required
def task_entrust(request):
	user_req = User.objects.get(username=request.user.username)
	usertasks=Service.objects.filter(user_ordering=user_req)
	return render(request,'entrust_app/task_entrust.html',{'tasks_name':usertasks, 'username' : request.user.username})

@login_required
def task_accept(request, task_id):
	context = []
	task_info = Service.objects.get(id=task_id)
	user_info = User.objects.get(username = request.user.username)
	already_accepted = 0
	exists = TaskQueue.objects.filter(task = task_info.id, user = request.user).count()
	if exists >= 1:
		already_accepted = 1
		discussion_obj = Discussion.objects.get(participant1 = task_info.user_ordering.username, participant2 = request.user.username, task_id = task_id)
		discussion_id = discussion_obj.id;
		people_in_queue = TaskQueue.objects.filter(task = task_info.id).count()
		address = task_info.country+","+task_info.state+","+task_info.city+","+task_info.street+","+task_info.door_number
		context = {'task_info' : task_info, 'first_name' : request.user.first_name, 'user_info' : user_info, 'already_accepted' : already_accepted, 'address' : address, 'people_in_queue':people_in_queue, 'discussion_id' : discussion_id}
		return render (request, 'entrust_app/task_accept.html', context)

	people_in_queue = TaskQueue.objects.filter(task = task_info.id).count()
	address = task_info.country+","+task_info.state+","+task_info.city+","+task_info.street+","+task_info.door_number
	context = {'task_info' : task_info, 'first_name' : request.user.first_name, 'user_info' : user_info, 'already_accepted' : already_accepted, 'address' : address, 'people_in_queue':people_in_queue}
	
	return render (request, 'entrust_app/task_accept.html', context)

@login_required
#LOGOUT THE USER
def logout_view(request):
        logout(request)
        return redirect('/entrust-app/')

@login_required
@csrf_exempt
def post_task(request):
	if request.method=='POST':
		name=request.POST['name']
		tasktype=request.POST['tasktype']
		username=request.user.username
		door=request.POST['door']
		street=request.POST['street']
		city=request.POST['city']
		state=request.POST['state']
		pin=request.POST['pin']
		deadline=request.POST['deadline']
		value=request.POST['value']
		description=request.POST['description']
		country="United States"
		task_date = datetime.now()
		user_req = User.objects.get(username=request.user.username)
		taskmodel=Service.objects.create(task_name=name,door_number=door,street=street,city=city,pincode=pin,state=state,money_paid=int(value),task_details=description,task_type=tasktype,country=country,user_ordering=user_req,deadline=deadline, task_post_date = task_date, task_status = "open")
		taskmodel.save()
		usertasks=Service.objects.filter(user_ordering=user_req).order_by('task_post_date').reverse()
		user_obj = User_information.objects.get(user=request.user)
		first_name = user_obj.user.first_name
		context = {'prevtasks':usertasks, 'username' : request.user.username}
	#	return render(request,'entrust_app/task_entrust.html',{'tasks_name':usertasks, 'first_name' : first_name})
		return render(request,'entrust_app/tasks.xml',context,content_type='application/xml')
	else:
		usertasks = Service.objects.filter(user_ordering=request.user)
		user_obj = User_information.objects.get(user=request.user)
		first_name = user_obj.user.first_name
		country="United States"
		# To display user address for MAP		
		user_address = User_information.objects.get(user=request.user)
		address = country+","+user_address.state+","+user_address.city+","+user_address.street+","+user_address.door_number
		context = {'tasks_name':usertasks, 'first_name' : first_name,'address':address, 'username' : request.user.username}

		return render(request,'entrust_app/task_entrust.html', context)

def password_reset(request, is_admin_site=False,
                   template_name='entrust_app/registration/password_reset_form.html',
                   email_template_name='entrust_app/registration/password_reset_email.html',
                   subject_template_name='entrust_app/registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('entrust_app.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': settings.EMAIL_HOST_USER,
				'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def password_reset_done(request,
                        template_name='entrust_app/registration/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
                           template_name='entrust_app/registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb36 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('entrust_app.views.password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
        user = UserModel._default_manager.get(pk=uid_int)
    except (ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_complete(request,
                            template_name='entrust_app/registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL)
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='entrust_app/registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('entrust_app.views.password_change_done')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def password_change_done(request,
                         template_name='entrust_app/registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='entrust_app/registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('entrust_app.views.password_change_done')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def password_change_done(request,
                         template_name='entrust_app/registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
@login_required
def viewprofile(request, u_name):
	context = []
	user_obj = User.objects.get(username = u_name)
	user_obj = User_information.objects.get(user = user_obj)
	full_name = user_obj.user.first_name + ' ' + user_obj.user.last_name
	username = request.user.username
	first_name = request.user.first_name
	context = { 'user_info' : user_obj, 'full_name' : full_name, 'username' : username, 'first_name' : first_name }
	return render (request, 'entrust_app/profile.html', context)

@login_required
def get_photo(request, u_name):

	if u_name:
		user_obj = User.objects.get(username = u_name)
	else:
		user_obj = request.user
	user_info = User_information.objects.get(user=user_obj)
	if not user_info.picture:
		image_data = open(settings.PROJECT_ROOT+"../entrust_app/static/media/person.png", "rb").read()
		return HttpResponse(image_data, mimetype="image/png")
	
	content_type = guess_type(user_info.picture.name)
	return HttpResponse(user_info.picture, mimetype=content_type)

@login_required
def editprofile(request):
	
	user_obj = User_information.objects.get(user=request.user)
	full_name = user_obj.user.first_name + ' ' + user_obj.user.last_name

	if request.method == 'POST':
		form = UserInforForm (request.POST, request.FILES, instance = user_obj)
		if not form.is_valid():
			context = {'form':form, 'first_name' : request.user.first_name, 'full_name' : full_name}
			return render(request, 'entrust_app/edit_profile.html', context)
		form.save()
		return redirect("profile/"+request.user.username)

	else:
		form = UserInforForm(instance = User_information.objects.get(user=request.user))
		context = {'form':form, 'first_name' : request.user.first_name, 'full_name' : full_name, 'user_info' : user_obj}
		return render(request, 'entrust_app/edit_profile.html', context)

@login_required
def search(request):
	
	if request.GET.get("search"):
		search_term = request.GET.get("search")
		search_area = request.GET.get("search_area")
		user_req  = User.objects.get(username=request.user.username)
		user_address = User_information.objects.get(user=request.user)
		
		if search_area=="Neighbourhood":
			searchtasks=Service.objects.exclude(user_ordering=user_req).filter(pincode=user_address.pincode).filter(task_details__icontains=search_term)
			search_count = Service.objects.exclude(user_ordering=user_req).filter(pincode=user_address.pincode).filter(task_details__icontains=search_term).count()
			return render (request, 'entrust_app/task_search.html',{'tasks_name':searchtasks, 'user_info' : user_req,'search_area':search_area, 'keyword' : search_term, 'search_count' : search_count})

		if search_area=="Intracity":
			searchtasks=Service.objects.exclude(user_ordering=user_req).filter(city=user_address.city).filter(task_details__icontains=search_term)
			search_count = Service.objects.exclude(user_ordering=user_req).filter(city=user_address.city).filter(task_details__icontains=search_term).count()
			return render (request, 'entrust_app/task_search.html',{'tasks_name':searchtasks, 'user_info' : user_req,'search_area':search_area, 'keyword' : search_term, 'search_count' : search_count})

		if search_area=="Intercity":
			searchtasks=Service.objects.exclude(user_ordering=user_req).filter(country=user_address.country).filter(task_details__icontains=search_term)
			search_count = Service.objects.exclude(user_ordering=user_req).filter(country=user_address.country).filter(task_details__icontains=search_term).count()
			return render (request, 'entrust_app/task_search.html',{'tasks_name':searchtasks, 'user_info' : user_req,'search_area':search_area, 'keyword' : search_term, 'search_count':search_count })


@login_required
def accept_list(request):
	

	context=[]
	task_ids = TaskQueue.objects.filter(user=request.user).values_list('task',flat=True)
	task_list = Service.objects.filter(id__in = task_ids)
	task_list_count = Service.objects.filter(id__in = task_ids).count()
	user_req  = User.objects.get(username=request.user.username)
	context = {'tasks_name':task_list,'user_info':user_req, 'task_list_count' : task_list_count}
	return render (request,'entrust_app/accepted_list.html',context)

			
@login_required
def task_queue(request, task_id):
	context = []
	task_info = Service.objects.get(id=task_id)
	user_info = User.objects.get(username = request.user.username)
	address = task_info.country+","+task_info.state+","+task_info.city+","+task_info.street+","+task_info.door_number
	# new discussion, so create a discussion
	new_discussion = Discussion(participant1 = task_info.user_ordering.username, participant2 = request.user.username, task_id = task_id)
	new_discussion.save()

	task_q_obj = TaskQueue(user=request.user, task=task_info.id, discussion_id = new_discussion.id)
	task_q_obj.save()
	already_accepted = 1
	people_in_queue = TaskQueue.objects.filter(task = task_info.id).count()

	discussion_id = new_discussion.id;

	context = {'task_info' : task_info, 'first_name' : request.user.first_name, 'user_info' : user_info, 'people_in_queue' : people_in_queue, 'already_accepted' : already_accepted, 'address' : address, 'discussion_id' : discussion_id}
	
	return render (request, 'entrust_app/task_accept.html', context)

@login_required
def task_discussion(request, discussion_id):
	context = []

	discussion_obj = Discussion.objects.get(id=discussion_id)
	task_info = Service.objects.get(id=discussion_obj.task_id)

	user_info = User.objects.get(username = request.user.username)
	people_in_queue = TaskQueue.objects.filter(task = task_info.id).count()
	address = task_info.country+","+task_info.state+","+task_info.city+","+task_info.street+","+task_info.door_number

	# use something like this to SHOW APPROVAL already_approval = 0
	# might have to add a field

	if (request.method == 'GET') or (len(request.POST['comment_info']) == 0) :
		comments = Comments.objects.filter(discussion_id = discussion_id)

		context = {'task_info' : task_info, 'first_name' : request.user.first_name, 'user_info' : user_info, 'address' : address, 'people_in_queue':people_in_queue, 'username' : request.user.username, 'comments' : comments, 'task_id' : task_info.id, 'discussion_id' : discussion_id}

		return render (request, 'entrust_app/task_discussion.html', context)

	else:
		if len(request.POST['comment_info']) > 0:
			new_comment = Comments(comment_info = request.POST['comment_info'], comment_date = datetime.now(), comment_owner = request.user.username, discussion_id = discussion_id, task_id = discussion_obj.task_id)
			new_comment.save()
			comments = Comments.objects.filter(discussion_id = discussion_id)

			context = {'task_info' : task_info, 'first_name' : request.user.first_name, 'user_info' : user_info, 'address' : address, 'people_in_queue':people_in_queue, 'username' : task_info.user_ordering.username, 'comments' : comments, 'discussion_id' : discussion_id}
	
			return render (request, 'entrust_app/task_discussion.html', context)

def viewtasks(request):
	
		user_req  = User.objects.get(username=request.user.username)
		user_address = User_information.objects.get(user=request.user)
		usertasks=Service.objects.filter(user_ordering=user_req)
		task_count = usertasks.count()
		search_area="Neighbourhood"
		return render (request, 'entrust_app/owntask_view.html',{'tasks_name':usertasks, 'user_info' : user_req,'search_area':search_area, 'task_count' : task_count})

def show_queue(request, task_id):
	context = []
	task_info = Service.objects.get(id=task_id)
	user_info = User.objects.get(username = request.user.username)
	people_in_queue = TaskQueue.objects.filter(task = task_id).count()
	doers = TaskQueue.objects.filter(task = task_id)

	address = task_info.country+","+task_info.state+","+task_info.city+","+task_info.street+","+task_info.door_number

	context = {'task_info' : task_info, 'first_name' : request.user.first_name, 'user_info' : user_info, 'address' : address, 'username' : request.user.username, 'people_in_queue' : people_in_queue, 'doers' : doers}
	
	return render (request, 'entrust_app/task_queue.html', context)


def task_approved(request, discussion_id):
	context = []
	discussion_obj = Discussion.objects.get(id=discussion_id)
	discussion_id = discussion_obj.id
	task_id = discussion_obj.task_id
	task_info = Service.objects.get(id=task_id)
	participant2 = User.objects.get(username = discussion_obj.participant2)
	task_info.user_delivering = User_information.objects.get(user = participant2)
	task_info.task_status = "approved"
	task_info.save()
	user_info = User.objects.get(username = request.user.username)
	TaskQueue.objects.filter(task = task_info.id).exclude(user = task_info.user_delivering.user).delete()
	#Discussion.objects.exclude(participant1 = task_info.user_ordering.username, participant2 = task_info.user_delivering.user.username, task_id = task_info.id).delete()
	Discussion.objects.filter(task_id = task_info.id).exclude(participant1 = task_info.user_ordering.username, participant2 = task_info.user_delivering.user.username).delete()
	Comments.objects.filter(task_id = task_info.id).exclude(discussion_id = discussion_id).delete()

	people_in_queue = TaskQueue.objects.filter(task = task_info.id).count()
	address = task_info.country+","+task_info.state+","+task_info.city+","+task_info.street+","+task_info.door_number
	doers = TaskQueue.objects.filter(task = task_id)

	context = {'task_info' : task_info, 'first_name' : request.user.first_name, 'user_info' : user_info, 'address' : address, 'people_in_queue':people_in_queue, 'username' : request.user.username, 'doers' : doers}
	
	return render (request, 'entrust_app/task_queue.html', context)

def task_completed(request, discussion_id):

	context = []

	user_info = User.objects.get(username = request.user.username)

	discussion_obj = Discussion.objects.get(id = discussion_id)
	task_info = Service.objects.get(id=discussion_obj.task_id)
	people_in_queue = TaskQueue.objects.filter(task = task_info.id)
	comments = Comments.objects.filter(discussion_id = discussion_id)

	user_delivering = discussion_obj.participant2;
	user_obj = User.objects.get(username = user_delivering)
	full_name = user_obj.first_name + ' ' + user_obj.last_name

	discussion_obj.delete()
	task_info.delete()
	people_in_queue.delete()
	comments.delete()

	testimonials = Testimonial.objects.filter(user_whoReceived = user_delivering)

	context = {'first_name' : request.user.first_name, 'user_info' : user_info, 'username' : request.user.username, 'whoReceived' : user_delivering, 'full_name' : full_name, 'testimonials' : testimonials}
	return render (request, 'entrust_app/task_completed.html', context)

def testimonial(request):

	new_testimonial = Testimonial(user_whoReceived = request.POST['whoReceived'], user_whoGave = request.user.username, content = request.POST['testimonial_info'], testimonial_date = datetime.now(), rating = request.POST['rate'])
	i = int(request.POST['rate'])
	rating_display = ''
	while i > 0:
		rating_display += 'x'
		i = i-1
	new_testimonial.rating_display = rating_display
	new_testimonial.save()

	return redirect('/entrust-app/home/?id=1')

def view_testimonials(request, req_user):

	user_info = User.objects.get(username = request.user.username)
	full_name = request.user.first_name + ' ' + request.user.last_name
	testimonials = Testimonial.objects.filter(user_whoReceived = req_user)

	context = {'first_name' : request.user.first_name, 'user_info' : user_info, 'username' : request.user.username, 'full_name' : full_name, 'testimonials' : testimonials}
	return render (request, 'entrust_app/testimonial.html', context)

def task_deleted(request, task_id):

	context = []

	user_info = User.objects.get(username = request.user.username)

	discussion_obj = Discussion.objects.filter(task_id = task_id)
	task_info = Service.objects.get(id = task_id)
	people_in_queue = TaskQueue.objects.filter(task = task_id)
	comments = Comments.objects.filter(task_id = task_id)

	username = request.user.username
	user_obj = User.objects.get(username = username)
	full_name = user_obj.first_name + ' ' + user_obj.last_name

	discussion_obj.delete()
	task_info.delete()
	people_in_queue.delete()
	comments.delete()
	
	usertasks=Service.objects.filter(user_ordering = request.user)
	task_count = usertasks.count()
	search_area="Neighbourhood"

	context = {'first_name' : request.user.first_name, 'user_info' : user_info, 'username' : username, 'full_name' : full_name, 'tasks_name':usertasks, 'search_area' : search_area, 'task_count' : task_count}

	return render (request, 'entrust_app/owntask_view.html', context)

def task_refresh(request):

	context = []
	user_info = User.objects.get(username = request.user.username)
	tasks = Service.objects.all()

	for task in tasks:
		if task.deadline < datetime.now().date():
			Discussion.objects.filter(task_id = task.id).delete()
			people_in_queue = TaskQueue.objects.filter(task = task.id)
			comments = Comments.objects.filter(task_id = task.id)
			task.delete()

	if request.GET.get('id'):
		area_id = request.GET.get('id')
		if area_id == 'Neighbourhood':
			return redirect('/entrust-app/home/?id=1')
		elif area_id == 'Intracity':
			return redirect('/entrust-app/home/?id=2')
		elif area_id == 'Intercity':
			return redirect('/entrust-app/home/?id=3')
	else:
		return redirect('/entrust-app/home/?id=1')
