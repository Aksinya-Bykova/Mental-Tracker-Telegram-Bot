from typing import Dict, List, Union
import pygsheets
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class GoogleTable:
    """Класс для работы с Google Sheet."""
    def __init__(
        self, credence_service_file:str = "", googlesheet_file_url:str = ""
    ) -> None:
        """Инициализирует класс.
        Args:
            credence_service_file (str): Путь до сервисного файла credence.json (Google Sheet API).
            googlesheet_file_url (str): Ссылка на Google Sheet.
        Returns:
        """
        self.credence_service_file = credence_service_file
        self.googlesheet_file_url = googlesheet_file_url
        self.client = None  # Client object for gspread

    def _get_googlesheet_by_url(
        self, googlesheet_client: pygsheets.client.Client
    ) -> pygsheets.Spreadsheet:
        """Получает Google.Docs таблицу по ссылке на документ."""
        sheets: pygsheets.Spreadsheet = googlesheet_client.open_by_url(
            self.googlesheet_file_url
        )
        return sheets.sheet1

    def _get_googlesheet_client(self):
        """Авторизуется с помощью сервисного ключа и 
        возвращает клиентский объект Google Docs.
        """
        return pygsheets.authorize(
            service_file=self.credence_service_file
        )
    
    def _authorize_client(self):
      """Авторизация клиента Google Sheets с использованием сервисного ключа."""
      scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
      creds = ServiceAccountCredentials.from_json_keyfile_name(self.credence_service_file, scope)
      self.client = gspread.authorize(creds)
      
    def _read_cell(self, row, col):
        googlesheet_client = self._get_googlesheet_client()
        wks = self._get_googlesheet_by_url(googlesheet_client)
        cell_value = wks.cell((row, col)).value
        return cell_value
    
    def _update_cell(self, row: int, col: int, value: Union[str, int, float, bool]) -> None:
        """Обновляет значение одной ячейки в таблице.
        Args:
            row (int): Номер строки ячейки.
            col (int): Номер столбца ячейки.
            value (Union[str, int, float, bool]): Новое значение для ячейки.
        """
        googlesheet_client: pygsheets.client.Client = self._get_googlesheet_client()
        wks = self._get_googlesheet_by_url(googlesheet_client)
        wks.update_value((row, col), value)
    
    def _set_metric(self):
        googlesheet_client: pygsheets.client.Client = self._get_googlesheet_client()
        wks: pygsheets.Spreadsheet = self._get_googlesheet_by_url(googlesheet_client)
        wks.update_cell(self, 'A1', "Hey yank this numpy array")
        
    def _load_data_as_dataframe(self, googlesheet_url: str, sheet_name: str) -> pd.DataFrame:
        """Загружает данные из Google Sheet в Pandas DataFrame.
        Args:
            googlesheet_url (str): Ссылка на Google Sheet.
            sheet_name (str): Название листа Google Sheet.
        Returns:
            pd.DataFrame: Загруженные данные.
        """
        if not self.client:
            self._authorize_client()

        try:
            # Открываем Google Sheet по URL
            sheet = self.client.open_by_url(googlesheet_url)
            worksheet = sheet.worksheet(sheet_name)
            
            values = worksheet.get_all_values()
            #print(f"Values from Google Sheet: {values}")  # Выводим данные для отладки
            df = pd.DataFrame(values[1:], columns=values[0])

            return df

        except gspread.exceptions.APIError as e:
            print(f"API Error: {e.response}")
            return pd.DataFrame()

        except Exception as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()
