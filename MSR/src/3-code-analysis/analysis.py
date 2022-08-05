from distutils.log import error
import os, yaml, json, sys

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
# CODE TO PARSE THE YML FILES INTO A JSON FILE:
# PARAMS USED: .\2-code-mining\files-first-run .\3-code-parse\parsedData.json
# EXAMPLE: python .\3-code-parse\parse.py .\2-code-mining\files-first-run .\3-code-parse\parsedData.json

files=[]

def getContent(filePath):
    with open(filePath,'r') as file:
        try:
            data = yaml.safe_load(file)
            if 404 in data:
                return None
            return data
        except:
            return None
        #adding tags is possible and we can retrive the value of the dict by values()

def getStages(data):
    stages = []
    order = 1
    if ('stages' in data):
        stagesList = data['stages']
    else:
        stagesList = [
            ".pre @Commit",
            "build @Commit",
            "test @Test",
            "deploy @Release",
            ".post @Release"
        ]
        
    try:
        for stage in stagesList:
            stagedic = {}
            if isinstance(stage, str):
                if ' @' in stage:
                    pair = stage.split(' @')
                    name = pair[0]
                    stagedic['Type'] = pair[1]
                else:
                    name = stage
                    stagedic['Type'] = 'Unknown'
            else:
                name = list(stage.keys())[0][:-11]
                stagedic['Type'] = list(stage.values())[0]
            stagedic['Name'] = name
            stagedic['Order'] = order
            order += 1
            
            activities = getActivities(data, name)
            if len(activities) > 0:
                stagedic['Activities'] = getActivities(data, name)
                stages.append(stagedic)
        return stages
    except:
        return []

def getActivities(data, stageName):
    activities = []
    order = 1
    for section in data:
        activity = {}
        if 'script' in list(data[section]):
            if (('stage' in data[section] and data[section]['stage'] == stageName) or 
                ((not 'stage' in data[section]) and stageName == "test")):
                if ' @' in section:
                    pair = section.split(' @')
                    activity['Type'] = pair[1]
                    activity['Name'] = pair[0]
                else:
                    activity['Type'] = 'Unknown'
                    activity['Name'] = section
                activity['Order'] = order
                order += 1
                activity['Steps'] = getSteps(data, section)
                activities.append(activity)
    return activities

def getSteps(data, section):
    steps=[]
    for tag in list(data[section]):
        if 'script' in tag:
            order = 1
            for step in data[section][tag]:
                script = {}
                script['Order']=order
                order+=1
                script['Script']=step
                steps.append(script)   
            # print(steps)
    return steps            
            

def saveToJSON(data, savepath):
    #from dictionary to .json file.
    with open(savepath,'w') as file:
        json.dump(data, file)
    

def scanDir(path):
    directories = os.scandir(path)
    for item in directories:
        if (item.is_dir(follow_symlinks=False)):
            scanDir(item.path)
        elif (item.name[-4:] == '.yml'):
            parsedData = {}
            parsedData['Name'] = item.name
            path = item.path
            parsedData['Path'] = path
            data = getContent(path)
            # print(data)
            if(data!= None):
                print("{}".format(path))
                parsedData['Stages'] = getStages(data)
            else:
                parsedData['Error']= 'not a valid yml file for the loader'
            files.append(parsedData)
    directories.close()

def parseMain(path, savepath):
    scanDir(path)
    saveToJSON(files, savepath)

if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")
    if(len(sys.argv)<3):
        print('missing one of the necessary arguments: yml files folder path or save file path')
    else:
        ymlFilesPath = sys.argv[1]
        savepath = sys.argv[2]

        parseMain(ymlFilesPath, savepath)