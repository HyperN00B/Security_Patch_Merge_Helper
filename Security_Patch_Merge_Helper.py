import os
import requests
import sys
import time
import subprocess
import numpy

os.system('clear')

def mWelcome():
	os.system("clear")
	print("Welcome to Security Patch Merge Helper or SPMH for short!")
	print("Made by: HyperN00B")
	time.sleep(4)
	os.system("clear")
pass

def mGetSourceRoot():
	os.system("clear")
	print("Please enter the path to the source root!")
	mrSourceRootPath=input("Drag&dropping the folder also works 😉\nHere:")
	if os.path.isdir(mrSourceRootPath) and "build" in os.listdir(mrSourceRootPath) and "vendor" in os.listdir(mrSourceRootPath):
		mvStoreSource=open("PreviousSourceRoot.txt","w")
		mvStoreSource.write(mrSourceRootPath)
		mvStoreSource.flush()
		return mrSourceRootPath
	elif os.path.isdir(mrSourceRootPath) and "build" in os.listdir(mrSourceRootPath) and not "vendor" in os.listdir(mrSourceRootPath):
		print("This is a pure AOSP source, just change the tag in the manifest and resync the source!")
		time.sleep(4)
		sys.exit()
	elif os.path.isdir(mrSourceRootPath) and not "build" in os.listdir(mrSourceRootPath) and not "vendor" in os.listdir(mrSourceRootPath):
		print("The path you chose is not pointing to an Android ROM source code")
		time.sleep(3)
		mGetSourceRoot()
	elif not mrSourceRootPath:
		print("Empty input is not valid, sorry")
		time.sleep(3)
		mGetSourceRoot()
	else:
		print("Using some random bulls*it as source root won't work! :D")
		time.sleep(3)
		mGetSourceRoot()
	pass
pass

def mPreviousRootCheck():
	os.system("clear")
	mvPreviousPathContainer=open("PreviousSourceRoot.txt","r")
	mvPreviousPathContainerContent=mvPreviousPathContainer.readlines()
	if os.path.exists("PreviousSourceRoot.txt") and len(mvPreviousPathContainerContent)!=0 \
	and os.path.isdir(mvPreviousPathContainerContent[0]) \
	and "build" in os.listdir(mvPreviousPathContainerContent[0]) \
	and "vendor" in os.listdir(mvPreviousPathContainerContent[0]):
		#TODO: Make the except display the invalid input msg
		while True:
			try:
				os.system("clear")
				mvUsePrev=input("Previous source root usage found!\nDo you want to use that? (y/n)\n:")
			except mvUsePrev.upper()!="Y":
				os.system("clear")
				print("A yes or no would've been enough 😐")
				time.sleep(3)
				continue
			pass
			if mvUsePrev.upper()=="Y" or mvUsePrev.upper()=="YES":
				mrSourceRootPath=open("PreviousSourceRoot.txt","r").readlines()[0]
				return mrSourceRootPath
			elif mvUsePrev.upper()=="N" or mvUsePrev.upper()=="NO":
				mrNewPath=mGetSourceRoot()
				return mrNewPath
			pass
		pass
	pass
pass

def mGetManifestXmls(miSourceRootPath):
	os.system("clear")
	if not len(miSourceRootPath)==0 and os.path.isdir(miSourceRootPath):
		mvRepoManifestsPath=os.path.join(str(miSourceRootPath)+".repo/manifests/")
		os.chdir(mvRepoManifestsPath)
		mvManifestFolderContent=os.listdir(mvRepoManifestsPath)
		mvSubFolders=[]
		mvFilesFound=[]
		for i,item in enumerate(mvManifestFolderContent):
			if os.path.isdir(item) and not item==".git":
				mvSubFolders.append(item)
			elif os.path.isfile(item) and item.endswith(".xml") and item!="default.xml":
				mvFilesFound.append(item)
			pass
		pass
		if bool(mvSubFolders):
			mvFilesInSubdir=os.listdir(mvSubFolders[0])
			for i,item in enumerate(mvFilesInSubdir):
				mvFilesFound.append(str(mvSubFolders[0])+"/"+str(mvFilesInSubdir[i]))
			pass
		pass
		return mvFilesFound
	pass
pass

def mListAndSelectXml(miFoundXmls):
	os.system("clear")
	mvManifestIds=[]
	mvManifestFiles=[]
	print("Please choose an xml file to use!")
	for i,item in enumerate(miFoundXmls):
		mvManifestIds.append(i)
		mvManifestFiles.append(item)
	pass
	mvIdAndFiles=numpy.array((mvManifestIds,mvManifestFiles))
	for i,item in enumerate(miFoundXmls):
		mvMenuItemIndex=int(mvIdAndFiles[0][i])+1
		mvMenuItemValue=mvIdAndFiles[1][i]
		mvMenuItemAndValue=str(mvMenuItemIndex)+": "+str(mvMenuItemValue)
		print(mvMenuItemAndValue)
	pass
	mvChosenXml=input("Your choice:")
	if str(int(mvChosenXml)-1) in mvIdAndFiles:
		return mvIdAndFiles[1][int(mvChosenXml)-1]
	else:
		os.system("clear")
		print("Sorry but \""+mvChosenXml+"\" is not a valid option")
		time.sleep(3)
		mListAndSelectXml(miFoundXmls)
	pass
pass

def mReadReposFromManifest(miRequestedManifestFile):
	mrReposRead=[]
	mvOpenedXml=open(miRequestedManifestFile,"r")
	mvOpenedXmlLines=mvOpenedXml.readlines()
	for i,item in enumerate(mvOpenedXmlLines):
		if "project" in item and "name=" in item:
			mrReposRead.append(item)
		pass
	pass
	return mrReposRead
pass

#def mReadReposFromManifest(miRequestedManifestFile):

#def mGetWebpageResponse(URL):

mWelcome()
vSourceRootFound=mPreviousRootCheck()
vAvailableXmlFiles=mGetManifestXmls(vSourceRootFound)
vSelectedXml=mListAndSelectXml(vAvailableXmlFiles)
vReposInList=mReadReposFromManifest(vSelectedXml)
