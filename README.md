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
   project_id = "your-project-id"
   bq_project = "your-bigquery-project"
   bq_dataset = "your-dataset-name"
