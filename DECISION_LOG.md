# Decision Log

This document tracks every major decision in the project, why it was made, and what alternatives were considered.

## Format for Each Decision:
```
### Decision [N]: [Short Title]

**Date:** [Date]
**Phase:** [Which phase]

**Decision:** [What we decided]

**Alternatives Considered:**
1. [Alternative 1]
   - Pros: [...]
   - Cons: [...]
   
2. [Alternative 2]
   - Pros: [...]
   - Cons: [...]

**Rationale:** [Why we chose this]

**Trade-offs:** [What we're giving up]

**Implications:** [How this affects downstream phases]

**Reversibility:** [Easy/Moderate/Hard to reverse]
```

---

## Decision 1: Use Classification (Not Regression)

**Date:** 2026-06-04
**Phase:** 1 - Planning

**Decision:** 
Approach this as a classification problem where we predict discrete ship type categories, rather than trying to predict ship type as a ranking or regression problem.

**Alternatives Considered:**

1. **Regression approach:** Assign numbers to ship types (e.g., 1=Cargo, 2=Fishing) and predict the number
   - Pros: Simpler mathematically, fewer algorithms needed
   - Cons: Creates artificial ordering, confuses model, assumes ship types are ranked
   
2. **Clustering approach:** Find natural groups in the data without labels
   - Pros: Unsupervised, discover patterns
   - Cons: Don't leverage the ship type labels we have, harder to evaluate

3. **Multi-label classification:** Allow multiple ship types per record
   - Pros: More realistic for some edge cases
   - Cons: Complex, our data appears to be single-label

**Rationale:**
Ship types are distinct categories with no inherent order. We have labeled data showing what type each ship is. Classification is the natural fit.

**Trade-offs:**
We give up flexibility to handle ambiguous cases, but gain interpretability and appropriate modeling.

**Implications:**
- Metrics will be precision/recall/F1, not regression metrics
- Algorithms: Logistic Regression, Random Forest, SVM, Neural Networks (all for classification)
- Evaluation will use confusion matrices

**Reversibility:** 
Hard - would require reconceptualizing entire pipeline, but we're highly confident in this choice.

---

## Decision 2: Single CSV File (Not Database)

**Date:** 2026-06-04
**Phase:** 1 - Planning

**Decision:**
Keep data in CSV format for Phases 1-5, use pickle for models. Move to database only if performance requires it.

**Alternatives Considered:**

1. **Load to SQL database immediately**
   - Pros: Better for large datasets, easier querying
   - Cons: Overkill for this size, setup overhead, unnecessary complexity
   
2. **Use HDF5 format**
   - Pros: Efficient storage and access for numerical data
   - Cons: Learning curve, less portable than CSV
   
3. **Parquet format**
   - Pros: Columnar storage, compressed, fast
   - Cons: Overkill for 358K rows, adds tool complexity

**Rationale:**
358K rows fit comfortably in memory (~100-200MB). CSV is universally readable. Keep tools simple for learning.

**Trade-offs:**
Slower I/O than optimized formats, but gains simplicity and portability.

**Implications:**
- Can load entire dataset into memory with pandas
- No SQL queries needed
- Easier to share/reproduce

**Reversibility:** 
Easy - just load CSV differently if we later need a database.

---

## Decision 3: Jupyter Notebooks for Exploration, Python Scripts for Production

**Date:** 2026-06-04
**Phase:** 1 - Planning

**Decision:**
Use Jupyter notebooks for exploratory work (phases 1-5), then refactor to Python modules (src/ folder) for the FastAPI backend (phase 6).

**Alternatives Considered:**

1. **All Python scripts from the start**
   - Pros: More organized, reusable from day one
   - Cons: Slower exploration, less interactive
   
2. **All Jupyter notebooks throughout**
   - Pros: Interactive and explorable
   - Cons: Not reproducible, hard to test, bad for production

3. **Mix notebooks and scripts equally**
   - Pros: Best of both worlds
   - Cons: Can become messy, unclear which is source of truth

**Rationale:**
Notebooks are great for learning and exploration. Scripts are necessary for production. Refactor as we understand what works.

**Trade-offs:**
Some refactoring work in Phase 6, but gain learning clarity earlier phases.

**Implications:**
- Phases 1-5: Use .ipynb files in notebooks/ folder
- Phase 6: Refactor working code to src/ modules
- Clear separation between exploration and production code

**Reversibility:** 
Easy - notebooks can be converted to scripts or vice versa.

---

## Decision 4: Handle Missing Data Per-Column, Not Global

**Date:** 2026-06-04
**Phase:** 1 - Planning (Decision to make during Phase 2)

**Status:** *Not yet made - will decide during Phase 2 after seeing patterns*

**Preview of how we'll approach it:**
Each column's missing data tells a story. We won't use the same strategy for all:
- Numerical features with <5% missing → impute with median
- Categorical features with missing → create "Unknown" category  
- Columns with >50% missing → probably exclude from features
- Special patterns → investigate and document

**Why:** Different columns have different meanings of "missing"

---

---

## Decision 5: Handle Missing Draught Data - REMOVE ROWS

**Date:** 2026-06-04
**Phase:** 2 - Data Cleaning

**Decision:** 
Remove all rows where draught is missing (7.1% of dataset, ~25K rows).

**Alternatives Considered:**

1. **Fill with global median**
   - Pros: Keep all data
   - Cons: Creates unrealistic uniformity, destroys variance, model assumes all ships have same depth
   
2. **Fill with median by ship type**
   - Pros: More realistic, ship types have different typical drafts
   - Cons: Still creates fake data, assumes uniformity within type
   
3. **Keep missing as separate category (for numerical)**
   - Pros: Preserves information that it was missing
   - Cons: Can't use for predictions

4. **Remove rows** ← WE CHOSE THIS
   - Pros: Only real data, no guessing, defensible decision
   - Cons: Lose 7% of records

**Rationale:**
Draught has sparse/unreliable reporting. Ships that don't report draught may be unreliable reporters overall. Better to have 330K high-quality records than 358K with guessed data. 7% loss is acceptable for quality.

**Trade-offs:**
Smaller training dataset, but higher data quality and model confidence.

**Implications:**
- Final dataset will have ~330K records instead of 358K
- No bias from artificial draught values
- Model won't see unrealistic depth patterns

**Reversibility:** 
Medium - if we later need more data, we could impute instead, but would need to re-run all downstream phases.

---

## Decision 6: Handle Missing Heading Data - FILL WITH MEDIAN BY SHIP TYPE

**Date:** 2026-06-04
**Phase:** 2 - Data Cleaning

**Decision:** 
Fill missing heading values (5.8% of dataset, ~20K rows) with the median heading for that ship type.

**Alternatives Considered:**

1. **Remove rows**
   - Pros: Only real data
   - Cons: Combined with draught removal = 12% total loss, heading is predictable
   
2. **Fill with global median**
   - Pros: Simple
   - Cons: Destroys direction patterns (180° and 0° are same but math treats them opposite), all ships get same heading
   
3. **Fill with Course (COG) value**
   - Pros: Course ≈ Heading (related data)
   - Cons: Not always true (ships drift, tow), adds assumption
   
4. **Fill with median by ship type** ← WE CHOSE THIS
   - Pros: Ship types have characteristic heading patterns, realistic, only 5.8% missing
   - Cons: Creates artificial data, assumes uniformity within type

**Rationale:**
Only 5.8% missing (acceptable). Heading varies significantly by ship type (Tankers vs Fishing boats move differently). Median by type is most realistic guess. Better to keep 358K records with slight bias than lose 12% combined with draught removal.

**Trade-offs:**
We're creating fake data, but more training data > perfect data for ML. Model learns "ships of type X typically head direction Y" which is useful signal.

**Implications:**
- Keeps more training data
- Introduces slight bias toward ship-type-typical headings
- Model learns type-specific patterns
- Loss of individual ship variation

**Reversibility:** 
Easy - if model performance is bad, we can try removing instead.

---

## Decision 7: Handle Missing Width/Length Data - FILL WITH MEDIAN BY SHIP TYPE

**Date:** 2026-06-04
**Phase:** 2 - Data Cleaning

**Decision:** 
Fill missing width and length values (~1% of dataset, ~3.7K rows each) with median values by ship type.

**Alternatives Considered:**

1. **Remove rows**
   - Pros: Only real data
   - Cons: Unnecessary - only 1% missing
   
2. **Fill with global median**
   - Pros: Simple
   - Cons: Unrealistic (cargo ships and fishing boats very different sizes)
   
3. **Fill with median by ship type** ← WE CHOSE THIS
   - Pros: Width/Length are engineering specs (standardized per type), very predictable, only 1% loss
   - Cons: Still creates artificial data

**Rationale:**
Width and length are standardized specifications for ship types. Every Cargo ship of a class has similar dimensions. Only 1% missing (likely data entry errors). Filling by type is highly accurate and preserves training data.

**Trade-offs:**
Creates artificial data, but for highly predictable values where 1% loss would hurt more than artificial data helps.

**Implications:**
- Preserves all records
- Model sees realistic ship size distributions
- Small bias toward type-typical sizes (acceptable)

**Reversibility:** 
Easy - only 1% so removing wouldn't hurt much if needed.

---

## Decision 8: Validation Strategy - CHECK DATA RANGES

**Date:** 2026-06-04
**Phase:** 2 - Data Cleaning

**Decision:** 
After imputation, validate that all numerical values fall within realistic ranges:
- SOG (Speed): 0-50 knots (realistic for ships)
- COG/Heading: 0-360 degrees
- Width: 1-100 meters
- Length: 2-400 meters
- Draught: 0.4-15 meters

Remove any outliers outside these ranges as data errors.

**Rationale:**
These ranges are based on:
- Physical ship constraints (ships don't go 100+ knots)
- AIS specification (angles are 0-360)
- Our Phase 1 exploration findings (min/max values)

**Trade-offs:**
May remove some valid edge cases, but catches garbage data.

**Implications:**
- Additional rows removed (small number expected)
- Cleaner, more realistic training data
- Less variance in features, but more trustworthy

**Reversibility:** 
Medium - would need to track which rows were removed.

---

## Decision 8: Handle Missing Width/Length - FILL WITH MEDIAN BY SHIP TYPE

**Date:** 2026-06-04
**Phase:** 2 - Data Cleaning

**Decision:** 
Fill missing width/length values (1% of dataset) with median by ship type.

**Alternatives Considered:**

1. **Remove rows**
   - Pros: Only real data
   - Cons: Unnecessary - only 1% missing and width/length are standardized

2. **Fill with global median**
   - Pros: Simple
   - Cons: Destroys ship-type specific size differences

3. **Fill with median by ship type** ← WE CHOSE THIS
   - Pros: Only 1% missing, width/length are engineering specs, ships of same type have similar dimensions
   - Cons: Creates artificial data

**Rationale:**
Width and length are engineering specifications - standardized by ship type. Every Cargo ship of a type is roughly same size. Missing only 1% means data loss would be minimal, but imputation is reliable because dimension patterns are very consistent within type.

**Trade-offs:**
Creates artificial data, but for standardized engineering specs that are highly predictable.

**Implications:**
- All features can be used for modeling (no rows excluded)
- 332K final records (clean and complete)

**Reversibility:** 
Easy - could re-run with removal instead.

---

## Decision 9: Create Navigational Status Encoding

**Date:** 2026-06-04
**Phase:** 3 - Feature Engineering

**Decision:**
Convert navigational status (text) to numerical encoding (0-8 scale).

**Why:**
Many machine learning algorithms require numerical inputs. Encoding preserves the categorical information while making it machine-readable.

**Encoding scheme:**
- 0 = Under way using engine (most common)
- 1-7 = Other specific statuses by frequency
- 8 = Unknown/rare statuses (grouped)

**Implications:**
- Algorithms can now use navigation behavior as a feature
- Model learns that different statuses relate to different ship types

---

## Decision 10: Create Ship Size Categories

**Date:** 2026-06-04
**Phase:** 3 - Feature Engineering

**Decision:**
Create categorical ship size (Small/Medium/Large/VeryLarge) from ship length.

**Why:**
Ship size is a key characteristic for classification:
- Small (<25m): Fishing boats, pleasure craft
- Medium (25-100m): Tugs, smaller cargo
- Large (100-200m): Standard cargo, tankers
- Very Large (>200m): Mega ships

**Trade-offs:**
Loses some information (continuous → categorical), but categories are more interpretable.

---

## Decision 11: Create Length-to-Width Ratio

**Date:** 2026-06-04
**Phase:** 3 - Feature Engineering

**Decision:**
Create aspect ratio (length/width) as derived feature.

**Why:**
Different ship types have different shapes:
- Fishing boats: roughly square (ratio ~2-4)
- Cargo ships: long and narrow (ratio ~5-7)
- Special ships: even more extreme ratios

This captures shape characteristic important for classification.

---

## Decision 12: Create Speed Categories

**Date:** 2026-06-04
**Phase:** 3 - Feature Engineering

**Decision:**
Convert continuous speed (SOG) to speed categories (Stationary/Slow/Normal/Fast).

**Why:**
Speed reveals ship activity patterns:
- 0-2 knots: stationary/drifting (fishing, moored)
- 2-8 knots: slow (fishing, tugs working)
- 8-15 knots: normal transit (cargo, passenger)
- 15+ knots: fast (SAR, military, HSC)

Categories capture behavioral patterns important for predicting ship type.

---

## Decision 13: Create Depth-to-Length Ratio

**Date:** 2026-06-04
**Phase:** 3 - Feature Engineering

**Decision:**
Create normalized draft ratio (draught/length) as derived feature.

**Why:**
Different ships have different drafts:
- Cargo/Tankers: deep draft (ratio ~0.06-0.10)
- Fishing/Pleasure: shallow draft (ratio ~0.1-0.2)
- Pilot/Tugs: very shallow (ratio <0.1)

Normalizing by length makes it comparable across different ship sizes.

---

## Future Decisions to Track

Decisions we'll make in upcoming phases:
- Which features are most important (Phase 4)
- How to handle class imbalance (Phase 4)
- Which algorithm to use (Phase 4)
- Model evaluation metrics (Phase 5)
- API design (Phase 6)

---

## Decision 14: Replace Ordinal Navigation Encoding With One-Hot Encoding

**Date:** 2026-06-04
**Phase:** 3 - Feature Engineering

**Decision:**
Use one-hot columns for navigational status instead of a single ordinal numeric code.

The generated columns use the pattern `nav_status_*`, for example:
- `nav_status_under_way_engine`
- `nav_status_moored`
- `nav_status_at_anchor`
- `nav_status_other`

**Alternatives Considered:**

1. **Ordinal encoding**
   - Pros: Compact, only one column, easy to create
   - Cons: Creates fake order between categories; bad for linear models and distance-based models

2. **One-hot encoding**
   - Pros: Preserves category identity without fake order; model-ready CSV remains numeric
   - Cons: Adds more columns

3. **Keep raw text and encode in the Phase 4 model pipeline**
   - Pros: Cleanest long-term ML architecture
   - Cons: Slightly harder for a beginner to inspect because the CSV is not fully numeric

**Rationale:**
For the current portfolio stage, one-hot encoding is the best balance. It keeps the dataset ready for Phase 4 modeling while avoiding the misleading assumption that one navigational status is numerically greater than another.

**Trade-offs:**
The dataset grows from 12 columns to 23 columns, but the meaning of each category is clearer and safer for multiple model families.

**Implications:**
- Phase 4 can train on a fully numeric feature table.
- Linear models, tree models, and distance-based models can all use navigation status safely.
- Rare statuses are grouped into `nav_status_other`.

**Reversibility:**
Easy - the feature pipeline can be rerun with a different encoding strategy if Phase 4 requires it.

---

## Decision 15: Add Geometry and Movement Domain Features

**Date:** 2026-06-04
**Phase:** 3 - Feature Engineering

**Decision:**
Create three additional domain features:
- `ship_footprint_area = length * width`
- `course_heading_delta = circular difference between COG and heading`
- Validation before ratio features to ensure width and length are positive

**Alternatives Considered:**

1. **Use only raw features**
   - Pros: Simpler; fewer assumptions
   - Cons: Model must discover all relationships by itself

2. **Add many complex maritime formulas**
   - Pros: Potentially more predictive
   - Cons: Harder to explain; may overfit; requires deeper naval architecture assumptions

3. **Add a small set of explainable domain features**
   - Pros: Strong interview story; simple; useful for tabular models
   - Cons: Still adds assumptions about which relationships matter

**Rationale:**
The chosen features are easy to explain and closely tied to the maritime domain:
- Area captures physical scale.
- Course-heading difference captures movement alignment.
- Validation prevents divide-by-zero or infinite ratio features.

**Trade-offs:**
We add some feature correlation because area relates to length and width, but tree-based models can usually handle this and Phase 5 can evaluate feature importance.

**Implications:**
Phase 4 starts from a stronger feature table and Phase 5 can test whether these engineered features actually helped.

**Reversibility:**
Easy - features can be dropped during model comparison or feature selection.
