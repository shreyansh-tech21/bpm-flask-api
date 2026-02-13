"""
Clear all claims and policies from the database.
Run from project root:  python clear_data.py
"""
from app import app, db
from models import Claim, Policy,Claims_History

with app.app_context():
    n_claims = Claims_History.query.delete()
    db.session.commit()
    print(f"Deleted {n_claims} claims .")
