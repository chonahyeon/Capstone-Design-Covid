import joblib
import pandas as pd
from DB.models import Symptom
from django.http import HttpResponse
from django.shortcuts import render

###chart###
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from django.shortcuts import render
###

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
    lis.append(int(request.POST['미각손실']))
    lis.append(int(request.POST['후각손실']))
    lis.append(int(request.POST['코가려움']))
    lis.append(int(request.POST['눈가려움']))
    lis.append(int(request.POST['목가려움']))
    lis.append(int(request.POST['귀아픔']))
    lis.append(int(request.POST['오한']))
    lis.append(int(request.POST['충혈']))

    kor_list =get_korList(lis)

    print('출력',lis) # chekbox값이 잘 전달되는지 확인
    print('기타값',lis_typing)
    print('증상 한글 변환 값', kor_list)

    pred = tree.predict([lis])
    kor_pred = ''
    if pred[0] == 3:
        kor_pred = '코로나'
    elif pred[0]== 1:
        kor_pred = '감기'
    elif pred[0]== 0:
        kor_pred = '알러지'
    elif pred[0]== 2:
        kor_pred = '독감'    
    else:
        kor_pred = 'error'
    upload_sym(request,kor_pred)
    return render(request,'result.html',{'kor_pred':kor_pred,'pred':pred,'kor_list':kor_list})

def get_korList(lis):
    count = 0
    kor_list= []
    for symptom in lis:
        if count == 0 and symptom ==1:
            kor_list.append('기침')
        elif count == 1 and symptom ==1: 
            kor_list.append('근육통')
        elif count == 2 and symptom ==1: 
            kor_list.append('피곤함')
        elif count == 3 and symptom ==1: 
            kor_list.append('목아픔')
        elif count == 4 and symptom ==1: 
            kor_list.append('콧물')
        elif count == 5 and symptom ==1: 
            kor_list.append('코막힘')
        elif count == 6 and symptom ==1: 
            kor_list.append('열')
        elif count == 7 and symptom ==1: 
            kor_list.append('매스꺼움')
        elif count == 8 and symptom ==1: 
            kor_list.append('구토')
        elif count == 9 and symptom ==1: 
            kor_list.append('설사')
        elif count == 10 and symptom ==1: 
            kor_list.append('호흡곤란')
        elif count == 11 and symptom ==1: 
            kor_list.append('숨막힘')
        elif count == 12 and symptom ==1: 
            kor_list.append('미각손실')
        elif count == 13 and symptom ==1: 
            kor_list.append('후각손실')
        elif count == 14 and symptom ==1: 
            kor_list.append('코가려움')
        elif count == 15 and symptom ==1: 
            kor_list.append('목가려움')
        elif count == 16 and symptom ==1: 
            kor_list.append('귀아픔')
        elif count == 17 and symptom ==1: 
            kor_list.append('오한')
        elif count == 18 and symptom ==1: 
            kor_list.append('충혈')
        count+=1
    return kor_list

def upload_sym(request,pred):
   if request.method == 'POST':
        sym=Symptom()
        sym.name=request.POST['이름']
        sym.email=request.POST['이메일']
        sym.age=request.POST['나이']
        sym.etc_symptom=request.POST['기타증상']
        sym.result = pred
        sym.save()

        
class ResultAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request): 
        data = request.session.get('chart')
        return Response(data)

def chart(request):
    context = {}
    return render(request, 'chart.html', context )