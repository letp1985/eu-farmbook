import token_management as token_management
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Process some commands.')

# Add arguments
parser.add_argument('command', choices=['get_api_status', 'get_projects'], help='The command to execute.')

# Parse the arguments
args = parser.parse_args()

# Perform actions based on the arguments
if args.command == 'get_api_status':
    print(token_management.get_api_status())
elif args.command == 'get_projects':
    print(token_management.get_projects())
else:
    print('Please provide a valid command: get_api_status or get_projects.')

