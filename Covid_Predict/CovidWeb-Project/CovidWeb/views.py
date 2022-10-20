from multiprocessing import context
import joblib
from django.http import HttpResponse
from django.shortcuts import render,redirect

from etc_symptom.models import Etc_Symptom
###chart###
from .fusioncharts import FusionCharts
from collections import OrderedDict
import pandas as pd
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
def chart(request):
    df = pd.read_csv("/Users/jinjoa/Downloads/Covid19_Prediction_Using_Symptoms-main/trainingSet.csv")

    count_covid = len(df.loc[df['TYPE'] == 'MILD COVID']) + len(df.loc[df['TYPE'] == 'SEVERE COVID'])
    count_flu = len(df.loc[df['TYPE'] == 'COMMON FLU'])
    count_allergy = len(df.loc[df['TYPE'] == 'ALLERGY'])
    count_cold = len(df.loc[df['TYPE'] == 'COLD'])
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
    chartData["COVID 19"] = count_covid
    chartData["COMMON FLU"] = count_flu
    chartData["ALLERGY"] = count_allergy
    chartData["COLD"] = count_cold

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
                                 "subCaption" : "기침",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "증상있음",
                                 "value": "1046"
                             }, {
                                 "label": "증상없음",
                                 "value": "1039"
                             }]
                         }""")
    pie2 = FusionCharts("pie3d", "ex3", "400", "400", "chart-3", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{
                             "chart": {
                                 "caption": "코로나 증상",
                                 "subCaption" : "근육통",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "증상있음",
                                 "value": "1038"
                             }, {
                                 "label": "증상없음",
                                 "value": "1047"
                             }]
                         }""")
    pie3 = FusionCharts("pie3d", "ex4", "400", "400", "chart-4", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{
                             "chart": {
                                 "caption": "코로나 증상",
                                 "subCaption" : "열",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "증상있음",
                                 "value": "1040"
                             }, {
                                 "label": "증상없음",
                                 "value": "1045"
                             }]
                         }""")
    pie4 = FusionCharts("pie3d", "ex5", "400", "400", "chart-5", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{
                             "chart": {
                                 "caption": "코로나 증상",
                                 "subCaption" : "미각상실",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "증상있음",
                                 "value": "2"
                             }, {
                                 "label": "증상없음",
                                 "value": "2083"
                             }]
                         }""")

    pie5 = FusionCharts("pie3d", "ex6", "400", "400", "chart-6", "json",

                         """{
                             "chart": {
                                 "caption": "코로나 증상",
                                 "subCaption" : "구토",
                                 "showValues":"1",
                                 "showPercentInTooltip" : "0",
                                 "numberPrefix" : "$",
                                 "enableMultiSlicing":"1",
                                 "theme": "fusion"
                             },
                             "data": [{
                                 "label": "증상있음",
                                 "value": "1041"
                             }, {
                                 "label": "증상없음",
                                 "value": "1044"
                             }]
                         }""")


    return render(request, 'chart.html', {'output': column2D.render(), 'output2': pie1.render(), 'output3': pie2.render(), 'output4': pie3.render(), 'output5': pie4.render(), 'output6': pie5.render()})
