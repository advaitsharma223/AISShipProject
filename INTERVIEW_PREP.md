# Interview Preparation Guide

## Phase 1: Dataset Exploration Interview Questions

### Question 1: "Tell me about your dataset"

**What they want to hear:**
- Comfortable explaining what you're working with
- Numbers and specifics
- Understanding of the domain

**Strong Answer Structure:**
```
"I'm working with an AIS (Automatic Identification System) dataset 
containing ~358,000 ship tracking records. Each record includes:
- Navigation data: speed, course, heading
- Ship characteristics: width, length, draught  
- Status information: navigational status
- The target: ship type (Cargo, Fishing, Passenger, etc.)

The goal is to build a classifier that predicts ship type from these features.
This is valuable because it enables automatic maritime monitoring without
manual labeling, which helps with port operations and maritime safety."
```

**Why this works:**
- Shows you understand the size and scope
- Explains what each field represents
- Connects to business value
- Shows this isn't arbitrary - it solves a real problem

---

### Question 2: "What data quality issues did you encounter?"

**What they want to hear:**
- You actually looked at the data
- Specific issues with numbers
- Your approach to handling them

**Strong Answer Structure:**
```
"Three main quality issues:

1. Missing Data: 
   - ~X% null values in [column]
   - My approach: [removal/imputation/categorization]
   
2. Class Imbalance:
   - Cargo ships were [X%], Military were [Y%]
   - This means [model behavior] without [mitigation strategy]
   
3. Outliers:
   - Found [specific example] which seems invalid
   - Handled by [specific strategy]"
```

**Why this works:**
- Specific numbers show analysis depth
- Explains impact (not just "there are issues")
- Shows you had a strategy to handle them

---

### Question 3: "How did you approach the exploratory data analysis?"

**What they want to hear:**
- Systematic thinking
- Understanding of what to look for
- Balance of statistical and visual analysis

**Strong Answer Structure:**
```
"I followed a structured approach:

1. Statistical Summary:
   - Mean, median, std dev for numerical features
   - Identified ranges and distributions
   
2. Missing Data Analysis:
   - Quantified % missing per column
   - Determined if missing was random or pattern-based
   
3. Target Distribution:
   - Counted each ship type
   - Visualized imbalance
   
4. Feature Relationships:
   - Checked correlation between features
   - Compared feature distributions across ship types
   
5. Visual Analysis:
   - Histograms for distributions
   - Box plots for outliers
   - Scatter plots for relationships"
```

**Why this works:**
- Shows methodical thinking
- Not random - you have a framework
- Covers both quantitative and qualitative

---

### Question 4: "What surprised you about the data?"

**What they want to hear:**
- You engaged critically
- Insights beyond surface-level
- Thinking about implications

**Good Answers:**
- "I expected [assumption] but found [reality]"
- "This suggests [insight] which means [implication]"
- "This could affect [downstream phase] because..."

**Examples:**
```
"I was surprised by the high proportion of 'Unknown' status values.
This suggests ships may not always report their status, which means
we might be training on noisier data than expected. It could impact
model reliability for predicting ships in certain states."

OR

"The draught field was almost entirely missing. This is actually 
interesting because it suggests [domain insight], so we probably 
shouldn't rely on it heavily as a feature."
```

**Why this works:**
- Shows critical thinking
- Connects observations to consequences
- Demonstrates domain awareness

---

### Question 5: "How would you handle the missing data?"

**What they want to hear:**
- Options, not just one approach
- Understanding of trade-offs
- Reasoning for your choice

**Strong Answer Framework:**
```
"For [specific column], I considered three approaches:

1. Removal: Delete rows with missing values
   Pros: Simple, no assumptions
   Cons: Lose data, may remove patterns
   
2. Imputation: Fill with mean/median
   Pros: Keep data volume
   Cons: Biases distribution, assumes MCAR
   
3. Categorization: Mark as 'Unknown' category
   Pros: Preserves information that it was missing
   Cons: Only works for categorical fields
   
I chose [X] because [reasoning specific to your data]"
```

**Why this works:**
- Shows you understand trade-offs
- Not just copying a tutorial
- Connects choice to your specific data

---

### Question 6: "How many distinct ship types are in the dataset?"

**What they want to hear:**
- You know your data
- Can list them

**Strong Answer:**
```
"We have approximately [X] distinct ship types:
- [List with approximate counts]
- The most common is [X] at roughly [%]%
- The rarest is [X] at roughly [%]%
- This imbalance is important because [implication]"
```

**Why this works:**
- Specific numbers
- Shows you looked
- Acknowledges implications

---

## Common Mistakes to Avoid

### ❌ Mistake 1: "The data looks fine"
This suggests you didn't look carefully enough.

### ✅ Fix: "I found these specific issues: [list 3-5 concrete findings]"

---

### ❌ Mistake 2: Vague descriptions
"There was missing data" - no specifics

### ✅ Fix: "Column X had 23% missing values, suggesting..."

---

### ❌ Mistake 3: No connection to downstream work
Exploration feels like busywork

### ✅ Fix: "This missing data pattern will affect feature engineering because..."

---

### ❌ Mistake 4: Treating all missing data the same
Different columns need different strategies

### ✅ Fix: "For numerical columns I used mean imputation, but for categorical I used a missing category"

---

## Questions To Prepare For Later Phases

(Save these for when you reach those phases)

- Phase 2: "Walk me through your data cleaning strategy"
- Phase 3: "What features did you engineer? Why?"
- Phase 4: "Why did you choose that specific algorithm?"
- Phase 5: "How do you explain model predictions?"
- Phase 6: "How would you handle prediction latency?"

---

## Practice

### Before Looking at This Guide:
Try answering these without reference:
1. What does your dataset contain?
2. What's the target variable?
3. What are the main features?
4. What issues did you find?
5. How will you handle them?

### Then Compare:
Read this guide. Where were you vague? Specific? Missing details?

### Refine:
Practice your 60-second version and your 5-minute version.

---

## Phase 3: Feature Engineering Interview Questions

### Question 1: "What features did you engineer and why?"

**Strong Answer:**
```
I engineered features in three groups: navigation behavior, ship geometry,
and movement alignment.

For navigation behavior, I one-hot encoded navigational status so the model
can use states like moored, under way, or engaged in fishing without creating
a fake numeric order.

For geometry, I created ship size category, length-to-width ratio, footprint
area, and depth-to-length ratio. These capture whether a ship is small or
large, long and narrow, physically large, or deep-drafted relative to its size.

For movement alignment, I created course-heading delta, which measures whether
the ship is moving in the same direction it is pointing. This can capture
drifting, turning, or maneuvering behavior.
```

**Why this works:**
- Groups features logically
- Connects each feature to maritime meaning
- Shows you did not just add random columns

---

### Question 2: "Why did you one-hot encode navigational status?"

**Strong Answer:**
```
Navigational status is categorical text, so it must become numeric before most
machine learning models can use it. I considered ordinal encoding, where each
status gets a number, but that creates a false order. For example, if Moored=3
and At anchor=7, some models may treat At anchor as mathematically larger,
which is not meaningful.

I chose one-hot encoding because it creates independent yes/no columns for each
status. That preserves the category information without implying ranking.
```

**Common follow-up: "What is the downside?"**
```
It creates more columns. In this dataset the number of status categories is
small, so the increase is acceptable. If we had thousands of categories, I
would consider target encoding, hashing, or model-specific categorical support.
```

---

### Question 3: "Why create ratio features if the model already has length, width, and draught?"

**Strong Answer:**
```
Raw dimensions tell the model absolute size, but ratios describe shape and
relative structure. A 150m ship and a 300m ship can both be long and narrow;
length-to-width ratio captures that shared shape pattern. Similarly,
depth-to-length ratio tells us how deep the ship sits relative to its size,
which is more comparable across different ship sizes than raw draught alone.
```

**Why this works:**
- Explains the difference between raw magnitude and normalized relationship
- Uses simple domain language

---

### Question 4: "How did you handle angle features correctly?"

**Strong Answer:**
```
Angles are circular, so normal subtraction can be wrong. For example, heading
359 degrees and course 1 degree are only 2 degrees apart, not 358. I used a
circular difference formula:

abs((cog - heading + 180) % 360 - 180)

This gives the smallest angular difference between course over ground and
heading, always between 0 and 180 degrees.
```

---

### Question 5: "How did you make sure feature engineering did not create bad values?"

**Strong Answer:**
```
Before creating ratio features, I validate that all required columns exist and
that width and length are positive. This prevents divide-by-zero and infinite
values. After running the pipeline, I verified the output had 332,068 rows, 23
columns, zero missing values, and zero infinite numeric values.
```

---

## Phase 3 Common Mistakes

### Mistake 1: Encoding categories with fake order
Bad answer: "I mapped categories to numbers because models need numbers."

Better answer: "I used one-hot encoding because the categories do not have a natural order."

### Mistake 2: Creating features without domain reasoning
Bad answer: "I added ratios because feature engineering is good."

Better answer: "I added ratios because ship type depends on shape, not just absolute dimensions."

### Mistake 3: Forgetting circular math for angles
Bad answer: "I subtracted heading from course."

Better answer: "I used circular difference because 359 degrees and 1 degree are close."

### Mistake 4: Not validating generated features
Bad answer: "The code ran, so the features are fine."

Better answer: "I checked for missing values, infinite values, and invalid ratio denominators."
