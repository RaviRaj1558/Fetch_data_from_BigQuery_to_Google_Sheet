# **Google Sheets Data Exporter**

A Cloud Function that automatically exports employee management data from BigQuery to Google Sheets.

## **📋 Overview**

**This Python-based Google Cloud Function** securely transfers employee information (employee codes, email IDs, and manager email IDs) from BigQuery to specified Google Sheets, creating an organized "Manager_Mail_id" worksheet for management reporting.

## **🚀 Features**

- **Secure Credential Management** - Uses GCP Secret Manager for service account credentials
- **Automated Data Sync** - Exports BigQuery data to Google Sheets automatically
- **Dynamic Worksheet Management** - Creates or updates sheets as needed
- **Comprehensive Error Handling** - Detailed logging and structured error responses
- **Data Cleaning** - Converts zero values to blanks for better presentation

## **🛠️ Setup**

### **Prerequisites**
- **Google Cloud Platform project** with:
  - Cloud Functions enabled
  - Secret Manager enabled
  - BigQuery API enabled
- **Service accounts** with appropriate permissions

### **Configuration**

1. **Store Secrets in Secret Manager:**
   - `gs_service_account`: Google Sheets service account credentials (JSON)
   - `long_terminal_447308_d1_service_account`: BigQuery service account credentials (JSON)

2. **Update Environment Variables:**
   ```python
   bq_project = "long-terminal-447308-d1"
   bq_dataset = "freshsales_data"
   bq_table = "WTi_employee_details"
   
### **Functions**

**get_secret(secret_name, project_id)**
Fetches and parses secrets from GCP Secret Manager.

**load_data_from_bigquery(bq_dict, bq_project, bq_dataset)**
Loads employee data from BigQuery using service account credentials.

**send_data_to_gsheet(df, worksheet_name, spreadsheet_id, gs_dict)**
Sends DataFrame data to Google Sheets, creating or clearing worksheets as needed.

**zero_to_blank(df)**
Data cleaning function that converts zero values to blanks.

**main(request)**
Cloud Function entry point that orchestrates the entire data export process.

### **Output (Google Sheets)**
Worksheet named "Manager_Mail_id" with columns:

1.Employee Code

2.Email ID

3.Manager Email ID
   
