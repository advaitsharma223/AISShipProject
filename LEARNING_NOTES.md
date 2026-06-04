# Learning Notes: AIS Ship Prediction

## Table of Contents
1. [What is AIS?](#what-is-ais)
2. [The Problem We're Solving](#the-problem)
3. [Key Concepts](#key-concepts)
4. [Dataset Overview](#dataset-overview)
5. [Why This Project Matters](#why-this-matters)

---

## What is AIS?

### Simple Definition
AIS (Automatic Identification System) is a tracking system used by ships at sea. Think of it like a "transponder" that ships broadcast to say: "I'm here, this is who I am, here's what I'm doing."

### How It Works (Simple)
1. **Every ship has a transponder** that broadcasts data automatically
2. **Ground/satellite receivers** pick up these signals
3. **Data includes:** position, speed, direction, ship characteristics
4. **It's constantly updating** - multiple readings per ship

### Real-World Use Cases
- **Maritime Safety:** Know where ships are to prevent collisions
- **Port Operations:** Manage incoming/outgoing traffic
- **Insurance:** Understand ship behavior and routes
- **Environmental:** Monitor illegal fishing, pollution
- **Intelligence:** Track shipping patterns globally

### Key AIS Fields in Our Dataset
| Field | Meaning | Example |
|-------|---------|---------|
| **MMSI** | Unique ship identifier | 219019621 |
| **Navigational Status** | What the ship is doing | "At anchor", "Underway", "Moored" |
| **SOG** | Speed Over Ground (knots) | 5.2 |
| **COG** | Course Over Ground (degrees) | 45.0 |
| **Heading** | Direction ship is pointing | 48.0 |
| **Ship Type** | Category of ship | "Cargo", "Fishing", "Passenger" |
| **Width** | Ship width in meters | 23.0 |
| **Length** | Ship length in meters | 149.0 |
| **Draught** | How deep ship sits in water | 6.3 |

---

## The Problem We're Solving

### The Challenge
**Given AIS data about a ship, can we predict what TYPE of ship it is?**

This is a **classification problem** - we have multiple possible categories (Cargo, Fishing, Passenger, etc.) and we need to predict which one.

### Why This Is Hard
1. **Missing Data:** Some ships don't report all information
2. **Imbalanced Classes:** More cargo ships than military ships (real-world distribution)
3. **Overlapping Characteristics:** Different ship types may have similar speeds/sizes
4. **Complex Relationships:** Features might interact in non-obvious ways

### Why This Matters
- **Automatic monitoring:** Systems that can classify ships without manual review
- **Anomaly detection:** Identify ships behaving unusually
- **Maritime intelligence:** Understand global shipping patterns

---

## Key Concepts

### 1. Classification (Not Regression)
**Regression:** Predict a number (e.g., "this ship's speed is 5.2 knots")
**Classification:** Predict a category (e.g., "this ship is Cargo")

Our problem is **classification** because ship type is a category, not a number.

### 2. Features vs Target
- **Features (X):** The inputs we use to make predictions
  - In our case: SOG, COG, heading, width, length, draught, navigationalstatus
- **Target (y):** What we're trying to predict
  - In our case: ship_type

### 3. Training vs Testing
- **Training Data:** Historical data we learn from (e.g., 70% of data)
- **Test Data:** New data we evaluate on (e.g., 30% of data)
- **Why separate?** To measure how well the model works on unseen data

### 4. Data Quality Issues

#### Missing Data (NaN/Null)
```
Problem: Some ships don't report all information
Example: Many ships don't report "draught" (we saw empty cells)
Solution: 
  - Remove that row (if too many nulls)
  - Fill with average (if just a few)
  - Mark as "unknown" (if it's a category)
```

#### Imbalanced Data
```
Problem: Not all ship types equally represented
Example: 50,000 Cargo ships but only 500 Military ships
Impact: Model might always guess "Cargo"
Solution: Weighted loss, resampling, or different metrics
```

#### Outliers
```
Problem: Unusual extreme values
Example: Ship with width=1000m (probably data entry error)
Solution: Remove or cap values at reasonable ranges
```

---

## Dataset Overview

### What We Have
- **358,352 records** of ship observations
- **9 columns** of information
- **Multiple ship types** (categorical target)
- **Mix of numerical and categorical features**
- **Missing values** in several columns

### Key Questions About Our Data
1. **How many ship types exist?** (How many categories?)
2. **Which types are common?** (Data distribution)
3. **How much data is missing?** (Data quality)
4. **What do typical values look like?** (Min/max/mean)
5. **Do features relate to ship type?** (Predictability)

---

## Why This Project Matters

### For Learning
✅ **Real ML Pipeline:** Covers full cycle - data → model → evaluation → deployment
✅ **Production Skills:** Not just Jupyter notebooks - actually serves predictions via API
✅ **Multiple Technologies:** Python, pandas, scikit-learn, FastAPI
✅ **Explainability:** Understanding WHY the model makes predictions

### For Interviews
You'll be able to discuss:
- **Data exploration:** "Here's how I analyzed 358K records"
- **Data cleaning:** "Here's my strategy for handling missing values"
- **Feature engineering:** "These features matter because..."
- **Model selection:** "I compared 5 algorithms and chose X because..."
- **Deployment:** "Here's how I productionized the model"

### For Career
- **Demonstrates full-stack capability:** Not just ML theory, but end-to-end systems
- **Real-world problem:** Maritime/logistics is actual industry use case
- **Shows reasoning:** Ability to explain EVERY decision
- **Portfolio value:** Shows you think like an engineer, not just a data scientist

---

## Technical Stack We'll Use

### Phase 1-5: Analysis & ML
- **pandas:** Data manipulation (think of it as Excel on steroids)
- **numpy:** Numerical computations
- **matplotlib/seaborn:** Data visualization
- **scikit-learn:** Machine learning algorithms
- **jupyter:** Interactive notebooks for exploration

### Phase 6: Deployment
- **FastAPI:** Modern Python web framework (like Flask but faster)
- **Pydantic:** Data validation for API inputs
- **Python pickle:** Save/load trained models

---

## Key Principles For This Project

### 1. Understand Before Code
Before writing any code, understand:
- What problem are we solving?
- What data do we have?
- What approach makes sense?

### 2. Document Everything
- Explain your reasoning
- Document decisions
- Write clear comments
- Create visualizations

### 3. Think in Layers
- **Data layer:** Get clean, valid data
- **Feature layer:** Create meaningful signals
- **Model layer:** Train on features to predict target
- **API layer:** Serve predictions to users

### 4. Always Measure
- Define success metrics BEFORE building
- Measure on unseen test data
- Compare approaches objectively
- Explain trade-offs

---

## What You'll Learn By Phase

### Phase 1: Dataset Exploration
✓ How to profile a dataset
✓ Understanding data distributions
✓ Identifying data quality issues
✓ Visualizing data characteristics

### Phase 2: Data Cleaning
✓ Handling missing data strategies
✓ Outlier detection and treatment
✓ Data validation techniques
✓ Creating cleaned data pipelines

### Phase 3: Feature Engineering
✓ Creating derived features
✓ Understanding feature relationships
✓ Normalization vs scaling
✓ Feature selection methods

### Phase 4: Modeling
✓ Classification algorithms (Logistic Regression, Random Forest, SVM, etc.)
✓ Train/test splitting
✓ Cross-validation
✓ Hyperparameter tuning

### Phase 5: Evaluation
✓ Classification metrics (Precision, Recall, F1, AUC)
✓ Confusion matrices
✓ Per-class analysis
✓ Model explainability (SHAP)

### Phase 6: Deployment
✓ API design principles
✓ Input validation
✓ Model serving
✓ Error handling

---

## Phase 3: Feature Engineering Notes

### Simple Definition
Feature engineering means creating better input columns for a machine learning model.

Raw data tells us facts:
- `length`: how long the ship is
- `width`: how wide the ship is
- `sog`: how fast it is moving

Engineered features turn those facts into stronger signals:
- `length_width_ratio`: what shape the ship has
- `ship_footprint_area`: how much physical space it takes
- `speed_category`: what movement mode it is likely in

### Why Feature Engineering Matters
A model does not understand maritime domain knowledge by default. It only sees numbers.

Feature engineering is how we inject useful human understanding into the dataset.

Example:

```
length = 150
width = 25

The model sees two numbers.

length_width_ratio = 6.0

Now the model also sees: this ship is long and narrow.
That pattern is common in cargo/tanker-style ships.
```

### Phase 3 Data Flow

```
Phase 2 cleaned data
        |
        v
Validate required columns
        |
        v
Create navigation, size, shape, speed, draft, and angle features
        |
        v
Drop raw text navigational status
        |
        v
Save model-ready featured data
```

### Features We Created

| Feature | Type | Meaning | Why it helps |
|---|---|---|---|
| `nav_status_*` | One-hot categorical flags | What the ship is doing | Fishing, moored, sailing, and cargo vessels behave differently |
| `ship_size_category` | Ordinal category | Small, medium, large, very large | Ship type is strongly related to size |
| `length_width_ratio` | Continuous number | Long/narrow vs short/wide shape | Cargo and tanker ships often have different shapes from tugs or fishing vessels |
| `ship_footprint_area` | Continuous number | Length times width | Captures overall physical scale |
| `speed_category` | Ordinal category | Stationary, slow, normal, fast | Speed behavior differs by ship type |
| `depth_length_ratio` | Continuous number | Draft relative to length | Normalizes draft so small and large ships can be compared |
| `course_heading_delta` | Continuous number | Difference between movement direction and pointing direction | Large differences can reveal drifting, turning, or special maneuvers |

### One-Hot Encoding

Simple explanation:
One-hot encoding turns a text category into yes/no columns.

Example:

```
navigationalstatus = "Moored"

nav_status_moored = 1
nav_status_at_anchor = 0
nav_status_under_way_engine = 0
```

Why we chose it:
- Machine learning models need numbers, not text.
- One-hot encoding avoids fake ranking.
- It keeps the data easy to inspect in a CSV.

Alternative we avoided:

```
Moored = 3
At anchor = 7
```

That looks compact, but it can accidentally tell some models that "At anchor" is mathematically larger than "Moored". That ordering is not real.

### Course vs Heading

Simple explanation:
- `heading`: where the ship is pointing
- `cog`: where the ship is actually moving

Usually these are close. If they differ a lot, the ship may be drifting, turning, or maneuvering.

Important detail:
Angles wrap around. `359` degrees and `1` degree are only `2` degrees apart, not `358`.

That is why the code uses a circular angle formula:

```python
abs((cog - heading + 180) % 360 - 180)
```

### Understanding Check

Try answering these before moving to Phase 4:
1. Why is `length_width_ratio` more informative than length alone?
2. Why is one-hot encoding safer than assigning numbers like 0, 1, 2 to navigation status?
3. What does it mean if `course_heading_delta` is very large?
