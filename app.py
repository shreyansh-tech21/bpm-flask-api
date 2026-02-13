from flask import Flask,request,jsonify
import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Claim, Policy,Document,Claims_History
import logging,json

logging.basicConfig(
    filename='claims.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Server has started and logging started")


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///claims.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

def log_claim_history(claim_id,old_status,new_status):
    new_history=Claims_History(
        claim_id=claim_id,
        old_status=old_status,
        new_status=new_status,
        changed_at=datetime.now()
    )
    db.session.add(new_history)
    db.session.commit()
    logging.info(f"Claim history logged: claim_id={claim_id}, old_status={old_status}, new_status={new_status}")

@app.route("/create-claim", methods=["POST"])
def create_claim():
    logging.info("create-claim: request received")

    data = request.get_json(force=True, silent=True)

    # If data is a string (common with Camunda), we need to parse it again
    if isinstance(data, str):
        logging.info("Data received as stringified JSON; parsing...")
        data = json.loads(data)

    # If data is still None, let's look at the raw bytes
    if data is None:
        raw = request.data.decode('utf-8')
        logging.info(f"create-claim: raw data fallback: {raw}")
        data = json.loads(raw)

    print(f"Successfully parsed data: {data}")
    if(data["incidentDate"]):
        date_str=data["incidentDate"]
        clean_date_st=date_str.replace("IST","")
        incident_dt=datetime.strptime(clean_date_st,'%a %b %d %H:%M:%S %Y')


    claim = Claim(
        claim_id=str(uuid.uuid4()),
        customer_id=data["customerId"],
        policy_number=data["policyNumber"],
        claim_amount=data["claimAmount"],
        claim_type=data["claimType"],
        description=data["description"],
        uploaded_documents=data["uploadedDocuments"],
        incident_date=incident_dt if incident_dt else None,
        status="SUBMITTED"
    )
    db.session.add(claim)
    db.session.commit()
    logging.info(f"create-claim: claim saved to DB claim_id={claim.claim_id}")
    log_claim_history(claim.claim_id,"NONE",claim.status)

    logging.info(f"Saved to DB: {claim.claim_id}")


    return {"claimId": claim.claim_id, "status": "SUBMITTED"}

@app.route("/send-ack",methods=["POST"])
def send_ack():
    data=request.data
    data=json.loads(data)
    

    logging.info(f"Acknowledgement sent for the claim {data['claimId']}")
    return {"acknowledgementSent":True,"acknowledgementTime":datetime.now().isoformat()}

@app.route("/validate-policy",methods=["POST"])
def validate_policy():
    logging.info("validate-policy: request received")
    data=request.data
    data=json.loads(data)
    print("the data is ",data)
    policy_number=data["policyNumber"]
    customer_id=data["customerId"]
    claim_id=data["claimId"]
    logging.info(f"Validating Policy: {policy_number} for Customer: {customer_id}")
    claim=Claim.query.filter_by(claim_id=claim_id).first()
    

    policy=Policy.query.filter_by(policy_number=policy_number).first()
    if not policy:
        logging.info(f"Policy validation failed: Policy {policy_number} not found")
        log_claim_history(claim_id,old_status,"REJECTED")
        return {"policyValid":False}
    if policy.status != "ACTIVE":
        logging.info(f"Policy validation failed: Policy {policy_number} is not active")
        log_claim_history(claim.claim_id,old_status,"REJECTED")
        return {"policyValid":False}
  
    print("the policy is Valid")
    log_claim_history(claim_id,claim.status,"VALIDATED")
    return {"policyValid":True,"coverageLimit":policy.coverageLimit,"deductible":policy.deductible}

@app.route("/claim-history",methods=["GET"])
def claim_history():
    claims_history=Claims_History.query.all()
    output=[]
    for claim in claims_history:
        state={
            "claim_id":claim.claim_id,
            "old_status":claim.old_status,
            "new_status":claim.new_status,
            "changed_at":claim.changed_at
        }
        output.append(state)
    return output

@app.route("/add-policy",methods=["POST"])
def add_policy():
    logging.info("add-policy: request received")
    data=request.data.decode('utf-8')
    print(type(data))
    print(data)
    data=json.loads(data)
    print("the data is ",data)
    policy=Policy(
        policy_number=data["policyNumber"],
        customer_id=data["customerId"],
        coverageLimit=data["coverageLimit"],
        deductible=data["deductible"],
        status="ACTIVE"
    )
    existing_policy=Policy.query.filter_by(
        policy_number=data["policyNumber"],
        customer_id=data["customerId"],
    ).first()
    if existing_policy:
        logger.info(f"Policy addition failed: Policy {data['policyNumber']} already exists")
        return {"policyAdded":False}
    db.session.add(policy)
    db.session.commit()
    logging.info(f"Policy {data['policyNumber']} added successfully")
    return {"policyAdded":True}

@app.route("/reject-claim",methods=["POST"])
def reject_claim():
    logging.info("reject-claim: request received")
    data=request.data.decode('utf-8')
    print(type(data))
    data=json.loads(data)
    claim_id=data["claimId"]
    reason=data["reason"]
    if not reason:
        reason="Policy not valid"
    claim=Claim.query.filter_by(claim_id=claim_id).first()
    if not claim:
        logger.info(f"Claim rejection failed: Claim {claim_id} not found")
        return {"error":"Claim not found"},404
    if claim.status != "SUBMITTED":
        logger.info(f"Claim rejection failed: Claim {claim_id} is not in SUBMITTED state")
        return {"error":"Claim not in SUBMITTED state"},400
    if claim.status in ["REJECTED","APPROVED"]:
        logger.info(f"Claim rejection failed: Claim {claim_id} is already processed")
        return {"error":"Claim already processed"},400
    claim.status="REJECTED"
    claim.rejection_reason=reason
    claim.closed_at=datetime.now()
    db.session.commit()
    logging.info(f"Claim {claim_id} rejected by {reason}")
    log_claim_history(claim.claim_id,old_status,claim.status)
    return {"claimRejected":True}


@app.route("/claims",methods=["GET"])
def get_claims():
    logging.info("claims: request received")
    claims=Claim.query.all()
    output=[]
    for c in claims:
        output.append({
            "policy_number":c.policy_number,
            "customer_id":c.customer_id,
            "claim_amount":c.claim_amount,
            "claim_type":c.claim_type,
            "claim_id":c.claim_id,
            "approvedPayout":c.approvedPayout,
            "description":c.description,
            "uploaded_documents":c.uploaded_documents,
            "incident_date":c.incident_date,
            "status":c.status
        })
    return {"claims":output}

@app.route("/trigger-payment",methods=["POST"])
def trigger_payment():
    logging.info("trigger-payment: request received. Changing the policy status to PAYMENT_TRIGGERED")
    data=request.data.decode('utf-8')
    data=json.loads(data)
    logging.info(f"trigger-payment: data received: {data}")
    get_claim=Claim.query.filter_by(claim_id=data["claimId"]).first()
    approved_payout=data["approvedPayout"]
    logging.info(f"trigger-payment: approved payout: {approved_payout}")
    get_claim.approvedPayout=approved_payout
    print({
        "claim_id":get_claim.claim_id,
        "approved_payout":get_claim.approvedPayout
    })
    if not get_claim:
        logging.info(f"trigger-payment: claim {data['claimId']} not found")
        return {"error":"Claim not found"},404
    if get_claim.status in ["APPROVED","REJECTED"]:
        logging.info(f"trigger-payment: claim {data['claimId']} is already processed")
        return {"error":"Claim already processed"},400
    old_status=get_claim.status
    get_claim.status="APPROVED"
    db.session.commit()
    logging.info(f"trigger-payment: claim {data['claimId']} status changed to APPROVED")
    log_claim_history(get_claim.claim_id,old_status,get_claim.status)
    policy=Policy.query.filter_by(policy_number=get_claim.policy_number,customer_id=get_claim.customer_id).first()
    policy.status="PAYMENT_TRIGGERED"
    db.session.commit()
    logging.info(f"Policy status changed to PAYMENT_TRIGGERED")
    return {"verificationStatus":"APPROVED"}


@app.route("/store-documents",methods=["POST"])
def store_documents():
    logging.info("store-documents: request received")
    data=request.data.decode('utf-8')
    print(type(data))
    data=json.loads(data)
    logging.info(f"store-documents: data received: {data}")
    uploaded_documents=[doc.strip() for doc in data["uploadedDocuments"].split(",")]
    claim_id=data["claimId"]
    store_ids=[]
    for doc in uploaded_documents:
        doc_id=str(uuid.uuid4())
        new_doc=Document(
            document_id=doc_id,
            claim_id=claim_id,
            file_name=doc,
            uploaded_at=datetime.now()
        )
        db.session.add(new_doc)
        db.session.commit()
        store_ids.append(doc_id)
    return {"documentIds":store_ids,"dateStored":datetime.now().isoformat()}

@app.route("/notify-additional-documents",methods=["POST"])
def notify_additional_documents():
    logging.info("notify-additional-documents: request received")
    data=request.data.decode('utf-8')
    data=json.loads(data)
    additional_documents=data["additionalDocuments"]
    customer_id=data["customerId"]
    return {"additionalDocuments":additional_documents,"customerId":customer_id,"notificationTime":datetime.now().isoformat(),"customerNotified":True,"notificationType":"ADDITIONAL_DOCUMENTS"}


@app.route("/policies",methods=["GET"])
def get_policies():
    logging.info("policies: request received")
    policies=Policy.query.all()
    output=[]
    for p in policies:
        output.append({
            "policy_number":p.policy_number,
            "customer_id":p.customer_id,
            "coverageLimit":p.coverageLimit,
            "deductible":p.deductible,
            "status":p.status
        })
    return {"policies":output}
    

@app.route("/")
def home():
    return "Claims backend browser is opened."

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)