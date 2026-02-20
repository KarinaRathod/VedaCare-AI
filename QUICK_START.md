# ⚡ Quick Start Guide - AI Healthcare Assistant

Get started in 3 minutes!

---

## 🚀 Step 1: Install Dependencies

Open PowerShell in this folder and run:

```powershell
pip install -r requirements_crewai.txt
```

**This installs:**
- CrewAI framework
- Google Gemini AI integration
- Required libraries

**Time:** ~2 minutes

---

## 🎯 Step 2: Run the Application

### Option A: GUI (Recommended)

```powershell
python healthcare_agent_gui.py
```

**A window will open with:**
- 7 healthcare specialists to choose from
- Input area for your health query
- Beautiful medical-themed interface

### Option B: Interactive CLI

```powershell
python healthcare_agent_interactive.py
```

**Terminal-based interface:**
- Menu-driven specialist selection
- Multi-line input support
- Fast and lightweight

---

## 💡 Step 3: Ask Your Health Question

### 1. Select a Specialist

Choose from:
- **Medical Advisor** - General health questions
- **Symptom Analyzer** - "I have headache and nausea"
- **Nutrition Specialist** - "Healthy diet for diabetes"
- **Mental Health Counselor** - "Feeling anxious"
- **Fitness Coach** - "Exercises for back pain"
- **Treatment Recommender** - "Managing high blood pressure"
- **Disease Educator** - "What is arthritis?"

### 2. Describe Your Query

**Good examples:**
```
"I have persistent headaches with sensitivity to light for 2 days"

"What are the best foods for heart health? I'm 45 with high cholesterol"

"I want to start running but have knee problems. What's safe?"

"Feeling stressed and anxious lately. What can help?"
```

### 3. Get Intelligent Guidance

The AI specialist will provide:
- ✅ Accurate information
- ✅ Practical recommendations
- ✅ When to see a doctor
- ✅ Relevant health tips
- ✅ Safety warnings

---

## 🎨 GUI Interface Guide

```
┌────────────────────────────────────────┐
│  🏥 AI Healthcare Assistant            │
│  Medical | Health Info | Wellness      │
│  ⚠️  For informational purposes only   │
├────────────────────────────────────────┤
│                                        │
│  👨‍⚕️ Select Healthcare Specialist      │
│  [Medical Advisor           ▼]         │
│                                        │
│  📝 Describe Your Health Query         │
│  ┌────────────────────────────────┐   │
│  │ Your question here...          │   │
│  │                                │   │
│  └────────────────────────────────┘   │
│                                        │
│  [🩺 Consult] [🗑️ Clear] [Progress]    │
│                                        │
│  💡 AI Healthcare Guidance             │
│  ┌────────────────────────────────┐   │
│  │ Response appears here...       │   │
│  │                                │   │
│  └────────────────────────────────┘   │
└────────────────────────────────────────┘
```

---

## 💻 CLI Interface Guide

```
======================================================================
🏥 AI HEALTHCARE ASSISTANT
Medical Guidance | Health Information | Wellness Support
======================================================================

👨‍⚕️ SELECT HEALTHCARE SPECIALIST:

  1. Medical Advisor
  2. Symptom Analyzer
  3. Treatment Recommender
  4. Nutrition Specialist
  5. Mental Health Counselor
  6. Fitness Coach
  7. Disease Educator

Enter your choice (1-7): 2

📝 Describe your query (press Enter twice):

I have a headache and nausea
[Enter]
[Enter]

⏳ SYMPTOM ANALYZER IS ANALYZING YOUR QUERY...

💡 RESPONSE:
[Detailed guidance appears here...]
```

---

## ⚠️ Important Reminders

### This App Is For:
✅ Health education
✅ General information
✅ Understanding conditions
✅ Learning about treatments
✅ Wellness guidance

### This App Is NOT For:
❌ Emergency situations → Call 911
❌ Definitive diagnosis → See a doctor
❌ Prescriptions → Consult physician
❌ Replacing medical advice

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:**
```powershell
pip install -r requirements_crewai.txt
```

### Issue: "API key not found"
**Solution:** Check `.env` file exists with:
```
GOOGLE_API_KEY=AIzaSyC4PTL-1JT6tEaZiObMaleCFtO9-lXC_Nc
```

### Issue: GUI doesn't open
**Solution:** Try CLI version instead:
```powershell
python healthcare_agent_interactive.py
```

### Issue: Slow response
**Solution:** 
- First query always slower (initialization)
- Check internet connection
- Wait 20-30 seconds

---

## 📝 Example Session

### Query 1: Symptoms
**Specialist:** Symptom Analyzer
**Query:** "Persistent dry cough for 3 days with mild fever"
**Response:** Possible explanations, severity assessment, when to seek help

### Query 2: Nutrition
**Specialist:** Nutrition Specialist  
**Query:** "Best foods for lowering blood pressure"
**Response:** Dietary recommendations, foods list, meal ideas

### Query 3: Fitness
**Specialist:** Fitness Coach
**Query:** "Safe exercises for beginners with back pain"
**Response:** Recommended exercises, safety tips, progression plan

---

## 🎯 Tips for Best Results

### 1. Be Specific
❌ "I feel bad"
✅ "I have sharp stomach pain after eating, lasting 2 hours"

### 2. Include Context
- Duration of symptoms
- Severity (mild/moderate/severe)
- What makes it better/worse
- Other relevant health conditions

### 3. Choose Right Specialist
- Symptoms? → Symptom Analyzer
- Diet questions? → Nutrition Specialist
- Exercise? → Fitness Coach
- Mental health? → Mental Health Counselor

### 4. Ask Follow-ups
You can run multiple consultations in one session!

---

## 📊 What to Expect

### Response Time
- **First query:** 15-30 seconds (initialization)
- **Subsequent queries:** 10-20 seconds
- **Complex queries:** Up to 30 seconds

### Response Quality
- **Comprehensive:** Detailed explanations
- **Practical:** Actionable recommendations
- **Safe:** Always includes disclaimers
- **Educational:** Helps you understand

---

## 🎓 Learning Opportunity

Use this app to:
1. **Learn about** health conditions
2. **Understand** medical terminology
3. **Prepare** questions for your doctor
4. **Research** treatment options
5. **Improve** health literacy

**Always verify** information with healthcare professionals!

---

## 🔗 Next Steps

After using the app:

1. ✅ **Note Important Points** - Write down key information
2. ✅ **Consult Your Doctor** - Discuss findings with physician
3. ✅ **Research Further** - Use provided information as starting point
4. ✅ **Take Action** - Implement recommended lifestyle changes (after medical approval)

---

## 📞 Emergency Situations

**If you have any of these, call 911 immediately:**
- Chest pain or pressure
- Difficulty breathing
- Severe bleeding
- Loss of consciousness
- Signs of stroke
- Severe allergic reaction

**Do NOT use this app for emergencies!**

---

## ✅ You're Ready!

### Quick Command Reference

**GUI:**
```powershell
python healthcare_agent_gui.py
```

**CLI:**
```powershell
python healthcare_agent_interactive.py
```

**Install:**
```powershell
pip install -r requirements_crewai.txt
```

---

**Have a healthy day! 🏥💚**

*Remember: This is educational information only. Always consult healthcare professionals for medical advice.*
