from functools import cached_property
from pydantic import computed_field
from pydantic_settings import BaseSettings
from pandas import DataFrame

import gspread
from gspread.spreadsheet import Spreadsheet, Worksheet
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetReader(BaseSettings):
    """_summary_: Google Service Account Reader"""

    private_key_id: str
    private_key_str: str
    client_email: str
    client_id: int
    project_id: str
    type: str = "service_account"
    auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    token_uri: str = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    universe_domain: str = "googleapis.com"

    @computed_field
    @property
    def client_x509_cert_url(self) -> str:
        """_summary_: _description_"""
        return f"https://www.googleapis.com/robot/v1/metadata/x509/{self.client_email}"

    @computed_field
    @property
    def private_key(self) -> str:
        """_summary_: _description_"""
        return self.private_key_str.replace("\\n", "\n")

    @cached_property
    def scopes(self):
        """_summary_: _description_"""
        return [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

    @cached_property
    def credentials(self) -> ServiceAccountCredentials:
        """_summary_: _description_"""
        return ServiceAccountCredentials.from_json_keyfile_dict(
            self.model_dump(), scopes=self.scopes
        )

    @cached_property
    def client(self) -> gspread.Client:
        """_summary_: _description_"""
        return gspread.authorize(self.credentials)

    def get_workbook(self, workbook_name: str) -> Spreadsheet:
        """_summary_: _description_"""
        return self.client.open(workbook_name)

    def get_worksheet(self, workbook_name: str, worksheet_name: str) -> Worksheet:
        """_summary_: _description_"""
        return self.get_workbook(workbook_name).worksheet(worksheet_name)

    def get_worksheet_data(self, workbook_name: str, worksheet_name: str) -> list[dict]:
        """_summary_: _description_"""
        return self.get_worksheet(workbook_name, worksheet_name).get_all_records()

    def get_worksheet_dataframe(
        self, workbook_name: str, worksheet_name: str
    ) -> DataFrame:
        """_summary_: _description_"""
        return DataFrame.from_dict(
            self.get_worksheet_data(workbook_name, worksheet_name)
        )
