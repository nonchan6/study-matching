from django.shortcuts import render
from django.http import HttpResponse
from .forms import TestForm
from .models import StudentInfo, Subject
from django.shortcuts import redirect
from .forms import StudentInfoAdd


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


def info(request):
    infodata = StudentInfo.objects.all()
    header = ['名前', '学籍番号', '性別', '学部', '学年', '']
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
    subject = Subject.objects.filter(faculty_id__exact=1).all()
    modelform_dict = {
        'title': 'modelformテスト',
        'form': StudentInfoAdd(),
        'subject': subject,
    }
    return render(request, 'study/signup.html', modelform_dict)


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
