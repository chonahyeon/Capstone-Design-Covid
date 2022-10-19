from multiprocessing import context
import joblib
from django.http import HttpResponse
from django.shortcuts import render,redirect

from etc_symptom.models import Etc_Symptom


def home(request):
    return render(request,'home.html')

def Survey_home(request):
    return render(request,'Survey_home.html')

def result(request):
    tree = joblib.load('covid_model.sav')
    lis_typing=[]
    lis = []
    lis_typing.append(request.POST['이름'])
    lis_typing.append(request.POST['이메일'])
    lis_typing.append(request.POST['나이'])
    lis_typing.append(request.POST['기타증상'])

    lis.append(int(request.POST['기침']))
    lis.append(int(request.POST['근육통']))
    lis.append(int(request.POST['피곤함']))
    lis.append(int(request.POST['목아픔']))
    lis.append(int(request.POST['콧물']))
    lis.append(int(request.POST['코막힘']))
    lis.append(int(request.POST['열']))
    lis.append(int(request.POST['매스꺼움']))
    lis.append(int(request.POST['구토']))
    lis.append(int(request.POST['설사']))

    lis.append(int(request.POST['호흡곤란']))
    lis.append(int(request.POST['숨막힘']))
    lis.append(int(request.POST['미각손실']))
    lis.append(int(request.POST['후각손실']))
    lis.append(int(request.POST['코가려움']))
    lis.append(int(request.POST['눈가려움']))
    lis.append(int(request.POST['목가려움']))
    lis.append(int(request.POST['귀아픔']))
    lis.append(int(request.POST['오한']))
    lis.append(int(request.POST['충혈']))

    print('출력',lis) # chekbox값이 잘 전달되는지 확인
    print('기타값',lis_typing)

    pred = tree.predict([lis])
    upload_sym(request)
    return render(request,'result.html',{'pred':pred,'lis':lis})

def upload_sym(request):
        if request.method == 'POST':
            sym=Etc_Symptom()
            sym.name=request.POST['이름']
            sym.email=request.POST['이메일']
            sym.age=request.POST['나이']
            sym.etc_symptom=request.POST['기타증상']
            sym.save()
            #return redirect('sym') 