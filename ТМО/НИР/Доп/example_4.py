import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

@st.cache
def load_data():
    '''
    Загрузка данных
    '''
    data = pd.read_csv('data/data.csv', sep=",")
    data = data.drop(columns=['slope', 'ca', 'thal', 'oldpeak'])
    return data


@st.cache
def preprocess_data(data_in):
    '''
    Масштабирование признаков, функция возвращает X и y для кросс-валидации
    '''
    data_out = data_in.copy()
    return data_out


# Отрисовка ROC-кривой
def draw_roc_curve(y_true, y_score, ax, pos_label=1, average='micro'):
    fpr, tpr, thresholds = roc_curve(y_true, y_score, 
                                     pos_label=pos_label)
    roc_auc_value = roc_auc_score(y_true, y_score, average=average)
    #plt.figure()
    lw = 2
    ax.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc_value)
    ax.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    ax.set_xlim([0.0, 1.0])
    ax.set_xlim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver operating characteristic')
    ax.legend(loc="lower right")


# Модели
models_list = ['LogR', 'KNN_5', 'SVC', 'Tree', 'RF', 'GB']
clas_models = {'LogR': LogisticRegression(C = 0.25, random_state = 0), 
               'KNN_5':KNeighborsClassifier(n_neighbors=29),
               'SVC':SVC(probability=True),
               'Tree':DecisionTreeClassifier(criterion = 'entropy', random_state = 0),
               'RF':RandomForestClassifier(criterion = 'entropy', n_estimators = 119, random_state = 0),
               'GB':GradientBoostingClassifier(criterion = 'friedman_mse', learning_rate = 0.5, loss = 'exponential', n_estimators = 11, random_state = 0)}

prop_list = [#'Возраст', 
               'Пол',
               #'Тип боли',
               #'Давление(покой)',
               #'Холестерин',
               'Сахар',
               #'Макс частота',
               'Физ нагрузки',
               'Болезнь сердца']
clas_prop = {'Возраст': 'age', 
               'Пол':'sex',
               'Тип боли':'cp',
               'Давление(покой)':'trestbps',
               'Холестерин':'chol',
               'Сахар':'fbs',
               'Макс частота':'thalach',
               'Физ нагрузки':'exang',
               'Болезнь сердца':'num'}

@st.cache(suppress_st_warning=True)
def print_models(models_select, data_out, prop_select):  
    temp_X = data_out.drop(clas_prop[prop_select], axis=1)
    temp_y = data_out[clas_prop[prop_select]]
    print(prop_select)
    print(temp_y)
    X_train, X_test, y_train, y_test = train_test_split(temp_X, temp_y, train_size=0.75, random_state=1)    
    current_models_list = []
    roc_auc_list = []
    for model_name in models_select:
        model = clas_models[model_name]
        model.fit(X_train, y_train)
        # Предсказание значений
        Y_pred = model.predict(X_test)
        # Предсказание вероятности класса "1" для roc auc
        Y_pred_proba_temp = model.predict_proba(X_test)
        Y_pred_proba = Y_pred_proba_temp[:,1]
   
        roc_auc = roc_auc_score(y_test.values, Y_pred_proba, multi_class='ovr')
        current_models_list.append(model_name)
        roc_auc_list.append(roc_auc)

        #Отрисовка ROC-кривых 
        fig, ax = plt.subplots(ncols=2, figsize=(10,5))    
        draw_roc_curve(y_test.values, Y_pred_proba, ax[0])
        cm = confusion_matrix(y_test, Y_pred, normalize='all', labels=model.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
        disp.plot(ax=ax[1], cmap=plt.cm.Blues)
        fig.suptitle(model_name)
        st.pyplot(fig)

    if len(roc_auc_list)>0:
        temp_d = {'roc-auc': roc_auc_list}
        temp_df = pd.DataFrame(data=temp_d, index=current_models_list)
        st.bar_chart(temp_df)


st.sidebar.header('Модели машинного обучения')
models_select = st.sidebar.multiselect('Выберите модели', models_list)
st.sidebar.header('Признак машинного обучения')
prop_select = st.sidebar.selectbox('Выберите признак', prop_list)

data = load_data()
data_out = preprocess_data(data)

st.header('Оценка качества моделей')
print_models(models_select, data_out, prop_select)

