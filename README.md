# KnowledgeUI
Application to Interact with a Knowledge Base in a Triple Store

# How to run the project
1) Clone it: git clone \<link to the repo\>
2) open the directory where you cloned it.
3) Good practice but not mandatory: Create a virtualenvironnement in it *1
4) run: ``` pip install -r requirements.txt```
5) repeat with all the requiremetns files :p
5) open the file .env
6) uncomment the last line. Just get rid of the # in front of the DATASET_LINK
    if you want to connect to an other dataset replace the link
7) run: ```python run.py```

*1) To know how to create a virtualenvironnement using virtualenv on BAM's laptops that uses Windows 
    you can take a look Below

# How to set up a virtualenv on BAM's laptops
## First step: Installation
- Download python on: https://www.python.org/downloads/

- Install it only locally(Not on the global machine because NO RIGTHS)

- Open the cmd (Not the powershell)

- Install virtualenv: pip install virtualenv

## Create the virtualenv:
- Using the cmd go to your working directory: cd Path\To\the\directory

- Run the virtualenv script (That's bothersome because you need to use the static path)
```sh
C:\Users\<ReplaceByYourUserName>\AppData\Local\Packages\<PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0>\LocalCache\local-packages\<Python39>\Scripts\virtualenv venv
```
**Everything to be replaced is in <>**<br/>
**dir** is the equivalent of **ls** in cmd in case you want to search for the names<br/>
**Important**:
You need to replace also: PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0
by the version you downloaded and same goes for Python39 not only your username<br />


## What if you find that really to bothersome:
Try to run the script: createNewVirtualEnv.py<br />
    ```python createNewVirtualEnv.py```
 
 *Disclaimer:*<br />
 The script may not work on all the machines. It needs to be more tested to certify that.
 Do not hesitate to make any feedback :)
## Activate virtualenv:
- In your working directory type:
```venv\Scripts\activate```
- Once you see (venv) at the beginning of your prompt Install all the requirements.
- Your virtual environnement is ready to be used.
- It's working also on vscode once it's activated

## Deactivate virtualenv:
- In your working directory:
- ```venv\Scripts\deactivate.bat```

## What if it doesn't work:

You can contact me via:
- MSteams: ilias deligiannis
- Mail: ilias.deligiannis@bam.de
