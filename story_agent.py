import os
from urllib import response

#import torch
#from transformers import AutoTokenizer, AutoModelForCausalLM


    # You can change this later without changing the rest of the app.
    #MODEL_NAME = os.getenv(
    #    "GEMMA_MODEL",
    #    "google/gemma-3-1b-it"
   # )


   # print(f"Loading Gemma model: {MODEL_NAME}")

   # tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

   # model = AutoModelForCausalLM.from_pretrained(
  #      MODEL_NAME,
   #     torch_dtype=torch.float32
   # )

    #model.eval()
import os
from huggingface_hub import InferenceClient

MODEL_NAME = os.getenv("GEMMA_MODEL", "google/gemma-3-27b-it")
PROVIDER = os.getenv("HF_PROVIDER", "auto")  # or "scaleway"
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(provider=PROVIDER, api_key=HF_TOKEN)

print(f"Using Gemma model: {MODEL_NAME} via {PROVIDER}")

MAX_TOKENS = {"short": 400, "medium": 800, "long": 1000}


def generate_story(
    child_name,
    age,
    favorite_animal,
    favorite_character,
    setting,
    mood,
    length,
    language,
):
    """Generate a personalized bedtime story using Gemma."""

    prompt = f"""
You are DreamTales, a gentle bedtime-story writer. Write the ENTIRE story in {language}.

Child: {child_name} (a human child)
Age: {age}
Favorite animal: {favorite_animal} (separate companion)
Favorite character: {favorite_character} (separate character)
Setting: {setting}
Mood: {mood}
Length: {length}

RULES:
- Start with just the story, no preamble or explanations.
- Every sentence, narration, dialogue, and the final rhyme must be entirely in {language}.
- Keep all character names and roles consistent; never rename or merge characters.
- Begin with {child_name} discovering the adventure.
- Include {favorite_animal} and {favorite_character} naturally.
- Make {setting} important to the story.
- Create a simple, peaceful, imaginative adventure.
- No violence, fear, frightening scenes, or mature themes.
- End with {child_name} feeling safe, cozy, and peaceful.
- Do not use emojis.

ENDING:
- End with EXACTLY 4 short rhyming lines expressing the story's lesson.
- Do not label the rhyme.
- Do not write "The End".
- Do not add explanations, questions, or anything after the story.
- Nothing should be outside the story; do not add any commentary or extra text.

OUTPUT:
Return ONLY the bedtime story.
No HTML, Markdown, XML, code fences, or formatting tags.
"""

    response = client.chat_completion(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS.get(length, 1000),
        temperature=0.8,
        top_p=0.9,
        frequency_penalty=0.3,  # replaces repetition_penalty from the local version
    )

    return response.choices[0].message.content.strip()