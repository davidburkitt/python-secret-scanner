import os,sys,re

fileList = []
fileMatches = {}
flags = {"-patterns":[1,1],"-dir":[1,1],"-negative":[0,0]}
props = {}

def help(errorMessage):
   """ Exit with help."""
   usage = "\n### Usage: -patterns <regex-list> -dir <scan-location>"
   sys.exit(errorMessage + usage)

def parseArgs():
   """ Parse input arguments. """
   global props, flags
   for flag in flags.keys():
      if flag in sys.argv:         
         if flags[flag][0]:
            if sys.argv.index(flag)+1 == len(sys.argv) or sys.argv[sys.argv.index(flag)+1] in flags.keys():
               help("### " + flag + " requires a value.")
            else:            
               props[flag] = sys.argv[sys.argv.index(flag)+1]
         else:
            props[flag] = 1
      else:
         if flags[flag][1]:
            help("### " + flag + " is a required flag.")

def importPatterns(fileLoc):
   """ Import regex patterns from a file. """
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

def scanTree(dirLoc):
   """ Recursively search for files """
   global fileList, fileMatches
   for entry in os.scandir(dirLoc):
      if entry.is_dir(follow_symlinks=False):
         scanTree(entry.path)
      else:
         fileList.append(entry.path)
         fileMatches[entry.path] = []

def scanForMatches(dirLoc, regexList):
   """ Scan all files for regex matches """
   global fileList, fileMatches
   scanTree(dirLoc)
   for item in fileList:
      for pattern in regexList:
         regexp = re.compile(pattern)
         print("Scanning " + item)
         with open(item, 'r') as f:
            try:
               for line in f:
                  match = re.match(regexp,line)
                  if match:
                     fileMatches[item].append(line.replace('\n',''))
            except UnicodeDecodeError:
               pass

def main():
   parseArgs()
   regexList = importPatterns(props["-patterns"])
   scanForMatches(props["-dir"], regexList)
   if len(fileMatches) > 0:
      print("\n### Found matches")
      for key in fileMatches.keys():
         if len(fileMatches[key]) > 0:
            print(key)
            print(fileMatches[key])
      if "-negative" in props.keys():
         sys.exit(1)
      else:
         sys.exit(0)
   else:
      if "-negative" in props.keys():
         sys.exit(0)
      else:
         sys.exit(1)

if __name__ == "__main__":
    main()