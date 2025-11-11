import json
import logging
import traceback
import gspread


import pandas as pd
import numpy as np
from google.oauth2 import service_account
from google.cloud import secretmanager
from google.cloud import bigquery

# Enable debug logging
logging.basicConfig(level=logging.INFO)

def get_secret(secret_name: str, project_id: str):
    """
    Fetch secret from GCP Secret Manager and parse it as JSON.
    """
    try:
        logging.info(f"Fetching secret {secret_name} from project {project_id}")
        client = secretmanager.SecretManagerServiceClient()
        secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(name=secret_path)
        secret_string = response.payload.data.decode("UTF-8")
        return json.loads(secret_string)
    except Exception as e:
        logging.exception("Error fetching secret from Secret Manager")
        raise

def send_data_to_gsheet(df, worksheet_name, spreadsheet_id, gs_dict):
    """
    Send a DataFrame to Google Sheets.
    """
    try:
        logging.info(f"Preparing to send data to Sheet: {worksheet_name}")
        
        

        # Calculate needed rows and columns
        total_rows = len(df) + 1  # plus 1 for header row
        total_cols = len(df.columns)

        # Log the counts for debugging
        logging.info(f"Columns: {total_cols}, Rows: {total_rows}")

        data = [df.columns.tolist()] + df.values.tolist()

        credentials = service_account.Credentials.from_service_account_info(
            gs_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)

        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            worksheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name,
                rows=str(total_rows),  # Add some buffer rows
                cols=str(total_cols)    # Add some buffer cols
            )

        worksheet.update(values=data, value_input_option="USER_ENTERED")
        logging.info(f"Data successfully written to Google Sheet: {worksheet_name}")

    except Exception as e:
        logging.exception("Error writing to Google Sheet")
        raise

def load_data_from_bigquery(bq_dict, bq_project, bq_dataset):
    """
    Load DataFrames from BigQuery using service account credentials.
    """
    credentials = service_account.Credentials.from_service_account_info(bq_dict)
    bq_client = bigquery.Client(credentials=credentials, project=bq_project)

    # Queries without date filtering
    wis_query = f"""
        SELECT employee_code, email_id, manager_email_id
        FROM `{bq_project}.{bq_dataset}.WTi_employee_details`
    """

    logging.info("Loading wis_df from BigQuery...")
    wis_df = bq_client.query(wis_query).to_dataframe()

    return wis_df

def zero_to_blank(df):
    df.replace(0, None, inplace=True)
    return df

def main(request):
    """
    HTTP Cloud Function entry point.
    """
    try:
        logging.info("Function triggered")

        project_id = "28472539111"
        gs_key_req = "gs_service_account"        
        bq_project = "long-terminal-447308-d1"
        bq_key_req = "long_terminal_447308_d1_service_account"
        bq_dataset = "freshsales_data"

        # Get service account credentials from Secret Manager
        gs_dict = get_secret(gs_key_req, project_id)        
        bq_dict = get_secret(bq_key_req, project_id)

        # Parse incoming JSON
        data = request.get_json(silent=True) or {}
        logging.info(f"Incoming request data: {data}")

        spreadsheet_id = data.get("spreadsheet_id")

        if not spreadsheet_id:
            raise ValueError("spreadsheet_id is a required parameter")

        # Load data from BigQuery without date filtering
        wis_df = load_data_from_bigquery(bq_dict, bq_project, bq_dataset)

        # Send raw data to GSheet
        send_data_to_gsheet(zero_to_blank(wis_df), "Manager_Mail_id", spreadsheet_id, gs_dict)

        return (
            json.dumps({
                "status": "success",
                "message": f"Data sent to spreadsheet '{spreadsheet_id}'"
            }),
            200,
            {"Content-Type": "application/json"}
        )

    except Exception as e:
        tb = traceback.format_exc()
        logging.error(f"Exception: {e}")
        logging.error(tb)
        return (
            json.dumps({
                "status": "error",
                "error": str(e),
                "traceback": tb
            }),
            500,
            {"Content-Type": "application/json"}
        )