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
# Add your metadata file name and .xlsx extension
metadata_file_name = "ENTER_FILE_NAME.xlsx"
metadata_file_path = os.path.join(metadata_folder_path, metadata_file_name)
ko_folder_path = "data/kos/"
file_type = '.pdf'


def process_metadata():
    """
    Processes the metadata from the metadata_file_path variable set on the top of the script
    See process_metadata.py for more details
    """
    processor = ExcelDataProcessor(metadata_file_path)
    processor.rename_columns()
    processor.convert_list_properties()
    processor.convert_file_name_and_language()
    processor.convert_creators_column()
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


def upload_metadata_to_eufarmbook(knowledge_objects: list, metadata: dict, dry_run: bool):
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

    metadata['knowledge_objects'] = knowledge_objects

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

        filename_lang = row['file_name_lang']
        print(f"Processing metadata for {filename_lang}")

        doc_id_lang = []

        for file in filename_lang:
            filename = file['filename']
            ko_file_name = f"{filename}{file_type}"
            print(f"Attempting upload for {ko_file_name}")
            ko_file_name, ko_content = get_knowledge_object(knowledge_object_file_name=ko_file_name)
            print(f"Uploading knowledge object {ko_file_name}")
            try:
                upload_ko = upload_ko_to_eufarmbook(ko_file_name, ko_content)
                database_id = upload_ko.json()['database_id']
                doc_id_lang.append({"database_id": database_id, "language": file['language']})
            except Exception as e:
                print(f"An error occurred uploading knowledge object {e}")

        # Convert the current row to JSON with proper formatting
        metadata_json = row.to_json(orient='index', indent=4)
        metadata_json = metadata_json.replace("\\/", "/")
        metadata_json_dict = json.loads(metadata_json)

        response = upload_metadata_to_eufarmbook(knowledge_objects=doc_id_lang,
                                                 metadata=metadata_json_dict,
                                                 dry_run=dry_run)
        if response.status_code != 200:
            print(f"An error occurred {response.status_code} - {response.json()}")
        else:
            print(f"Success: Uploaded metadata for Row {index + 1}: knowledge objects {doc_id_lang}. "
                  f"EU-FarmBook ID: {response.json()}")

