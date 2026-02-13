"""
One-time script: recreates the policy table WITHOUT the UNIQUE constraint on policy_number.
Run once: python fix_policy_table.py
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "instance", "claims.db")
conn = sqlite3.connect(db_path)

conn.execute("""
CREATE TABLE policy_new (
    id INTEGER NOT NULL PRIMARY KEY,
    policy_number VARCHAR(50),
    customer_id VARCHAR(50),
    "coverageLimit" FLOAT,
    deductible FLOAT,
    status VARCHAR(50)
)
""")
conn.execute("INSERT INTO policy_new SELECT id, policy_number, customer_id, \"coverageLimit\", deductible, status FROM policy")
conn.execute("DROP TABLE policy")
conn.execute("ALTER TABLE policy_new RENAME TO policy")
conn.commit()
conn.close()
print("Done: policy table recreated without UNIQUE on policy_number.")
