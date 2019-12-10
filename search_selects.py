import os

l_all_selects, l_without_relationship, l_with_relationship = [], [], []
found_select = False
b_without_relationship = False
current_select = ''

dirName = os.getcwd()
print('Current dir: ' + dirName)

def print_select(select, file, num_line, file_to_write):
  file_to_write.write('################################################################################################## \r\n')
  #file_to_write.write('\r\n')
  file_to_write.write('ARCHIVO: ' + file + '\r')
  file_to_write.write('LINEA: ' + str(num_line) + '\r\n')
  file_to_write.write(select + '\r')
  file_to_write.write('################################################################################################## \r')

def end_print_and_close(file, list):
  file.write('\r')
  file.write('----------------------------------\r')
  file.write('TOTAL SELECTS: ' + str(len(list)))
  file.close()

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
without_relationship = open('without_relationship.txt', mode='w+', encoding='utf8')
with_relationship = open('with_relationship.txt', mode='w+', encoding='utf8')

for file in listOfFiles:
  print(file)
  current_file = file
  with open(file, mode='r', encoding='utf8') as f:
    for num, line in enumerate(f, 1):
      if (line.upper().rfind('= " SELECT') > -1 or line.upper().rfind('= "SELECT') > -1 or line.upper().rfind('=" SELECT') > -1) and file.rfind('search_selects.py') == -1 and file.rfind('search_selects_of_table.py') == -1:
        found_select = True
        line_select = num
      if found_select:
        current_select += line
        if line.upper().rfind('FROM') > -1:
          index_of_from = line.upper().rfind('FROM')
          if line.rfind(',', index_of_from) == -1:
            b_without_relationship = True
        if line.rfind(';') > -1:
          found_select = False
          l_all_selects.append(current_select)
          print_select(current_select, current_file, line_select, all_selects)
          if b_without_relationship:
            print_select(current_select, current_file, line_select, without_relationship)
            l_without_relationship.append(current_select)
            b_without_relationship = False
          else:
            print_select(current_select, current_file, line_select, with_relationship)
            l_with_relationship.append(current_select)
          current_select = ''

end_print_and_close(all_selects, l_all_selects)
end_print_and_close(without_relationship, l_without_relationship)
end_print_and_close(with_relationship, l_with_relationship)
