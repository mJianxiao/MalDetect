# coding:utf-8
import os
import sys
import joblib
from FeatureExtraction import FeatureExtraction
from FeatureProcess import FeatureProcess
from attention import attention
from Test import test
from keras.models import load_model


if __name__ == '__main__':
	benApkpath = ".."+os.sep+"BenignAPK"
	malApkPath = ".."+os.sep+"MaliciousAPK"
	benDatapath = ".."+os.sep+"Data"+os.sep+"BenData"
	malDatapath = ".."+os.sep+"Data"+os.sep+"MalData"
	FeaturePath = ".."+os.sep+"Data"+os.sep+"Featurelist"
	matrixPath = ".."+os.sep+"Data"+os.sep+"matrix"
	labelPath = ".."+os.sep+"Data"+os.sep+"label"
	modelPath = ".."+os.sep+"Data"+os.sep+"train_model"
	xtrainPath = ".."+os.sep+"Data"+os.sep+"xtrain"


# Extract features from apps
#	FeatureExtraction().productFeature(benApkpath, malApkPath, benDatapath, malDatapath)
#	Matrix, label = FeatureProcess().featureDeal(benDatapath, malDatapath, FeaturePath, matrixPath, labelPath)


# Model train
#	clf = attention().train(Matrix, label, modelPath)


# Detect samples
	trained_clf = load_model(modelPath)
	test(trained_clf).check()
