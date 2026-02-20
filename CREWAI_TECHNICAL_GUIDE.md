# 📚 CrewAI Technical Documentation - Healthcare Assistant

Complete technical guide covering CrewAI framework, setup, API access, and implementation.

---

## 📑 Table of Contents

1. [CrewAI Framework Overview](#crewai-framework-overview)
2. [Environment Setup](#environment-setup)
3. [API Key Setup](#api-key-setup)
4. [CrewAI Core Components](#crewai-core-components)
5. [Tasks in CrewAI](#tasks-in-crewai)
6. [Tools in CrewAI](#tools-in-crewai)
7. [Complete Code Implementation](#complete-code-implementation)
8. [Functions Reference](#functions-reference)

---

## 🤖 CrewAI Framework Overview

### What is CrewAI?

**CrewAI** is a framework for orchestrating autonomous AI agents to work together on complex tasks.

**Official Website:** https://docs.crewai.com

### Key Concepts

```
Agent → Individual AI with specific role and expertise
  ↓
Task → Specific job assigned to an agent
  ↓
Crew → Collection of agents working together
  ↓
LLM → Large Language Model powering agents (Gemini)
```

### Why CrewAI?

- ✅ **Multi-Agent Systems** - Multiple specialized agents
- ✅ **Task Management** - Structured task execution
- ✅ **LLM Integration** - Works with various AI models
- ✅ **Flexible** - Easy customization
- ✅ **Production Ready** - Built for real applications

---

## ⚙️ Environment Setup

### 1. System Requirements

```
Python: 3.10 or higher
Operating System: Windows, macOS, Linux
Internet: Required for API calls
```

### 2. Install Dependencies

**Create requirements file:**
```txt
crewai>=1.4.1
crewai-tools>=1.4.1
litellm>=1.79.0
python-dotenv>=1.0.0
google-generativeai>=0.8.0
requests>=2.31.0
```

**Install command:**
```powershell
pip install -r requirements_crewai.txt
```

### 3. Verify Installation

```python
import crewai
print(crewai.__version__)

from crewai import Agent, Task, Crew, LLM
print("✅ CrewAI installed successfully!")
```

### 4. Environment Variables Setup

**Create `.env` file:**
```bash
GOOGLE_API_KEY=your-api-key-here
```

**Load in Python:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
```

---

## 🔑 API Key Setup

### How to Get Google Gemini API Key

#### Step 1: Visit Google AI Studio
**URL:** https://makersuite.google.com/app/apikey

#### Step 2: Sign In
- Use your Google account
- Accept terms of service

#### Step 3: Create API Key
1. Click "Create API Key"
2. Select existing project or create new
3. Copy the generated key

#### Step 4: Configure in Project

**Method 1: .env File (Recommended)**
```bash
# Create .env file in project root
GOOGLE_API_KEY=AIzaSyC4PTL-1JT6tEaZiObMaleCFtO9-lXC_Nc
```

**Method 2: Environment Variable**
```powershell
# Windows PowerShell
$env:GOOGLE_API_KEY="your-key-here"

# Linux/Mac
export GOOGLE_API_KEY="your-key-here"
```

**Method 3: Direct in Code (Not Recommended)**
```python
api_key = "AIzaSyC4PTL-1JT6tEaZiObMaleCFtO9-lXC_Nc"
```

### Access API Key in Code

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access API key
api_key = os.getenv("GOOGLE_API_KEY")

# Validate
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found!")

print(f"✅ API Key loaded: {api_key[:10]}...")
```

### API Key Security

- ✅ **DO:** Use .env files
- ✅ **DO:** Add .env to .gitignore
- ✅ **DO:** Keep keys private
- ❌ **DON'T:** Commit keys to Git
- ❌ **DON'T:** Share keys publicly
- ❌ **DON'T:** Hardcode in source

---

## 🧩 CrewAI Core Components

### 1. Agent Class

**Definition:**
An autonomous entity with specific role, goal, and expertise.

**Syntax:**
```python
from crewai import Agent

agent = Agent(
    role="Role Name",
    goal="What the agent aims to achieve",
    backstory="Agent's expertise and background",
    verbose=True/False,
    llm=llm_instance
)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `role` | str | Yes | Agent's job title/role |
| `goal` | str | Yes | Agent's objective |
| `backstory` | str | Yes | Agent's expertise/personality |
| `verbose` | bool | No | Print detailed logs (default: False) |
| `llm` | LLM | Yes | Language model instance |
| `tools` | list | No | Tools agent can use |
| `allow_delegation` | bool | No | Can delegate to other agents |
| `max_iter` | int | No | Max iterations (default: 25) |

**Example:**
```python
medical_advisor = Agent(
    role="Medical Advisor",
    goal="Provide accurate medical information",
    backstory="""You are an experienced medical advisor 
    with extensive knowledge of various conditions.""",
    verbose=False,
    llm=llm
)
```

### 2. Task Class

**Definition:**
A specific job assigned to an agent with expected output.

**Syntax:**
```python
from crewai import Task

task = Task(
    description="Detailed task description",
    agent=agent_instance,
    expected_output="What output should look like"
)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `description` | str | Yes | What task needs to do |
| `agent` | Agent | Yes | Which agent handles task |
| `expected_output` | str | Yes | Desired output format |
| `tools` | list | No | Tools for this task |
| `async_execution` | bool | No | Run asynchronously |
| `context` | list | No | Output from previous tasks |

**Example:**
```python
analysis_task = Task(
    description="""Analyze these symptoms and provide 
    possible explanations: headache, fever, fatigue""",
    agent=medical_advisor,
    expected_output="Comprehensive symptom analysis"
)
```

### 3. Crew Class

**Definition:**
Manages multiple agents and coordinates task execution.

**Syntax:**
```python
from crewai import Crew, Process

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    verbose=True/False,
    process=Process.sequential  # or Process.hierarchical
)

result = crew.kickoff()
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agents` | list | Yes | List of Agent instances |
| `tasks` | list | Yes | List of Task instances |
| `verbose` | bool | No | Print execution details |
| `process` | Process | No | Sequential or hierarchical |
| `manager_llm` | LLM | No | For hierarchical process |

**Example:**
```python
healthcare_crew = Crew(
    agents=[symptom_analyzer, treatment_advisor],
    tasks=[analyze_task, recommend_task],
    verbose=False
)

result = healthcare_crew.kickoff()
print(result)
```

### 4. LLM Class

**Definition:**
Language model configuration for agents.

**Syntax:**
```python
from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.7,
    api_key=api_key
)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | str | Yes | Model identifier |
| `temperature` | float | No | Creativity (0.0-1.0) |
| `api_key` | str | Yes | Authentication key |
| `max_tokens` | int | No | Max response length |

**Available Models:**
```python
"gemini/gemini-2.5-flash"      # Fast, free
"gemini/gemini-2.5-pro"        # More capable
"gemini/gemini-1.5-flash"      # Stable version
```

**Temperature Guide:**
- `0.0-0.3`: Focused, deterministic (medical facts)
- `0.4-0.7`: Balanced (general healthcare)
- `0.8-1.0`: Creative (wellness advice)

---

## 📋 Tasks in CrewAI

### Task Structure

```python
task = Task(
    description="""
    Multi-line description of what needs to be done.
    Can include:
    - Specific instructions
    - Context information
    - Format requirements
    """,
    agent=assigned_agent,
    expected_output="Clear description of desired result"
)
```

### Task Types in Healthcare App

#### 1. Analysis Task
```python
symptom_task = Task(
    description=f"""
    Analyze the following symptoms: {symptoms}
    
    Provide:
    1. Possible explanations
    2. Severity assessment
    3. When to seek help
    4. Self-care recommendations
    """,
    agent=symptom_analyzer,
    expected_output="Comprehensive symptom analysis"
)
```

#### 2. Recommendation Task
```python
treatment_task = Task(
    description=f"""
    Recommend treatment options for: {condition}
    
    Include:
    1. Evidence-based treatments
    2. Lifestyle modifications
    3. When to see doctor
    """,
    agent=treatment_recommender,
    expected_output="Treatment recommendations"
)
```

#### 3. Educational Task
```python
education_task = Task(
    description=f"""
    Explain {disease} in simple terms
    
    Cover:
    1. What it is
    2. Causes and risk factors
    3. Prevention strategies
    4. Management approaches
    """,
    agent=disease_educator,
    expected_output="Clear disease explanation"
)
```

### Task Execution

```python
# Create crew
crew = Crew(agents=[agent], tasks=[task])

# Execute
result = crew.kickoff()

# Access result
print(str(result))
```

---

## 🛠️ Tools in CrewAI

### What are Tools?

Tools extend agent capabilities with external functions and APIs.

### Built-in CrewAI Tools

```python
from crewai_tools import (
    SerperDevTool,      # Google search
    WebsiteSearchTool,  # Website scraping
    FileReadTool,       # Read files
    DirectoryReadTool   # Read directories
)
```

### Using Tools with Agents

```python
from crewai_tools import SerperDevTool

# Initialize tool
search_tool = SerperDevTool()

# Assign to agent
researcher = Agent(
    role="Researcher",
    goal="Find information",
    backstory="Expert researcher",
    tools=[search_tool],
    llm=llm
)
```

### Custom Tools

```python
from crewai.tools import tool

@tool("symptom_checker")
def check_symptoms(symptoms: str) -> str:
    """Checks symptoms against database"""
    # Your logic here
    return "Analysis result"

# Use in agent
agent = Agent(
    role="Doctor",
    tools=[check_symptoms],
    llm=llm
)
```

### Healthcare App Tools

Our app doesn't use external tools but leverages LLM capabilities:

```python
# No external tools needed
agent = Agent(
    role="Medical Advisor",
    goal="Provide medical information",
    backstory="Expert medical advisor",
    tools=[],  # Empty - uses LLM only
    llm=llm
)
```

---

## 💻 Complete Code Implementation

### Main Healthcare GUI Code

```python
"""
healthcare_agent_gui.py
Complete GUI implementation
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv
import threading

# Load environment
load_dotenv()

class HealthcareAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 AI Healthcare Assistant")
        self.root.geometry("1000x750")
        
        # Get API key
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            messagebox.showerror("Error", "API key not found!")
            return
        
        self.setup_ui()
        self.is_processing = False
    
    def execute_consultation(self, query):
        """Execute healthcare consultation"""
        try:
            # Get specialist
            specialist = self.role_var.get()
            
            # Agent configurations
            agent_configs = {
                "Medical Advisor": {
                    "role": "Medical Advisor",
                    "goal": "Provide accurate medical information",
                    "backstory": "Experienced medical advisor"
                },
                "Symptom Analyzer": {
                    "role": "Symptom Analyzer",
                    "goal": "Analyze symptoms and suggest conditions",
                    "backstory": "Symptom analysis expert"
                }
                # ... more specialists
            }
            
            config = agent_configs.get(specialist)
            
            # Create LLM
            llm = LLM(
                model="gemini/gemini-2.5-flash",
                temperature=0.7,
                api_key=self.api_key
            )
            
            # Create agent
            agent = Agent(
                role=config["role"],
                goal=config["goal"],
                backstory=config["backstory"],
                verbose=False,
                llm=llm
            )
            
            # Create task
            task = Task(
                description=f"""
                As a {specialist}, analyze: {query}
                
                Provide comprehensive guidance.
                """,
                agent=agent,
                expected_output="Healthcare guidance"
            )
            
            # Create crew and execute
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=False
            )
            
            result = crew.kickoff()
            
            # Display result
            self.root.after(0, self.display_result, str(result))
            
        except Exception as e:
            self.root.after(0, self.display_error, str(e))
```

### CLI Implementation

```python
"""
healthcare_agent_interactive.py
Interactive command-line version
"""

from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

load_dotenv()

def consult_healthcare_agent(specialist, query, api_key):
    """Execute consultation"""
    try:
        # Create LLM
        llm = LLM(
            model="gemini/gemini-2.5-flash",
            temperature=0.7,
            api_key=api_key
        )
        
        # Create agent
        agent = Agent(
            role=specialist,
            goal="Provide healthcare guidance",
            backstory="Healthcare expert",
            verbose=False,
            llm=llm
        )
        
        # Create task
        task = Task(
            description=query,
            agent=agent,
            expected_output="Healthcare guidance"
        )
        
        # Execute
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        
        result = crew.kickoff()
        return True, str(result)
        
    except Exception as e:
        return False, str(e)

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ API key not found!")
        return
    
    while True:
        # Get specialist and query
        specialist = get_specialist()
        query = get_query()
        
        # Run consultation
        success, result = consult_healthcare_agent(
            specialist, query, api_key
        )
        
        # Display result
        print(result)
        
        # Continue?
        if input("Continue? (yes/no): ") != 'yes':
            break

if __name__ == "__main__":
    main()
```

---

## 📖 Functions Reference

### Core Functions

#### 1. load_dotenv()
```python
from dotenv import load_dotenv

load_dotenv()
```
**Purpose:** Loads environment variables from .env file
**Returns:** None
**Usage:** Call once at program start

#### 2. os.getenv()
```python
api_key = os.getenv("GOOGLE_API_KEY")
```
**Purpose:** Gets environment variable value
**Parameters:** Variable name (string)
**Returns:** Variable value or None

#### 3. LLM()
```python
llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.7,
    api_key=api_key
)
```
**Purpose:** Creates language model instance
**Returns:** LLM object
**Usage:** Pass to Agent constructor

#### 4. Agent()
```python
agent = Agent(
    role="Doctor",
    goal="Help patients",
    backstory="Experienced doctor",
    llm=llm
)
```
**Purpose:** Creates AI agent
**Returns:** Agent object
**Usage:** Assign to tasks

#### 5. Task()
```python
task = Task(
    description="Analyze symptoms",
    agent=agent,
    expected_output="Analysis"
)
```
**Purpose:** Defines work for agent
**Returns:** Task object
**Usage:** Add to Crew

#### 6. Crew()
```python
crew = Crew(
    agents=[agent],
    tasks=[task]
)
```
**Purpose:** Manages agents and tasks
**Returns:** Crew object
**Usage:** Call kickoff() to execute

#### 7. crew.kickoff()
```python
result = crew.kickoff()
```
**Purpose:** Executes all tasks
**Returns:** Result object (convert to string)
**Usage:** Get final output

### GUI-Specific Functions

#### 1. threading.Thread()
```python
thread = threading.Thread(
    target=function,
    args=(arg1, arg2)
)
thread.daemon = True
thread.start()
```
**Purpose:** Run function in background
**Why:** Prevents GUI freezing
**Usage:** For long-running operations

#### 2. root.after()
```python
self.root.after(0, function, data)
```
**Purpose:** Schedule GUI update
**Why:** Thread-safe GUI updates
**Usage:** From worker threads

### Utility Functions

#### 1. str()
```python
result_str = str(result)
```
**Purpose:** Convert CrewAI result to string
**Usage:** For display or processing

#### 2. strip()
```python
clean_text = text.strip()
```
**Purpose:** Remove whitespace
**Usage:** Clean user input

---

## 🔄 Complete Execution Flow

### Step-by-Step Process

```
1. User Input
   ↓
2. Load API Key (from .env)
   ↓
3. Create LLM Instance
   ↓
4. Create Agent (with role, goal, backstory)
   ↓
5. Create Task (with description, agent)
   ↓
6. Create Crew (with agents, tasks)
   ↓
7. Execute: crew.kickoff()
   ↓
8. Get Result
   ↓
9. Display to User
```

### Code Flow

```python
# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Create LLM
llm = LLM(model="gemini/gemini-2.5-flash", api_key=api_key)

# 3. Create Agent
agent = Agent(role="Doctor", goal="Help", backstory="Expert", llm=llm)

# 4. Create Task
task = Task(description="Analyze X", agent=agent, expected_output="Y")

# 5. Create Crew
crew = Crew(agents=[agent], tasks=[task])

# 6. Execute
result = crew.kickoff()

# 7. Use Result
print(str(result))
```

---

## 📝 Summary

### Key Takeaways

1. **CrewAI** = Framework for multi-agent AI systems
2. **Agent** = AI with specific role and expertise
3. **Task** = Work assigned to agent
4. **Crew** = Manages agents and tasks
5. **LLM** = AI model (Gemini) powering agents

### Essential Code Pattern

```python
# Load environment
from dotenv import load_dotenv
import os
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create LLM
from crewai import LLM
llm = LLM(model="gemini/gemini-2.5-flash", api_key=api_key)

# Create Agent
from crewai import Agent
agent = Agent(role="Role", goal="Goal", backstory="Story", llm=llm)

# Create Task
from crewai import Task
task = Task(description="Do X", agent=agent, expected_output="Y")

# Execute
from crewai import Crew
crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()

# Use result
print(str(result))
```

---

**Made with ❤️ for AI Healthcare Assistant**

🏥 Complete technical reference for CrewAI implementation
