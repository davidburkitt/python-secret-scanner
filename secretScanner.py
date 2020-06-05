import os,sys,re, mmap

fileList = []
fileMatches = {}

#function1 to suck in regex list
def importPatterns(fileLoc):
   regexList = []
   if os.path.exists(fileLoc):
      with open(fileLoc, 'r') as f:
         for line in f:
            regexp = re.compile("(^#|^\\s*$)")
            if not re.search(regexp,line):
               regexList.append(line)
      print("### Loaded regex list:")
      print(*regexList)
      f.close()
   else:
      print("### Could not read regex list from " + fileLoc)
   return regexList

#function2 to scan files against regex list and return matches
def scanTree(dirLoc):
   global fileList, fileMatches
   for entry in os.scandir(dirLoc):
      if entry.is_dir(follow_symlinks=False):
         scanTree(entry.path)
      else:
         fileList.append(entry.path)
         fileMatches[entry.path] = []

def scanForSecrets(dirLoc, regexList):
   global fileList, fileMatches
   scanTree(dirLoc)
   for item in fileList:
      for pattern in regexList:
         regexp = re.compile(pattern)
         with open(item, 'r') as f:
            for line in f:
               match = re.match(regexp,line)
               if match:
                  fileMatches[item].append(line.replace('\n',''))

#main to run function1 then function2 and exit with status 
regexList = importPatterns("/Users/davidburkitt/git/repos/devops-secret-scanner/patterns.txt")
scanForSecrets("/Users/davidburkitt/git/repos/devops-secret-scanner", regexList)
for key in fileMatches.keys():
   if len(fileMatches[key]) > 0:
      print(key)
      print(fileMatches[key])