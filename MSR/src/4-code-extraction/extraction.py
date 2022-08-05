import json, sys, os
from numpy import append

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
# CODE TO RETRIEVE INFORMATION FROM THE JSON WITH THE PARSED YML DATA
# PARAMS USED: .\3-code-parse\parsedData.json .\4-code-analysis\results
# EXAMPLE: python .\4-code-analysis\analysis.py .\3-code-parse\parsedData.json .\4-code-analysis\results

def getAllStagesTypes():
    result={}
    with open(path, 'r') as fileContent:
        data = json.load(fileContent)
        for file in data:
            if 'Stages' in file:
                for stage in file['Stages']:
                    if '/' in stage['Type']:
                        types = stage['Type'].split('/')
                        for typeName in types:
                            if typeName in result.keys():
                                result[typeName] += 1
                            else:
                                result[typeName] = 1
                    else:
                        if stage['Type'] in result.keys():
                                result[stage['Type']] += 1
                        else:
                            result[stage['Type']] = 1
            else:
                if 'parsing-error' in result.keys():
                    result['parsing-error'] += 1
                else:
                    result['parsing-error'] = 1
    sorted_list = sortDictIntoList(result)
    saveCSV(sorted_list, '{}/stage_types.csv'.format(savepath))
    print(result)

def getAllStage():
    result={}
    with open(path, 'r') as fileContent:
        data = json.load(fileContent)
        for file in data:
            if 'Stages' in file:
                for stage in file['Stages']:
                    if stage['Name'] in result.keys():
                        result[stage['Name']] += 1
                    else:
                        result[stage['Name']] = 1
            else:
                if 'error' in result.keys():
                    result['error'] += 1
                else:
                    result['error'] = 1
    sorted_list = sortDictIntoList(result)
    saveCSV(sorted_list, '{}/stages.csv'.format(savepath))
    print(result)

def getActivities(wantedStage = None, wantedFilePath = None, wantedStageType = None):
    #returns all activities in the json file unless a stage is specified, then it will return al activities of a specific stage.
    result={}
    with open(path, 'r') as fileContent:
        data = json.load(fileContent)
        for file in data:
            if wantedFilePath:
                if file['Path']==wantedFilePath:
                    searchStage(result,file, wantedStage, wantedStageType)
            else:
                searchStage(result,file, wantedStage, wantedStageType)
    sorted_list = sortDictIntoList(result)
    saveCSV(sorted_list, '{}/activities.csv'.format(savepath))
    print(result)

def getActivityTypes(wantedStage = None, wantedFilePath = None, wantedStageType = None):
    #returns all activity types in the json file unless a stage is specified, then it will return al activity types of a specific stage.
    result={}
    with open(path, 'r') as fileContent:
        data = json.load(fileContent)
        for file in data:
            if wantedFilePath:
                if file['Path']==wantedFilePath:
                    searchStage(result,file, wantedStage, wantedStageType, True)
            else:
                searchStage(result,file, wantedStage, wantedStageType, True)
    sorted_list = sortDictIntoList(result)
    saveCSV(sorted_list, '{}/activity_types.csv'.format(savepath))
    print(result)

def searchStage(result, file, wantedStage, wantedStageType, byType = False):
    if 'Stages' in file:
        for stage in file['Stages']:
            if wantedStage:
                if stage['Name'] == wantedStage:
                    searchActivity(stage, result, byType)
            elif wantedStageType:
                if stage['Type'] == wantedStageType:
                    searchActivity(stage, result, byType)
            else: 
                searchActivity(stage, result, byType)    

def searchActivity(stage, result, byType = False):
    if 'Activities' in stage:
        for activity in stage['Activities']:
            if byType:
                if '/' in activity['Type']:
                    types = activity['Type'].split('/')
                    for typeName in types:
                        if typeName in result.keys():
                            result[typeName] += 1
                        else:
                            result[typeName] = 1
                else:
                    if activity['Type'] in result.keys():
                        result[activity['Type']] += 1
                    else:
                        result[activity['Type']] = 1
            else:
                if activity['Name'] in result.keys():
                    result[activity['Name']] += 1
                else:
                    result[activity['Name']] = 1

def getSteps(wantedStage=None, wantedActivity=None, wantedFilePath=None):
    result={}
    with open(path, 'r') as fileContent:
        data = json.load(fileContent)
        for file in data:
            if wantedFilePath:
                if file['Path'] == wantedFilePath:
                    getStepsPart2(wantedActivity, wantedStage, result, file)
            else:
                getStepsPart2(wantedActivity, wantedStage, result, file)
    if len(result)>0:
        result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
        saveCSV(result, '{}/steps.csv'.format(savepath))
        print(result)
    else:
        print('No Steps Found with these criteria')
    
def getStepsPart2(wantedActivity, wantedStage, result, file):
    if 'Stages' in file:
        for stage in file['Stages']:
            if wantedStage:
                if stage['Name']== wantedStage:
                    getStepsPart3(wantedActivity, result ,stage)
            else:
                getStepsPart3(wantedActivity, result ,stage)

def getStepsPart3(wantedActivity, result ,stage):
    if 'Activities' in stage:
        for activity in stage['Activities']:
            if wantedActivity:
                if activity['Name']==wantedActivity:
                    getStepsFinalPart(result, activity)
            else:
                getStepsFinalPart(result, activity)
        
def getStepsFinalPart(result, activity):
    if 'Steps' in activity:
        for step in activity['Steps']:
            if step['Script'] in result.keys():
                result[step['Script']] += 1
            else:
                result[step['Script']] = 1

def getFiles(wantedStage):
    result = []
    with open(path, 'r') as fileContent:
        data = json.load(fileContent)
        for file in data:
            if 'Stages' in file:
                for stage in file['Stages']:
                    if wantedStage == stage['Name']:
                        result.append(file['Path'])
    print(result)

def sortDictIntoList(data):
    l = []
    for k in data.keys():
        l.append([k, data[k]])
    l.sort(key=lambda x: x[1], reverse=True)
    return l

def saveCSV(data, path):
    with open(path,'w') as file:
        for pair in data:
            file.write("%s,%s\n"%(pair[0],pair[1]))

def createDir():
    try:
        os.makedirs(savepath)
    except OSError as error:
        print(error)
        print('Directory not created!')

def activitiesOptions():
    # Activity from Specific Stage
    answer = None
    while (answer != 'y' and answer != 'n'):
        answer=input('\nDo you want the Activities of a specific Stage?(y/n)')
    if answer=='y':
        wantedStage = input('Which stage: ')
    else: 
        wantedStage = None

    # Activity from Specific Stage Type
    if (not wantedStage):
        answer = None
        while (answer != 'y' and answer != 'n'):
            answer=input('\nDo you want the Activities of a specific Stage Type?(y/n)')
        if answer == 'y':
            wantedStageType = input('Which stage type: ')
        else: 
            wantedStageType = None
    else: 
        wantedStageType = None
    
    # Activity from Specific File
    answer = None
    while (answer != 'y' and answer != 'n'):
        answer=input('\nDo you want the Activities of a specific File?(y/n)')
    if answer=='y':
        wantedFilePath = input('What is the file\'s path: ')
    else: 
        wantedFilePath = None
    
    getActivities(wantedStage, wantedFilePath, wantedStageType)

def activityTypesOptions():
    # Activity Types from Specific Stage
    answer = None
    while (answer != 'y' and answer != 'n'):
        answer=input('\nDo you want the Activity Types of a specific Stage?(y/n)')
    if answer=='y':
        wantedStage = input('Which stage: ')
    else: 
        wantedStage = None

    # Activity Types from Specific Stage Type
    if (not wantedStage):
        answer = None
        while (answer != 'y' and answer != 'n'):
            answer=input('\nDo you want the Activity Types of a specific Stage Type?(y/n)')
        if answer == 'y':
            wantedStageType = input('Which stage type: ')
        else: 
            wantedStageType = None
    else: 
        wantedStageType = None

    # Activity Types from Specific File
    answer = None
    while (answer != 'y' and answer != 'n'):
        answer=input('\nDo you want the Activity Types of a specific File?(y/n)')
    if answer=='y':
        wantedFilePath = input('What is the file\'s path: ')
    else: 
        wantedFilePath = None

    getActivityTypes(wantedStage, wantedFilePath, wantedStageType)

def stepsOptions():
    # Steps from Specific Stage
    answer = None
    while (answer != 'y' and answer != 'n'):
        answer=input('\nDo you want the Steps of a specific Stage?(y/n)')
    if answer=='y':
        wantedStage = input('Which stage: ')
    else: 
        wantedStage = None

    # Steps from Specific 
    answer = None
    while (answer != 'y' and answer != 'n'):
        answer=input('\nDo you want the Steps from a specific File?(y/n)')
    if answer=='y':
        wantedFilePath = input('What is the file\'s path: ')
    else: 
        wantedFilePath=None

    # Steps from Specific Activity
    answer = None
    while (answer != 'y' and answer != 'n'):
        answer=input('\nDo you want the Steps from a specific Activity?(y/n)')
    if answer=='y':
        wantedActivity = input('Which Activity: ')
    else: 
        wantedActivity=None

    getSteps(wantedStage, wantedActivity , wantedFilePath)

def runProgram():
    op1 = "1. Stages"
    op2 = "2. Stage Types"
    op3 = "3. Activities"
    op4 = "4. Activity Types"
    op5 = "5. Steps"
    op6 = "6. Files containing specific Stage"

    while(True):
        print('\n\n{}\n{}\n{}\n{}\n{}\n{}\n0. Exit'.format(op1, op2, op3, op4, op5, op6))
        search=input('\nWhat are you looking for:')
        
        if search == '1':
            getAllStage()
        elif search == '2':
            getAllStagesTypes()
        elif search == '3':
            activitiesOptions()
        elif search == '4':
            activityTypesOptions()
        elif search == '5':
            stepsOptions()
        elif search == '6':
            wantedStage = input('Which stage: ')
            getFiles(wantedStage)
        elif search == '0':
            print('\nGoodbye!!')
            break
        else: print('not a valid entry')

def start():
    try:
        os.makedirs(savepath)
    except:
        print('Directory already created')
    
    runProgram()

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    if(len(sys.argv)<3):
        print('missing one of the necessary arguments: json file path')
    else:
        path = sys.argv[1]
        savepath = sys.argv[2]
        start()