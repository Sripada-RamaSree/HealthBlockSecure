HealthBlockSecure
Decentralised Health Record Management with Blockchain, Privacy-Preserving Authentication, and Intelligent Access Control
HealthBlockSecure is a research-oriented framework for secure, decentralised, privacy-aware, and auditable Electronic Health Record (EHR) management.
The framework integrates:
•	Permissioned blockchain-based access control
•	Encrypted off-chain health record storage
•	Decentralised identity management
•	Zero-Knowledge Proof (ZKP)-assisted authentication
•	Smart-contract-based policy enforcement
•	PrivAccessNet for contextual access validation and anomaly detection
•	Short-lived access-token generation
•	SHA-256-based integrity verification
•	Immutable audit logging
•	Security, latency, throughput, ablation, and baseline evaluation
The implementation is designed to reproduce the methodology of the HealthBlockSecure research framework using a modular architecture suitable for experimentation, validation, and further extension.
1. Overview
Conventional cloud-based EHR systems depend heavily on centralised trust and may provide limited transparency, auditability, and adaptability in access-control decisions.
HealthBlockSecure addresses these limitations through a hybrid blockchain-cloud architecture in which:
1.	Health records are encrypted before storage.
2.	Encrypted records are stored off-chain.
3.	Integrity hashes, policies, metadata, and audit information are maintained through the access-control infrastructure.
4.	Requesters are represented using decentralised identifiers.
5.	ZKP-assisted authentication verifies eligibility with reduced disclosure of sensitive attributes.
6.	PrivAccessNet evaluates contextual access behaviour.
7.	Deterministic policy rules and the learned access-compliance score jointly support the final access decision.
8.	Approved users receive time-limited access credentials.
9.	Retrieved records are decrypted locally and verified against the stored SHA-256 hash.
10.	Security-relevant events are recorded in an auditable ledger.
2. Main Contributions
The implementation contains the following major components:
•	Hybrid blockchain and off-chain EHR storage architecture
•	AES-based health-record encryption
•	ECC/ECDH-based protection of symmetric keys
•	SHA-256 integrity verification
•	DID-based identity representation
•	External ZKP verification workflow
•	Smart-contract-style access-policy management
•	Patient consent validation
•	Role- and context-aware access control
•	PrivAccessNet neural access-validation model
•	Access-token generation and expiration
•	Replay and anomaly simulation
•	Append-only audit logging
•	Synthetic access-request generation
•	Baseline machine-learning models
•	Security and tampering experiments
•	Latency and throughput benchmarking
•	Component-wise ablation experiments
•	Multi-seed reproducibility support
3. System Architecture
User Layer
Represents:
•	Patients
•	Doctors
•	Nurses
•	Researchers
•	Healthcare organisations
•	Authorised third parties
Each participant can be associated with a decentralised identifier and cryptographic credentials.
Blockchain and Access-Control Layer
Responsible for:
•	Record metadata registration
•	Access-policy management
•	Consent verification
•	DID validation
•	ZKP verification result processing
•	PrivAccessNet decision support
•	Token issuance
•	Access approval or denial
•	Immutable audit-event registration
Off-Chain Storage Layer
Stores encrypted EHR data outside the ledger.
Only references, hashes, encrypted key material, policies, and relevant metadata are retained by the access-control infrastructure.
4. End-to-End Workflow
The complete HealthBlockSecure workflow is:
Patient EHR
   |
   v
Schema Harmonisation
   |
   v
AES Record Encryption
   |
   +----> SHA-256 Integrity Hash
   |
   v
ECC/ECDH-Based Session-Key Protection
   |
   v
Encrypted Off-Chain Storage
   |
   v
Metadata Registration
   |
   v
Provider Access Request
   |
   v
DID Validation
   |
   v
ZKP-Assisted Authentication
   |
   v
Consent + Role + Policy Validation
   |
   v
PrivAccessNet Inference
   |
   v
Final Access Decision
   |
   +------ DENY ---> Audit Event
   |
   v
Time-Limited Access Token
   |
   v
Encrypted Record Retrieval
   |
   v
Local Key Recovery
   |
   v
AES Decryption
   |
   v
SHA-256 Integrity Verification
   |
   v
Audit Logging
5. PrivAccessNet
PrivAccessNet is the learning-based access-validation component of HealthBlockSecure.
It processes contextual access-request attributes such as:
•	Requester role
•	Access time
•	Request type
•	Patient-consent status
•	Token validity
•	Previous access frequency
•	Policy-match status
•	Credential validity
•	Temporal validity
•	Replay indicators
•	Frequency anomalies
•	Privilege-escalation indicators
Architecture
Input Features
    |
Dense(64)
    |
Batch Normalisation
    |
ReLU
    |
Dropout(0.30)
    |
Dense(32)
    |
Batch Normalisation
    |
ReLU
    |
Dropout(0.30)
    |
Dense(16)
    |
Batch Normalisation
    |
ReLU
    |
Dense(1)
    |
Sigmoid
Default Training Configuration
Parameter	Value
Optimiser	Adam
Learning Rate	0.001
Batch Size	32
Maximum Epochs	50
Loss	Class-weighted Binary Cross-Entropy
Hidden Units	64, 32, 16
Activation	ReLU
Dropout	0.30
Output	Sigmoid
Early Stopping	Validation Loss
Sampling	Balanced Mini-Batches
The final neural score is used as a decision-support signal rather than replacing deterministic access-control conditions.
6. Access Decision Logic
The final access decision follows the general logic:
Grant Access =
    ZKP Verified
    AND DID Valid
    AND Consent Valid
    AND Role Permitted
    AND Access Purpose Permitted
    AND Temporal Policy Valid
    AND Token Conditions Valid
    AND PrivAccessNet Score >= Threshold
This allows HealthBlockSecure to combine deterministic policy enforcement with data-driven anomaly-aware validation.
7. Supported Security Scenarios
Legitimate
•	Valid provider request
•	Valid role
•	Active consent
•	Valid credential
•	Allowed access time
•	Valid request purpose
Adversarial / Invalid
•	Role violation
•	Consent violation
•	Expired credentials
•	Expired access token
•	Out-of-hours access
•	Privilege escalation
•	Replay attack
•	Excessive request frequency
•	Policy mismatch
•	Invalid credential
•	Record tampering
These scenarios are used to generate reproducible access-control datasets for PrivAccessNet training and evaluation.
8. Cryptographic Components
AES Record Encryption
Electronic health records are protected using symmetric encryption.
The implementation supports authenticated AES encryption for protecting confidentiality and detecting ciphertext modification.
ECC/ECDH Key Protection
The per-record symmetric session key is protected using elliptic-curve-based key agreement and key derivation.
A typical workflow is:
ECDH
  |
Shared Secret
  |
HKDF-SHA256
  |
Derived Key-Encryption Key
  |
Protected AES Session Key
SHA-256
SHA-256 is used to generate integrity fingerprints for the original health records.
During retrieval, the decrypted record is rehashed and compared against the registered hash.
Any mismatch is treated as an integrity failure.
9. Decentralised Identity
HealthBlockSecure includes a lightweight DID-oriented identity module.
Example identifiers:
did:hbs:patient001
did:hbs:doctor001
did:hbs:researcher001
did:hbs:hospital001
The identity layer can associate:
•	DID
•	Public key
•	Role
•	Organisation
•	Credential status
Private cryptographic keys remain outside the ledger.
10. Zero-Knowledge Proof Integration
The architecture supports an external ZKP verification service.
Conceptually:
Requester
   |
Generate Proof
   |
   v
External ZKP Verification Service
   |
   v
Verification Result
   |
   v
HealthBlockSecure Access Layer
The proof may demonstrate conditions such as:
credential_valid = true
role_is_permitted = true
consent_eligible = true
credential_not_expired = true
without disclosing the underlying sensitive identity attributes.
The repository includes support for integrating a Circom/snarkjs-style Groth16 workflow.
The default standalone research mode may use a deterministic verification adapter so that the complete workflow can be executed without installing a full ZKP proving environment.
11. Blockchain Integration
The repository contains components for integrating HealthBlockSecure with Hyperledger Fabric.
The target architecture includes:
•	Two healthcare organisations
•	Multiple peer nodes
•	Certificate Authorities
•	Raft ordering service
•	Go smart contracts
•	LevelDB state storage
•	Private-data support
•	Audit-event registration
Typical smart-contract operations include:
RegisterRecord
GetRecordMetadata
RegisterPolicy
UpdatePolicy
GrantConsent
RevokeConsent
RegisterDID
RequestAccess
IssueToken
ValidateToken
LogAuditEvent
GetAuditTrail
The standalone mode can also use a lightweight local ledger backend for development and automated testing.
12. Off-Chain Storage
Encrypted EHRs are stored outside the ledger.
Supported or extensible storage backends include:
•	Local filesystem
•	MinIO
•	Amazon S3-compatible storage
•	IPFS-compatible references
A storage abstraction allows the backend to be changed without modifying the rest of the access-control workflow.
Typical on-ledger metadata includes:
record_id
patient_did
data_category
storage_pointer
integrity_hash
encrypted_session_key
policy_id
timestamp
Plaintext EHR content is not stored on the ledger.
13. Datasets
SyntheticMass / Synthea
Used for:
•	Initial implementation
•	Synthetic patient workflows
•	Smart-contract testing
•	Access-policy simulation
•	Encryption experiments
•	DID mapping
•	Security testing
MIMIC-IV
Used for:
•	Realistic clinical-record structures
•	Complex access scenarios
•	Policy evaluation
•	Retrieval experiments
•	Performance analysis
MIMIC-IV is not redistributed with this repository.
Users must obtain authorised access to MIMIC-IV through the official PhysioNet process and place the required files in the configured data directory.
14. Repository Structure
HealthBlockSecure/
|
├── config/
│   ├── base.yaml
│   ├── datasets.yaml
│   ├── crypto.yaml
│   ├── blockchain.yaml
│   └── experiments.yaml
|
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── generated_requests/
|
├── src/
│   ├── datasets/
│   ├── crypto/
│   ├── identity/
│   ├── zkp/
│   ├── privaccessnet/
│   ├── storage/
│   ├── blockchain/
│   ├── workflow/
│   └── utils/
|
├── chaincode/
│   └── healthblocksecure/
|
├── circuits/
|
├── experiments/
│   ├── run_all.py
│   ├── run_privaccessnet.py
│   ├── run_security.py
│   ├── run_latency.py
│   ├── run_throughput.py
│   ├── run_tampering.py
│   ├── run_zkp.py
│   ├── run_ablation.py
│   └── run_baselines.py
|
├── scripts/
│   └── run_demo.py
|
├── tests/
|
├── results/
│   ├── raw/
│   ├── tables/
│   ├── figures/
│   ├── models/
│   └── logs/
|
├── docker-compose.yml
├── requirements.txt
├── requirements-tensorflow.txt
├── pyproject.toml
└── README.md
15. Installation
Prerequisites
Recommended environment:
Python 3.10+
Git
Docker
Docker Compose
Optional components:
TensorFlow
Hyperledger Fabric
Go
Node.js
Circom
snarkjs
MinIO
Clone the repository:
git clone https://github.com/YOUR_USERNAME/HealthBlockSecure.git
cd HealthBlockSecure
Create a virtual environment:
Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
Windows
python -m venv .venv
.venv\Scripts\activate
Install the standard dependencies:
pip install --upgrade pip
pip install -r requirements.txt
For the TensorFlow implementation:
pip install -r requirements-tensorflow.txt
16. Quick Start
Run the standalone end-to-end demonstration:
python scripts/run_demo.py
The demo performs a representative workflow including:
Identity creation
Record encryption
Off-chain storage
Record registration
Access request creation
Authentication
Policy evaluation
PrivAccessNet-style decision processing
Token issuance
Encrypted record retrieval
Decryption
Integrity verification
Audit-event creation
17. Run PrivAccessNet Experiments
Using the lightweight default backend:
python experiments/run_privaccessnet.py --backend sklearn
Using TensorFlow/Keras:
python experiments/run_privaccessnet.py --backend tensorflow
The TensorFlow mode follows the proposed PrivAccessNet neural architecture.
18. Run the Complete Experimental Pipeline
python experiments/run_all.py --backend sklearn
or:
python experiments/run_all.py --backend tensorflow
The full experimental pipeline can execute:
•	Dataset preparation
•	Access-request generation
•	PrivAccessNet training
•	Baseline training
•	Security evaluation
•	Tampering experiments
•	Latency evaluation
•	Throughput testing
•	ZKP-related benchmarking
•	Ablation experiments
•	Reproducibility analysis
•	Result export
19. Reproducibility
The experiments support multiple random seeds.
Default reproducibility seeds:
SEEDS = [42, 123, 256, 512, 1024]
The seeds are used for:
•	Python random generation
•	NumPy
•	Machine-learning initialisation
•	Dataset splitting
•	Synthetic request generation
•	Workload ordering
Where applicable, results should be reported as:
mean ± standard deviation
20. Evaluation Metrics
Machine-Learning Metrics
•	Accuracy
•	Precision
•	Recall
•	F1-score
•	AUROC
•	AUPRC
•	Specificity
•	False Positive Rate
•	False Negative Rate
•	Confusion Matrix
Security Metrics
•	Access-violation prevention rate
•	Tampering detection rate
•	Replay rejection rate
•	Invalid-consent rejection rate
•	Invalid-role rejection rate
•	Audit verification accuracy
Performance Metrics
•	Authentication latency
•	ZKP verification latency
•	Policy-validation latency
•	Model-inference latency
•	Token-generation latency
•	Blockchain-processing latency
•	Retrieval latency
•	Decryption latency
•	End-to-end access latency
•	Throughput
21. Baselines
The implementation supports comparison against conventional access-control and machine-learning approaches.
Access-Control Baselines
RBAC only
RBAC + Consent
Static Attribute-Based Access Control
Blockchain + Deterministic Policy
Blockchain + Learning-Based Validation
Full HealthBlockSecure
Machine-Learning Baselines
Depending on installed dependencies:
Logistic Regression
Decision Tree
Random Forest
Gradient-Boosted Models
MLP
PrivAccessNet
22. Ablation Study
The framework supports component-wise ablation.
Example variants:
Variant	Configuration
Full	Complete HealthBlockSecure
A1	Without PrivAccessNet
A2	Without ZKP-assisted verification
A3	Without audit verification
A4	Without dynamic contextual policy checks
A5	Without DID validation
A6	Without integrity verification
Ablation analysis can compare security effectiveness, decision accuracy, latency, throughput, and auditability.
23. Tamper-Detection Experiment
The repository supports controlled corruption of encrypted or recovered records.
Typical experiments may alter:
Single byte
Small percentage of record
Large percentage of record
Entire record
Integrity is verified using SHA-256 comparison against the registered reference hash.
24. Testing
Run all automated tests:
pytest -q
Tests cover major components such as:
•	Cryptographic operations
•	Encryption/decryption
•	Integrity verification
•	Token behaviour
•	Access-policy logic
•	Workflow execution
•	Tamper detection
25. Docker
Where Docker configuration is available, start the required containerised services with:
docker compose up -d
Check services:
docker compose ps
Stop services:
docker compose down
The Docker environment can be extended to include:
•	Application service
•	MinIO
•	ZKP verification service
•	Blockchain components
•	Supporting APIs
26. Research Mode vs Full Deployment Mode
Standalone Research Mode
Designed for:
•	Immediate execution
•	Unit testing
•	Algorithm validation
•	Access-request experiments
•	ML experiments
•	Security evaluation
•	Reproducibility
It may use lightweight local substitutes for infrastructure-heavy components.
Full Infrastructure Mode
Designed for integration with:
•	Hyperledger Fabric
•	Go chaincode
•	MinIO/AWS S3
•	Circom
•	snarkjs
•	Groth16 proofs
•	External ZKP verification APIs
This separation makes it possible to test the research methodology without requiring an entire blockchain and cryptographic toolchain for every experiment.
27. Important Dataset Note
This repository does not include MIMIC-IV data.
MIMIC-IV is governed by PhysioNet access requirements. Researchers must independently obtain authorised access and comply with the applicable data-use agreement.
The code should be configured to point to the locally available authorised dataset.
28. Security Disclaimer
This repository is a research prototype.
It is intended for:
•	Academic experimentation
•	Reproducibility studies
•	Security research
•	Performance evaluation
•	Blockchain-healthcare research
It has not undergone the certification, penetration testing, regulatory validation, key-management hardening, operational security review, or clinical deployment assessment required for production healthcare systems.
Do not use this research prototype to manage identifiable patient information in a production environment.
29. Reproducing the Main Workflow
A typical execution sequence is:
# Install dependencies
pip install -r requirements.txt

# Test installation
pytest -q

# Run the demonstration
python scripts/run_demo.py

# Run the complete experimental pipeline
python experiments/run_all.py --backend sklearn
For neural experiments:
pip install -r requirements-tensorflow.txt

python experiments/run_all.py --backend tensorflow
30. Expected Outputs
Experimental outputs are stored under:
results/
and may include:
CSV metric files
Raw run logs
Trained model checkpoints
Confusion matrices
Performance summaries
Security results
Ablation results
Latency measurements
Throughput measurements
Statistical summaries
Publication-ready figures
31. Extending the Framework
HealthBlockSecure can be extended in several directions:
•	Real Hyperledger Fabric multi-organisation deployment
•	Production-grade DID frameworks
•	Verifiable Credentials
•	More sophisticated ZKP circuits
•	Attribute-Based Encryption
•	Hardware Security Modules
•	Federated access-risk learning
•	Explainable AI for PrivAccessNet
•	Differential privacy
•	Post-quantum key encapsulation
•	Post-quantum digital signatures
•	FHIR-native interoperability
•	Real-time healthcare IoT integration
•	Multi-hospital scalability evaluation
32. Citation
If you use this repository in academic work, please cite the associated research paper.
@article{healthblocksecure,
  title   = {Decentralised Health Record Management with Blockchain: Privacy and Security in Cloud-Based Systems},
  author  = {Authors},
  journal = {Journal},
  year    = {2026}
}
Please update the bibliographic information after publication.
33. License
Add the licence appropriate for your publication and institutional requirements.
A commonly used option for academic open-source research is:
MIT License
If the code or data are subject to institutional, commercial, or dataset-specific restrictions, use the corresponding licence instead.
34. Repository Status
Research Prototype
Active Development
Experimental Validation
Not for Clinical Deployment
35. Contact
For research questions, reproducibility issues, or collaboration requests, add the corresponding author or project-maintainer contact information here.
Acknowledgement
This implementation was developed as a research prototype for investigating decentralised, privacy-aware, intelligent, and auditable health-record access management using blockchain, cryptographic mechanisms, and learning-based access validation.
