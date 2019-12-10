import os

l_all = []
found_select = False
current_select = ''

dirName = os.getcwd()
print('Current dir: ' + dirName)

def print_select(select, file, numLine):
  all_selects.write('################################################################################################## \r\n')
  #all_selects.write('\r\n')
  all_selects.write('ARCHIVO: ' + file + '\r')
  all_selects.write('LINEA: ' + str(numLine) + '\r\n')
  all_selects.write(select + '\r')
  all_selects.write('################################################################################################## \r')

def getListOfFiles(dirName):
  # create a list of file and sub directories 
  # names in the given directory 
  listOfFile = os.listdir(dirName)
  allFiles = list()
  # Iterate over all the entries
  for entry in listOfFile:
    # Create full path
    fullPath = os.path.join(dirName, entry)
    # If entry is a directory then get the list of files in this directory 
    if os.path.isdir(fullPath):
      allFiles = allFiles + getListOfFiles(fullPath)
    else:
      allFiles.append(fullPath)
              
  return allFiles  

# Get the list of all files in directory tree at given path
listOfFiles = getListOfFiles(dirName)

# Print the files
all_selects = open('all_selects.txt', mode='w+', encoding='utf8')

for file in listOfFiles:
  print(file)
  current_file = file
  with open(file, mode='r', encoding='utf8') as f:
    for num, line in enumerate(f, 1):
      if (line.rfind('= " select') > -1 or line.rfind('= "select') > -1 or line.rfind('=" select') > -1 or line.rfind('= " Select') > -1 or line.rfind('= "Select') > -1 or line.rfind('=" Select') > -1 or line.rfind('= " SELECT') > -1 or line.rfind('= "SELECT') > -1 or line.rfind('=" SELECT') > -1) and file.rfind('search_selects.py') == -1:
        found_select = True
        line_select = num
      if found_select:
        current_select += line
        if line.rfind(';') > -1:
          found_select = False
          l_all.append(current_select)
          print_select(current_select, current_file, line_select)
          current_select = ''

all_selects.write('\r')
all_selects.write('----------------------------------\r')
all_selects.write('TOTAL SELECTS: ' + str(len(l_all)))
all_selects.close()
