`***Google Sheets Data Exporter***`
A Cloud Function that automatically exports employee management data from BigQuery to Google Sheets.

📋 Overview
This Python-based Google Cloud Function securely transfers employee information (employee codes, email IDs, and manager email IDs) from BigQuery to specified Google Sheets, creating an organized "Manager_Mail_id" worksheet for management reporting.

🚀 Features
Secure Credential Management - Uses GCP Secret Manager for service account credentials

Automated Data Sync - Exports BigQuery data to Google Sheets automatically

Dynamic Worksheet Management - Creates or updates sheets as needed

Comprehensive Error Handling - Detailed logging and structured error responses

Data Cleaning - Converts zero values to blanks for better presentation

🛠️ Setup
Prerequisites
Google Cloud Platform project with:

Cloud Functions enabled

Secret Manager enabled

BigQuery API enabled

Service accounts with appropriate permissions

Configuration
Store Secrets in Secret Manager:

gs_service_account: Google Sheets service account credentials (JSON)

long_terminal_447308_d1_service_account: BigQuery service account credentials (JSON)

Update Environment Variables:

python
project_id = "your-project-id"
bq_project = "your-bigquery-project"
bq_dataset = "your-dataset-name"
📤 Usage
HTTP Request
bash
POST https://[REGION]-[PROJECT-ID].cloudfunctions.net/[FUNCTION-NAME]
Content-Type: application/json

{
    "spreadsheet_id": "your-google-sheet-id"
}
Response Examples
Success (200):

json
{
    "status": "success",
    "message": "Data sent to spreadsheet 'your-spreadsheet-id'"
}
Error (500):

json
{
    "status": "error",
    "error": "Error description",
    "traceback": "Detailed traceback information"
}
🗂️ Data Structure
Source (BigQuery)
Table: WTi_employee_details

employee_code

email_id

manager_email_id

Destination (Google Sheets)
Worksheet: "Manager_Mail_id"

Employee Code

Email ID

Manager Email ID

🔧 Deployment
bash
gcloud functions deploy employee-data-exporter \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s
📊 Monitoring
Check Cloud Function logs in GCP Console for:

Secret retrieval status

BigQuery query execution

Google Sheets update operations

Error details and tracebacks

🛡️ Security
No hardcoded credentials

Service account authentication

Secure API scopes

Secret Manager for credential storage

🤝 Support
For issues check:

Secret Manager permissions

BigQuery dataset access

Google Sheets sharing with service account

Cloud Function execution logs
