import joblib
import pandas as pd
from DB.models import Symptom
from django.http import HttpResponse
from django.shortcuts import render

###chart###
from .fusioncharts import FusionCharts
from collections import OrderedDict
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
    lis.append(int(request.POST['숨막힘']))
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
    if pred[0] =='MILD COVID' or pred=='SEVERE COVID':
        kor_pred = '코로나'
    elif pred[0]=='COLD':
        kor_pred = '일반 감기'
    elif pred[0]=='ALLERGY':
        kor_pred = '알러지'
    elif pred[0]=='COMMON FLU':
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

def chart(request):
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "질병별 발생률"
    chartConfig["subCaption"] = "-"
    chartConfig["xAxisName"] = "질병 명"
    chartConfig["yAxisName"] = "감염 인구"
    chartConfig["numberSuffix"] = "(명)"
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    chartData["COVID 19"] = 2085
    chartData["COMMON FLU"] = 25008
    chartData["ALLERGY"] = 16389
    chartData["COLD"] = 1024

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

   
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)

    column2D = FusionCharts("column2d", "ex1", "400", "400", "chart-1", "json", dataSource)


    pie1 = FusionCharts("pie3d", "ex2", "400", "400", "chart-2", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{
                             "chart": {
                                 "caption": "코로나 증상",
                                 "subCaption" : "총 2085명 중",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "기침",
                                 "value": "1046"
                             }, {
                                 "label": "근육통",
                                 "value": "1038"
                             },{
                                 "label": "피곤함",
                                 "value": "1037"
                             }, {
                                 "label": "목아픔",
                                 "value": "1039"
                             },{
                                 "label": "콧물",
                                 "value": "10"
                             }, {
                                 "label": "코막힘",
                                 "value": "8"
                             },{
                                 "label": "열",
                                 "value": "1040"
                             }, {
                                 "label": "매스꺼움",
                                 "value": "1043"
                             }, {
                                 "label": "구토",
                                 "value": "1041"
                             },{
                                 "label": "설사",
                                 "value": "1027"
                             },{
                                 "label": "호흡곤란",
                                 "value": "1055"
                             }, {
                                 "label": "숨막힘",
                                 "value": "1046"
                             }, {
                                 "label": "미각손실",
                                 "value": "2"
                             },{
                                 "label": "후각손실",
                                 "value": "2"
                             },{
                                 "label": "코가려움",
                                 "value": "5"
                             }, {
                                 "label": "눈가려움",
                                 "value": "15"
                             }, {
                                 "label": "목가려움",
                                 "value": "6"
                             },{
                                 "label": "귀아픔",
                                 "value": "9"
                             },{
                                 "label": "오한",
                                 "value": "1037"
                             }, {
                                 "label": "충혈",
                                 "value": "24"
                             }]
                         }""")
    pie2 = FusionCharts("pie3d", "ex3", "400", "400", "chart-3", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{
                             "chart": {
                                 "caption": "알러지 증상",
                                 "subCaption" : "총 16389명 중",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "기침",
                                 "value": "8193"
                             }, {
                                 "label": "근육통",
                                 "value": "8192"
                             },{
                                 "label": "피곤함",
                                 "value": "8193"
                             }, {
                                 "label": "목아픔",
                                 "value": "8191"
                             },{
                                 "label": "콧물",
                                 "value": "8197"
                             }, {
                                 "label": "코막힘",
                                 "value": "8194"
                             },{
                                 "label": "열",
                                 "value": "0"
                             }, {
                                 "label": "매스꺼움",
                                 "value": "0"
                             }, {
                                 "label": "구토",
                                 "value": "0"
                             },{
                                 "label": "설사",
                                 "value": "0"
                             },{
                                 "label": "호흡곤란",
                                 "value": "0"
                             }, {
                                 "label": "숨막힘",
                                 "value": "0"
                             }, {
                                 "label": "미각손실",
                                 "value": "8195"
                             },{
                                 "label": "후각손실",
                                 "value": "8195"
                             },{
                                 "label": "코가려움",
                                 "value": "8197"
                             }, {
                                 "label": "눈가려움",
                                 "value": "8194"
                             }, {
                                 "label": "목가려움",
                                 "value": "8193"
                             },{
                                 "label": "귀아픔",
                                 "value": "8196"
                             },{
                                 "label": "오한",
                                 "value": "8196"
                             }, {
                                 "label": "충혈",
                                 "value": "8198"
                             }]
                         }""")
    
    pie3 = FusionCharts("pie3d", "ex4", "400", "400", "chart-4", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{
                             "chart": {
                                 "caption": "독감 증상",
                                 "subCaption" : "총 250089명 중",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                            "data": [{
                                 "label": "기침",
                                 "value": "13422"
                             }, {
                                 "label": "근육통",
                                 "value": "13384"
                             },{
                                 "label": "피곤함",
                                 "value": "13390"
                             }, {
                                 "label": "목아픔",
                                 "value": "13366"
                             },{
                                 "label": "콧물",
                                 "value": "13361"
                             }, {
                                 "label": "코막힘",
                                 "value": "13343"
                             },{
                                 "label": "열",
                                 "value": "12936"
                             }, {
                                 "label": "매스꺼움",
                                 "value": "13395"
                             }, {
                                 "label": "구토",
                                 "value": "13406"
                             },{
                                 "label": "설사",
                                 "value": "13360"
                             },{
                                 "label": "호흡곤란",
                                 "value": "13378"
                             }, {
                                 "label": "숨막힘",
                                 "value": "13402"
                             }, {
                                 "label": "미각손실",
                                 "value": "10106"
                             },{
                                 "label": "후각손실",
                                 "value": "10106"
                             },{
                                 "label": "코가려움",
                                 "value": "0"
                             }, {
                                 "label": "눈가려움",
                                 "value": "0"
                             }, {
                                 "label": "목가려움",
                                 "value": "0"
                             },{
                                 "label": "귀아픔",
                                 "value": "0"
                             },{
                                 "label": "오한",
                                 "value": "13365"
                             }, {
                                 "label": "충혈",
                                 "value": "0"
                             }]
                         }""")
    
    pie4 = FusionCharts("pie3d", "ex5", "400", "400", "chart-5", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{
                             "chart": {
                                 "caption": "감기 증상",
                                 "subCaption" : "총 1024명 중",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "기침",
                                 "value": "512"
                             }, {
                                 "label": "근육통",
                                 "value": "512"
                             },{
                                 "label": "피곤함",
                                 "value": "512"
                             }, {
                                 "label": "목아픔",
                                 "value": "512"
                             },{
                                 "label": "콧물",
                                 "value": "512"
                             }, {
                                 "label": "코막힘",
                                 "value": "512"
                             },{
                                 "label": "열",
                                 "value": "512"
                             }, {
                                 "label": "매스꺼움",
                                 "value": "0"
                             }, {
                                 "label": "구토",
                                 "value": "0"
                             },{
                                 "label": "설사",
                                 "value": "0"
                             },{
                                 "label": "호흡곤란",
                                 "value": "0"
                             }, {
                                 "label": "숨막힘",
                                 "value": "0"
                             }, {
                                 "label": "미각손실",
                                 "value": "512"
                             },{
                                 "label": "후각손실",
                                 "value": "512"
                             },{
                                 "label": "코가려움",
                                 "value": "0"
                             }, {
                                 "label": "눈가려움",
                                 "value": "0"
                             }, {
                                 "label": "목가려움",
                                 "value": "0"
                             },{
                                 "label": "귀아픔",
                                 "value": "0"
                             },{
                                 "label": "오한",
                                 "value": "512"
                             }, {
                                 "label": "충혈",
                                 "value": "0"
                             }]
                         }""")




    return render(request, 'chart.html', {'output': column2D.render(), 'output2': pie1.render(), 'output3': pie2.render(), 'output4': pie3.render(), 'output5': pie4.render()})
