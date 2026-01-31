import gspread
# Cambiamos la librería de autenticación
from google.oauth2.service_account import Credentials

class SheetsAdapter:
    def __init__(self, creds_json_path: str, spreadsheet_key: str):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        try:
            creds = Credentials.from_service_account_file(creds_json_path, scopes=scope)
            
            self.client = gspread.authorize(creds)
            
            self.spreadsheet = self.client.open_by_key(spreadsheet_key)
            
            print(f"Conection succes to : {self.spreadsheet.title} spreadsheet")
            
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Error: Spreadsheet '{spreadsheet_key}' not found. Did you share it with the service account email?")
        except Exception as e:
            print(f"Error on initialize: {type(e).__name__} - {e}")
            raise

    def get_worksheet(self, worksheet_name: str):
        return self.spreadsheet.worksheet(worksheet_name)

    def get_all_records(self, worksheet_name: str):
        worksheet = self.get_worksheet(worksheet_name)
        return worksheet.get_all_records()

    def append_row(self, worksheet_name: str, row_data: list):
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.append_row(row_data)

    def append_rows(self, worksheet_name: str, rows_data: list):
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.append_rows(rows_data)