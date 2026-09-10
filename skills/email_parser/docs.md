# Email Ingestion Stabilizer (Inbox Librarian)

## Strict Read-Only Policy
This agent is hardcoded to **only** read emails. It cannot send, forward, delete, or modify emails in any way.

## Secrets Management
Requires API keys to be located in `/secrets/email_api/.env`. 
The agent will refuse to initialize if keys are placed in the global root `.env`.

## Core Capabilities
- **Classify**: Identifies if an email is a receipt, invoice, subscription renewal, or standard correspondence.
- **Extract**: Pulls structured data (amounts, dates, vendor names) from unstructured email bodies.
