# AIS Ship Prediction & Map Visualization

## 📋 Quick Start

This is a **mentor-guided** portfolio project where you'll build a complete machine learning system - from raw data to production API.

**Goal:** Predict ship types from AIS tracking data, with deep understanding of every decision.

**Status:** Phase 1 - Dataset Exploration (Starting Now)

---

## 📚 Documentation Structure

Read these files in order:

### 1. **LEARNING_NOTES.md** ← START HERE
Explains concepts clearly, no prior knowledge assumed.
- What is AIS?
- Why we're building this
- Key ML concepts explained simply
- Common terminology

### 2. **PROJECT_PLAN.md** ← Then read this
Overall roadmap and what we're building.
- 6 phases with clear deliverables
- Architecture overview
- Success criteria
- Project structure

### 3. **TECH_STACK.md** ← Then understand tools
Every technology explained with "why we chose it".
- What is pandas? Why it matters
- How scikit-learn compares to alternatives
- Why FastAPI for the backend

### 4. **DECISION_LOG.md** ← Reference as we go
Tracks important decisions and trade-offs.
- Why we chose classification (not regression)
- Why we use CSV (not databases)
- What we're trading off and why

### 5. **INTERVIEW_PREP.md** ← Practice with this
Real interview questions with strong answers.
- How to talk about your data
- Common mistakes to avoid
- Practice questions

---

## 🎯 Right Now: Phase 1 - Dataset Exploration

### What We're Doing
Deeply understand our dataset before any modeling.

### What You'll Produce
- Comprehensive data analysis (Jupyter notebook)
- Data quality report
- Visualizations of key patterns
- Clear documentation of findings

### Key Questions to Answer
1. How many records? How many features?
2. What ship types exist? (balanced or imbalanced?)
3. Where is missing data? How much?
4. What do typical values look like?
5. Are there relationships between features and ship type?

---

## 🚀 Next Steps

### Step 1: Understand the Foundation (30 minutes)
- [ ] Read LEARNING_NOTES.md completely
- [ ] Understand what AIS is and why it matters
- [ ] Know the key ML concepts we'll use

### Step 2: Review the Plan (20 minutes)
- [ ] Skim PROJECT_PLAN.md
- [ ] Note the 6 phases and deliverables
- [ ] Understand the overall architecture

### Step 3: Know Your Tools (15 minutes)
- [ ] Skim TECH_STACK.md
- [ ] Understand why we chose each technology

### Step 4: Begin Phase 1 (2-3 hours)
When you're ready to code, we'll:
1. Create a Jupyter notebook: `notebooks/01_exploration.ipynb`
2. Load and profile the data
3. Answer all 5 key questions above
4. Create visualizations
5. Document findings

---

## 📊 Dataset Overview

### What We Have
```
Raw Data: ais_data.csv
Records: ~358,000 ship observations
Size: ~26 MB

Columns:
- mmsi: Ship identifier
- navigationalstatus: What ship is doing (e.g., "At anchor")
- sog: Speed Over Ground (knots)
- cog: Course Over Ground (degrees)
- heading: Direction ship is pointing (degrees)
- shiptype: CATEGORY WE'RE PREDICTING (e.g., "Cargo")
- width: Ship width (meters)
- length: Ship length (meters)
- draught: How deep ship sits in water (meters)
```

### Why This Data
- Real maritime data
- Actually useful (insurance, ports, logistics use this)
- Classification problem (predict ship type)
- Good size (not too small, not massive)
- Realistic data quality issues (missing values, outliers)

---

## 🎓 Learning Approach

### Not a Tutorial
This is **mentored pair-programming**. You're learning by building, not watching tutorials.

### Why Understand First?
- Code you write *means something* to you
- You can explain trade-offs in interviews
- You build intuition, not just copy-paste
- You're learning to think, not just code

### The Pattern
For each phase:
1. **Explain:** What/why/how BEFORE coding
2. **Plan:** Multiple approaches, compare them
3. **Decide:** Choose approach with reasoning
4. **Implement:** Code with clear understanding
5. **Document:** Why you made choices
6. **Reflect:** Interview prep questions

---

## 📈 Success Looks Like

### End of Phase 1
You can say:
- "My dataset has 358K records with these 9 columns"
- "Cargo ships are 40% of the data, Military only 2%"
- "23% of draught values are missing, so I'll..."
- "Here's the distribution of ship speeds"
- "I found these data quality issues and here's my plan"

### End of Phase 6
You can say:
- Full explanation of every design decision
- Why you chose those algorithms
- How the model works and why it works
- How the API serves predictions
- Discussion of trade-offs and alternatives

---

## 💡 Key Principles

### 1. Understand Before Code
Don't just follow steps. Understand why each step matters.

### 2. Think in Trade-offs
Every choice has pros and cons. Know them both.

### 3. Document Everything
Future you (and interviewers) will thank present you.

### 4. Validate Understanding
Frequently ask yourself: "Do I understand *why* we're doing this?"

### 5. Connect to Real World
Remember: real ports, real insurance, real money involved.

---

## 📞 Questions as We Go

I'm your mentor. As we work:

- **"Why are we doing this?"** → Explain the purpose
- **"What are the options?"** → Show alternatives
- **"Is there a simpler way?"** → Push toward clarity
- **"How does this connect?"** → Show the bigger picture
- **"Can you explain that?"** → Test your understanding

---

## 📁 Folder Structure (Will Grow)

```
ais-ship-prediction/
├── data/
│   └── raw/
│       └── ais_data.csv                 ← You have this
├── notebooks/
│   └── 01_exploration.ipynb             ← Create next
├── docs/
│   ├── PROJECT_PLAN.md                  ✅ Done
│   ├── LEARNING_NOTES.md                ✅ Done
│   ├── INTERVIEW_PREP.md                ✅ Done
│   ├── DECISION_LOG.md                  ✅ Done
│   ├── TECH_STACK.md                    ✅ Done
│   └── README.md                        ✅ Done
└── src/
    └── (added in Phase 6)
```

---

## 🎬 Ready to Start?

### Path Forward

**When you're ready to begin Phase 1 exploration:**

Tell me you understand:
1. What AIS is and why we're building this (from LEARNING_NOTES)
2. The 6-phase roadmap (from PROJECT_PLAN)
3. Why we chose our tools (from TECH_STACK)

Then we'll:
1. Create the first notebook
2. I'll guide you through data exploration
3. You'll ask questions (I expect lots!)
4. Build deep understanding as we go

---

## 🤔 Before You Move Forward

### Quick Check - Do You Understand?

Without looking back:
1. What does "ship type classification" mean?
2. Why might missing data be a problem?
3. What's the difference between exploring data and training a model?
4. Name two alternatives we considered and rejected (from DECISION_LOG)

Can you answer these? If not, re-read LEARNING_NOTES.md until you can.

---

## 📝 Notes for Future Self

### During Each Phase
- Update PROJECT_PLAN.md with progress
- Add to DECISION_LOG.md when making choices
- Add to INTERVIEW_PREP.md with new questions
- Update LEARNING_NOTES.md if you learn something new

### End of Each Phase
- Review what you built
- Document the "why"
- Write interview questions
- Reflect on trade-offs

---

## Questions?

Before we dive into Phase 1, what would you like me to clarify?

Some common starting points:
- "Can you explain classification in more detail?"
- "Why is class imbalance a problem?"
- "What exactly happens in the modeling phase?"
- "How will we know if the model is good?"
- "What does an API endpoint actually do?"

**The goal of Phase 1 isn't to rush. It's to build solid understanding.**

---

**Next Step:** 
Let me know you're ready to begin Phase 1 exploration, and we'll create your first Jupyter notebook together!
