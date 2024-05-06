from api_interaction.upload_knowledge_objects import upload_knowledge_objects_and_metadata

def input_boolean(prompt):
    while True:
        response = input(prompt)
        if response.lower() in ['true', 't', 'yes', 'y']:
            return True
        elif response.lower() in ['false', 'f', 'no', 'n']:
            return False
        else:
            print("Invalid input. Please enter True or False.")

if __name__ == '__main__':
    print("Starting the process...")
    dry_run = input_boolean("Is this a dry run? (True/False): ")
    if dry_run:
        print("Dry run to check metadata validity in progress...")
    else:
        print("Actual API run in progress...")
    upload_knowledge_objects_and_metadata(dry_run=dry_run)

    print("Process finished")
