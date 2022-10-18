import joblib
import pandas as pd
import sklearn.metrics as mt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('covid.csv')
x_train, x_test, y_train, y_test = train_test_split(data.loc[:,'기침':'충혈'],data['병명'], test_size=0.3, random_state=2)
tree_model = DecisionTreeClassifier(max_depth=9) # hyperparameter tunig before (max_depth)
tree_model.fit(x_train,y_train)

# 예측값 저장
y_pred = tree_model.predict(x_test)

# 학습결과 평가 
score = tree_model.score(x_train, y_train)
print('TRAIN 정확도: ',format(score,'.2f'),'\n')
accuracy = mt.accuracy_score(y_test, y_pred)
print('TEST 정확도: ', format(accuracy,'.2f'),'\n') # train,test 모두 잘 맞춘다.

# 모델 저장하기
filename = 'covid_model.sav'
joblib.dump(tree_model,filename)