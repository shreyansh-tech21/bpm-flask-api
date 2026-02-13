from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class Claim(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    claim_id=db.Column(db.String(50),unique=True)
    customer_id=db.Column(db.String(50))
    policy_number=db.Column(db.String(50))
    claim_amount=db.Column(db.Float)
    claim_type=db.Column(db.String(50))
    description=db.Column(db.String(200))
    uploaded_documents=db.Column(db.String(150))
    incident_date=db.Column(db.DateTime,nullable=True)
    status=db.Column(db.String(50))
    rejection_reason=db.Column(db.String(200),nullable=True)
    closed_at=db.Column(db.DateTime,nullable=True)
    approvedPayout=db.Column(db.Float,nullable=True)

class Policy(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    policy_number=db.Column(db.String(50))
    customer_id=db.Column(db.String(50))
    coverageLimit=db.Column(db.Float)
    deductible=db.Column(db.Float)
    status=db.Column(db.String(50))

class Document(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    document_id=db.Column(db.String(50))
    claim_id=db.Column(db.String(50))
    file_name=db.Column(db.String(100))
    uploaded_at=db.Column(db.DateTime)

class Claims_History(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    claim_id=db.Column(db.String(50))
    old_status=db.Column(db.String(50))
    new_status=db.Column(db.String(50))
    changed_at=db.Column(db.DateTime)