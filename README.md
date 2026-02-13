# BPM Flask Claims API

A Flask-based REST API for **claims and policy management**, designed to integrate with BPM workflows (e.g. Camunda). It handles claim submission, policy validation, document storage, approval/rejection, and payment triggering, with full audit history.

## Features

- **Claims** – Create, list, reject, and approve claims with status tracking
- **Policies** – Add and list policies; validate policy and coverage for claims
- **Documents** – Store and link documents to claims; request additional documents
- **Claim history** – Audit trail of status changes (SUBMITTED → VALIDATED → APPROVED/REJECTED)
- **Payment** – Trigger payment and update policy status after approval
- **Logging** – Request and status changes logged to `claims.log`

## Tech Stack

- **Python 3** with **Flask 3**
- **SQLAlchemy** + **SQLite** (`claims.db`)
- JSON APIs suitable for BPM/camunda integration

## Prerequisites

- Python 3.8+
- pip

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shreyansh-tech21/bpm-flask-api.git
   cd bpm-flask-api
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   # source .venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

From the project root:

```bash
python app.py
```

- The app runs at **http://127.0.0.1:5000** (Flask default).
- On first run, the SQLite database and tables are created automatically.
- Logs are written to `claims.log`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health / welcome message |
| POST | `/create-claim` | Create a new claim (customerId, policyNumber, claimAmount, claimType, description, incidentDate, uploadedDocuments) |
| POST | `/send-ack` | Send acknowledgement for a claim |
| POST | `/validate-policy` | Validate policy for a claim (policyNumber, customerId, claimId) |
| GET | `/claim-history` | Get full claim status history |
| POST | `/add-policy` | Add a new policy (policyNumber, customerId, coverageLimit, deductible) |
| POST | `/reject-claim` | Reject a claim with reason (claimId, reason) |
| GET | `/claims` | List all claims |
| POST | `/trigger-payment` | Approve claim and trigger payment (claimId, approvedPayout) |
| POST | `/store-documents` | Store document metadata for a claim (claimId, uploadedDocuments) |
| POST | `/notify-additional-documents` | Notify customer about required additional documents |
| GET | `/policies` | List all policies |

Request/response bodies are JSON unless noted otherwise.

## Project Structure

```
.
├── app.py              # Flask app, routes, and business logic
├── models.py           # SQLAlchemy models (Claim, Policy, Document, Claims_History)
├── requirements.txt    # Python dependencies
├── routes/             # Route modules (claim_routes, policy_routes, document_routes)
├── claims.db           # SQLite database (created at runtime, gitignored)
├── claims.log          # Application logs (gitignored)
└── README.md
```

## Design Document

See **MSA_CS_GP_Software_Design_Document.pdf** in this repository for the software design and requirements.

## License

Use as per your organization’s policy.
