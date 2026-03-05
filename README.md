# Coordination Analysis Toolkit (MaterialsCoord)

A professional toolkit for analyzing, extracting, and classifying coordination environments in crystal structures. This project combines traditional crystallography (softBV) with modern machine learning to identify 3D atomic geometries.

## Features

- **Geometric Feature Extraction**: Compute plane normal dot products and bond angles to fingerprint 3D symmetry.
- **softBV Wrapper**: Automated extraction of coordination numbers and ligand positions from CIF files.
- **Machine Learning Classification**: Pre-trained and customizable neural networks to classify 4-coordinate environments (e.g., Tetrahedral, Square Planar).
- **Benchmarking Framework**: Compare different coordination detection methods (e.g., softBV vs. CrystalNN) against reference data.

## Installation

### Prerequisites
- Python 3.8+
- [softBV executables](http://www.softbv.com/) (required for coordination extraction)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/materialscoord.git
   cd materialscoord
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Quick Start

### 1. Extracting Coordination with softBV
```python
from materialscoord.extraction.softbv import SoftBVExtractor

extractor = SoftBVExtractor(bin_dir="path/to/bin")
site_dic = extractor.extract_site_dic("path/to/crystal.cif", sites={"Fe": {"type": "Fe", "os": "3"}})
```

### 2. Computing Geometric Descriptors
```python
from materialscoord.geometry import coordinates_to_planes, planes_to_dot_products

planes = coordinates_to_planes(site_dic["Fe"]["coordinates"])
dots = planes_to_dot_products(planes)
```

### 3. Classifying Geometry
```python
from materialscoord.ml import CoordinationClassifier

clf = CoordinationClassifier()
# Train with your data or load a pre-trained model
# clf.train(X_train, y_labels)
predictions, probs = clf.predict(new_features)
```

## Project Structure

- `src/materialscoord/`: Main package source code.
  - `core.py`: Benchmarking and core coordination logic.
  - `geometry.py`: 3D symmetry and plane calculations.
  - `ml.py`: Neural network classification models.
  - `extraction/`: Utilities for external tool integration (softBV).
- `data/`: Datasets for training and benchmarking.
- `bin/`: External binaries (softBV).
- `tests/`: Automated test suite (Pytest).

## License

[MIT License](LICENSE)

## Citation

If you use this toolkit in your research, please cite:
*Dai, R. (2021). Coordination Analysis Toolkit.*
