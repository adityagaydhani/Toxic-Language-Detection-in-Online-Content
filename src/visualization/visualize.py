import itertools

import matplotlib.pyplot as plt
import numpy as np

def draw_performance_comparison(x, y):
	fig = plt.figure(figsize=(12,6))
	ax1 = fig.add_subplot(111)

	ax1.plot(x, y[0], label="Naive Bayes")
	ax1.plot(x, y[1], label="Logistic Regression")
	ax1.plot(x, y[2], label="Support Vector Machine")

	plt.xlabel('Features')
	plt.ylabel('Validation Accuracy')
	plt.title('Performance Comparison of Algorithms w.r.t different Features')
	ax1.legend(loc=2)
	plt.grid(True)

	plt.savefig("../../reports/figures/performance_comparison.png")
	plt.show()

def draw_hp_performance_nb(x, y):
	fig = plt.figure(figsize=(12,6))
	ax1 = fig.add_subplot(111)

	ax1.plot(x, y, label="Naive Bayes")
	ax1.annotate('0.934416', xy=(x[1], y[1]), xytext=(x[1], 0.92),
	            arrowprops=dict(facecolor='black', shrink=0.05))
	plt.xlabel('Hyperparameters')
	plt.ylabel('Validation Accuracy')
	plt.title('Result of Naive Bayes for different hyperparameter values')
	plt.grid(True)

	plt.savefig("../../reports/figures/naive_bayes_hp.png")
	plt.show()

def draw_hp_performance_lr(x, y):
	fig = plt.figure(figsize=(12,6))
	ax1 = fig.add_subplot(111)

	x, y = zip(*sorted(zip(x, y)))

	ax1.plot(x, y, label="Logistic Regression")
	ax1.annotate('0.951104', xy=(x[3], y[3]), xytext=(x[3], 0.9506),
	            arrowprops=dict(facecolor='black', shrink=0.05))
	plt.xlabel('Hyperparameters')
	plt.ylabel('Validation Accuracy')
	plt.title('Result of Logistic Regression for different hyperparameter values')
	plt.grid(True)

	plt.savefig("../../reports/figures/logistic_regression_hp.png")
	plt.show()

def draw_confusion_matrix(cm, classes,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
	fig = plt.figure()
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	fmt = '.3f'
	thresh = cm.max() / 2.
	for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
	    plt.text(j, i, format(cm[i, j], fmt),
	             horizontalalignment="center",
	             color="white" if cm[i, j] > thresh else "black")

	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')

	plt.savefig("../../reports/figures/confusion_matrix.png")
	plt.show()
