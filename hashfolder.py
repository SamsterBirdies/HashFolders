import hashlib, os, sys
'''
This script will take a hash of a folder. This scans subfolders recursively. This does not scan empty folders.
Argument usage: <mode ('save' or 'load')> <folder to hash> <hash savefile name>
Example argument usage: py hashfolder.py save pictures picturesHash.txt
'''
#constants
HashType = hashlib.sha256 #valid choices are sha1,sha224,sha256,sha384,sha512,md5,blake2b,blake2s. Default is sha256
#globals
fileslist = []
hashfiles = []
totalhash = ""
#functions
def ScanFolderRecursive(folder):
	with os.scandir(folder) as dir:
		for item in dir:
			if item.is_file():
				fileslist.append(folder+"/"+item.name)
			else:
				ScanFolderRecursive(folder+"/"+item.name)
#gather input
if len(sys.argv) > 1:
	mode = sys.argv[1]
	scanfolder = sys.argv[2]
	savefile = sys.argv[3]
else:
	mode = input("'load' or 'save' hash save:")
	scanfolder = input("Folder to hash:")
	savefile = input("Hash save filename:")
#adjust HashType to loaded type.
if mode == "load":
	with open(savefile,"rt") as file:
		tempType = file.readline()[:-1]
		if tempType == "sha1":
			HashType = hashlib.sha1
		elif tempType == "sha224":
			HashType = hashlib.sha224
		elif tempType == "sha256":
			HashType = hashlib.sha256
		elif tempType == "sha384":
			HashType = hashlib.sha384
		elif tempType == "sha512":
			HashType = hashlib.sha512
		elif tempType == "md5":
			HashType = hashlib.md5
		elif tempType == "blake2b":
			HashType = hashlib.blake2b
		elif tempType == "blake2s":
			HashType = hashlib.blake2s
		else:
			print("Error: invalid algorithm '"+tempType+"'")
			exit(0)
#scan folder
ScanFolderRecursive(scanfolder)
#hash folder
print("Hashing with "+HashType().name+". Algorithm can be changed in file.\n")
for x in fileslist:
	with open(x,'rb') as file:
		hash = HashType
		hashfiles.append(hash(file.read()).hexdigest())
#total hash
hash = HashType()
for x in hashfiles:
	hash.update(bytes(x,'utf-8'))
totalhash = hash.hexdigest()
#save/load
if mode == "save":
	with open(savefile,"wt") as file:
		txt = ""
		txt+=HashType().name
		txt+="\n"
		txt+= ",".join(fileslist)
		txt+="\n"
		txt+= ",".join(hashfiles)
		txt+="\n"+totalhash
		file.write(txt)
	print("Hash Successfully completed and saved as "+savefile)
	print("Total hash:"+totalhash)
elif mode == 'load':
	#load data
	with open(savefile,"rt") as file: #process file into lists
		HashTypeLoad = file.readline()[:-1]#remove \n from last entry
		fileslistLoad = file.readline().split(",")
		fileslistLoad[len(fileslistLoad)-1] = fileslistLoad[len(fileslistLoad)-1][:-1] #remove \n from last entry
		hashfilesLoad = file.readline().split(",")
		hashfilesLoad[len(hashfilesLoad)-1] = hashfilesLoad[len(hashfilesLoad)-1][:-1] #remove \n from last entry
		totalhashLoad = file.readline()
	#create dictionary for name,hash. (this was tacked on)
	LoadHashDict = {}
	i=0
	for x in fileslistLoad:
		LoadHashDict[x]= hashfilesLoad[i]
		i+=1
	#test
	if totalhashLoad == totalhash:
		print("Total hash matches with hash:"+totalhash)
	else:
		print("Total hash does not match!\nCurrent hash:"+totalhash+"\nSaved hash  :"+totalhashLoad)
	if fileslistLoad != fileslist:
		print("Folder has new/deleted items!")
		for x in fileslist:
			if x not in fileslistLoad:
				print("new item:"+x)
		for x in fileslistLoad:
			if x not in fileslist:
				print("deleted item:"+x)
	if hashfilesLoad != hashfiles:
		#print("Items with new hash:")
		i=0
		for x in hashfiles:
			try:
				if x != LoadHashDict[fileslist[i]]:
					print(fileslist[i]+" new hash:"+x+".")
					print(fileslist[i]+" old hash:"+LoadHashDict[fileslist[i]]+".")
			except:
				pass
			i+=1