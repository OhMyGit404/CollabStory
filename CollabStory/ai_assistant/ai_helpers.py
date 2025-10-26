import google.generativeai as genai
import os
import random
from django.conf import settings

def generate_ai_suggestion(context, prompt_type, story_genre=None):
    """
    Generate AI writing suggestions using Google Gemini API
    """
    prompts = {
        'plot_twist': f"Generate an unexpected plot twist for this {story_genre or 'story'} context:",
        'character': "Suggest character development or a new character introduction:",
        'dialogue': "Write compelling dialogue that fits this scene:",
        'setting': "Describe a vivid setting that continues this story:",
        'conflict': "Introduce a new conflict or challenge:",
        'continuation': "Continue the story naturally from this point:",
        'description': "Add rich, descriptive details to enhance this scene:"
    }
    
    prompt = f"{prompts.get(prompt_type, prompts['continuation'])}\n\nContext: {context}\n\nSuggestion:"
    
    try:
        # Check if Gemini API key is configured
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key or api_key == "your-gemini-api-key-here":
            return get_fallback_suggestion(prompt_type, story_genre)
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Create the full prompt with system instructions
        full_prompt = f"""You are a creative writing assistant. Provide concise, imaginative suggestions that inspire writers. Keep responses under 200 words and be creative and engaging.

{prompt}"""
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=200,
                temperature=0.8,
                top_p=0.8,
                top_k=40
            )
        )
        
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return get_fallback_suggestion(prompt_type, story_genre)

def get_fallback_suggestion(prompt_type, story_genre=None):
    """Fallback suggestions if API fails"""
    fallback_suggestions = {
        'plot_twist': [
            "The protagonist discovers they've been living in a simulation",
            "The trusted mentor is actually the villain",
            "The magical artifact was a distraction from the real power within",
            "A character thought to be dead returns with crucial information",
            "The entire adventure was a test of character"
        ],
        'character': [
            "Introduce a character with a hidden connection to the past",
            "Reveal a secret talent or fear in an existing character",
            "Create a character who sees the world completely differently",
            "Add a character who challenges the protagonist's beliefs",
            "Introduce someone from the protagonist's forgotten past"
        ],
        'dialogue': [
            "Add tension with a character who speaks in riddles",
            "Create conflict through a heated argument",
            "Reveal important information through casual conversation",
            "Show character growth through their choice of words",
            "Add humor with witty banter between characters"
        ],
        'setting': [
            "Describe a mysterious location that changes the mood",
            "Add atmospheric details that enhance the tension",
            "Create a setting that reflects the characters' emotions",
            "Describe a place that holds hidden secrets",
            "Paint a vivid picture of an otherworldly environment"
        ],
        'conflict': [
            "Introduce a moral dilemma that tests the protagonist",
            "Create a physical obstacle that seems impossible to overcome",
            "Add a time constraint that increases pressure",
            "Introduce a character with conflicting goals",
            "Create a situation where all choices have consequences"
        ],
        'continuation': [
            "Continue with a surprising turn of events",
            "Add a moment of reflection or character development",
            "Introduce a new element that changes everything",
            "Continue with action that builds tension",
            "Add a scene that reveals important backstory"
        ],
        'description': [
            "Add sensory details that bring the scene to life",
            "Describe the emotional atmosphere of the moment",
            "Include details that foreshadow future events",
            "Add descriptions that reveal character personality",
            "Create vivid imagery that engages all five senses"
        ]
    }
    
    suggestions = fallback_suggestions.get(prompt_type, fallback_suggestions['continuation'])
    return random.choice(suggestions)

def analyze_writing_style(text):
    """
    Analyze writing style and provide suggestions
    """
    if not text:
        return {"error": "No text provided"}
    
    words = text.split()
    sentences = text.split('.')
    
    # Basic metrics
    word_count = len(words)
    sentence_count = len([s for s in sentences if s.strip()])
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Vocabulary diversity (simple measure)
    unique_words = len(set(word.lower() for word in words))
    vocabulary_diversity = unique_words / word_count if word_count > 0 else 0
    
    # Dialogue ratio
    dialogue_lines = [line for line in text.split('\n') if line.strip().startswith('"')]
    dialogue_ratio = len(dialogue_lines) / len([line for line in text.split('\n') if line.strip()]) if text.split('\n') else 0
    
    # Suggestions based on analysis
    suggestions = []
    
    if avg_sentence_length > 25:
        suggestions.append("Consider breaking up long sentences for better readability")
    elif avg_sentence_length < 8:
        suggestions.append("Try varying sentence length for more dynamic writing")
    
    if vocabulary_diversity < 0.3:
        suggestions.append("Consider using more varied vocabulary")
    
    if dialogue_ratio < 0.1:
        suggestions.append("Adding more dialogue can make scenes more engaging")
    elif dialogue_ratio > 0.7:
        suggestions.append("Consider adding more narrative description to balance dialogue")
    
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": round(avg_sentence_length, 2),
        "vocabulary_diversity": round(vocabulary_diversity, 3),
        "dialogue_ratio": round(dialogue_ratio, 3),
        "suggestions": suggestions
    }

def generate_story_outline(genre, initial_prompt):
    """
    Generate a basic story outline structure
    """
    outline_templates = {
        'fantasy': [
            "The Call to Adventure",
            "Meeting the Mentor",
            "Crossing the Threshold",
            "Tests and Trials",
            "The Ordeal",
            "The Reward",
            "The Return"
        ],
        'mystery': [
            "The Crime is Discovered",
            "Initial Investigation",
            "Red Herrings and Clues",
            "The Plot Thickens",
            "The Breakthrough",
            "The Revelation",
            "Justice Served"
        ],
        'romance': [
            "The Meet-Cute",
            "Initial Attraction",
            "The Obstacle",
            "Growing Closer",
            "The Crisis",
            "The Resolution",
            "The Happy Ending"
        ],
        'horror': [
            "The Normal World",
            "The First Sign",
            "Escalating Tension",
            "The Confrontation",
            "The Climax",
            "The Aftermath",
            "The New Normal"
        ]
    }
    
    template = outline_templates.get(genre, outline_templates['fantasy'])
    
    return {
        "genre": genre,
        "initial_prompt": initial_prompt,
        "outline_points": template,
        "suggestions": [
            "Each point can be expanded into multiple story nodes",
            "Consider adding subplots for character development",
            "Remember to maintain consistency with your established world",
            "Don't be afraid to deviate from the outline as the story develops"
        ]
    }
