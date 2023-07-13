import json
import os.path

from flask import jsonify, request, render_template, render_template_string, redirect, url_for, flash, make_response
from . import analysis
##  基础函数库
import numpy as np
import pandas as pd
## 绘图函数库
import matplotlib.pyplot as plt
import seaborn as sns
import os, csv
from io import BytesIO
import base64

@analysis.route('/function', methods=['GET', 'POST'])
def analysis():
    if request.method == 'GET':
        print(1)
        return render_template('function.html')
    if request.method == 'POST':
        print(4)
        if request.files:
            print(2)
            uploaded_file = request.files['csvfile']  # This line uses the same variable and worked fine
            filepath = os.path.join("E:\\flaskProject\\app\\static\\train", uploaded_file.filename)
            uploaded_file.save(filepath)
            df = pd.read_csv(filepath)
            df.info()
            df.head()
            y = df.label
            y.value_counts()
            drop_cols = ['sample_id', 'label']
            x = df.drop(drop_cols, axis=1)
            ## 对于特征进行一些统计描述
            x.describe()
            xnull = x.isnull().sum()

            from sklearn.impute import SimpleImputer
            imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
            imputerimpyter = imputer.fit(x)
            x1 = imputer.transform(x)
            ## 将nan处理为0
            # for i in range(x1.shape[0]):
            #     for j in range(x1.shape[1]):
            #         if (x1[i][j] == np.nan or x1[i][j] == 0):
                        # print(f'x1[{i}][{j}] is {x1[i][j]}')

            ## 为了正确评估模型性能，将数据划分为训练集和测试集，并在训练集上训练模型，在测试集上验证模型性能。
            from sklearn.model_selection import train_test_split

            ## 选择其类别为0和1的样本 （不包括类别为2的样本）
            data_target_part = y
            data_features_part = x1

            ## 测试集大小为20%， 80%/20%分
            x_train, x_test, y_train, y_test = train_test_split(data_features_part, data_target_part, test_size=0.2,
                                                                random_state=2020)

            ## 导入LightGBM模型
            from lightgbm.sklearn import LGBMClassifier
            ## 定义 LightGBM 模型
            clf = LGBMClassifier()
            # 在训练集上训练LightGBM模型
            clf.fit(x_train, y_train)

            ## 在训练集和测试集上分布利用训练好的模型进行预测
            train_predict = clf.predict(x_train)
            test_predict = clf.predict(x_test)
            from sklearn import metrics

            ## 利用accuracy（准确度）【预测正确的样本数目占总预测样本数目的比例】评估模型效果
            print('The accuracy of the Logistic Regression is:', metrics.accuracy_score(y_train, train_predict))
            print('The accuracy of the Logistic Regression is:', metrics.accuracy_score(y_test, test_predict))
            d2 = metrics.accuracy_score(y_train, train_predict)
            data2 = d2.tolist()
            d3 = metrics.accuracy_score(y_test, test_predict)
            data3 = d3.tolist()

            ## 查看混淆矩阵 (预测值和真实值的各类情况统计矩阵)
            confusion_matrix_result = metrics.confusion_matrix(test_predict, y_test)
            d1 = confusion_matrix_result.tolist()
            print('The confusion matrix result:\n', confusion_matrix_result)

            # 利用热力图对于结果进行可视化
            plt.figure(figsize=(8, 6))
            sns.heatmap(confusion_matrix_result, annot=True, cmap='Blues')
            plt.xlabel('Predicted labels')
            plt.ylabel('True labels')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()

            # 将PNG文件编码为base64字符串
            image_base64 = base64.b64encode(image_png).decode('utf-8')
            # print({'image_data': image_base64,
            #                 'The accuracy of the Logistic Regression is':d2,
            #                 'The accuracy of the Logistic Regression is:':d3,
            #                 'The confusion matrix result':d1
            # })
            responde_data = {'image_data': image_base64,
                    'train_accuracy': metrics.accuracy_score(y_train, train_predict),
                    'test_accuracy': metrics.accuracy_score(y_test, test_predict),
                    'confusion_matrix': d1
                    }
            return jsonify(responde_data)


            plt.show()

            from sklearn.metrics import f1_score
            f1_score(y_test, test_predict, average='macro')
            print('yes')
            # return render_template_string('<img src="data:image/png;base64,{{ image_base64 }}" />', image_base64=image_base64)
        return render_template('index.html')
    print(3)
    return render_template('index.html')

