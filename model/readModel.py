import pandas as pd

class ReadModel:

    INCLUDED = set(["trail_num", "n1", "n2", "result"])

    HEADERS = [
            "subject", "trail_num", "n1", "n2", "result",
            "start", "end", "1 start", "1 end", "2 start", "2 end",
            "final start", "final end"
        ]

    def __init__(self) -> None:
        pass

    def read_excel_to_dict(self, file_path):
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Add missing columns with None values
        for header in self.HEADERS:
            if header not in df.columns:
                df[header] = ""

        # Reorder columns to match HEADERS order
        df = df[self.HEADERS]
        df = df.fillna("")
        
        # Convert the DataFrame to a dictionary
        data_dict = df.to_dict(orient='records')
        
        return data_dict
    
    def read(self, file_path):
        data = self.read_excel_to_dict(file_path)
        
        if len(data) > 0:
            if not self.INCLUDED.issubset(data[0].keys()):
                return None
        
        return data
