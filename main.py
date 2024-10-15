import streamlit as st
from static import Static
from crews import Crews

def main():
    
    Static.config()
    Static.styling()
    Static.logo('gema.png')
    Static.title('HISTORIAN GPT')
    
    with st.form("historian_form"):
        question = st.text_input("Question", placeholder="What historical event do you want to know about?", key="question", help="Ask any historical question.")
        location = st.text_input("Location", placeholder="Enter a specific location if relevant", key="location", help="Optional location for narrowing down the historical context.")
        language = st.text_input("Language", placeholder="Enter a language for the output", key="language", help="Choose the language for the answer.")
        submit_button = st.form_submit_button(label="Ask HistorianGPT")    
    
        if submit_button:
            
            Static.load_api()
            
            inputs = {'question': question, 'location': location, 'language': language}
            
            crew = Crews(question=question, location=location, language=language)
                        
            validation_result = crew.validate_crew().kickoff(inputs=inputs)
                
            if str(validation_result).lower().strip() == "yes":
                
                st.success("Validation successful! Proceeding with research...")
                
                crew_output = crew.main_crew().kickoff()
                                
                st.markdown(f"""
                            {crew_output}
                            """)
            else:
                st.error("Validation failed. Please check your inputs.")
        
if __name__ == "__main__":
    main()