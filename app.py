import streamlit as st
from gtts import gTTS
import os
import base64
import random
import re

class TextToSpeechConverter:
    def __init__(self):
        # Supported languages
        self.languages = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it"
        }
        
        # Voice tone modifications
        self.tone_modifications = {
            "Normal": self._normal_tone,
            "Excited": self._excited_tone,
            "Sad": self._sad_tone,
            "Formal": self._formal_tone,
            "Casual": self._casual_tone,
            "Dramatic": self._dramatic_tone
        }
    
    def _normal_tone(self, text):
        """Standard text without modifications"""
        return text
    
    def _excited_tone(self, text):
        """Add excitement and energy to the text"""
        excitement_words = [
            "Wow!", "Amazing!", "Incredible!", "Fantastic!", "Awesome!"
        ]
        # Add excitement markers
        text = text + " " + random.choice(excitement_words)
        
        # Capitalize for emphasis
        words = text.split()
        words = [word.upper() if len(word) > 3 and random.random() < 0.3 else word for word in words]
        return " ".join(words)
    
    def _sad_tone(self, text):
        """Modify text to sound more melancholic"""
        sad_prefixes = [
            "Sadly,", "With a heavy heart,", "Unfortunately,", "In sorrow,"
        ]
        sad_suffixes = [
            "...", "♥", "😢", "with a deep sigh"
        ]
        return f"{random.choice(sad_prefixes)} {text} {random.choice(sad_suffixes)}"
    
    def _formal_tone(self, text):
        """Convert text to a more professional tone"""
        formal_replacements = {
            "good": "excellent",
            "bad": "unsatisfactory",
            "thing": "matter",
            "stuff": "materials"
        }
        
        # Replace casual words
        for casual, formal in formal_replacements.items():
            text = re.sub(r'\b{}\b'.format(casual), formal, text, flags=re.IGNORECASE)
        
        return f"Hereby, {text}. Respectfully submitted."
    
    def _casual_tone(self, text):
        """Make text sound more conversational and relaxed"""
        casual_prefixes = [
            "Hey,", "So,", "Like,", "Basically,", "You know,"
        ]
        filler_words = [
            "um", "like", "you know", "basically"
        ]
        
        # Add casual prefix
        text = f"{random.choice(casual_prefixes)} {text}"
        
        # Potentially add a filler word
        if random.random() < 0.4:
            words = text.split()
            words.insert(random.randint(0, len(words)), random.choice(filler_words))
            text = " ".join(words)
        
        return text
    
    def _dramatic_tone(self, text):
        """Add dramatic flair to the text"""
        dramatic_prefixes = [
            "In a world where...", "Behold!", "Lo and behold,", "Hear ye,"
        ]
        dramatic_suffixes = [
            "...and so it begins.", "...the saga continues.", "...destiny awaits."
        ]
        
        # Break text into dramatic segments
        words = text.split()
        dramatic_words = [word.upper() if len(word) > 4 and random.random() < 0.5 else word for word in words]
        
        return (f"{random.choice(dramatic_prefixes)} " + 
                " ".join(dramatic_words) + 
                f" {random.choice(dramatic_suffixes)}")
    
    def convert_text_to_speech(self, text, language_code, tone="Normal"):
        """
        Convert text to speech with tone modification
        """
        try:
            # Ensure output directory exists
            os.makedirs('audio_outputs', exist_ok=True)
            
            # Apply tone modification
            modified_text = self.tone_modifications[tone](text)
            
            # Generate unique filename
            output_filename = f'audio_outputs/speech_{tone}_{hash(modified_text)}.mp3'
            
            # Create text-to-speech object
            tts = gTTS(text=modified_text, lang=language_code)
            
            # Save the audio file
            tts.save(output_filename)
            
            return output_filename, modified_text
        
        except Exception as e:
            st.error(f"Error generating speech: {e}")
            return None, None

def main():
    # Initialize converter
    converter = TextToSpeechConverter()
    
    # Set page configuration
    st.set_page_config(
        page_title="Expressive Text-to-Speech",
        page_icon="🎙️",
        layout="wide"
    )
    
    # Title
    st.title("🎙️ Expressive Text-to-Speech Converter")
    
    # Create columns
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Text input
        text_input = st.text_area(
            "Enter Text to Convert", 
            height=300,
            placeholder="Type or paste your text here..."
        )
    
    with col2:
        # Language selection
        selected_language = st.selectbox(
            "Select Language", 
            list(converter.languages.keys())
        )
    
    with col3:
        # Tone selection
        selected_tone = st.selectbox(
            "Select Tone", 
            list(converter.tone_modifications.keys())
        )
    
    # Tone description
    st.info(f"🔊 {selected_tone} Tone: {converter.tone_modifications[selected_tone].__doc__}")
    
    # Convert button
    if st.button("Generate Expressive Speech"):
        if text_input:
            try:
                # Get language code
                language_code = converter.languages[selected_language]
                
                # Convert text to speech
                audio_file, modified_text = converter.convert_text_to_speech(
                    text_input, 
                    language_code, 
                    selected_tone
                )
                
                if audio_file:
                    # Display audio player
                    st.audio(audio_file, format='audio/mp3')
                    
                    # Show modified text
                    st.subheader("Modified Text")
                    st.write(modified_text)
                    
                    # Download link
                    with open(audio_file, 'rb') as f:
                        audio_bytes = f.read()
                    
                    st.download_button(
                        label="Download MP3",
                        data=audio_bytes,
                        file_name=f"speech_{selected_tone}.mp3",
                        mime="audio/mp3"
                    )
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter some text to convert")
    
    # Sidebar information
    st.sidebar.header("About Tones")
    st.sidebar.info("""
    Choose from different voice tones:
    - Normal: Standard speech
    - Excited: High energy and enthusiasm
    - Sad: Melancholic and emotional
    - Formal: Professional and refined
    - Casual: Conversational and relaxed
    - Dramatic: Theatrical and intense
    """)

# Run the main function
if __name__ == "__main__":
    main()