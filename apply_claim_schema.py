"""
Recreate the claim table with the updated schema (new columns: rejection_reason, closed_at).
Run once with DB empty or when you've changed the Claim model:  python apply_claim_schema.py
"""
from app import app, db
from models import Claims_History,Claim

with app.app_context():
    
    db.create_all()
    print("Claim history table created.")
