import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from time import time

iris = load_iris()
x = iris.data
y = iris.target
train_data, test_data, train_classes, test_classes = train_test_split(x, y, test_size=0.2, random_state=4)
test_lambdas = np.linspace(0.1, 1.0, 10)

l_times = []
p_times = []
accs = []
fs = []

for i in test_lambdas:
    print('Learning for lambda=' + str(i))
    l_start = time()
    log = LogisticRegression(C=i, solver='newton-cg', multi_class='ovr')
    log.fit(train_data, train_classes)
    l_times.append(time() - l_start)

    print('Predicting for lambda=' + str(i))
    p_start = time()
    pred_classes = log.predict(test_data)
    p_times.append(time() - p_start)

    acc = accuracy_score(test_classes, pred_classes)
    f = f1_score(test_classes, pred_classes, average='micro')
    accs.append(acc)
    fs.append(f)

max_acc = np.max(accs)
max_f = np.max(fs)
best_acc = []
best_f = []

for i in range(len(accs)):
    if accs[i] == max_acc:
        best_acc.append(test_lambdas[i])
    if fs[i] == max_f:
        best_f.append(test_lambdas[i])

print('Learning time:', np.sum(l_times))
print('Prediction time:', np.sum(p_times))
print('\nBest accuracy: {:.3f}'.format(max_acc))
print('Best f-score: {:.3f}'.format(max_f))
print('\nlambda values with best accuracy:', best_acc)
print('lambda values with best f-score:', best_f)
print(best_acc == best_f)

plt.plot(test_lambdas, accs)
plt.title('Logistic regression IRIS')
plt.xlabel('lambda', fontweight='bold')
plt.ylabel('Accuracy')
plt.show()
plt.clf()

plt.plot(test_lambdas, fs)
plt.title('Logistic regression IRIS')
plt.xlabel('lambda', fontweight='bold')
plt.ylabel('f-score')
plt.show()
