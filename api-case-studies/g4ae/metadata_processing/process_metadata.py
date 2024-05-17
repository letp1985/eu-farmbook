import pandas as pd
import os

class ExcelDataProcessor:
    def __init__(self, file_loc: str):
        self.file_loc = file_loc
        self.df = self.load_excel_to_pandas()  # Load data directly during initialization


    def load_excel_to_pandas(self):
        """Loads an Excel file into a pandas DataFrame."""

        if not os.path.exists(self.file_loc):
            raise FileNotFoundError(f"No file found at the specified path: {self.file_loc}")

        try:
            with open(self.file_loc, 'rb') as f:
                df = pd.read_excel(f, sheet_name='Fill Me')
                #
                # # Drop empty columns and rows that could exist after skipping rows
                df.dropna(axis=1, how='all', inplace=True)
                df.dropna(axis=0, how='all', inplace=True)
                return df
        except Exception as e:
            # Handle other potential exceptions that could arise during file reading
            raise Exception(f"Failed to load Excel file: {e}")

    def pivot_table(self):
        """Creates a pivoted table with headers as column names and row values."""
        # Assuming headers are in the first non-empty column and values in the next
        headers = self.df.iloc[:, 0].tolist()  # Convert to list for dynamic handling
        values = self.df.iloc[:, 1].tolist()  # Convert to list for dynamic handling

        # Match the length of headers and values by truncating the longer of the two if necessary
        min_length = min(len(headers), len(values))
        headers = headers[:min_length]
        values = values[:min_length]

        # Create the DataFrame using headers for column names and values for the row
        self.df = pd.DataFrame([values], columns=headers)

        return self.df

    def rename_columns(self):
        """Renames DataFrame columns according to a predefined schema."""
        self.df.rename(columns={
            'title (*)': 'title',
            'description (*)': 'description',
            'keywords (*) ': 'keywords',
            'creator(s) (*)': 'creators_names',
            'creator(s) contact(s) (*)': 'creators_emails',
            'geographic location(s) 6': 'geographic_locations',
            'date of completion (*)': 'date_of_completion',
            'language(s) (*) 6': 'language',
            'category (*) 6': 'type',
            'type (*) 6': 'category',
            'subject - Level 1 (*) 6': 'topics',
            'subject - Level 2 (*) 6': 'subtopics',
            'license (*)': 'license',
            'intended purpose (*) 6': 'intended_purpose'
        }, inplace=True)

    def remove_columns(self):
        """Renames DataFrame columns according to a predefined schema."""
        self.df.drop(['format (*) 6',
                      'file size (*)',
                      'project name (*) 6'
                      ], axis=1, inplace=True)

    def convert_creators_columns(self):
        """Converts creators columns to a single 'creators' column with name and email."""
        # Split the strings by semicolon to obtain lists of names and emails
        names = self.df['creators_names'].str.split(';')
        emails = self.df['creators_emails'].str.split(';')

        # Create a list of dictionaries
        creators_list = [{'name': name.strip(), 'email': email.strip()} for name, email in zip(names[0], emails[0])]

        # Assign the list to the 'creators' column
        self.df['creators'] = [creators_list]

        # Drop the original columns
        self.df.drop(['creators_names', 'creators_emails'], axis=1, inplace=True)

    def convert_semi_colon_separated_string_to_list(self, column_name):
        """Converts a comma-separated string in a DataFrame column to a list of unique strings, preserving the order."""

        def unique_ordered_list(s):
            seen = set()
            return [item.strip() for item in s.split(';') if item.strip() not in seen and not seen.add(item.strip())]

        self.df[column_name] = self.df[column_name].apply(
            lambda x: unique_ordered_list(x) if isinstance(x, str) else [])

    def convert_list_properties(self):

        for column in ['keywords', 'geographic_locations', 'intended_purpose', 'topics', 'subtopics', 'type']:
            self.convert_semi_colon_separated_string_to_list(column)
