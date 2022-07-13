# coding:utf-8
import numpy as np
import os
import logging
import sys
from GetFeature import GetFeature
from log import Log
import pandas as pd
import threading
import random


class GetFeatureMatrix:
	def __init__(self):
		self.featureList = GetFeature().generateFeatureList()
		self.APKlist = list()
		self.Matrix = np.zeros((0, self.featureList.__len__()), dtype=int)
		self.label = list()
		self.MatrixLock = threading.Lock()
		self.APKlistLock = threading.Lock()
		self.logger = Log(self)
		
	def featureFromFile(self, filePath):

		if not os.path.exists(filePath):
			self.logger.error(filePath+" does not exist")
			print(filePath+" does not exist")
			return
		ls=list()
		with open(filePath, 'r', encoding='UTF-8')as f:
			while(True):
				line=f.readline()
				if not line:break
				s=line.replace("\n","")
				s=s.replace("\r","")
				ls.append(s)
		return ls

	def filesInFolder(self, folderPath, suffix):
		self.logger.info("Traversing " + folderPath + " folder")
		if not os.path.exists(folderPath):
			self.logger.error(folderPath + " does not exist")
			return
		files = os.listdir(folderPath)
		#print files
		suit = list()
		for file in files:
			if file.endswith(suffix):
				suit.append(file)
		return suit
		
	def getFeaturefromAPK(self, dataPath, apkName):
		apiFile = apkName.replace(".apk","_API.txt")
		permissionFile = apkName.replace(".apk","_Permission.txt")
		
		apkFeature = np.zeros((1,self.featureList.__len__()), dtype=int)
		try:		
			perList = self.featureFromFile(dataPath+os.sep+apiFile)
			self.logger.info("Extract" + apiFile + "feature Matrix")
			print("Extract" + apiFile + "feature Matrix")
			for p in perList:
				if p in self.featureList:
					i = self.featureList.index(p)
					apkFeature[0][i] = 1
		
			perList = self.featureFromFile(dataPath+os.sep+permissionFile)
			self.logger.info("Extract" + permissionFile + "feature Matrix")
			print("Extract" + permissionFile + "feature Matrix")
			for p in perList:
				if p in self.featureList:
					i = self.featureList.index(p)
					apkFeature[0][i] = 1

		except Exception as e:
			self.logger.info(apkName+"feature matrix extraction errors.")
			print(apkName+"feature matrix extraction errors.")
		return apkFeature

	def getFeaturefromDocument(self,dataPath,flag):
		apks = self.filesInFolder(dataPath, "_Permission.txt")
		for i in range(apks.__len__()):
			apks[i] = apks[i].replace("_Permission.txt", ".apk")

		ll = list(set(apks).difference(set(self.APKlist)))
		random.shuffle(ll)
		
		for apk in ll:
			self.APKlistLock.acquire()
			if apk not in self.APKlist:
				self.APKlist.append(apk)
				self.APKlistLock.release()
				features = self.getFeaturefromAPK(dataPath, apk)
				self.MatrixLock.acquire()
				self.Matrix = np.vstack((self.Matrix, features))
				self.label.append(flag)
				self.MatrixLock.release()
			else:
				self.APKlistLock.release()


	def getFeatureMatric(self,benDatapath,malDatapath):
		print("Start multithreading to extract API features")
		bthreads = []
		mthreads = []
		
		for i in range(10):
			bthread= threading.Thread(target=self.getFeaturefromDocument, args=(benDatapath,0) )
			bthreads.append(bthread)
		
		for i in range(10):
			mthread= threading.Thread(target=self.getFeaturefromDocument, args=(malDatapath,1) )
			mthreads.append(mthread)
			
		for bthread in bthreads:
			bthread.start()
		for mthread in mthreads:
			mthread.start()
		
		for bthread in bthreads:
			bthread.join()
		for mthread in mthreads:
			mthread.join()
		print("exist multithreading")
		
		self.label = np.array(self.label)
		return self.Matrix,self.label,self.featureList
		

if __name__=='__main__':
	adapter = GetFeatureMatrix()
	Matrix,label,EachfeaNum,featureList = adapter.getFeatureMatric(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
#	print(Matrix)
#	print(label)
#	print(EachfeaNum)
#	print(featureList)
