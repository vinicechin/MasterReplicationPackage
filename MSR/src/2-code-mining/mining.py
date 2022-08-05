import csv, requests, time, os, sys;
from urllib.parse import quote;

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
# CODE TO DOWNLOAD THE GITLAB FILES FROM THE GITHUB REPOSITORIES:
# PARAMS USED: <YOUR_GITHUB_TOKEN> .\1-code-extraction\repo_paths.csv .\2-code-mining\files
# EXAMPLE: python .\2-code-mining\mining.py <YOUR_GITHUB_TOKEN> .\1-code-extraction\repo_paths.csv .\2-code-mining\files

def createDir(repo, save_path):
    directoryPath = '{}/{}'.format(save_path, repo)
    try:
        os.makedirs(directoryPath)
    except OSError as error:
        print(error)
        print('Directory not created!')

def saveFile(data, repo, filename, save_path):
    fullPath = '{}/{}/{}'.format(save_path, repo, filename)
    with open(fullPath,'wb') as file:
        file.write(data.encode("utf-8"))

def downloadRequest(access_token, url, repo, filename, save_path):
    status=0
    while status!=200:
        result = requests.get(
            url, 
            headers={'Authorization': 'token '+access_token, 'Accept': 'application/vnd.github.v3+json'} 
        )
        status = result.status_code
        if result.ok:
            print("Downloading: ", result.json()['download_url'])
            response = requests.get(
                result.json()['download_url'], 
                headers={'Authorization': 'token '+access_token, 'Accept': 'application/vnd.github.v3+json'} 
            )
            rawContent = response.text
            createDir(repo, save_path)
            saveFile(rawContent, repo, filename, save_path)

def makeRequest(access_token, repo, save_path):
    query ="repo:"+repo+"+filename:.gitlab-ci.yml"
    payload='q='+query
    result = requests.get(
        "https://api.github.com/search/code", 
        params=payload, 
        headers={'Authorization': 'token '+access_token, 'Accept': 'application/vnd.github.v3+json'} 
    )
    
    if result.ok:
        for file in result.json()['items']:
            file_name = file['name']
            url = file['url']
            downloadRequest(access_token, url, repo, file_name, save_path)
    else:
        print("Error: ", result.status_code, repo)
    time.sleep(5)

def downloadGitlabFiles(access_token, file_path, save_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader((x.replace('\0', '') for x in csv_file), delimiter=',')
        for (index, row) in enumerate(csv_reader):
            if index != 0 and len(row) >= 2:
                makeRequest(access_token, row[1].replace('https://github.com/', ''), save_path)

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    if(len(sys.argv)<4):
        print('missing one of the necessary arguments: token, repos file path or save files path')
    else:
        token = sys.argv[1]
        reposCsvPath = sys.argv[2]
        savepath = sys.argv[3]

        downloadGitlabFiles(token, reposCsvPath, savepath)
