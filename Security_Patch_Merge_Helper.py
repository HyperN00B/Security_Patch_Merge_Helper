import os
import requests
import sys
import time
import numpy
import subprocess
import shutil

os.system("clear")
vPathForScript=os.getcwd()

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
		if not mrSourceRootPath.endswith("/"):
			mrSourceRootPath=mrSourceRootPath+"/"
		pass
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
		while True:
			os.system("clear")
			mvUsePrev=input("Previous source root usage found!\nDo you want to use that? (y/n)\n:")
			if mvUsePrev.upper()=="Y" or mvUsePrev.upper()=="YES":
				mrSourceRootPath=open("PreviousSourceRoot.txt","r").readlines()[0]
				return mrSourceRootPath
			elif mvUsePrev.upper()=="N" or mvUsePrev.upper()=="NO":
				mrNewPath=mGetSourceRoot()
				return mrNewPath
			else:
				os.system("clear")
				print("A yes or no would've been enough 😐")
				time.sleep(3)
				continue
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
	for i,item in enumerate(miFoundXmls):
		mvManifestIds.append(i)
		mvManifestFiles.append(item)
	pass
	while True:
		os.system("clear")
		print("Please choose an xml file to use!")
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
			continue
		pass
	pass
pass

def mReadReposFromManifest(miRequestedManifestFile):
	print("Reading repos from the selected manifest...")
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

def mFormatReposList(miRawReposList):
	mvListItemsSplit=[]
	mrPathsList=[]
	for i,item in enumerate(miRawReposList):
		mvListItemsSplit.append(item.split(" "))
	pass
	for i,item in enumerate(mvListItemsSplit):
		for j,jtem in enumerate(item):
			if "path=" in jtem:
				mrPathsList.append(jtem[6:][:-1])
			pass
		pass
	pass
	mvIndexOfBuildMake=mrPathsList.index("build/make")
	for i,item in enumerate(mrPathsList):
		if item=="build/make":
			mrPathsList[i]="build"
		pass
	pass
	return mrPathsList
pass

def mCheckRemoteRepoState(miListOfRepos):
	os.system("clear")
	print("Checking repo availability on AOSP site!\nThis may take a while depending on your internet bandwidth and the length of the selected manifest file")
	mr404Repos=[]
	mrAvailablePlatform=[]
	mrAvailableNonPlatform=[]
	for i,item in enumerate(miListOfRepos):
		mvResponsePlatform=requests.get("https://android.googlesource.com/platform/"+item)
		mvResponseNonPlatform=requests.get("https://android.googlesource.com/"+item)
		if not mvResponsePlatform and not mvResponseNonPlatform:
			mr404Repos.append(item)
		elif mvResponsePlatform:
			mrAvailablePlatform.append(item)
		elif mvResponseNonPlatform:
			mrAvailableNonPlatform.append(item)
		else:
			return -1
		pass
	pass
	return mr404Repos,mrAvailablePlatform,mrAvailableNonPlatform
pass

def mDetermineOSVersion():
	os.chdir(vSourceRootFound)
	os.chdir("build/make/core")
	mvVersionDef=open("version_defaults.mk","r").readlines()
	for i,line in enumerate(mvVersionDef):
		if "PLATFORM_VERSION_LAST_STABLE :=" in line:
			mrAndroidVersion=line.split(" := ")
		pass
	pass
	return mrAndroidVersion[1]
pass

def mGetAvailableTags():
	mrAvailableTagsLst=[]
	if "manifest" in os.listdir(vPathForScript):
		os.chdir(vPathForScript)
		shutil.rmtree("manifest")
	subprocess.run("git clone https://android.googlesource.com/platform/manifest "+vPathForScript+"/manifest",shell=True,capture_output=True)
	os.chdir("manifest")
	mrAvailableTagsStr=str(subprocess.check_output("git tag -l | grep android-"+vOSVersionFound,shell=True))
	mrAvailableTagsLst=mrAvailableTagsStr.split("\\n")
	mrAvailableTagsLst[0]=mrAvailableTagsLst[0][2:]
	mrAvailableTagsLst=mrAvailableTagsLst[:-1]
	return mrAvailableTagsLst
pass

def mFetchRepos(miReposList):
	print("Fetching AOSP tags...")
	mvPlatformRepos=miReposList[1]
	mvNonPlatformRepos=miReposList[2]
	for i,item in enumerate(mvPlatformRepos):
		os.chdir(vSourceRootFound)
		if miReposList[1][i]=="build":
			os.chdir("build/make")
		else:
			os.chdir(item)
		pass
		mvFetchState=str(subprocess.run("git remote add AOSP https://android.googlesource.com/platform/"+item+" && git fetch AOSP",shell=True,capture_output=True))
		if "already exists" in mvFetchState:
			subprocess.run("git remote set-url AOSP https://android.googlesource.com/platform/"+item+" && git fetch AOSP",shell=True,capture_output=True)
			print("Updated remote: \"AOSP\" in "+item)
		pass
	pass
	for i,item in enumerate(mvNonPlatformRepos):
		os.chdir(vSourceRootFound)
		os.chdir(item)
		mvFetchState=str(subprocess.run("git remote add AOSP https://android.googlesource.com/"+item+" && git fetch AOSP",shell=True,capture_output=True))
		if "already exists" in mvFetchState:
			subprocess.run("git remote set-url AOSP https://android.googlesource.com/"+item+" && git fetch AOSP",shell=True,capture_output=True)
		pass
	pass
pass

def mMergeTags(miReposList,miAvailableTags):
	while True:
		os.system("clear")
		print("The available tags are the following:")
		print("-------------------------------------")
		for i,item in enumerate(miAvailableTags):
			print(item)
		pass
		print("-------------------------------------")
		mvChosenTag=input("Please select one of the above tags!\nTag to be merged: ")
		if mvChosenTag in miAvailableTags:
			mvMergableTag=mvChosenTag
			break
		else:
			print("The chosen tag is invalid!")
			time.sleep(3)
			continue
		pass
	pass
	print("Merging security patch...")
	mrMergedRepos=[]
	mrConflictingRepos=[]
	mrReposAlreadyOnTag=[]
	mrDirtyRepos=[]
	mvCompleteRepoList=miReposList[1]+miReposList[2]
	for i,item in enumerate(mvCompleteRepoList):
		os.chdir(vSourceRootFound)
		if item=="build":
			os.chdir("build/make")
		else:
			os.chdir(item)
		pass
		if mvMergableTag in str(subprocess.run("git log",shell=True,capture_output=True)):
			mvCompleteRepoList.pop(mvCompleteRepoList.index(item))
			mrReposAlreadyOnTag.append(item)
		pass
	pass
	for i,item in enumerate(mvCompleteRepoList):
		os.chdir(vSourceRootFound)
		if mvCompleteRepoList[i]=="build":
			os.chdir("build/make")
		else:
			os.chdir(item)
		pass
		mvMergeState=str(subprocess.run("git merge "+mvMergableTag,shell=True,capture_output=True))
		if "CONFLICT" in mvMergeState:
			mrConflictingRepos.append(item)
		elif "Merging is not possible" in mvMergeState:
			mrDirtyRepos.append(item)
		elif "Merge made" in mvMergeState:
			mrMergedRepos.append(item)
		else:
			print("Even god don't know what happened to "+item)
		pass
	pass
	return miReposList[0], mrMergedRepos, mrConflictingRepos, mrReposAlreadyOnTag, mrDirtyRepos
pass

def mExportResults(mi404, miMerged, miConflicting, miAlready, miDirty):
	os.chdir(vPathForScript)
	if "Results.txt" in os.listdir():
		os.remove("Results.txt")
	mvFile=open("Results.txt","a")
	mvFile.write("Succesfully Merged:\n")
	for i,item in enumerate(miMerged):
		mvFile.write(item+"\n")
	pass
	mvFile.write("")
	mvFile.write("Conflicting:")
	for i,item in enumerate(miConflicting):
		mvFile.write(item+"\n")
	pass
	mvFile.write("")
	mvFile.write("Already up-to-date:")
	for i,item in enumerate(miAlready):
		mvFile.write(item+"\n")
	pass
	mvFile.write("")
	mvFile.write("Contains uncommitted changes:")
	for i,item in enumerate(miDirty):
		mvFile.write(item+"\n")
	pass
	mvFile.write("")
	mvFile.write("Not found in AOSP:")
	for i,item in enumerate(mi404):
		mvFile.write(item+"\n")
	pass
	mvFile.flush()
pass

#TODO: Add a way to unshallow repos

if 

mWelcome()
vSourceRootFound=mPreviousRootCheck()
vAvailableXmlFiles=mGetManifestXmls(vSourceRootFound)
vSelectedXml=mListAndSelectXml(vAvailableXmlFiles)
vReposRawList=mReadReposFromManifest(vSelectedXml)
vReposFormattedList=mFormatReposList(vReposRawList)
vOSVersionFound=mDetermineOSVersion()
vAvailableAnd404Repos=mCheckRemoteRepoState(vReposFormattedList)
vAvailableTags=mGetAvailableTags()
mFetchRepos(vAvailableAnd404Repos)
vExportableResults=mMergeTags(vAvailableAnd404Repos,vAvailableTags)
mExportResults(vExportableResults[0],vExportableResults[1],vExportableResults[2],vExportableResults[3],vExportableResults[4])