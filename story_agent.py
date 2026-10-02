import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


# You can change this later without changing the rest of the app.
MODEL_NAME = os.getenv(
    "GEMMA_MODEL",
    "google/gemma-3-1b-it"
)


print(f"Loading Gemma model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
)

model.eval()


def generate_story(
    child_name,
    age,
    favorite_animal,
    favorite_character,
    setting,
    mood,
    length,
    language
):
    """
    Generate a personalized bedtime story using Gemma.
    """

    prompt = f"""
You are DreamTales, a gentle bedtime-story writer.

Create a warm, imaginative and age-appropriate bedtime story for a
{age}-year-old child.

Child's name: {child_name}
Favorite animal: {favorite_animal}
Favorite character: {favorite_character}
Setting: {setting}
Mood: {mood}
Length: {length}

Requirements:
- The main character, {child_name}, is a HUMAN CHILD.
- Never describe {child_name} as an animal.
- The favorite animal must be a SEPARATE companion character.
- If the favorite animal is a cat, create a separate cat companion with its own name.
- The favorite character type must also remain separate from the child unless explicitly requested.
- Make the setting important to the adventure.
- Keep the story warm, playful, imaginative, and age-appropriate.
- Avoid violence, frightening scenes, and mature themes.
- End with a calm, comforting bedtime moment.
- Finish with a short 2–4 line rhyming moral that is easy for a child to remember.
- The rhyme should relate naturally to the lesson of the story.
- Return only the story and the final rhyme. Do not explain your choices.
LANGUAGE:
- Write the entire story in {language}.
- Use natural, child-friendly language.
- Do not translate word-for-word from English.
- Keep names of characters unchanged.
Begin the story.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        repetition_penalty=1.15,
        no_repeat_ngram_size=4,
    )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    story = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return story.strip()

