import csv, sys

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
# CODE TO FILTER THE REPOSITORIES FROM THE OTHER PAPER TO GET:
# * gitlab repositories
# * package data states that it still has a gitlab-ci file in the repository
# PARAMS USED: .\0-article-packages\NPM_cs_protions_700k_7cis.csv GitLabCI .\1-code-extraction\repo_paths.csv
# EXAMPLE: python .\1-code-extraction\extract.py .\0-article-packages\NPM_cs_protions_700k_7cis.csv GitLabCI .\1-code-extraction\repo_paths.csv

def filterRepositories(file_path, searched_CI, save_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        id = 0
        rows = []
        for (index, row) in enumerate(csv_reader):
            if index == 0:
                print(f'id,{row[0]}')
                rows.append(f'id,{row[0]}')
            else:
                if len(row) > 6 and row[3] == searched_CI and row[5] == '+inf':
                    print(f'{id},{row[0]}')
                    rows.append(f'{id},{row[0]}')
                    id += 1
        saveRowsToCSV(rows, save_path)

def saveRowsToCSV(data, path):
    with open(path,'w') as file:
        for row in data:
            file.write("%s\n"%(row))

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    if(len(sys.argv)<4):
        print('missing one of the necessary arguments: csv file path, save file path or CI field name')
    else:
        filepath = sys.argv[1]
        savepath = sys.argv[2]
        ciName = sys.argv[3]
        filterRepositories(filepath, ciName, savepath)