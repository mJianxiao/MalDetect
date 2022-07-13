# -*- coding: utf-8 -*-
import os
import pandas as pd
from log import Log


class GetFeature:

	def __init__(self):
		self.logger=Log(self)
		self.APIFile = ".."+os.sep+"Feature"+os.sep+"API.txt"
		self.permissionFile = ".."+os.sep+"Feature"+os.sep+"permission.txt"
		self.featurelistPath = ".."+os.sep+"Data"+os.sep+"featureList.csv"
		self.featurelist = list()
		
	def featureFromFile(self,filePath):
		if not os.path.exists(filePath):
			self.logger.error(filePath+"does not exist")
			print(filePath+"does not exist")
			return
		ls=list()
		with open(filePath,'r')as f:
			while(True):
				line=f.readline()
				if not line:break
				s=line.replace("\n","")
				s=s.replace("\r","")
				ls.append(s)
		return ls
		
	def generateFeatureList(self):
		ls1 = self.featureFromFile(self.APIFile)
		ls2 = self.featureFromFile(self.permissionFile)
		self.featurelist = ls1+ls2
		
		frame = pd.DataFrame(self.featurelist)
		frame.to_csv(self.featurelistPath,header=False,index=False)
		
		return self.featurelist


if __name__ == '__main__':
	adapter = GetFeature()
	ls = adapter.generateFeatureList()
	print(ls)
