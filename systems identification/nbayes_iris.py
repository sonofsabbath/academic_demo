from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, f1_score
from time import time

iris = load_iris()
x = iris.data
y = iris.target
train_data, test_data, train_classes, test_classes = train_test_split(x, y, test_size=0.2, random_state=4)
bayes = GaussianNB()

print('Learning')
start = time()
bayes.fit(train_data, train_classes)
end = time()
l_time = end - start

print('Predicting')
start = time()
pred_classes = bayes.predict(test_data)
end = time()
p_time = end - start

acc = accuracy_score(test_classes, pred_classes)
f = f1_score(test_classes, pred_classes, average='micro')

print('Learning time: {}'.format(l_time))
print('Prediction time: {}'.format(p_time))
print('\nAccuracy: {:.2f}'.format(acc))
print('f-score: {:.2f}'.format(f))
