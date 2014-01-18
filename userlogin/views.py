from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render
from django.template import loader
from internal.models import Employee, Branch
from .forms import LoginForm, UserForm, UserExtendedForm
from .tables import UserTable
from common.forms import ExcelUploadForm
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
import json
from django.core.serializers.json import DjangoJSONEncoder
from utils.upload import upload_user_list_file, handle_uploaded_file
from logistics.settings import MEDIA_ROOT


class AuthenticateUser:
    def __init__(self, request):
        self.request = request
        self.type = ''
        self.type_of_user = ''

    def authenticate(self, username, password):
        if '@' in username:
            self.type_of_user = 'username is email' #todo change
            try:
                user = User.objects.get(email=username)
                if user:
                    if user.check_password(password):
                        user = authenticate(username=username, password=password)
                        return user, None
                    else:
                        return None, {'password_msg': 'Wrong password'}
                else:
                    return None, {'username_msg': 'Wrong Username'}
            except Exception:
                return None, {'username_msg': 'Wrong Username'}
        else:
            self.type_of_user = 'no email required' #todo change
            try:
                user = User.objects.get(username=username)
                if user:
                    if user.check_password(password):
                        user = authenticate(username=username, password=password)
                        return user, None
                    else:
                        return None, {'password_msg': 'Wrong Password'}
                else:
                    return None, {'username_msg': 'Wrong Username'}
            except Exception:
                return None, {'username_msg': 'Wrong Username'}

    def logger(self):
        username = self.request.POST['username']
        password = self.request.POST['password']

        user, message = self.authenticate(username=username, password=password)
        if user is None:
            return HttpResponse(
                loader.get_template('userlogin/login_form.html').render(RequestContext(self.request, message))), message
        else:
        #try:
        #   res = user.resident
        #except Exception:
        #   return HttpResponse(loader.get_template('Login.html').render(RequestContext(self.request,{'msg':'ResidentOnly'})))
            login(request=self.request, user=user)
            return HttpResponseRedirect('/'), ''


def login_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    request.session['branch'] = request.user.profile.branch.pk
                except Exception:
                    pass
                return HttpResponseRedirect('/')
            else:
                form = LoginForm()
                return render(request, 'userlogin/login_form.html', {'form': form})
        else:
            form = LoginForm()
            return render(request, 'userlogin/login_form.html', {'form': form})
    elif request.method == 'GET':
        form = LoginForm()
        return render(request, 'userlogin/login_form.html', {'form': form})


#no need to define seperate logout handler for the si login
def logout_handler(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def home(request):
    if not request.GET.keys():
        return render(request, 'home.html')

    elif request.GET.get('type') == 'charts':
        json_dict = {}
        if request.GET.get('graph_type') == 'branch_incoming':
            json_dict['series_name'] = ['Reverse pickup', 'Cash on Delivery', 'Prepaid']
            branch = request.session['branch']
            reverse = Branch.objects.get(pk=branch).get_awbs(['DR', 'ISC', 'TB', 'TBD', 'MTS', 'MTD'], 'REV').count()
            cod = Branch.objects.get(pk=branch).get_awbs(['DR', 'ISC', 'TB', 'TBD', 'MTS', 'MTD'], 'COD').count()
            pre_paid = Branch.objects.get(pk=branch).get_awbs(['DR', 'ISC', 'TB', 'TBD', 'MTS', 'MTD'],
                                                              'PRE').count()
            json_dict['data_list'] = [reverse, cod, pre_paid]
            json_dict['title'] = 'Expected Incoming AWBs'

        #elif request.GET.get('graph_type') == 'branch_drs':
        #    reverse = AWB.objects.filter(type='REV', awb_status__status='DR').count()
        #    cod = AWB.objects.filter(type='COD', awb_status__status='DR').count()
        #    pre_paid = AWB.objects.filter(type='PRE', awb_status__status='DR').count()
        #    json_dict['series_name'] = ['Reverse pickup', 'Cash on Delivery', 'Prepaid']
        #    json_dict['data_list'] = [reverse, cod, pre_paid]
        #    json_dict['title'] = 'Expected Incoming AWBs'

        if json_dict:
            json_dict['invalid_request'] = False
        else:
            json_dict['invalid_request'] = True

        json_data = json.dumps(json_dict, cls=DjangoJSONEncoder)
        return HttpResponse(json_data, mimetype='application/json')


def users(request):
    table = UserTable(User.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'common/table.html', {'table': table, 'model': 'user', 'url': '/users/add'})


def add_user(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=User())
        extended_form = UserExtendedForm(request.POST, instance=Employee())

        if user_form.is_valid() and extended_form.is_valid():
            user = user_form.save()
            u = User.objects.get(username__exact=request.POST['username'])
            u.set_password(request.POST['password'])
            u.is_staff = True
            u.save()
            if request.POST['role'] == 'BM':
                branch = Branch.objects.get(pk=request.POST['branch'])
                branch.branch_manager = u
                branch.save()
            instance = extended_form.save(commit=False)
            instance.user_id = user.pk
            instance.save()
            return HttpResponseRedirect('/users')
    else:
        user_form = UserForm()
        extended_form = UserExtendedForm()
    return render(request, 'userlogin/add_user.html', {'user_form': user_form, 'extended_form': extended_form})


def upload_user_list(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = handle_uploaded_file(request.FILES['file'], request.FILES['file'].name,
                                        MEDIA_ROOT + 'uploads/internal/')
            upload_user_list_file(file)
            return HttpResponseRedirect('/users')
    else:
        form = ExcelUploadForm()
    return render(request, 'common/upload_form.html', {'form': form})


def set_branch(request):
    if request.method == 'POST' and request.is_ajax():
        if Branch.objects.get(pk=int(request.POST['branch'])).branch_name == 'HQ':
            del request.session['branch']
        else:
            request.session['branch'] = int(request.POST['branch'])
        return HttpResponse(int(request.POST['branch']))


def get_message(request):
    if 'message' in request.session:
        print request.session
        context = {
            'class': request.session['message']['class'],
            'report': request.session['message']['report']
        }
        return render(request, 'message.html', context)



