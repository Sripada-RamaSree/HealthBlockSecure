# HealthBlockSecure

## Decentralised Health Record Management with Blockchain, Privacy-Preserving Authentication, and Intelligent Access Control

HealthBlockSecure is a research-oriented framework for secure, decentralised, privacy-aware, and auditable **Electronic Health Record (EHR)** management.

The framework combines blockchain-based access control, encrypted off-chain storage, decentralised identity, Zero-Knowledge Proof (ZKP)-assisted authentication, smart-contract policy enforcement, and **PrivAccessNet** for contextual access validation and anomaly detection.

### Key Capabilities

- Permissioned blockchain-based access control
- Encrypted off-chain EHR storage
- AES-based health-record encryption
- ECC/ECDH-based session-key protection
- SHA-256 integrity verification
- Decentralised Identity (DID)
- ZKP-assisted authentication
- Smart-contract-style policy enforcement
- Patient consent validation
- Role- and context-aware access control
- PrivAccessNet neural access validation
- Short-lived access-token generation
- Replay and anomaly detection
- Immutable audit logging
- Security and tampering evaluation
- Latency and throughput benchmarking
- Baseline comparison
- Component-wise ablation studies
- Multi-seed reproducibility

---

## System Overview

Conventional cloud-based EHR systems depend heavily on centralised trust and may provide limited transparency, auditability, and adaptability in access-control decisions.

HealthBlockSecure uses a hybrid blockchain-cloud architecture in which:

1. Health records are encrypted before storage.
2. Encrypted records are stored off-chain.
3. Integrity hashes, policies, metadata, and audit information are maintained by the access-control infrastructure.
4. Requesters are represented using decentralised identifiers.
5. ZKP-assisted authentication verifies eligibility while reducing disclosure of sensitive attributes.
6. PrivAccessNet evaluates contextual access behaviour.
7. Deterministic policy rules and the learned access-compliance score jointly support the final access decision.
8. Approved users receive time-limited access credentials.
9. Retrieved records are decrypted locally and verified against the registered SHA-256 hash.
10. Security-relevant events are recorded in an auditable ledger.

---

## Main Contributions

HealthBlockSecure integrates:

- Hybrid blockchain and off-chain EHR storage
- AES-based health-record encryption
- ECC/ECDH protection of symmetric keys
- SHA-256 integrity verification
- DID-based identity representation
- External ZKP verification workflow
- Smart-contract-style access-policy management
- Patient consent validation
- Role- and context-aware access control
- PrivAccessNet neural access-validation model
- Access-token generation and expiration
- Replay and anomaly simulation
- Append-only audit logging
- Synthetic access-request generation
- Machine-learning baselines
- Security and tampering experiments
- Latency and throughput benchmarking
- Component-wise ablation experiments
- Multi-seed reproducibility

---

## System Architecture

### User Layer

The user layer represents:

- Patients
- Doctors
- Nurses
- Researchers
- Healthcare organisations
- Authorised third parties

Each participant can be associated with a decentralised identifier and cryptographic credentials.

### Blockchain and Access-Control Layer

Responsible for:

- Record metadata registration
- Access-policy management
- Consent verification
- DID validation
- ZKP verification result processing
- PrivAccessNet decision support
- Token issuance
- Access approval or denial
- Immutable audit-event registration

### Off-Chain Storage Layer

Encrypted EHR data is stored outside the blockchain ledger.

Only references, hashes, encrypted key material, policies, and relevant metadata are maintained by the access-control infrastructure.

---

## End-to-End Workflow

```text
Patient EHR
    │
    ▼
Schema Harmonisation
    │
    ▼
AES Record Encryption
    │
    ├──────────────► SHA-256 Integrity Hash
    │
    ▼
ECC/ECDH-Based Session-Key Protection
    │
    ▼
Encrypted Off-Chain Storage
    │
    ▼
Metadata Registration
    │
    ▼
Provider Access Request
    │
    ▼
DID Validation
    │
    ▼
ZKP-Assisted Authentication
    │
    ▼
Consent + Role + Policy Validation
    │
    ▼
PrivAccessNet Inference
    │
    ▼
Final Access Decision
    │
    ├── DENY ──────► Audit Event
    │
    ▼
Time-Limited Access Token
    │
    ▼
Encrypted Record Retrieval
    │
    ▼
Local Key Recovery
    │
    ▼
AES Decryption
    │
    ▼
SHA-256 Integrity Verification
    │
    ▼
Audit Logging
```

---

## PrivAccessNet

**PrivAccessNet** is the learning-based access-validation component of HealthBlockSecure.

It evaluates contextual access-request information including:

- Requester role
- Access time
- Request type
- Patient-consent status
- Token validity
- Previous access frequency
- Policy-match status
- Credential validity
- Temporal validity
- Replay indicators
- Frequency anomalies
- Privilege-escalation indicators

### Architecture

```text
Input Features
      │
      ▼
Dense(64)
      │
      ▼
Batch Normalisation
      │
      ▼
ReLU
      │
      ▼
Dropout(0.30)
      │
      ▼
Dense(32)
      │
      ▼
Batch Normalisation
      │
      ▼
ReLU
      │
      ▼
Dropout(0.30)
      │
      ▼
Dense(16)
      │
      ▼
Batch Normalisation
      │
      ▼
ReLU
      │
      ▼
Dense(1)
      │
      ▼
Sigmoid
```

### Training Configuration

| Parameter | Value |
|---|---|
| Optimiser | Adam |
| Learning Rate | 0.001 |
| Batch Size | 32 |
| Maximum Epochs | 50 |
| Loss | Class-weighted Binary Cross-Entropy |
| Hidden Units | 64, 32, 16 |
| Activation | ReLU |
| Dropout | 0.30 |
| Output | Sigmoid |
| Early Stopping | Validation Loss |
| Sampling | Balanced Mini-Batches |

The PrivAccessNet score is used as a **decision-support signal** and does not replace deterministic access-control conditions.

---

## Access Decision Logic

Access is granted only when all required conditions are satisfied:

```text
Grant Access =
    ZKP Verified
    AND DID Valid
    AND Consent Valid
    AND Role Permitted
    AND Access Purpose Permitted
    AND Temporal Policy Valid
    AND Token Conditions Valid
    AND PrivAccessNet Score >= Threshold
```

This combines deterministic policy enforcement with data-driven, anomaly-aware validation.

---

## Security Scenarios

### Legitimate Requests

- Valid provider request
- Valid role
- Active consent
- Valid credential
- Allowed access time
- Valid request purpose

### Adversarial / Invalid Requests

- Role violation
- Consent violation
- Expired credentials
- Expired access token
- Out-of-hours access
- Privilege escalation
- Replay attack
- Excessive request frequency
- Policy mismatch
- Invalid credential
- Record tampering

These scenarios support reproducible access-control dataset generation and PrivAccessNet evaluation.

---

## Cryptographic Components

### AES Record Encryption

Electronic health records are protected using symmetric encryption.

Authenticated AES encryption is used to provide confidentiality and detect ciphertext modification.

### ECC/ECDH Key Protection

The per-record symmetric session key is protected using elliptic-curve key agreement and key derivation.

```text
ECDH
  │
  ▼
Shared Secret
  │
  ▼
HKDF-SHA256
  │
  ▼
Derived Key-Encryption Key
  │
  ▼
Protected AES Session Key
```

### SHA-256 Integrity Verification

SHA-256 generates integrity fingerprints for original health records.

During retrieval:

```text
Stored Reference Hash
        │
        │ compare
        ▼
Hash of Decrypted Record
        │
        ▼
Integrity Valid / Integrity Failure
```

Any mismatch is treated as an integrity failure.

---

## Decentralised Identity

HealthBlockSecure includes a lightweight DID-oriented identity module.

Example identifiers:

```text
did:hbs:patient001
did:hbs:doctor001
did:hbs:researcher001
did:hbs:hospital001
```

The identity layer can associate:

- DID
- Public key
- Role
- Organisation
- Credential status

Private cryptographic keys remain outside the ledger.

---

## Zero-Knowledge Proof Integration

The architecture supports an external ZKP verification service.

```text
Requester
    │
    ▼
Generate Proof
    │
    ▼
External ZKP Verification Service
    │
    ▼
Verification Result
    │
    ▼
HealthBlockSecure Access Layer
```

The proof can demonstrate conditions such as:

```text
credential_valid = true
role_is_permitted = true
consent_eligible = true
credential_not_expired = true
```

without disclosing the underlying sensitive identity attributes.

The repository supports a **Circom/snarkjs-style Groth16 workflow**.

The standalone research mode can use a deterministic verification adapter so that the complete workflow can be executed without requiring a full ZKP proving environment.

---

## Blockchain Integration

HealthBlockSecure contains components for integration with **Hyperledger Fabric**.

The target architecture includes:

- Two healthcare organisations
- Multiple peer nodes
- Certificate Authorities
- Raft ordering service
- Go smart contracts
- LevelDB state storage
- Private-data support
- Audit-event registration

### Smart-Contract Operations

```text
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
```

The standalone research mode can use a lightweight local ledger backend for development and automated testing.

---

## Off-Chain Storage

Encrypted EHRs are stored outside the blockchain ledger.

Supported or extensible storage backends include:

- Local filesystem
- MinIO
- Amazon S3-compatible storage
- IPFS-compatible references

### Typical On-Ledger Metadata

| Metadata | Description |
|---|---|
| `record_id` | Health-record identifier |
| `patient_did` | Patient decentralised identifier |
| `data_category` | Record category |
| `storage_pointer` | Off-chain storage reference |
| `integrity_hash` | SHA-256 integrity value |
| `encrypted_session_key` | Protected session key |
| `policy_id` | Access-policy identifier |
| `timestamp` | Registration/access timestamp |

**Plaintext EHR content is not stored on the ledger.**

---

## Datasets

### SyntheticMass / Synthea

Used for:

- Initial implementation
- Synthetic patient workflows
- Smart-contract testing
- Access-policy simulation
- Encryption experiments
- DID mapping
- Security testing

### MIMIC-IV

Used for:

- Realistic clinical-record structures
- Complex access scenarios
- Policy evaluation
- Retrieval experiments
- Performance analysis

MIMIC-IV is **not included in this repository**. Researchers must obtain authorised access through the official PhysioNet process and configure the code to use the locally available dataset.

---

## Repository Structure

```text
HealthBlockSecure/
│
├── config/
│   ├── base.yaml
│   ├── datasets.yaml
│   ├── crypto.yaml
│   ├── blockchain.yaml
│   └── experiments.yaml
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── generated_requests/
│
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
│
├── chaincode/
│   └── healthblocksecure/
│
├── circuits/
│
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
│
├── scripts/
│   └── run_demo.py
│
├── tests/
│
├── results/
│   ├── raw/
│   ├── tables/
│   ├── figures/
│   ├── models/
│   └── logs/
│
├── docker-compose.yml
├── requirements.txt
├── requirements-tensorflow.txt
├── pyproject.toml
└── README.md
```

---

## Installation

### Prerequisites

Recommended environment:

- Python 3.10+
- Git
- Docker
- Docker Compose

Optional components:

- TensorFlow
- Hyperledger Fabric
- Go
- Node.js
- Circom
- snarkjs
- MinIO

### Clone the Repository

```bash
git clone https://github.com/Sripada-RamaSree/HealthBlockSecure
cd HealthBlockSecure
```

### Create Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

For TensorFlow experiments:

```bash
pip install -r requirements-tensorflow.txt
```

---

## Quick Start

Run the standalone end-to-end demonstration:

```bash
python scripts/run_demo.py
```

The demonstration covers:

1. Identity creation
2. Record encryption
3. Off-chain storage
4. Record registration
5. Access-request creation
6. Authentication
7. Policy evaluation
8. PrivAccessNet-style decision processing
9. Token issuance
10. Encrypted record retrieval
11. Decryption
12. Integrity verification
13. Audit-event creation

---

## PrivAccessNet Experiments

### Scikit-learn Backend

```bash
python experiments/run_privaccessnet.py --backend sklearn
```

### TensorFlow/Keras Backend

```bash
python experiments/run_privaccessnet.py --backend tensorflow
```

The TensorFlow implementation follows the proposed PrivAccessNet neural architecture.

---

## Complete Experimental Pipeline

### Lightweight Backend

```bash
python experiments/run_all.py --backend sklearn
```

### TensorFlow Backend

```bash
python experiments/run_all.py --backend tensorflow
```

The experimental pipeline can execute:

- Dataset preparation
- Access-request generation
- PrivAccessNet training
- Baseline training
- Security evaluation
- Tampering experiments
- Latency evaluation
- Throughput testing
- ZKP-related benchmarking
- Ablation experiments
- Reproducibility analysis
- Result export

---

## Reproducibility

The experiments support multiple random seeds.

Default seeds:

```python
SEEDS = [42, 123, 256, 512, 1024]
```

The seeds are used for:

- Python random generation
- NumPy
- Machine-learning initialisation
- Dataset splitting
- Synthetic request generation
- Workload ordering

Where applicable, experimental results should be reported as:

```text
mean ± standard deviation
```

---

## Evaluation Metrics

### Machine-Learning Metrics

| Metric |
|---|
| Accuracy |
| Precision |
| Recall |
| F1-score |
| AUROC |
| AUPRC |
| Specificity |
| False Positive Rate |
| False Negative Rate |
| Confusion Matrix |

### Security Metrics

| Metric |
|---|
| Access-violation prevention rate |
| Tampering detection rate |
| Replay rejection rate |
| Invalid-consent rejection rate |
| Invalid-role rejection rate |
| Audit verification accuracy |

### Performance Metrics

| Metric |
|---|
| Authentication latency |
| ZKP verification latency |
| Policy-validation latency |
| Model-inference latency |
| Token-generation latency |
| Blockchain-processing latency |
| Retrieval latency |
| Decryption latency |
| End-to-end access latency |
| Throughput |

---

## Baselines

### Access-Control Baselines

- RBAC only
- RBAC + Consent
- Static Attribute-Based Access Control
- Blockchain + Deterministic Policy
- Blockchain + Learning-Based Validation
- Full HealthBlockSecure

### Machine-Learning Baselines

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient-Boosted Models
- MLP
- PrivAccessNet

---

## Ablation Study

The framework supports component-wise ablation.

| Variant | Configuration |
|---|---|
| Full | Complete HealthBlockSecure |
| A1 | Without PrivAccessNet |
| A2 | Without ZKP-assisted verification |
| A3 | Without audit verification |
| A4 | Without dynamic contextual policy checks |
| A5 | Without DID validation |
| A6 | Without integrity verification |

Ablation analysis can compare:

- Security effectiveness
- Decision accuracy
- Latency
- Throughput
- Auditability

---

## Tamper-Detection Experiment

The framework supports controlled corruption of encrypted or recovered records.

Tampering levels can include:

- Single byte modification
- Small percentage of the record
- Large percentage of the record
- Entire record

Integrity is verified by comparing the SHA-256 hash against the registered reference hash.

---

## Testing

Run all automated tests:

```bash
pytest -q
```

Tests cover:

- Cryptographic operations
- Encryption/decryption
- Integrity verification
- Token behaviour
- Access-policy logic
- Workflow execution
- Tamper detection

---

## Docker

Start containerised services:

```bash
docker compose up -d
```

Check services:

```bash
docker compose ps
```

Stop services:

```bash
docker compose down
```

The Docker environment can be extended to include:

- Application service
- MinIO
- ZKP verification service
- Blockchain components
- Supporting APIs

---

## Research Mode vs Full Deployment Mode

### Standalone Research Mode

Designed for:

- Immediate execution
- Unit testing
- Algorithm validation
- Access-request experiments
- Machine-learning experiments
- Security evaluation
- Reproducibility

Lightweight local substitutes may be used for infrastructure-heavy components.

### Full Infrastructure Mode

Designed for integration with:

- Hyperledger Fabric
- Go chaincode
- MinIO / AWS S3
- Circom
- snarkjs
- Groth16 proofs
- External ZKP verification APIs

This separation allows the research methodology to be evaluated without requiring the complete blockchain and cryptographic infrastructure for every experiment.

---

## Important Dataset and Security Notes

### Dataset

This repository does **not** include MIMIC-IV data.

MIMIC-IV is governed by PhysioNet access requirements. Researchers must independently obtain authorised access and comply with the applicable data-use agreement.

Configure the project to point to the authorised dataset available locally.

### Security Disclaimer

HealthBlockSecure is a **research prototype** intended for:

- Academic experimentation
- Reproducibility studies
- Security research
- Performance evaluation
- Blockchain-healthcare research

It has not undergone the certification, penetration testing, regulatory validation, key-management hardening, operational security review, or clinical deployment assessment required for production healthcare systems.

**Do not use this research prototype to manage identifiable patient information in a production environment.**

---

## Reproducing the Main Workflow

### Install dependencies

```bash
pip install -r requirements.txt
```

### Test installation

```bash
pytest -q
```

### Run the demonstration

```bash
python scripts/run_demo.py
```

### Run the complete experimental pipeline

```bash
python experiments/run_all.py --backend sklearn
```

### Run neural experiments

```bash
pip install -r requirements-tensorflow.txt
python experiments/run_all.py --backend tensorflow
```

---

## Expected Outputs

Experimental outputs are stored under:

```text
results/
```

Possible outputs include:

- CSV metric files
- Raw run logs
- Trained model checkpoints
- Confusion matrices
- Performance summaries
- Security results
- Ablation results
- Latency measurements
- Throughput measurements
- Statistical summaries
- Publication-ready figures

---

## Future Extensions

Potential extensions include:

- Real Hyperledger Fabric multi-organisation deployment
- Production-grade DID frameworks
- Verifiable Credentials
- More sophisticated ZKP circuits
- Attribute-Based Encryption
- Hardware Security Modules
- Federated access-risk learning
- Explainable AI for PrivAccessNet
- Differential privacy
- Post-quantum key encapsulation
- Post-quantum digital signatures
- FHIR-native interoperability
- Real-time healthcare IoT integration
- Multi-hospital scalability evaluation

---

## Citation

If you use HealthBlockSecure in academic work, please cite:

```bibtex
@article{healthblocksecure,
  title = {Decentralised Health Record Management with Blockchain: Privacy and Security in Cloud-Based Systems},
  year = {2026}
}
```

> Please update the bibliographic information after publication.

---

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---


---

## Contact

For research questions, reproducibility issues, or collaboration requests, add the corresponding author or project-maintainer contact information here.

---

## Acknowledgement

This implementation was developed as a research prototype for investigating decentralised, privacy-aware, intelligent, and auditable health-record access management using blockchain, cryptographic mechanisms, and learning-based access validation.
