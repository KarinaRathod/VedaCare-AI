"""
AI Ayurvedic Assistant - Interactive CLI
Specialized Ayurvedic agents powered by CrewAI and Gemini AI
"""

from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()

def print_header():
    """Display welcome header"""
    # 1. UPDATED HEADER TEXT
    print("\n" + "=" * 80)
    print("🌿 AI AYURVEDIC ASSISTANT")
    print("Personalized Dosha Guidance | Herbal & Lifestyle Advice")
    print("=" * 80)
    print("⚠️  DISCLAIMER: This system is based on traditional Ayurvedic principles.")
    print("It is for informational purposes only and is NOT a substitute for")
    print("consulting a qualified Ayurvedic or modern medical professional.")
    print("=" * 80)
    print()

def get_healthcare_specialist():
    """Let user select healthcare specialist"""
    print("🌿 SELECT AYURVEDIC SPECIALIST:")
    print()
    
    # 2. UPDATED SPECIALIST LIST FOR AYURVEDA
    specialists = {
        '1': ('Prakriti & Dosha Analyst', 'Determine constitution and current imbalance (Vikriti)'),
        '2': ('Ayurvedic Lifestyle Advisor', 'Suggest Dinacharya and Ritucharya for balance'),
        '3': ('Herbal & Remedy Guide', 'Suggest traditional herbs (Dravyaguna) and home remedies'),
        '4': ('Ahara (Diet) Specialist', 'Offer food recommendations specific to Dosha imbalance'),
        '5': ('Yoga & Pranayama Guide', 'Recommend specific Asanas and breathing techniques'),
        '6': ('Agni & Ama Consultant', 'Analyze digestion (Agni) and toxin (Ama) symptoms')
    }
    
    for key, (role, desc) in specialists.items():
        print(f"  {key}. {role:<25} - {desc}")
    
    print()
    choice = input("Enter your choice (1-6): ").strip() # Adjusted range
    
    if choice in specialists:
        role, description = specialists[choice]
        return role, description
    else:
        print("⚠️  Invalid choice. Using default 'Prakriti & Dosha Analyst'")
        return specialists['1']

def get_health_query():
    """Get health query from user"""
    print("\n" + "-" * 80)
    print("📝 DESCRIBE YOUR SYMPTOMS AND LIFESTYLE (for Ayurvedic analysis)")
    print("-" * 80)
    print()
    # 3. UPDATED EXAMPLES
    print("Examples:")
    print("  • I have joint pain, dry skin, and I feel anxious. My sleep is light and irregular.")
    print("  • I have excess heat, quick temper, and crave cooling foods. I have frequent acidity.")
    print("  • I feel sluggish, gain weight easily, and have high mucus. What should my diet be?")
    print()
    print("Your query (press Enter twice when done):")
    print()
    
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            if lines:
                break
    
    return ' '.join(lines)

def consult_healthcare_agent(specialist, description, query, api_key):
    """Execute healthcare consultation"""
    print("\n" + "=" * 80)
    print(f"🔍 {specialist.upper()} IS ANALYZING YOUR QUERY...")
    print("=" * 80)
    print()
    
    try:
        # 4. UPDATED AGENT CONFIGURATIONS FOR AYURVEDA
        agent_configs = {
            "Prakriti & Dosha Analyst": {
                "goal": "Determine the user's innate Prakriti (constitution) and current Dosha imbalance (Vikriti)",
                "backstory": """You are a highly knowledgeable Ayurvedic expert with deep understanding of 
                Tridosha theory (Vata, Pitta, Kapha). Your role is to analyze a user's physical and mental 
                characteristics, lifestyle, and symptoms to accurately assess their fundamental constitution 
                and identify the current state of Dosha imbalance. You frame all advice based on this analysis."""
            },
            "Ayurvedic Lifestyle Advisor": {
                "goal": "Provide personalized Dinacharya (daily) and Ritucharya (seasonal) recommendations",
                "backstory": """You are an expert in Ayurvedic lifestyle and routines. You provide detailed guidance 
                on daily practices (Dinacharya), including waking, cleansing, exercise, and sleep, as well as 
                seasonal adjustments (Ritucharya) to maintain balance and prevent illness."""
            },
            "Herbal & Remedy Guide": {
                "goal": "Suggest traditional Ayurvedic herbs (Dravyaguna) and practical home remedies",
                "backstory": """You are a specialist in Ayurvedic pharmacology (Dravyaguna). You suggest common, 
                safe, and effective herbs, spices, and simple home remedies based on their Rasa (taste), 
                Virya (potency), and Vipaka (post-digestive effect) to balance the specific Dosha imbalance mentioned."""
            },
            "Ahara (Diet) Specialist": {
                "goal": "Provide personalized Ahara (dietary) guidance to balance the current Dosha imbalance",
                "backstory": """You are an Ayurvedic nutritionist, expert in the principles of Ahara and its 
                effect on Agni. You recommend specific Rasa (tastes), cooking methods, and food combinations 
                that are appropriate for restoring health based on the user's Dosha imbalance (Vikriti)."""
            },
            "Yoga & Pranayama Guide": {
                "goal": "Recommend specific Yoga Asanas, Pranayama, and meditation techniques for physical and mental balance",
                "backstory": """You are a certified Yoga and Pranayama instructor with knowledge of therapeutic 
                applications in Ayurveda. You suggest practices that are either calming (Vata/Pitta) or stimulating 
                (Kapha) to address the root Dosha imbalance and promote physical and mental well-being."""
            },
            "Agni & Ama Consultant": {
                "goal": "Analyze symptoms related to Agni (digestive fire) and Ama (toxins) and suggest cleansing measures",
                "backstory": """You are an Ayurvedic consultant specializing in digestion. You interpret symptoms 
                to assess the state of the user's Agni (Mandagni, Tikshnagni, Vishamagni) and the presence of Ama. 
                You recommend gentle detoxifying measures, fasting protocols, and specific dietary adjustments to rekindle Agni."""
            }
        }
        
        config = agent_configs.get(specialist, agent_configs["Prakriti & Dosha Analyst"])
        
        # Create LLM
        llm = LLM(
            model="gemini/gemini-2.5-flash",
            temperature=0.7,
            api_key=api_key
        )
        
        # Create healthcare agent
        agent = Agent(
            role=specialist,
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=False,
            llm=llm
        )
        
        # 4. UPDATED TASK INSTRUCTIONS FOR AYURVEDA
        task = Task(
            description=f"""
            As a {specialist}, analyze the following health query from a purely **Ayurvedic perspective**:
            
            QUERY: {query}
            
            INSTRUCTIONS:
            1. Base the analysis on **Tridosha theory** (Vata, Pitta, Kapha) and the state of **Agni** and **Ama**.
            2. Suggest the likely **Dosha imbalance (Vikriti)** causing the symptoms.
            3. Provide actionable, personalized recommendations for **Ahara (diet), Vihara (lifestyle)**, and 
               **Dravyaguna (herbs/spices)** to restore balance.
            4. Explain the reasoning using Ayurvedic terminology (e.g., 'pitta-pacifying,' 'kapha-aggravating').
            5. Strictly adhere to the disclaimer—this is for informational, educational purposes in the context of traditional Ayurveda.
            6. Be compassionate and supportive in tone.
            
            Provide a comprehensive, well-structured response following these principles.
            """,
            agent=agent,
            expected_output="Comprehensive Ayurvedic guidance based on Dosha analysis, diet, and lifestyle recommendations."
        )
        
        # Create and run crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        
        result = crew.kickoff()
        
        return True, str(result)
        
    except Exception as e:
        return False, f"Error: {str(e)}\nPlease check your internet connection and API key."

def display_consultation_result(success, result, specialist):
    """Display the consultation response"""
    print("\n" + "=" * 80)
    if success:
        print(f"💡 {specialist.upper()} RESPONSE:")
    else:
        print("❌ ERROR:")
    print("=" * 80)
    print()
    print(result)
    print()
    print("=" * 80)
    if success:
        # 5. UPDATED FINAL DISCLAIMER
        print("⚠️  AYURVEDIC DISCLAIMER: This information is based on traditional Ayurvedic principles.")
        print("Always consult a qualified Ayurvedic Practitioner or modern healthcare professional for")
        print("personalized medical advice, diagnosis, or treatment.")
        print("=" * 80)

def main():
    """Main program loop"""
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("\n❌ ERROR: GOOGLE_API_KEY not found!")
        print("\nPlease ensure .env file exists with your API key.")
        print("Format: GOOGLE_API_KEY=your-key-here")
        return
    
    print_header()
    
    while True:
        # Get specialist
        specialist, description = get_healthcare_specialist()
        print(f"\n✅ Selected: {specialist}")
        print(f"   {description}")
        
        # Get query
        query = get_health_query()
        
        if not query.strip():
            print("\n⚠️  No query entered. Please try again.")
            continue
        
        # Run consultation
        success, result = consult_healthcare_agent(specialist, description, query, api_key)
        
        # Display result
        display_consultation_result(success, result, specialist)
        
        # Ask to continue
        print("\n" + "-" * 80)
        continue_choice = input("Would you like another consultation? (yes/no): ").strip().lower()
        
        if continue_choice not in ['yes', 'y']:
            print("\n👋 Thank you for using AI Ayurvedic Assistant!")
            print("Stay healthy and take care!")
            print("=" * 80)
            break
        
        print("\n\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Take care!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")