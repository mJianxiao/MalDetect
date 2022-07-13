# coding:utf-8
from sklearn.externals import joblib
import numpy as np
import os
from log import Log
import pickle 
import pandas as pd
from GetFeatureMatrix import GetFeatureMatrix

class FeatureProcess:
	def __init__(self):
		self.logger = Log(self)
		
	def featureDeal(self, benDatapath, malDatapath, FeaturePath, matrixPath, labelPath):
		GetFeatureMatrixClass = GetFeatureMatrix()
		Matrix,label,featureList= GetFeatureMatrixClass.getFeatureMatric(benDatapath, malDatapath)
		
		joblib.dump(featureList, FeaturePath)
		joblib.dump(Matrix, matrixPath)
		joblib.dump(label, labelPath)

		print("length:%d"%(Matrix.shape[1]))
		frame = pd.DataFrame(Matrix, columns=featureList)
		frame.to_csv(".."+os.sep+"Data"+os.sep+'feature.csv', index=False)
		frame = pd.DataFrame(label)
		frame.to_csv(".."+os.sep+"Data"+os.sep+'label.csv', header=False, index=False)
		
		return Matrix, label


if __name__=='__main__':
	adapter = FeatureProcess()
	Matrix, label = adapter.featureDeal()
