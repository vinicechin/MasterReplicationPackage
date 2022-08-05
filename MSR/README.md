# Mining Software Repositories

This folder contains the tools developed to mine Github for repository links that contain configuration files for Gitlab pipelines. 

## Assumptions/Pre-requisites

1. Python installed at local machine
2. Replication package from [On the rise and fall of CI services in GitHub](https://zenodo.org/record/5815352#.YpzKWKhBwuU) downloaded

<br>

## Folder Structure

```bash
MSR
├───data
|   ├───annotations
|   |   ├───annotated_dataset.zip
|   |   ├───Annotations.ods
|   |   └───Annotations.xlsx
|   ├───NPM_cs_protions_700k_7cis.csv.gz
|   └───original_dataset.zip
└───src
    ├───1-code-search
    ├───2-code-mining
    ├───3-code-analysis
    ├───4-code-extraction
    └───secret.py
```

Where:

1. The data folder contains:
    - a `.gz` retrieved from the above mentioned replication package that was used during the research presented in this thesis.
    - a `.zip` with the non-annotated original Gitlab pipeline configuration files.
    - an `annotations` folder containing:
        - the tables and charts with the procedures and results of the annotations procedures and results  (`.ods` and `/xlsx` file versions).
        - a `.zip` with the annotated Gitlab pipeline configuration files.
2. The src folder contains:
    - a folder with the python code for the repository links extraction from the `.csv` file.
    - a folder with the python code for the mining of Gitlab pipeline configuration files from Github.
    - a folder with the python code for the content analysis and parsing of the pipeline configuration files.
    - a folder with the python code for the data extraction from the parsed data retrieved during the content analysis.
    - a python file where a Github secret should be stored in order to run the mining part of this replication package (token is empty, so it needs to be set).

<br>

## How to use it 

### Step 0: Replication Package

Firstly extract the `.gz` file made available in the `./data/` folder of this replication package (it can be extracted to the same folder).

### Step 1: Search
Searches for the repository urls from one of the csv files provided by the replication package.

From the root directory, run:

`python ./src/1-code-search/extract.py <path/to/package/csv/file> <path/to/output-csv-file> <CI-platform/to/search>`

Where the first parameter indicates the csv package file containing the repositories informations. The second indicates which CI to search for in the csv file. And the third indicates where to save the output file.

**For example:**

`python ./src/1-code-search/extract.py ./data/NPM_cs_protions_700k_7cis.csv GitLabCI ./src/1-code-search/repo_paths.csv GitLabCI`

Where `NPM_cs_protions_700k_7cis.csv` was extracted from the data folder of the available replication package.

<br>

### Step 2: Mining
The goal of this step is to mine GitHub projects (i.e. repositories) contained in `<path/to/output-csv-file>` that still have one or more files with the name *.gitlab-ci.yml*.

**Note:** set token to your own github token

Then these files are download for each project and stored into `<path/to/yml/files/folder>` folder, organized into subfolders based on author and project name.

The following command (ran in the root folder) performs the action just described:

`python ./src/2-code-mining/mining.py <YOUR_GITHUB_TOKEN> <path/to/output-csv-file> <path/to/yml/files/folder>`

**Note:** the path `<path/to/output-csv-file>` needs to exist for the command to work.

**For example:**

`python ./src/2-code-mining/mining.py <YOUR_GITHUB_TOKEN> ./src/1-code-search/repo_paths.csv ./src/2-code-mining/files`

<br>

### Step 3: Parsing
Parsing the downloaded .yml files. From the root dir, run:

`python ./src/3-code-analysis/analysis.py <path/to/yml/files/folder> <path/to/json/file>`

The output of having executed this step is a .json file located at `<path/to/json/file>`

**Note 1:** The downloaded files from Step 2 need to be located at `<path/to/yml/files/folder>`

**For example:**

`python ./src/3-code-analysisa/nalysis.py ./src/2-code-mining/files ./src/3-code-analysis/parsedData.json`

<br>

### Step 4: Analysing
Querying the built model to find out meaningful insights, like:

* retrieve list of GitLab-based stages (and types when annotated), as well as the amount of appearances
* retrieve list of activities (and types when annotated) for a particular .yml file, as well as the amount of appearances
* retrieve list of activities (and types when annotated) for a particular .yml file and GitLab-based stage, as well as the amount of appearances
* retrieve list of steps for a particular activity, in a particular .yml file.

The following command activates the interaction on the command line for querying the informations:

`python ./src/4-code-extraction/analysis.py <path/to/json/file> <path/to/extracted/results>`

**Note 1:** the .json file generated in Step 3 must remain placed at `<path/to/json/file>`

**Note 2:** the results from the analysis are saved in the `<path/to/extracted/results>` folder

**For example:**

`python ./src/4-code-extraction/extraction.py ./src/3-code-analysis/parsedData.json ./src/4-code-extraction/results`

<br>

### Step 5: Manual Annotation
After getting the original results, we can annotate the .yml files to classify each stage and activity contained in the pipelines. For now this has to be done manually, but as a future work we could train a model to do this annotation automatically as well.

To classify a stage or an activity, we add '` @<stage-name>`' after the name of the stage/activity that we want to classify.


**For example:**

 ```yml
 stages:
    - build @Commit
    ...

install_dependencies @Dependencies:
  stage: build
  script:
  ...
 ```
