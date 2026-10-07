# QuantumDrugAI

## Quantum–Classical Hybrid Learning Framework for Molecular Property Prediction and Molecule Optimization in Drug Discovery

---

## Overview

**QuantumDrugAI** is a hybrid quantum–classical deep learning framework designed for molecular property prediction and molecule optimization in AI-driven drug discovery applications.

The framework integrates **Graph Neural Networks (GNNs)** with **Variational Quantum Circuits (VQCs)** to improve molecular representation learning, predictive performance, and optimization efficiency.

The system supports molecular graph construction, quantum-enhanced feature learning, explainability analysis, and scalable pharmaceutical AI workflows for computational chemistry and drug discovery research.

---

## Key Features

- Hybrid Quantum–Classical Architecture
- Graph Neural Network-based Molecular Encoding
- Variational Quantum Circuit Integration
- Molecular Graph Construction using RDKit
- Support for QM9, HIV, BBBP, and ZINC datasets
- Training, Evaluation, and Visualization Modules
- Molecule Optimization Pipeline
- Explainability Utilities
- Fully Modular Research-Oriented Codebase

---

## System Architecture

The framework follows a hybrid molecular learning pipeline:

```text
SMILES Input
      │
      ▼
Molecular Graph Construction
      │
      ▼
Graph Neural Network Encoder
      │
      ▼
Dense Projection Layer
      │
      ▼
Variational Quantum Circuit
      │
      ▼
Feature Fusion Layer
      │
      ▼
Property Prediction / Optimization Output
```

---

## Repository Structure

```text
QuantumDrugAI/
│
├── data/
│   ├── download_datasets.py
│   ├── preprocess.py
│   └── molecular_features.py
│
├── models/
│   ├── classical_gnn.py
│   ├── quantum_layer.py
│   ├── hybrid_qc_model.py
│   └── molecule_generator.py
│
├── training/
│   ├── train_property_model.py
│   ├── train_generator.py
│   └── optimize_molecules.py
│
├── evaluation/
│   ├── metrics.py
│   ├── compare_models.py
│   └── visualization.py
│
├── explainability/
│   ├── atom_importance.py
│   └── feature_attribution.py
│
├── results/
│
├── requirements.txt
├── README.md
└── main.py
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sripada-RamaSree/QuantumDrugAI
cd QuantumDrugAI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For **Windows**:

```bash
venv\Scripts\activate
```

For **Linux/macOS**:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Dataset Preparation

QuantumDrugAI supports the following datasets:

| Dataset | Application |
|---|---|
| **QM9** | Molecular property regression |
| **HIV** | Molecular activity classification |
| **BBBP** | Blood-brain barrier penetration prediction |
| **ZINC** | Molecule optimization and generation |

Run preprocessing using:

```bash
python data/preprocess.py
```

---

## Training

### Train Classical GNN Model

```bash
python training/train_property_model.py --model classical
```

### Train Hybrid Quantum–Classical Model

```bash
python training/train_property_model.py --model hybrid
```

### Molecule Optimization

```bash
python training/optimize_molecules.py
```

---

## Evaluation

Run evaluation and visualization using:

```bash
python evaluation/visualization.py
```

---

## Evaluation Metrics

### Regression Tasks

The following metrics are used for molecular property regression:

- MAE
- RMSE
- R² Score

### Classification Tasks

The following metrics are used for molecular activity classification:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

### Molecule Optimization

The molecule optimization pipeline evaluates:

- QED
- logP
- Validity
- Novelty
- Uniqueness

---

## Explainability

QuantumDrugAI supports explainability and interpretability analysis for molecular predictions.

The supported explainability features include:

- Atom Importance Analysis
- Feature Attribution
- Molecular Embedding Visualization
- Attention-Based Interpretability

These techniques help identify important atoms, molecular features, and learned representations that contribute to model predictions.

---

## Results Output

Generated outputs are stored in:

```text
results/
```

The output directory may contain:

- Trained models
- Evaluation reports
- Loss curves
- ROC curves
- Optimized molecules
- Embedding visualizations

---

## Example Output

An example model-training output is shown below:

```text
Epoch 20/50
Training Loss: 0.0214
Validation Accuracy: 94.82%
ROC-AUC: 0.963
```

---

## Reproducibility

To reproduce the complete experimental workflow, run:

```bash
python main.py
```

---

## Future Enhancements

Future extensions of QuantumDrugAI may include:

- Real quantum hardware execution
- Transformer-based molecular encoders
- Diffusion-based molecule generation
- Multi-objective molecular optimization
- Federated quantum molecular learning

---

## Citation

If you use **QuantumDrugAI** in academic research, please cite:

```bibtex
@article{QuantumDrugAI2026,
  title={QuantumDrugAI: Quantum–Classical Hybrid Learning Framework for Molecular Property Prediction and Molecule Optimization in Drug Discovery},
  year={2026}
}
```

---

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

## Research Areas

QuantumDrugAI is designed to support research in:

- Quantum Machine Learning
- Artificial Intelligence for Drug Discovery
- Computational Chemistry
- Molecular Property Prediction
- Molecular Optimization
- Molecular Generation
- Graph Neural Networks
- Variational Quantum Circuits
- Explainable Artificial Intelligence
- Hybrid Quantum–Classical Learning

---

## Project Status

**Research Prototype**

The framework is intended for research, experimentation, and development in quantum-enhanced molecular machine learning and AI-driven drug discovery.

---

## Acknowledgement

QuantumDrugAI was developed as a research-oriented framework for investigating the integration of **Graph Neural Networks**, **Variational Quantum Circuits**, molecular representation learning, and molecule optimization for computational drug discovery.
