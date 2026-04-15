# 🚀 AI-Powered Astrophysical Image Analysis System

## 📌 Overview

This project is an end-to-end **AI + Scientific Computing pipeline** that transforms raw astronomical images into **quantitative metrics and scientifically grounded interpretations**.

Unlike traditional image processing or black-box AI models, this system follows a **hybrid architecture**:


Image → Feature Extraction → Scientific Metrics → AI Interpretation


This ensures that interpretations are **data-driven, explainable, and scientifically constrained**, reducing hallucinations.

---

## 🎯 Objective

To build a system capable of:

- Extracting **meaningful scientific information** from space imagery
- Performing **quantitative and morphological analysis**
- Detecting **astronomical patterns (stars, clusters, emission regions)**
- Generating **AI-based scientific explanations** grounded in computed data

---

## 🧠 Core Architecture


User Query
↓
Data Fetching (NASA / Dataset)
↓
Image Processing Pipeline
↓
Feature Extraction
↓
Scientific Metric Computation
↓
Morphological & Spatial Analysis
↓
Segmentation & Energy Mapping
↓
AI Labelling Engine (Ollama + Phi)
↓
Final Scientific Output


---

## 🔬 System Components

### 1. Image Processing & Feature Extraction
- Brightness analysis (mean, std, min, max)
- Color distribution (RGB channels)
- Image embeddings
- Heatmap generation
- Segmentation masks

---

### 2. Quantitative Metrics Engine
- Mean intensity
- Variance & standard deviation
- Entropy (information content)
- Signal-to-noise ratio
- Contrast index

📌 Purpose: Converts image data into **measurable scientific signals**

---

### 3. Morphological Analysis
- Edge density
- Contour count
- Average contour complexity
- Symmetry score

📌 Purpose: Understands **structural geometry of celestial objects**

---

### 4. Space-Specific Metrics (Domain Intelligence)
- Star count
- Star density
- Cluster detection

📌 Purpose: Enables **astronomy-aware analysis**, not generic CV

---

### 5. Segmentation & Energy Analysis
- Emission percentage
- Dark region percentage
- Core region detection
- Core luminosity ratio
- Turbulence index

📌 Purpose: Detects **energy distribution and astrophysical activity**

---

### 6. AI Labelling Engine (Ollama + Phi)

- Locally deployed LLM using Ollama
- Converts computed metrics → scientific explanation
- Strict prompt constraints to prevent hallucination
- JSON-based structured output

📌 Key Innovation:
> AI reasoning is grounded in computed metrics, not raw images

---

## 🔥 Key Features

- ✅ Fully automated end-to-end pipeline
- ✅ Hybrid AI + scientific computation system
- ✅ Reduced hallucination via metric grounding
- ✅ Domain-specific (astronomy-focused) analysis
- ✅ Modular and extensible architecture
- ✅ Local LLM deployment (no API dependency)

---

## ⚙️ Tech Stack

- Python
- OpenCV (Image Processing)
- NumPy / SciPy (Numerical Computation)
- Matplotlib (Visualization)
- Ollama (Local LLM Runtime)
- Phi Model (Lightweight LLM)

---

## 🚀 How to Run

### 1. Activate Virtual Environment
```bash
venv\Scripts\activate
2. Run Full System
python -m Domain_1_Astronomy.full_test
🧪 Sample Output
{
  "mode": "dynamic",
  "query": "Globular Cluster Messier 2",
  "analysis": {
    "quantitative_metrics": {...},
    "morphological_metrics": {...},
    "space_metrics": {...},
    "segmentation_metrics": {...},
    "ai_interpretation": {
      "scientific_summary": "Detailed astrophysical interpretation..."
    }
  }
}
