import os
import shutil
import json

def sortLocation(targetDirectory):
    
    #Check Folder exists
    if not os.path.exists(targetDirectory):
        print(f"Error: The folder '{targetDirectory}' does not exist.")
        return

    #File Categories
    categoryMap = {
        '.mp4': 'Videos', '.mkv': 'Videos', '.mov': 'Videos', '.avi': 'Videos',
        '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio',
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
        '.pdf': 'Documents', '.txt': 'Documents', '.docx': 'Documents',
        '.exe': 'Executables', '.msi': 'Executables', 
        '.zip': 'Archives', '.rar': 'Archives'
    }

    # Ask the OS for a list of everything inside the target folder.
    listItems = os.listdir(targetDirectory)
    filesMoved = 0 

    # Loop through every item in the folder, one by one.
    for item in listItems:
        
        itemPath = os.path.join(targetDirectory, item)
        
        #Skip Folders only sort files
        if os.path.isfile(itemPath):
            
            fileName, fileExtension = os.path.splitext(item)
            fileExtension = fileExtension.lower()
            
            #Look up file type using category map & add Misc 
            categoryName = categoryMap.get(fileExtension, 'Misc')
            targetFolder = os.path.join(targetDirectory, categoryName)
            
            #Make sure folders for each category exists if mot move it
            if not os.path.exists(targetFolder):
                os.makedirs(targetFolder)
                
            targetPath = os.path.join(targetFolder, item)
            
            #Attempt to move files
            try:
                shutil.move(itemPath, targetPath)
                print(f"Moved: {item} -> {categoryName}")
                filesMoved += 1
                
            except PermissionError:
                print(f"Skipped: {item} (File might be open)")
            except Exception as e:
                print(f"Error moving {item}: {e}")

    print(f"\nSorting complete! Successfully organized {filesMoved} files.")



#
configFile = 'config.json'

#Make sure config.json exists
if not os.path.exists(configFile):
    print(f"Error: Could not find '{configFile}'. Please create it.")
    
else:
    with open(configFile, 'r') as file:
        configData = json.load(file)

    #Grab sorting location from config
    savedPath = configData.get('targetDirectory')
        
    #If location inside config is found
    if savedPath:
        sortLocation(savedPath)
    else:
        print(f"Error: Could not find 'targetDirectory' inside {configFile}.")            