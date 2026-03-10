# Coord-ML: Hybrid Physics-Informed Machine Learning for Crystal Coordination

A professional hybrid pipeline for analyzing and classifying coordination environments in inorganic crystals. **Coord-ML** bridges the gap between traditional crystallography and modern AI by integrating **softBV** physics-based extraction with **Neural Network** 3D geometry classification.

## The Hybrid Pipeline

Unlike "black-box" AI models, Coord-ML uses a domain-specific three-stage process:
1.  **Physics-Based Extraction**: Utilizes `softBV` (Bond Valence Sum theory) to accurately identify bonded neighbors and coordination numbers (CN) from CIF files.
2.  **Geometric Feature Engineering**: Transforms raw 3D coordinates into a unique symmetry fingerprint using **Plane Normal Dot Products**. This captures the underlying symmetry while remaining robust to bond-length distortions.
3.  **Neural Network Classification**: Employs a trained **Multi-layer Perceptron (MLP)** to recognize 3D geometries (e.g., T-4, SP-4, SS-4) from the geometric fingerprints.

## Key Features

- **Automated softBV Wrapper**: Seamlessly extract coordination data from bulk crystallographic datasets.
- **Symmetry Fingerprinting**: High-dimensional geometric descriptors that outperform simple bond-angle metrics.
- **Pre-trained Classifiers**: Specialized models for 4-coordinate environments, with infrastructure to extend to higher coordination numbers.
- **Benchmarking Integration**: Built on the foundational logic of the `MaterialsCoord` benchmarking suite.

## Scientific Acknowledgments

This toolkit is built upon several foundational works in the field:
- **softBV**: Physics-based neighbor extraction utilizes the `softBV` software suite. [http://www.softbv.com/](http://www.softbv.com/)
- **MaterialsCoord**: Core benchmarking infrastructure is based on the *MaterialsCoord* project (*Waroquiers et al., Inorganic Chemistry, 2021*).
- **Prof. Stefan Adams**: Special thanks for guidance and support in the development of these methodologies.

## Installation

### Prerequisites
- Python 3.8+
- [softBV executables](http://www.softbv.com/) (required for the extraction stage)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Roy027/Coord-ML.git
   cd Coord-ML
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

## Quick Start

```python
from coord_ml.extraction.softbv import SoftBVExtractor
from coord_ml.geometry import coordinates_to_planes, planes_to_dot_products
from coord_ml.ml import CoordinationClassifier

# 1. Extract coordination using softBV
extractor = SoftBVExtractor(bin_dir="data/bin")
site_data = extractor.extract_site_dic("my_crystal.cif", sites={"Li1": {"type": "Li", "os": "1"}})

# 2. Generate Geometric Fingerprint
coords = site_data["Li1"]["coordinates"]
planes = coordinates_to_planes(coords)
fingerprint = planes_to_dot_products(planes)

# 3. Classify 3D Geometry
clf = CoordinationClassifier()
# clf.train(X_train, y_labels) # Train or load a model
prediction, confidence = clf.predict([fingerprint])
print(f"Detected Geometry: {prediction[0]}")
```

## Acknowledging this toolkit

If you use this toolkit in your research, please link to this GitHub repository.

---
*Developed by Roy Dai, Oh CH, and Prof. Stefan Adams. This project is intended for research and educational purposes in the field of computational materials science.*
