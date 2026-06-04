# AIS Ship Prediction & Map Visualization - Project Plan

## Project Vision
Build an end-to-end machine learning system that predicts ship types from AIS (Automatic Identification System) tracking data, with interactive visualization and a production-ready FastAPI backend.

**Why this project matters:**
- **Real-world problem:** Accurate ship type classification helps maritime authorities, insurance companies, and logistics optimize operations
- **ML skills:** Classification, data preprocessing, feature engineering, model evaluation
- **Systems skills:** API design, data pipelines, visualization, production considerations
- **Interview value:** Full-stack data science project from data to deployment

---

## Overall Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   RAW AIS DATA (CSV)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────▼─────────────────┐
        │  Phase 1-2: Data Preparation    │
        │  (Clean, Explore, Engineer)     │
        └────────────────┬─────────────────┘
                         │
        ┌────────────────▼──────────────────┐
        │  Phase 3-4: ML Pipeline          │
        │  (Feature eng, Model training)   │
        └────────────────┬──────────────────┘
                         │
        ┌────────────────▼──────────────────┐
        │  Phase 5: Model Evaluation       │
        │  (Metrics, Explainability)       │
        └────────────────┬──────────────────┘
                         │
        ┌────────────────▼──────────────────┐
        │  Phase 6: FastAPI Backend        │
        │  (Predictions, Visualization)    │
        └──────────────────────────────────┘
```

---

## Phases & Milestones

### Phase 1: Dataset Exploration ✋ YOU ARE HERE
**Goal:** Understand the data deeply
**Duration:** ~2-3 hours
**Deliverables:**
- Comprehensive data profiling report
- Data quality assessment
- Visualization of key distributions
- Documentation of data characteristics

**Key Questions to Answer:**
1. What does each column represent?
2. How much missing data do we have?
3. What ship types exist? (class distribution)
4. How are numerical features distributed?
5. Are there data quality issues?

---

### Phase 2: Data Cleaning
**Goal:** Prepare data for modeling
**Duration:** ~2-3 hours
**Deliverables:**
- Cleaned dataset (CSV)
- Data quality report
- Handling strategy documentation

**Key Activities:**
- Handle missing values
- Remove/fix outliers
- Standardize formats
- Document all transformations

---

### Phase 3: Feature Engineering
**Goal:** Create meaningful predictors
**Duration:** ~3-4 hours
**Deliverables:**
- Feature engineering notebook
- New feature descriptions
- Feature importance analysis

**Key Activities:**
- Explore feature relationships
- Create derived features
- Normalize/scale features
- Feature selection

---

### Phase 4: Ship Type Prediction Model
**Goal:** Train classification model
**Duration:** ~4-5 hours
**Deliverables:**
- Trained model (pickle/joblib)
- Model selection report
- Hyperparameter tuning results

**Key Activities:**
- Try multiple algorithms
- Cross-validation
- Hyperparameter tuning
- Model comparison

---

### Phase 5: Model Evaluation & Explainability
**Goal:** Understand model behavior
**Duration:** ~3-4 hours
**Deliverables:**
- Evaluation metrics report
- Feature importance analysis
- SHAP values/explanations
- Confusion matrix visualizations

**Key Activities:**
- Comprehensive metrics (precision, recall, F1)
- Per-class analysis
- Error analysis
- Feature importance plots

---

### Phase 6: FastAPI Backend
**Goal:** Productionize the model
**Duration:** ~4-5 hours
**Deliverables:**
- FastAPI server running
- REST endpoints for predictions
- Interactive documentation
- Example client code

**Key Activities:**
- API design
- Model serving
- Input validation
- Error handling

---

## Project Structure

```
ais-ship-prediction/
├── data/
│   ├── raw/
│   │   └── ais_data.csv
│   ├── processed/
│   │   ├── cleaned_data.csv
│   │   └── featured_data.csv
│   └── stats/
│       └── data_profile.json
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation.ipynb
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── model.py
│   └── utils.py
├── models/
│   ├── model.pkl
│   └── scaler.pkl
├── api/
│   ├── main.py
│   ├── schemas.py
│   └── requirements.txt
├── docs/
│   ├── PROJECT_PLAN.md (this file)
│   ├── LEARNING_NOTES.md
│   ├── INTERVIEW_PREP.md
│   ├── DECISION_LOG.md
│   └── TECH_STACK.md
└── README.md
```

---

## Success Criteria

- [ ] Data exploration complete with visual insights
- [ ] 95%+ data clean and usable
- [ ] Features engineered and documented
- [ ] Model trained with >80% accuracy
- [ ] Full evaluation report with explanations
- [ ] FastAPI backend running locally
- [ ] Can confidently explain every design decision

---

## Current Status
- Raw data downloaded: 358,352 records
- Phase 1: Dataset Exploration (COMPLETE)
- Phase 2: Data Cleaning (COMPLETE)
  - Cleaned dataset: 332,068 records
  - Zero missing data
  - Data validated and saved to `data/processed/cleaned_data.csv`
- Phase 3: Feature Engineering (COMPLETE)
  - Featured dataset: 332,068 records, 23 columns
  - Zero missing values and zero infinite numeric values
  - Saved to `data/processed/featured_data.csv`
- Current phase: Phase 4 - Ship Type Prediction Model
- Phases 5-6 pending

---

## Interview Readiness
By end of Phase 3, you should be able to answer:
- "Tell me about your dataset"
- "What data quality issues did you find?"
- "How is the data distributed?"
- "What was surprising about the data?"
- "What features did you engineer and why?"
- "Why did you use one-hot encoding for navigational status?"
- "How did you prevent invalid ratio features?"

---

## Phase 3 Architecture Update

Simple view:

```
cleaned_data.csv
      |
      v
src/feature_engineering.py
      |
      v
featured_data.csv
      |
      v
Phase 4 model training
```

What Phase 3 now produces:
- Original numeric signals: `sog`, `cog`, `heading`, `width`, `length`, `draught`
- Target column: `shiptype`
- Navigation status one-hot flags: `nav_status_*`
- Size and behavior features: `ship_size_category`, `speed_category`
- Shape and geometry features: `length_width_ratio`, `ship_footprint_area`, `depth_length_ratio`
- Movement alignment feature: `course_heading_delta`

Next steps for Phase 4:
- Split `featured_data.csv` into features `X` and target `y`
- Create a train/test split using stratification because ship classes are imbalanced
- Train a simple baseline model first
- Compare stronger models such as Random Forest and Gradient Boosting
- Evaluate with accuracy, macro F1, weighted F1, and per-class metrics
