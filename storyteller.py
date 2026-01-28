import os
from dotenv import load_dotenv
from elevenlabs import generate, save, set_api_key

# Load environment variables
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise ValueError("ELEVENLABS_API_KEY is missing from .env file")

print("ELEVENLABS_API_KEY loaded successfully.")


# Set API key globally
set_api_key(api_key)


# # Initialize ElevenLabs client
# elevenlabs = ElevenLabs(api_key=api_key)

# Indian regional voice mapping for cultural storytelling
VOICE_MAPPING = {
    "English": "1qEiC6qsybMkmnNdVMbK",  # Bella voice for English
    "Hindi": "1qEiC6qsybMkmnNdVMbK",    # Default Hindi voice
    "Hindi-North": "vT0wMbLG5dssaBsksrb6",     # North Indian accent
    "Hindi-South": "izSi63MW0URDnszWlZMX",     # South Indian harini accent  
    "Hindi-West": "E2bgV4fdtiboH3Y1CEuQ",      # West Indian accent
    "Hindi-East": "1qEiC6qsybMkmnNdVMbK",      # East Indian accent
    "Hindi-Central": "1qEiC6qsybMkmnNdVMbK"    # Central Indian accent
}

# Indian regional accent detection based on cultural context
REGIONAL_ACCENTS = {
    "Punjabi": "Hindi-North",
    "Bengali": "Hindi-East",
    "Marathi": "Hindi-West",
    "Tamil": "Hindi-South",
    "Telugu": "Hindi-South",
    "Gujarati": "Hindi-West",
    "Rajasthani": "Hindi-North",
    "Bihari": "Hindi-East"
}

# Cultural themes for story generation
CULTURAL_THEMES = {
    "folklore": "Traditional folk tales and legends",
    "mythology": "Ancient myths and divine stories", 
    "festivals": "Cultural celebrations and traditions",
    "heroes": "Cultural heroes and legendary figures",
    "wisdom": "Traditional wisdom and moral tales",
    "nature": "Stories about nature and animals",
    "family": "Family values and relationships",
    "adventure": "Cultural adventures and journeys"
}

def generate_audio(text: str, filename="story_audio.mp3", language="English") -> str:
    """
    Generate audio narration with multi-language support.
    Optimized for cultural storytelling.
    """
    try:
        # Select appropriate voice for language
        voice = VOICE_MAPPING.get(language, VOICE_MAPPING["English"])
        
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_multilingual_v2"
        )

        save(audio, filename)
        return filename

    except Exception as e:
        return f"Error generating audio: {e}"
    

def get_cultural_themes():
    """Return available cultural themes for story generation."""
    return CULTURAL_THEMES

def get_supported_languages():
    """Return list of supported languages for narration."""
    return list(VOICE_MAPPING.keys())

def detect_regional_accent(culture: str, region: str = None) -> str:
    """
    Detect appropriate Indian regional accent based on culture and region.
    """
    if not culture or "Indian" not in culture:
        return "English"
    
    # If specific region is provided, use it
    if region and region in REGIONAL_ACCENTS:
        return REGIONAL_ACCENTS[region]
    
    # Auto-detect based on culture keywords
    culture_lower = culture.lower()
    for region_key, accent in REGIONAL_ACCENTS.items():
        if region_key.lower() in culture_lower:
            return accent
    
    # Default to standard Hindi
    return "Hindi"

def generate_audio_with_accent(text: str, culture: str = "Indian", region: str = None, filename="story_audio.mp3") -> str:
    """
    Generate audio with appropriate Indian regional accent.
    """
    try:
        # Detect appropriate accent
        language = detect_regional_accent(culture, region)
        
        # Select appropriate voice for detected accent
        voice = VOICE_MAPPING.get(language, VOICE_MAPPING["English"])
        
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_multilingual_v2"
        )

        save(audio, filename)
        return filename

    except Exception as e:
        return f"Error generating audio: {e}"

def generate_cultural_facts(culture: str) -> str:
    """
    Generate interesting cultural facts to enhance stories.
    """
    cultural_facts = {
        "Indian": "भारत में 1,600 से अधिक भाषाएं हैं और यह दुनिया का सबसे बड़ा लोकतंत्र है।",
        "North Indian": "उत्तर भारत में गंगा-यमुना का मैदान है और यहाँ समृद्ध मुगल विरासत है।",
        "South Indian": "दक्षिण भारत में द्रविड़ संस्कृति है और यहाँ के मंदिर वास्तुकला के अद्भुत नमूने हैं।",
        "West Indian": "पश्चिम भारत व्यापार का केंद्र है और यहाँ बॉलीवुड की जन्मभूमि मुंबई है।",
        "East Indian": "पूर्व भारत में बंगाली संस्कृति है और यहाँ कला, साहित्य और संगीत की समृद्ध परंपरा है।",
        "Central Indian": "मध्य भारत में वन संपदा है और यहाँ आदिवासी संस्कृति की अनूठी परंपराएं हैं।",
        "Chinese": "China has a 5,000-year history and invented paper, gunpowder, and the compass.",
        "Japanese": "Japan has a unique concept of 'ikigai' - finding purpose in life through passion and mission.",
        "African": "Africa is the birthplace of humanity and has over 3,000 distinct ethnic groups.",
        "European": "Europe has influenced world culture through art, philosophy, and scientific discoveries.",
        "Native American": "Native Americans have rich oral traditions and deep connections to nature.",
        "Middle Eastern": "The Middle East is the cradle of civilization and birthplace of major religions.",
        "Latin American": "Latin America has vibrant traditions mixing indigenous, European, and African cultures."
    }
    
    return cultural_facts.get(culture, "हर संस्कृति की अपनी अनूठी परंपराएं और ज्ञान होता है।")
