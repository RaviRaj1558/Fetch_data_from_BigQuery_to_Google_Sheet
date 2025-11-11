Google Sheets Data Exporter
A Cloud Function that exports employee data from BigQuery to Google Sheets, specifically designed to provide manager email information for organizational use.

Overview
This Python-based Google Cloud Function automatically retrieves employee data from BigQuery and exports it to a specified Google Sheet. The function focuses on extracting employee codes, email IDs, and corresponding manager email IDs for organizational reporting and management purposes.

Features
Secure Credential Management: Uses GCP Secret Manager to securely store and access service account credentials

BigQuery Integration: Connects to BigQuery to fetch employee data from the WTi_employee_details table

Google Sheets Automation: Automatically creates/updates worksheets in Google Sheets with the exported data

Error Handling: Comprehensive logging and error handling with detailed tracebacks

Data Cleaning: Converts zero values to blanks for better data presentation

Architecture
text
HTTP Request → Cloud Function → Secret Manager → BigQuery → Google Sheets
Prerequisites
Google Cloud Platform project with:

Cloud Functions enabled

Secret Manager enabled

BigQuery API enabled

Service accounts with appropriate permissions for:

BigQuery data access

Google Sheets modification

Secrets stored in Secret Manager containing service account credentials

Setup
1. Secret Configuration
Store the following secrets in GCP Secret Manager:

gs_service_account: Google Sheets service account credentials (JSON)

long_terminal_447308_d1_service_account: BigQuery service account credentials (JSON)

2. Environment Configuration
Update these variables in the code for your environment:

python
project_id = "28472539111"
bq_project = "long-terminal-447308-d1"
bq_dataset = "freshsales_data"
3. Required Permissions
Ensure the Cloud Function's service account has:

secretmanager.versions.access permission for Secret Manager

BigQuery Data Viewer role for the dataset

Appropriate permissions for the Google Sheets to be modified

Usage
HTTP Request
bash
POST https://[REGION]-[PROJECT-ID].cloudfunctions.net/[FUNCTION-NAME]
Content-Type: application/json

{
    "spreadsheet_id": "your-google-sheet-id-here"
}
Response
Success (200):

json
{
    "status": "success",
    "message": "Data sent to spreadsheet '[SPREADSHEET_ID]'"
}
Error (500):

json
{
    "status": "error",
    "error": "Error description",
    "traceback": "Detailed traceback information"
}
Data Structure
Input Data (BigQuery)
Query from WTi_employee_details table:

employee_code

email_id

manager_email_id

Output (Google Sheets)
Worksheet named "Manager_Mail_id" with columns:

Employee Code

Email ID

Manager Email ID

Functions
get_secret(secret_name, project_id)
Fetches and parses secrets from GCP Secret Manager.

load_data_from_bigquery(bq_dict, bq_project, bq_dataset)
Loads employee data from BigQuery using service account credentials.

send_data_to_gsheet(df, worksheet_name, spreadsheet_id, gs_dict)
Sends DataFrame data to Google Sheets, creating or clearing worksheets as needed.

zero_to_blank(df)
Data cleaning function that converts zero values to blanks.

main(request)
Cloud Function entry point that orchestrates the entire data export process.

Error Handling
Comprehensive logging at INFO level for monitoring

Structured error responses with tracebacks

Exception handling for Secret Manager, BigQuery, and Google Sheets operations

Security
No hardcoded credentials - all secrets retrieved from Secret Manager

Service account principle for all GCP services

Secure API scopes for Google Sheets access

Deployment
Deploy as a Google Cloud Function with HTTP trigger:

bash
gcloud functions deploy your-function-name \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s
Monitoring
Check Cloud Function logs in GCP Console for:

Secret retrieval status

BigQuery query execution

Google Sheets update operations

Error details and tracebacks

Support
For issues related to:

Secret access: Verify Secret Manager permissions

BigQuery: Check dataset permissions and table existence

Google Sheets: Verify spreadsheet sharing with service account

Function execution: Review Cloud Function logs and quotas


