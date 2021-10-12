import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from time import time

iris = load_iris()
x = iris.data
y = iris.target
train_data, test_data, train_classes, test_classes = train_test_split(x, y, test_size=0.2, random_state=4)

k_scores_acc = []
k_scores_f = []
start = time()
for k in range(1, 30):
    knn = KNeighborsClassifier(k)
    knn.fit(train_data, train_classes)
    pred_classes = knn.predict(test_data)

    acc = accuracy_score(test_classes, pred_classes)
    f = f1_score(test_classes, pred_classes, average='micro')
    k_scores_acc.append(acc)
    k_scores_f.append(f)
end = time()

pred_time = end - start
max_acc = np.max(k_scores_acc)
max_f = np.max(k_scores_f)
best_k_acc = []
best_k_f = []

for i in range(len(k_scores_acc)):
    if k_scores_acc[i] == max_acc:
        best_k_acc.append(i + 1)
    if k_scores_f[i] == max_f:
        best_k_f.append(i + 1)

print('Prediction time: {:.2f}'.format(pred_time))
print('\nBest accuracy: {:.3f}'.format(max_acc))
print('Best f-score: {:.3f}'.format(max_f))
print('k values with best accuracy:', best_k_acc)
print('k values with best f-score:', best_k_f)
print(best_k_acc == best_k_f)

plt.plot(range(1, 30), k_scores_acc)
plt.title('k-NN IRIS', fontweight='bold')
plt.xlabel('k', fontweight='bold')
plt.ylabel('accuracy', fontweight='bold')
plt.show()
plt.clf()

plt.plot(range(1, 30), k_scores_acc)
plt.title('k-NN IRIS', fontweight='bold')
plt.xlabel('k', fontweight='bold')
plt.ylabel('f-score', fontweight='bold')
plt.show()
