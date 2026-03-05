# Coord-ML (Coordination Geometric Analysis & Machine Learning)

A specialized toolkit for analyzing, extracting, and classifying coordination environments in crystal structures. This project extends standard coordination benchmarks with 3D Geometric Descriptors (Plane Normal Dot Products) and Neural Network-based classification.

## Features

- **Geometric Feature Engineering**: Compute plane normal dot products to fingerprint 3D symmetry.
- **softBV Wrapper**: Automated extraction of coordination numbers from CIF files via `softBV`.
- **Geometry Classification**: Neural networks to classify 4-coordinate environments (T-4, SP-4, etc.).
- **Benchmarking**: Integrated with industry-standard coordination benchmarks.

## Academic Acknowledgments

This toolkit utilizes the benchmarking infrastructure and foundational logic provided by the **MaterialsCoord** project (published in *Inorganic Chemistry*, 2021). Our work extends this by introducing 3D Geometric Descriptors and Machine Learning-based classification.

If you use this toolkit, please cite:
- *Waroquiers, S., et al. (2021). Benchmarking Coordination Number Prediction Algorithms. Inorganic Chemistry.* (For the core benchmarking framework).
- *Dai, R. (2021). Coord-ML: Geometric Descriptors and ML for Coordination Environments.* (For the geometric analysis and classification models).

## Installation

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Roy027/Coord.git
   cd Coord
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

### 1. Extracting Coordination
```python
from coord_ml.extraction.softbv import SoftBVExtractor

extractor = SoftBVExtractor(bin_dir="path/to/bin")
site_dic = extractor.extract_site_dic("path/to/crystal.cif", sites={"Fe": {"type": "Fe", "os": "3"}})
```

### 2. Computing Geometric Descriptors
```python
from coord_ml.geometry import coordinates_to_planes, planes_to_dot_products

planes = coordinates_to_planes(site_dic["Fe"]["coordinates"])
dots = planes_to_dot_products(planes)
```

### 3. Classifying Geometry
```python
from coord_ml.ml import CoordinationClassifier

clf = CoordinationClassifier()
predictions, probs = clf.predict(new_features)
```

## Project Structure

- `src/coord_ml/`: Main package source code.
- `data/training/`: Training datasets for ML models.
- `notebooks/`: Tutorial and demonstration notebooks.
- `legacy/`: Original research scripts and directories.
- `tests/`: Automated unit tests.

## License

Refer to individual file headers for original `MaterialsCoord` copyright. New contributions are provided under the MIT License.
