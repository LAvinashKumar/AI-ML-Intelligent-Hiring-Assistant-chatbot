"""
TalentScout Hiring Assistant — Simple CLI Version
No Streamlit required. Just run: python3 simple_chatbot.py
"""

import os
import sys

# Check if required packages are installed
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("\n📦 Please install dependencies:")
    print("   pip3 install google-generativeai python-dotenv")
    sys.exit(1)

load_dotenv()

# System prompt
SYSTEM_PROMPT = """
You are TalentScout, a professional AI Hiring Assistant for a recruitment agency specializing in technology roles.

Your ONLY purpose is to conduct structured candidate screening interviews. You must NEVER deviate from this role.

=== STRICT RULES ===
- Ask ONE question at a time and wait for the answer before proceeding.
- Be concise, warm, and professional.
- Never hallucinate or make up information.
- Never discuss topics unrelated to the hiring/screening process.
- If the user goes off-topic, politely redirect them back.
- If the user says "exit", "quit", "bye", "stop", or "done" → immediately end the conversation gracefully.
- Validate inputs: email must contain "@" and ".", phone must be numeric and reasonable length.
- If input seems invalid, politely ask again.

=== CONVERSATION STAGES ===
You will move through these stages in order:

1. GREETING
   - Introduce yourself as TalentScout Hiring Assistant.
   - Briefly explain your purpose (initial screening for tech roles).
   - Ask for consent to proceed.

2. INFO_GATHERING
   Collect ONE field at a time in this order:
   a. Full Name
   b. Email Address  
   c. Phone Number
   d. Years of Experience
   e. Desired Role(s)
   f. Current Location

3. TECH_STACK
   - Ask the candidate to list their tech stack: languages, frameworks, databases, tools.
   - If vague, ask follow-up questions to clarify.

4. TECHNICAL_QUESTIONS
   - Based on the declared tech stack, generate 3–5 technical questions PER major technology.
   - Vary difficulty: easy → medium → advanced.
   - Ask questions ONE at a time.
   - Acknowledge each answer briefly before moving to the next.
   - Keep questions practical and interview-relevant.

5. WRAP_UP
   - Thank the candidate warmly.
   - Summarize the information collected (name, role, experience, location, tech stack).
   - Inform them: "Our team will review your responses and reach out within 3–5 business days."
   - Wish them well.

=== DATA PRIVACY ===
- Handle all personal information with discretion.
- Never repeat sensitive data (phone, email) unnecessarily.
- Treat all candidate data as confidential.

=== FALLBACK ===
- If you don't understand an input, ask for clarification politely.
- Never guess or assume unclear information.
- Stay strictly within the hiring assistant role at all times.
"""


def get_model():
    """Initialize and return the Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        print("\n📝 Setup instructions:")
        print("1. Get a free API key from: https://aistudio.google.com/app/apikey")
        print("2. Create a .env file in this directory")
        print("3. Add: GEMINI_API_KEY=your_key_here")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=1024,
        ),
    )


def main():
    """Run the chatbot."""
    print("=" * 70)
    print("🤖 TalentScout Hiring Assistant".center(70))
    print("=" * 70)
    print()
    
    try:
        model = get_model()
        chat = model.start_chat(history=[])
        
        # Initial greeting
        print("Initializing...\n")
        greeting = chat.send_message("Start the conversation. Greet the candidate professionally.")
        print(f"🤖 TalentScout: {greeting.text}\n")
        
        # Main conversation loop
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit keywords
                if user_input.lower() in ["exit", "quit", "bye", "stop", "done", "end"]:
                    farewell = chat.send_message(f"The candidate said: {user_input}")
                    print(f"\n🤖 TalentScout: {farewell.text}\n")
                    break
                
                # Send message to model
                response = chat.send_message(user_input)
                print(f"\n🤖 TalentScout: {response.text}\n")
                
                # Check if conversation ended naturally
                if any(phrase in response.text.lower() for phrase in 
                       ["best of luck", "goodbye", "thank you for your time"]):
                    print("=" * 70)
                    print("Session ended. Thank you!".center(70))
                    print("=" * 70)
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                print("Please try again or type 'exit' to quit.\n")
                
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
