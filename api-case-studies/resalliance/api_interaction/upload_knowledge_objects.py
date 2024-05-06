import json
import os
import requests
from metadata_processing.process_metadata import ExcelDataProcessor
from auth.token_management import get_token
from dotenv import load_dotenv

# get environment variables
load_dotenv()
API_ADDRESS = os.environ.get("API_ADDRESS")
project_id = os.environ.get("PROJECT_ID")

metadata_folder_path = "data"
metadata_file_name = "20240409. Batch Upload Resalliance-EU_LPUpdate.xlsx"
metadata_file_path = os.path.join(metadata_folder_path, metadata_file_name)
ko_folder_path = "data/kos/"

# issue for the file types - should add this to the excel file
file_type = '_EN.pdf'


def process_metadata():
    """
    Processes the metadata from the metadata_file_path variable set on the top of the script
    See process_metadata.py for more details
    """
    processor = ExcelDataProcessor(metadata_file_path)
    processor.rename_columns()
    processor.convert_creators_column()
    processor.convert_list_properties()
    processor.create_contributor_custom_metadata()
    processor.remove_columns()

    df = processor.df
    return df


def get_knowledge_object(knowledge_object_file_name):
    """
    Imports the physical knowledge object from the data directory and returns the file name and content (Binary)
    """

    file_path = f"{ko_folder_path}{knowledge_object_file_name}"

    with open(file_path, 'rb') as file:
        ko_content = file.read()

    return knowledge_object_file_name, ko_content


def upload_ko_to_eufarmbook(ko_file_name, ko_content):
    """
    Uploads the knowledge object to the EU-FarmBook (file only, not metadata)
    """

    url = f"{API_ADDRESS}/api/upload/knowledge_object_file"

    token = get_token()

    headers = {
        'accept': 'application/json'
    }

    # Set the query parameters
    query_params = {
        'user_tokens': json.dumps(token),
        'project_id': project_id
    }

    # Set the file to upload
    files = {
        'ufile': (ko_file_name, ko_content)
    }
    response = requests.post(url, headers=headers, params=query_params, files=files)

    if response.status_code != 200:
        raise Exception(f"An error occurred uploading knowledge object {response.status_code} - {response.json()}")
        # print(f"An evrror occurred uploading knowledge object {response.status_code} - {response.json()}")
    else:
        return response


def upload_metadata_to_eufarmbook(database_id: str, metadata: dict, dry_run: bool):
    """
    Uploads the knowledge object metadata.
    If dry_run is set to True, it will only validate the metadata and not actually upload it.
    It is suggested you run this with dry_run set to True first to ensure the metadata is correct.
    """
    if dry_run is True:
        url = f"{API_ADDRESS}/api/upload/validate_knowledge_object_metadata"
    else:
        url = f"{API_ADDRESS}/api/upload/knowledge_object_metadata"

    token = get_token()

    headers = {
        'accept': 'application/json'
    }

    query_params = {
        'project_id': project_id
    }

    language = metadata['language']
    del metadata['language']
    metadata['knowledge_objects'] = [{'database_id': database_id,
                                      'language': language}]

    json = {
        'user_tokens': token,
        'metadata': metadata
    }

    response = requests.post(url, headers=headers, params=query_params, json=json)

    return response


def upload_knowledge_objects_and_metadata(dry_run: bool):
    """
    This is the main runner for the script
    """
    df = process_metadata()

    for index, row in df.iterrows():
        # Access the value of column 'A' for the current row
        filename = row['Factsheet']
        ko_file_name = f"{filename}{file_type}"
        print(f"Attempting upload for {ko_file_name}")
        ko_file_name, ko_content = get_knowledge_object(knowledge_object_file_name=ko_file_name)
        print(f"Uploading knowledge object {ko_file_name}")
        try:
            upload_ko = upload_ko_to_eufarmbook(ko_file_name, ko_content)
            database_id = upload_ko.json()['database_id']
            # Convert the current row to JSON with proper formatting
            metadata_json = row.to_json(orient='index', indent=4)
            metadata_json = metadata_json.replace("\\/", "/")
            # remove unnecessary columns
            metadata_json_dict = json.loads(metadata_json)
            del metadata_json_dict['Factsheet']

            response = upload_metadata_to_eufarmbook(database_id, metadata=metadata_json_dict, dry_run=dry_run)
            if response.status_code != 200:
                print(f"An error occured {response.status_code} - {response.json()}")
            else:
                print(f"Success: Uploaded metadata for {filename} and knowledge object {database_id}. "
                      f"EU-FarmBook ID: {response.json()}")
        except Exception as e:
            print(f"An error occurred uploading knowledge object {e}")

