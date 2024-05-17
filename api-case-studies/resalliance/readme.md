# ResAlliance integration with EU-FarmBook API

This python project is an example of how to integrate the ResAlliance platform with the EU-FarmBook API. 

The folder structure is as follows:

```
resalliance/
├── api_interaction/
│   ├── upload_knowledge_objects.py - This is the main file that interacts with the EU-FarmBook API
│   ├── __init__.py
├── auth/
│   ├── __init__.py
│   ├── admin.py - This allows you to check the API status and view projects which you can upload KOs to
│   ├── token_management.py - This is the main script which handles the authentication with the EU-FarmBook API
├── data/ - This folder is where you store the data that you want to upload to the EU-FarmBook  - you must create this folder yourself
│   ├── kos/  - you must create this folder yourself
├── metadata_processing/ - This folder converts the metadata from the data folder into the correct format for the EU-FarmBook API
│   ├── __init__.py
│   ├── process_metadata.py
├── main.py - This script runs the entire process for uploading KOs and metadata to the EU-FarmBook API
├── README.md - The file you're in now
├── requirements.txt - The required packages for the project
├── .env - Your environement variables
```  


## Prerequisites

Start by reading the `help.md` file in the root directory to get a better understanding of how to navigate the terminal and the basic commands you will need to use to run this project.

### Initial setup

- Clone the repository or copy all the files from this root directory to your local drive e.g. to `C:\Users\YOUR_USER\workspace\here`
- Ensure you have python installed on your machine. You can download python from [here](https://www.python.org/downloads/) 
  - **Note**: This project was built with python 3.10.11 
  - 
### 1. Create a .env file in the root directory with the following environment variables:
```
API_ADDRESS=https://api-public.eufarmbook.eu
EMAIL=Your email for the EU-FarmBook
PASSWORD=Your password for the EU-FarmBook
PROJECT_ID = The ID for the project you are uploading KOs for. See the command below in Step 3 to check the ID for your project
```

### 2. Create a virtual environment to handle the required python packages

Navigate to the root directory and run the following command to create a virtual environment:

```bash
python3 -m venv ./venv
```

Activate the virtual environment:

This works differently depending on your operating system.

First try (on windows):
```bash 
venv/Scripts/activate
```
If that fails try:
```bash 
source venv/Scripts/activate
```
On mac try
```bash
source venv/bin/activate
```

You should know that you have activated the virtual environment when you see the name of the virtual environment in the terminal prompt(e.g. `(venv) user@computer:~$` on MacOS or `(venv) C:\Users\user>` on a windows machine)

You can read more about activating virtual environments [here](https://docs.python.org/3/library/venv.html)

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Check the status of the EU-FarmBook API and see which projects you have access to

Ensure you are in the root directory of the ResAlliance project.

Run the following command to get the status of the API

```bash 
python auth/admin.py get_api_status
```

You should see {'status': 'OK'} if the API is up and running.

To see which projects you have access to run the following command

```bash 
python auth/admin.py get_projects
```
You will see a list of projects you have access to.

``` json
[
{'project_id': '123', 'project_name': 'Project A'}, 
{'project_id': '456', 'project_name': 'Project B'}
]
```

Make sure you enter the correct project_id in the .env file (`PROJECT_ID=123` or `PROJECT_ID=456`). 

### 4. Make sure your data is in the correct format and stored in the data folder. 

In the data folder you save the .xlsx file with your metadata, and the knowledge objects themselves.

- The metadata file goes directly in the `data/` folder
- The knowledge objects go in the `data/kos` folder

*Remember!!!* You must set the metadata_file_name in the `api_interaction/upload_knowledge_objects.py` file to the name of the
.xlsx file you have saved in the `data/` folder.

### 5. Run the main.py file to upload the KOs and metadata to the EU-FarmBook API

Ensure you are in the root directory of the ResAlliance project.

You can then execute the main.py file by running the following command:

```bash 
python main.py
```

After doing so, command line prompt will ask you if you want to run a dry run.

It is recommended to first run a dry run before uploading all KOs and metadata to the EU-FarmBook API. You do this by typing `true` when prompted `Is this a dry run?`

By doing so, the script uploads the physical KOs to the EU-FarmBook API but only checks the structure of the metadata without actually storing it.

If you do not choose to try a dry run first, you may find some of the KO's metadata are stored, and some not because of incorrect formatting or values of metadata.

By following this process you can ensure all metadata records are in the correct format and using the correct values and fix any issues before uploading all KO metadata to the EU-FarmBook API.

Once you have validated all metadata is correct, you can type `false` when prompted `Is this a dry run?` to upload all KOs and metadata to the EU-FarmBook API.



### 6. Issues?

If you have any issues please contact

- Louis Powell (louis.powell@maastrichtuniversity.nl)
- Pranav Bapat (p.bapat@maastrichtuniversity.nl)