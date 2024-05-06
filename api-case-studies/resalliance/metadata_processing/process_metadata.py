import pandas as pd


class ExcelDataProcessor:
    def __init__(self, file_loc: str):
        self.file_loc = file_loc
        self.df = self.load_excel_to_pandas()

    def load_excel_to_pandas(self):
        """Loads an Excel file into a pandas DataFrame."""
        with open(self.file_loc, 'rb') as f:
            return pd.read_excel(f, dtype={'Factsheet': str}, parse_dates=['Date of completion'])



    def rename_columns(self):
        """Renames DataFrame columns according to a predefined schema."""
        self.df.rename(columns={
            'Title': 'title',
            'Description': 'description',
            'keywords': 'keywords',
            'Creators': 'creators_preprocessing',
            'Geographic location(s)': 'geographic_locations',
            'Date of completion': 'date_of_completion',
            'Language': 'language',
            'Category': 'type',
            'Type': 'category',
            'Topics': 'topics',
            'Subtopics': 'subtopics',
            'Licence': 'license',
            'Intended Purpose': 'intended_purpose'
        }, inplace=True)



    def remove_columns(self):
        """Renames DataFrame columns according to a predefined schema."""
        self.df.drop(['Grant ID',
                      'Type of Solution',
                      'Sector',
                      'ResAlliance Partner',
                      'Climate hazard', 'Good Practice(s)'
                      ], axis=1, inplace=True)

    def convert_creators_column(self):
        """Convert 'creators_preprocessing' column to a list of unique dictionaries with 'name' and 'email'."""
        if 'creators_preprocessing' not in self.df.columns:
            raise ValueError("The 'creators_preprocessing' column does not exist in the DataFrame.")

        # Create a new column with empty lists for all rows
        self.df['creators'] = [set() for _ in range(len(self.df))]

        for index, row in self.df.iterrows():
            column_data = row['creators_preprocessing']
            pairs = column_data.split(", ")
            for pair in pairs:
                parts = pair.split(";") if ';' in pair else [pair, ""]
                name_email_tuple = (parts[0].strip(), parts[1].strip() if len(parts) > 1 else "")
                # Add the tuple to the set for this row
                self.df.at[index, 'creators'].add(name_email_tuple)

        # Convert each set to a list of dictionaries and update the DataFrame
        self.df['creators'] = self.df['creators'].apply(lambda s: [{"name": name, "email": email} for name, email in s])

        # Optionally, drop the 'creators_preprocessing' column
        self.df.drop(['creators_preprocessing'], axis=1, inplace=True)

    def convert_semi_colon_separated_string_to_list(self, column_name):
        """Converts a comma-separated string in a DataFrame column to a list of unique strings, preserving the order."""

        def unique_ordered_list(s):
            seen = set()
            return [item.strip() for item in s.split(';') if item.strip() not in seen and not seen.add(item.strip())]

        self.df[column_name] = self.df[column_name].apply(
            lambda x: unique_ordered_list(x) if isinstance(x, str) else [])

    def convert_list_properties(self):

        for column in ['keywords', 'geographic_locations', 'intended_purpose', 'topics', 'subtopics', 'type',
                       'Type of Solution', 'Sector', 'ResAlliance Partner', 'Climate hazard', 'Good Practice(s)']:

            self.convert_semi_colon_separated_string_to_list(column)

    def create_contributor_custom_metadata(self):

        """Creates a custom metadata dictionary from the DataFrame"""
        custom_properties = ['Type of Solution', 'Sector', 'ResAlliance Partner', 'Climate hazard', 'Good Practice(s)']

        self.df['contributor_custom_metadata'] = \
            self.df[custom_properties].apply(lambda x: dict(zip(custom_properties, x)), axis=1)
