from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Configuration
import logging
class Fetch_Sheet_Data :
    
    def __init__(self):
        self.credentials = Configuration().authenticate_google()


    def get_values(self,spreadsheet_id, range_name ):
        """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        creds = self.credentials
        # pylint: disable=maybe-no-member
        try:
            service = build("sheets", "v4", credentials=creds)

            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_name)
                .execute()
            )
            rows = result.get("values", [])
            logging.info(f"{len(rows)} rows retrieved")
            return result
        except HttpError as error:
            logging.info(f"An error occurred: {error}")
            return error


