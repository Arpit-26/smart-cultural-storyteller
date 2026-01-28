# models/story_generator.py
from gpt4all import GPT4All
import os
import re

# Load Orca Mini 3B model (optimized for low-spec machines)
model_path = os.path.join(os.path.dirname(__file__), "q4_0-orca-mini-3b.gguf")
model = GPT4All(model_path)



# approch 2

def generate_story(prompt: str, max_tokens: int = 280) -> str:
    """
    Generate an engaging story with clear paragraphs per scene.
    Uses Orca Mini model.
    """
    try:
        # Structured prompt for scene-based output
        enhanced_prompt = (
            f"Write a short story about {prompt}.\n\n"
            "Structure the story into 3–4 short paragraphs:\n"
            "1. Beginning: Introduce setting and characters.\n"
            "2. Middle: Describe the main conflict or event.\n"
            "3. Ending: Provide a resolution and conclusion.\n\n"
            "Make it vivid, easy to follow, and entertaining."
        )

        with model.chat_session():
            response = model.generate(
                enhanced_prompt,
                max_tokens=max_tokens,
                temp=0.75,
                top_p=0.9,
                top_k=40,
                repeat_penalty=1.15
            )

        # Cleanup
        story = response.strip()
        story = story.replace("assistant:", "").replace("user:", "")
        story = " ".join(story.split())

        # Split into paragraphs per scene (English only)
        sentences = story.split(". ")
        grouped = []
        buffer = []
        for i, sentence in enumerate(sentences, 1):
            sentence = sentence.strip()
            if sentence:
                buffer.append(sentence)
            if i % 3 == 0 or i == len(sentences):
                grouped.append(". ".join(buffer).strip() + ".")
                buffer = []

        return "\n\n".join(grouped)

    except Exception as e:
        print(f"Story englis to hindi translation error: {e}")   
        return f"Error generating story: {e}"






def translate_to_hindi(english_text: str) -> str:
    """
    Translate English text to Hindi using a simpler, more reliable approach.
    """
    try:
        import requests
        
        # Simple, reliable translation approach
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': 'en',  # source language: English
            'tl': 'hi',  # target language: Hindi
            'dt': 't',   # return translation
            'q': english_text.strip()
        }
        
        response = requests.get(url, params=params, timeout=5)  # Shorter timeout
        if response.status_code == 200:
            result = response.json()
            # Extract translated text from response
            translated_text = ""
            if result and len(result) > 0 and result[0]:
                for translation_part in result[0]:
                    if translation_part and translation_part[0]:
                        translated_text += translation_part[0]
            
            if translated_text.strip():
                # Post-processing for more natural Hindi
                hindi_text = post_process_hindi_translation(translated_text)
                return hindi_text
            else:
                return english_text  # Fallback to original
        else:
            return english_text  # Fallback to original
            
    except Exception as e:
        print(f"Translation error: {e}")
        return english_text  # Return original if translation fails



import re

def post_process_hindi_translation(hindi_text: str, sentences_per_paragraph: int = 3) -> str:
    """
    Post-process Hindi translation for natural flow and readability.
    Also splits the story into paragraphs per scene.
    
    Args:
        hindi_text: The raw translated Hindi story.
        sentences_per_paragraph: Number of sentences per paragraph for scene grouping.
    Returns:
        Cleaned and paragraph-formatted Hindi story.
    """
    try:
        # Common replacements for more natural Hindi
        replacements = {
            'एक बार': 'एक समय',
            'वह था': 'था',
            'वह थी': 'थी',
            'बहुत समय पहले': 'बहुत पुराने समय में',
            'अंत में': 'अंततः',
            'और फिर': 'फिर',
            'इसके बाद': 'उसके बाद',
            'वे सभी': 'सभी',
            'बहुत खुश': 'अत्यंत प्रसन्न',
            'बहुत दुखी': 'अत्यंत दुखी',
            'के साथ साथ': 'के साथ',
            'में से एक': 'में से',
            'की तरह': 'के समान',
            'के लिए': 'हेतु',
            'के द्वारा': 'से',
            'के कारण': 'की वजह से',
        }
        
        # Apply replacements
        for old, new in replacements.items():
            hindi_text = hindi_text.replace(old, new)
        
        # Clean up spaces and punctuation
        hindi_text = re.sub(r'\s+', ' ', hindi_text)
        hindi_text = re.sub(r'\s+([।,!?])', r'\1', hindi_text)
        hindi_text = re.sub(r'([।,!?])\s*([।,!?])', r'\1 \2', hindi_text)
        
        # Ensure proper sentence ending
        if hindi_text and not hindi_text.endswith(('।', '!', '?', '"', "'")):
            if hindi_text.endswith('.'):
                hindi_text = hindi_text[:-1] + '।'
            else:
                hindi_text += '।'
        
        # Split into paragraphs per scene
        sentences = hindi_text.split('।')
        grouped = []
        buffer = []
        for i, sentence in enumerate(sentences, 1):
            sentence = sentence.strip()
            if sentence:
                buffer.append(sentence + '।')
            if i % sentences_per_paragraph == 0 or i == len(sentences):
                grouped.append(" ".join(buffer).strip())
                buffer = []

        return "\n\n".join(grouped)
    
    except Exception as e:
        print(f"Post-processing error: {e}")
        return hindi_text.strip()



def generate_cultural_story(theme: str,  language: str = "English") -> str:
    """
    Generate a detailed cultural story suitable for video generation.
    Always generates in English first, then translates if needed.
    """
    # culture_context = f" from {culture} culture" if culture else ""
    print("generate_cultural_story func language :"+language)
    # Always generate in English first
    prompt = f"Tell a short and captivating {theme} story  with indian cultural details.. Include characters, vivid descriptions, and a complete narrative with cultural elements."
    
    english_story = generate_story(prompt, max_tokens=260)
    
    # Translate to Hindi if requested
    if language.strip().lower() == "hindi":
        return translate_to_hindi(english_story),english_story
    else:
        return english_story, english_story
