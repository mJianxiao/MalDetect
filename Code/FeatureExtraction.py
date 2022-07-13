# -*- coding: utf-8 -*-
import sys
import os
import shutil
from multiprocessing import Process, Manager, Lock
import random
from GetAPI import GetAPI
from GetPermission import GetPermission
from log import Log

class FeatureExtraction:
	def __init__(self):
		self.logger = Log(self)
		self.apk = ".."+os.sep+"apk"

	def filesInFolder(self, folderPath, suffix):
		self.logger.info("Traversing " + folderPath + " folder")
		if not os.path.exists(folderPath):
			self.logger.error(folderPath + "does not exist")
			return
		files = os.listdir(folderPath)
		suit = list()
		for file in files:
			if file.endswith(suffix):
				suit.append(file)
		return suit		

	def getFeature(self, Apkpath, apk, Datapath):
		GetAPIClass = GetAPI()
		GetPermissionClass = GetPermission()
		try:
			GetAPIClass.getAPICalls(Apkpath, apk, Datapath)
			GetPermissionClass.getPermissions(Apkpath, apk, Datapath)
		except Exception as e:
			name = apk.replace(".apk", "")
			permissionName = Datapath+os.sep+name+"_Permission.txt"
			if os.path.exists(permissionName):
				os.remove(permissionName)
			apiName=Datapath+os.sep+name+"_API.txt"
			if os.path.exists(apiName):
				os.remove(apiName)
			self.logger.info(apk+"Features Extraction errors.")
			print(apk+"Features Extraction errors.")

	def getFeatures(self,Apkpath,apks,Datapath,fileLock,getfile):
		random.shuffle(apks)
		
		for apk in apks:
			fileLock.acquire()
			if apk not in getfile:
				getfile.append(apk)
				fileLock.release()
				self.getFeature(Apkpath,apk,Datapath)
			else:
				fileLock.release()

	def productFeature(self, benApkpath, malApkPath, benDatapath, malDatapath):
		BenFileLock = Lock()
		MalFileLock = Lock()

		m = Manager()
		getBenFile = m.list()
		getMalFile = m.list()


		benApks = self.filesInFolder(benApkpath, ".apk")
		malApks = self.filesInFolder(malApkPath, ".apk")
		
		bthreads = []
		mthreads = []
		
		for i in range(1):
			bthread = Process(target=self.getFeatures, args=(benApkpath,benApks,benDatapath,BenFileLock,getBenFile))
			bthreads.append(bthread)
		
		for i in range(2):
			mthread = Process(target=self.getFeatures, args=(malApkPath,malApks,malDatapath,MalFileLock,getMalFile))
			mthreads.append(mthread)
			
		for bthread in bthreads:
			bthread.start()
		for mthread in mthreads:
			mthread.start()
		
		for bthread in bthreads:
			bthread.join()
		for mthread in mthreads:
			mthread.join()
		print("exists multi-process")


if __name__ == '__main__':
	adapter = FeatureExtraction()
	adapter.productFeature(sys.argv[1], sys.argv[2])
