# 🏥 AI Healthcare Assistant

Intelligent healthcare guidance system powered by CrewAI and Google Gemini AI.

---

## 🎯 What This Does

**AI Healthcare Assistant** provides intelligent health information and guidance through specialized AI agents. Each agent is trained for specific healthcare domains to provide accurate, helpful information.

### ⚠️ Important Disclaimer

**This application is for informational and educational purposes only.**
- NOT a substitute for professional medical advice
- NOT for emergency situations
- Always consult qualified healthcare professionals
- Never rely solely on AI for medical decisions

---

## 🤖 Available Healthcare Specialists

| Specialist | Expertise |
|------------|-----------|
| **Medical Advisor** | General medical information and guidance |
| **Symptom Analyzer** | Analyzes symptoms and suggests possible conditions |
| **Treatment Recommender** | Evidence-based treatment options and lifestyle changes |
| **Nutrition Specialist** | Dietary guidance and nutritional advice |
| **Mental Health Counselor** | Mental health support and coping strategies |
| **Fitness Coach** | Exercise guidance and fitness recommendations |
| **Disease Educator** | Disease information, prevention, and management |

---

## 🚀 Quick Start

### Prerequisites

1. Python 3.10 or higher
2. Google Gemini API key (free)

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements_crewai.txt
```

2. **Set up API key:**

Your `.env` file is already configured with:
```
GOOGLE_API_KEY=your-key-here
```

### Run the Applications

**GUI Version (Recommended):**
```bash
python healthcare_agent_gui.py
```

**Interactive CLI Version:**
```bash
python healthcare_agent_interactive.py
```

---

## 💡 Use Cases

### 1. Symptom Analysis
**Agent:** Symptom Analyzer
```
Query: "I have persistent headaches with sensitivity to light"
Response: Possible explanations, severity assessment, when to seek help
```

### 2. Nutritional Guidance
**Agent:** Nutrition Specialist
```
Query: "What foods should I eat to manage high blood pressure?"
Response: Dietary recommendations, foods to eat/avoid, meal ideas
```

### 3. Mental Health Support
**Agent:** Mental Health Counselor
```
Query: "I've been feeling anxious and stressed lately"
Response: Coping strategies, relaxation techniques, when to seek therapy
```

### 4. Fitness Advice
**Agent:** Fitness Coach
```
Query: "Safe exercises for someone with lower back pain"
Response: Recommended exercises, precautions, progression plan
```

### 5. Disease Education
**Agent:** Disease Educator
```
Query: "Explain diabetes type 2 and how to manage it"
Response: Disease overview, management strategies, prevention tips
```

---

## 📁 Project Files

### Complete Healthcare Application
- **`healthcare_agent_gui.py`** ⭐ - Beautiful GUI interface
- **`healthcare_agent_interactive.py`** ⭐ - Interactive CLI interface
- **`.env`** - API key configuration (already set)
- **`requirements_crewai.txt`** - All required dependencies
- **`README.md`** - Complete documentation
- **`QUICK_START.md`** - 3-minute setup guide

---

## 🎨 GUI Features

### Beautiful Healthcare-Themed Interface
- 🏥 Medical blue color scheme
- 👨‍⚕️ 7 specialized healthcare agents
- 📝 Large input area for detailed queries
- 💡 Clear, formatted responses
- ⚠️ Prominent disclaimers
- 🔄 Progress indicators

### User Experience
- Clean, professional design
- Easy agent selection
- Responsive interface
- Thread-safe processing
- Error handling

---

## 💻 Interactive CLI Features

### Command-Line Interface
- 🎯 Menu-driven specialist selection
- 📝 Multi-line input support
- 💡 Formatted responses
- 🔄 Multiple consultations
- ⚡ Fast and lightweight

---

## 🧠 How It Works

### Technology Stack

```
User Interface (GUI/CLI)
         ↓
    CrewAI Framework
         ↓
 Specialized AI Agents
         ↓
   Google Gemini AI
         ↓
  Healthcare Guidance
```

### Agent Intelligence

Each healthcare agent has:
1. **Specialized Role** - Specific healthcare domain
2. **Clear Goal** - What they aim to achieve
3. **Expert Backstory** - Training and expertise
4. **LLM Brain** - Powered by Gemini 2.5 Flash

### Response Generation

1. User submits health query
2. Selected specialist agent analyzes query
3. Agent generates comprehensive guidance
4. Response includes:
   - Accurate information
   - Practical recommendations
   - Safety warnings
   - When to seek professional help

---

## 🔧 Configuration

### Change AI Model

Edit in `healthcare_agent_gui.py` or `healthcare_agent_interactive.py`:

```python
llm = LLM(
    model="gemini/gemini-2.5-flash",  # Fast, free
    # model="gemini/gemini-2.5-pro",  # More capable
    temperature=0.7,
    api_key=api_key
)
```

### Add Custom Specialist

Add to `agent_configs` dictionary:

```python
"Your Specialist Name": {
    "role": "Your Role",
    "goal": "What they do",
    "backstory": "Their expertise and approach"
}
```

---

## 📊 Example Queries

### Good Queries (Detailed)
✅ "I've had a persistent dry cough for 3 days with mild fever. No other symptoms. What could this be?"

✅ "What are the best foods to eat for better heart health? I'm 45 and have slightly high cholesterol."

✅ "I want to start exercising but I have knee problems. What exercises are safe for me?"

### Poor Queries (Too Vague)
❌ "I don't feel good"
❌ "Tell me about health"
❌ "Cure me"

---

## 🛡️ Safety Features

### Built-in Safeguards
1. **Disclaimer Reminders** - Every response includes disclaimer
2. **No Diagnosis** - Agents never provide definitive diagnoses
3. **Urgent Care Flags** - Recommends immediate medical attention when needed
4. **Educational Focus** - Information and guidance, not treatment
5. **Professional Referral** - Always suggests consulting doctors

---

## 🐛 Troubleshooting

### GUI doesn't open
**Solution:** Ensure tkinter is installed (comes with Python)

### "API key not found" error
**Solution:** Check `.env` file exists with `GOOGLE_API_KEY=your-key`

### Slow responses
**Solution:** 
- Normal for first query (initialization)
- Check internet connection
- Gemini API may be rate-limited

### Agent gives generic responses
**Solution:**
- Be more specific in your query
- Include relevant details (symptoms, duration, severity)
- Select the appropriate specialist

---

## 📖 Documentation

### For Users
- **This README** - Overview and usage
- **In-app help** - Tooltips and examples

### For Developers
- Code comments in all `.py` files
- Agent configuration documentation
- CrewAI framework docs: https://docs.crewai.com

---

## 🎓 Educational Use

### Great For:
- 📚 Learning about health conditions
- 💡 Understanding treatment options
- 🥗 Nutritional education
- 🧠 Mental health awareness
- 🏃 Fitness planning
- 📖 Medical terminology

### NOT For:
- ❌ Emergency situations
- ❌ Definitive diagnosis
- ❌ Prescribing medications
- ❌ Replacing doctor visits
- ❌ Medical emergencies (call 911/emergency services)

---

## 🔒 Privacy & Security

- ✅ **No data storage** - Queries are not saved
- ✅ **API secure** - Uses encrypted connections
- ✅ **Local processing** - Runs on your computer
- ✅ **No tracking** - No user data collection

**Note:** Queries are sent to Google Gemini API for processing. Review Google's privacy policy for details.

---

## 📊 Project Overview

| Feature | Healthcare Assistant |
|---------|---------------------|
| **Interface** | GUI + CLI |
| **AI Power** | Gemini 2.5 Flash |
| **Specialists** | 7 Healthcare Agents |
| **Scope** | Any health query |
| **Responses** | Comprehensive AI guidance |
| **Technology** | CrewAI Framework |
| **Safety** | Built-in disclaimers & safeguards |

---

## 📞 When to Seek Immediate Medical Help

**Call emergency services (911) if you have:**
- Chest pain or pressure
- Difficulty breathing
- Severe bleeding
- Loss of consciousness
- Severe allergic reaction
- Sudden severe headache
- Signs of stroke
- Suicidal thoughts

---

## 🎉 Get Started!

1. Install dependencies: `pip install -r requirements_crewai.txt`
2. Run GUI: `python healthcare_agent_gui.py`
3. Select a specialist
4. Describe your health query
5. Get intelligent guidance!

**Remember:** This is educational information. Always consult healthcare professionals for medical advice!

---

## 🔗 Resources

- **Gemini API:** https://ai.google.dev/
- **CrewAI Docs:** https://docs.crewai.com/
- **Get API Key:** https://makersuite.google.com/app/apikey

---

**Made with ❤️ for health education and awareness**

⚕️ Stay informed. Stay healthy. Consult professionals.
