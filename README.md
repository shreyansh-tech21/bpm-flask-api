<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=sqlalchemy" alt="SQLAlchemy"/>
</p>

# BPM Flask Claims API

<p align="center">
  <strong>REST API for claims & policy lifecycle — from submission to payout.</strong>
</p>

<p align="center">
  Built for BPM workflows (e.g. Camunda). Submit claims, validate policies, store documents, approve or reject, trigger payment — with full audit history.
</p>

---

## ✨ What it does

| | |
|---|---|
| **Claims** | Create, list, reject, approve — with status flow `SUBMITTED → VALIDATED → APPROVED / REJECTED` |
| **Policies** | Add policies; validate coverage and deductible before approving claims |
| **Documents** | Attach documents to claims; request and track additional documents |
| **Audit** | Every status change logged in `Claims_History` and `claims.log` |
| **Payment** | Approve claim → set payout → mark policy as `PAYMENT_TRIGGERED` |

---

## 🚀 Quick start

```bash
# Clone & enter
git clone https://github.com/shreyansh-tech21/bpm-flask-api.git
cd bpm-flask-api

# Virtual env (recommended)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# Install & run
pip install -r requirements.txt
python app.py
```

**→ API:** `http://127.0.0.1:5000` · **→ Logs:** `claims.log` · **→ DB:** `claims.db` (SQLite, auto-created)

---

## 📡 API at a glance

### Claims
| Method | Endpoint | What it does |
|--------|----------|----------------|
| `POST` | `/create-claim` | Create claim (customerId, policyNumber, claimAmount, claimType, description, incidentDate, uploadedDocuments) |
| `POST` | `/send-ack` | Send acknowledgement for a claim |
| `POST` | `/validate-policy` | Validate policy for a claim → returns `policyValid`, `coverageLimit`, `deductible` |
| `POST` | `/reject-claim` | Reject with reason (`claimId`, `reason`) |
| `POST` | `/trigger-payment` | Approve and set payout (`claimId`, `approvedPayout`) |
| `GET`  | `/claims` | List all claims |
| `GET`  | `/claim-history` | Full audit trail of status changes |

### Policies
| Method | Endpoint | What it does |
|--------|----------|----------------|
| `POST` | `/add-policy` | Add policy (policyNumber, customerId, coverageLimit, deductible) |
| `GET`  | `/policies` | List all policies |

### Documents
| Method | Endpoint | What it does |
|--------|----------|----------------|
| `POST` | `/store-documents` | Store document metadata for a claim (claimId, uploadedDocuments) |
| `POST` | `/notify-additional-documents` | Notify customer about required additional documents |

### Other
| Method | Endpoint | What it does |
|--------|----------|----------------|
| `GET`  | `/` | Health / welcome |

All request/response bodies are **JSON**.

---

## 📁 Project layout

```
bpm-flask-api/
├── app.py                 # Flask app + routes + logic
├── models.py              # Claim, Policy, Document, Claims_History
├── requirements.txt
├── routes/
│   ├── claim_routes.py
│   ├── policy_routes.py
│   └── document_routes.py
├── claims.db              # SQLite (runtime, gitignored)
├── claims.log             # Logs (gitignored)
├── MSA_CS_GP_Software_Design_Document.pdf
└── README.md
```

---

## 📄 Design & docs

Full software design and requirements: **MSA_CS_GP_Software_Design_Document.pdf** in this repo.

---

<p align="center">
  <sub>Use as per your organization’s policy.</sub>
</p>
