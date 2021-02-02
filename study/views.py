from django.conf import settings
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.views.generic import CreateView
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from .forms import LoginForm, UserCreateForm
from .models import Faculty, User, Subject, Faculty

User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'study/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'study/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'study/top.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'study/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string(
            'study/mail_template/create/subject.txt', context)
        message = render_to_string(
            'study/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('study:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'study/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'study/user_create_complete.html'
    timeout_seconds = getattr(
        settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


"""
def index(request):
    my_dict = {
        'insert_something': "views.pyのinsert_something部分です。",
        'name': 'Bashi',
        'form': TestForm(),
        'insert_forms': '初期値',
    }
    if (request.method == 'POST'):
        my_dict['insert_forms'] = '文字列:' + \
            request.POST['text'] + '<br>整数型:' + request.POST['num']
        my_dict['form'] = TestForm(request.POST)
    return render(request, 'study/index.html', my_dict)
"""

# アカウント作成

"""
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            # フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            # フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'create.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(request, 'create.html', {'form': form, })


#create_account = Create_account.as_view()


def info(request):
    infodata = StudentInfo.objects.all()
    header = ['名前', '学籍番号', '性別', '学科', '学年', '']
    my_dict2 = {
        'title': 'テスト',
        'val': infodata,
        'header': header
    }
    return render(request, 'study/info.html', my_dict2)


def signup(request):
    if (request.method == 'POST'):
        obj = StudentInfo()
        info = StudentInfoAdd(request.POST, instance=obj)
        info.save()
        return redirect(to='/info')
    modelform_dict = {
        'title': 'modelformテスト',
        'form': StudentInfoAdd()
    }
    return render(request, 'study/signup.html', modelform_dict)


# class PostCreate(generic.CreateView):
    # template_name = 'signup.html'
    # model = StudentInfo
    # form_class = StudentInfoAdd
    # success_url = reverse_lazy('info')  # reverse_lazy等のほうが良い。これは手抜き

    # def get_context_data(self, **kwargs):
    # context = super().get_context_data(**kwargs)
    # context['faculty_list'] = Faculty.objects.all()
    # return context


def update(request, num):
    obj = StudentInfo.objects.get(id=num)
    # POST送信されていたら
    if (request.method == 'POST'):
        info = StudentInfoAdd(request.POST, instance=obj)
        info.save()
        return redirect(to='/info')
    update_dict = {
        'title': '登録情報更新画面',
        'id': num,
        'form': StudentInfoAdd(instance=obj),
    }
    return render(request, 'study/update.html', update_dict)


def delete(request, num):
    obj = StudentInfo.objects.get(id=num)
    if (request.method == 'POST'):
        obj.delete()
        return redirect(to='/info')
    delete_dict = {
        'title': '削除確認',
        'id': num,
        'obj': obj,
    }
    return render(request, 'study/delete.html', delete_dict)
"""
