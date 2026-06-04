# Tech Stack Documentation

## Overview

This document explains every technology we'll use, why we chose it, and what alternatives exist.

---

## Data Analysis & Exploration (Phases 1-5)

### 1. Python 3.11+

**What it is:** Programming language for data science

**Why we chose it:**
- Industry standard for ML/data science
- Massive ecosystem (pandas, scikit-learn, etc.)
- Clear syntax, great for learning
- Easy to transition to production (Phase 6)

**Alternatives:**
- R: Great for statistics, but less used in industry MLOps
- Julia: Fast numerical computing, but smaller ecosystem
- C++: Faster, but overkill and harder to learn

**How we use it:** 
Base language for all analysis and modeling.

---

### 2. Pandas

**What it is:** 
Data manipulation library - think "Excel as Python library"

**Why we chose it:**
- **Dataframes:** Table-like structure with labeled rows/columns
- **Operations:** Filter, group, aggregate, transform data easily
- **Integration:** Works seamlessly with numpy, scikit-learn
- **Industry standard:** Used everywhere in data science

**Key concepts you'll use:**
```python
df.head()              # See first rows
df.describe()          # Statistical summary
df.isnull().sum()      # Count missing values
df['column'].value_counts()  # Count categories
df[df['age'] > 30]     # Filter rows
df.groupby('type').mean()    # Group and aggregate
```

**Alternatives:**
- Polars: Faster, but smaller community (newer)
- DuckDB: Great for SQL-like queries, but different API
- NumPy only: Too low-level, would reinvent wheels

**How we use it:**
Load data, explore distributions, clean columns, engineer features.

---

### 3. NumPy

**What it is:** 
Numerical computing library - foundation for all Python data science

**Why we chose it:**
- **Arrays:** Fast numerical arrays (faster than Python lists)
- **Operations:** Vectorized math (apply operations to whole arrays at once)
- **Dependency:** Pandas and scikit-learn both use NumPy under the hood
- **Efficiency:** C code underneath means fast computation

**Key concepts:**
- Arrays vs lists: Arrays are faster for numerical work
- Vectorization: Do math on entire arrays without loops
- Broadcasting: Apply operations across different shaped arrays

**How we use it:**
Mostly indirectly through pandas and scikit-learn, but we'll use it for numerical transformations.

---

### 4. Matplotlib & Seaborn

**What they are:**
Visualization libraries for creating charts and plots

**Matplotlib:** Low-level, fine-grained control
**Seaborn:** High-level built on matplotlib, prettier defaults

**Why we chose them:**
- **Standard:** Most common in data science
- **Flexible:** Can create almost any chart
- **Integration:** Works with pandas DataFrames directly
- **Static images:** Good for reports and documentation

**What we'll create:**
- Histograms: See distributions of features
- Box plots: Find outliers
- Scatter plots: See relationships between features
- Heatmaps: Correlation matrices
- Count plots: Visualize categories

**Alternative:**
- Plotly: Interactive, prettier, but heavier
- Altair: Declarative, but less common
- ggplot2 (R): Not available in Python

**How we use it:**
Explore data patterns, create visualizations for documentation.

---

### 5. Scikit-learn

**What it is:** 
Machine learning library - the "one-stop shop" for ML algorithms

**Why we chose it:**
- **Comprehensive:** 50+ algorithms for classification, clustering, regression
- **Consistent API:** All models follow same interface (fit, predict)
- **Built-in tools:** Cross-validation, hyperparameter tuning, metrics
- **Well-documented:** Huge community, countless tutorials
- **Industry standard:** Used in production everywhere

**Models we'll try:**
- Logistic Regression: Fast baseline
- Random Forest: Ensemble, handles features well
- SVM: Works for classification
- Gradient Boosting: Often the best performance
- Neural Networks: If time permits

**Tools we'll use:**
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
```

**Alternatives:**
- XGBoost: Better gradient boosting, but specialized
- TensorFlow/PyTorch: For deep learning, overkill for tabular data
- LightGBM: Faster than XGBoost, but less common

**How we use it:**
Train models, evaluate performance, compare algorithms.

---

### 6. Jupyter Notebook

**What it is:**
Interactive environment - code, text, and visualizations in one document

**Why we chose it:**
- **Interactivity:** Run code cell-by-cell, see results immediately
- **Documentation:** Mix code with explanations and markdown
- **Exploration:** Perfect for trying things and learning
- **Reproducibility:** Clear record of what you did
- **Visualization:** Charts and outputs displayed inline

**How it works:**
- Create cells with code or markdown
- Run cells independently (Shift+Enter)
- Variables persist between cells
- Create a narrative of your analysis

**When to use:**
- Phases 1-5: Perfect for exploration
- Phase 6: Will refactor to Python scripts for API

**Alternatives:**
- Python scripts: Less interactive, harder to explore
- RMarkdown: For R language
- Google Colab: Cloud-hosted notebooks

**How we use it:**
Create 5 notebooks - one per exploration/analysis phase.

---

## Machine Learning Specific Tools

### 7. Pickle (or Joblib)

**What it is:**
Serialization format - save Python objects to disk

**Why we chose it:**
- **Simple:** One line to save, one line to load
- **Compatible:** Works with any scikit-learn model
- **Standard:** Industry standard for model storage
- **Files:** Create .pkl files that contain trained models

**Code:**
```python
# Save
import pickle
pickle.dump(model, open('model.pkl', 'wb'))

# Load
model = pickle.load(open('model.pkl', 'rb'))
```

**When it's used:**
- Phase 4: Save trained model
- Phase 6: Load model in FastAPI

**Alternatives:**
- MLflow: Track experiments, more complex setup
- ONNX: Industry standard, but more complex
- Cloud storage: If using cloud ML services

**How we use it:**
Save trained model after Phase 4, load it in Phase 6 API.

---

## Production & Deployment (Phase 6)

### 8. FastAPI

**What it is:**
Modern web framework - build REST APIs in Python

**Why we chose it:**
- **Fast:** Actually fast (hence the name), competitive with Go/Node
- **Easy:** Minimal code to get started
- **Type hints:** Uses Python type hints for validation
- **Auto docs:** Automatically generates interactive documentation
- **Async:** Handle multiple requests efficiently

**Core concepts:**
- **Endpoint:** URL path where requests can be sent
- **Route:** Define what happens at each endpoint
- **Request body:** Data sent to the API
- **Response:** Data returned from the API

**Example:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict")
def predict(ship_data: ShipInput):
    prediction = model.predict(ship_data)
    return {"ship_type": prediction}
```

**Alternatives:**
- Flask: Simpler, but less features, slower
- Django: Heavyweight, better for full web apps
- Starlette: Lower-level, more control
- Node.js/Express: Different language, not Python

**How we use it:**
Build API server in Phase 6.

---

### 9. Pydantic

**What it is:**
Data validation library - ensure data is correct shape/type

**Why we chose it:**
- **Automatic:** Define once, validates everywhere
- **FastAPI integration:** Works perfectly with FastAPI
- **Type safe:** Uses Python type hints
- **Clear errors:** Tells you exactly what's wrong with input

**Example:**
```python
from pydantic import BaseModel, Field

class ShipInput(BaseModel):
    sog: float = Field(..., ge=0, le=50)
    heading: float = Field(..., ge=0, le=360)
    width: float = Field(..., gt=0)
    
    # FastAPI will validate these automatically
```

**When it's used:**
Phase 6 - validate API inputs before predictions.

**Alternatives:**
- Manual validation: Tedious and error-prone
- Marshmallow: Flask-specific, more boilerplate

**How we use it:**
Define input/output schemas for FastAPI endpoints.

---

## Development Tools

### 10. Git & GitHub

**What they are:**
Version control - track changes to code

**Why we use it:**
- **History:** See what changed and when
- **Collaboration:** Work with others
- **Backup:** Code is backed up
- **Portfolio:** Show your work to employers

**How we use it:**
- Track all project files
- Create clean commit history
- Document changes with good messages

---

## Summary Table

| Phase | Tool | Purpose | Key Why |
|-------|------|---------|---------|
| 1-5 | Pandas | Data manipulation | Industry standard for DataFrames |
| 1-5 | NumPy | Numerical computing | Fast array operations |
| 1-5 | Matplotlib/Seaborn | Visualization | Standard for static plots |
| 1-5 | Scikit-learn | Machine learning | Comprehensive, consistent API |
| 1-5 | Jupyter | Interactive analysis | Exploration and learning |
| 4 | Pickle | Model serialization | Simple, standard format |
| 6 | FastAPI | REST API | Modern, fast, well-integrated |
| 6 | Pydantic | Data validation | Works perfectly with FastAPI |
| All | Git | Version control | Standard practice |

---

## Why This Stack?

### Three guiding principles:

1. **Industry standard:** These are what real data scientists use
2. **Learning progression:** Start with exploration tools, graduate to production tools
3. **Integration:** Tools work well together, not a hodgepodge

### What we're NOT using:

- **Keras/TensorFlow:** For deep learning - tabular data works better with classical ML
- **Apache Spark:** For big data processing - our dataset fits in memory
- **Docker:** For containerization - would be Phase 6 enhancement, not core
- **Kubernetes:** For orchestration - overkill for this project scope

These are great technologies, but not needed for this project scope. Learning to choose the right tool is important!

---

## Installation & Setup

This will be covered in Phase 1 actual work, but you'll need:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter fastapi pydantic uvicorn
```

That's it! Small, focused toolset.

---

## Phase 3 Feature Engineering Tools

### Pandas `get_dummies`

**What it is:**
A pandas function that turns categorical values into one-hot encoded columns.

**Why we used it:**
- The dataset is already loaded as a pandas DataFrame.
- Navigational status has a small number of categories.
- It produces plain numeric columns that are easy to inspect in `featured_data.csv`.

**Alternatives:**
- scikit-learn `OneHotEncoder`: better inside a full ML pipeline, especially for production training
- Ordinal encoding: simpler but creates fake category order
- Target encoding: useful for high-cardinality categories, but can leak target information if done incorrectly

**Why this choice fits now:**
For Phase 3, we want a model-ready CSV and a beginner-friendly feature table. In Phase 4, we can still move encoding into a scikit-learn pipeline if we want stricter production architecture.

---

### NumPy for Circular Angle Math

**What it is:**
NumPy provides fast numerical operations across entire columns.

**Why we used it:**
The `course_heading_delta` feature needs circular math because angles wrap around at 360 degrees. NumPy lets us compute that efficiently for all 332,068 records.

**Formula used:**

```python
abs((cog - heading + 180) % 360 - 180)
```

**Alternatives:**
- Plain Python loops: easier to read at first, but slower and less idiomatic for pandas data
- Trigonometric sine/cosine features: useful for advanced directional modeling, but less intuitive for this phase

**Why this choice fits now:**
The formula is compact, explainable, and produces a single interpretable feature between 0 and 180 degrees.
