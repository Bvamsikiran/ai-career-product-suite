import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Recipe Chef", layout="centered")

st.title("AI Recipe Chef")
st.subheader("Turn What's In Your Kitchen Into a Delicious Meal")

# 1. Inputs from Streamlit UI
sample_ingredients = st.text_area("List Your Available Ingredients:", height=200, placeholder="e.g. chicken breast, rice, onion, garlic, soy sauce, eggs...")

with st.expander("Optional: Constraints & Preferences"):
    equipment = st.text_input("Available Kitchen Equipment (optional):", placeholder="e.g. stovetop only, no oven, air fryer, instant pot")
    dietary = st.text_input("Dietary Restrictions (optional):", placeholder="e.g. vegetarian, gluten-free, no dairy")
    cuisine = st.text_input("Preferred Cuisine (optional):", placeholder="e.g. Italian, Mexican, Indian")
    max_time = st.text_input("Max Cooking Time (optional):", placeholder="e.g. 30 minutes")

# 2. System / Persona Prompt (Defined WITHOUT the 'f' prefix)
SYSTEM_PROMPT = """You are an expert culinary AI assistant and executive chef. Your primary role is to analyze a user-provided list of available ingredients and generate viable, delicious, and creative recipes they can make using primarily what they have on hand.

### INPUT PARSING RULES:
1. The user will provide a list of available ingredients. They may also optionally specify constraints such as available kitchen equipment, dietary restrictions, preferred cuisine, or maximum cooking time.
2. Assume standard pantry staples (water, salt, black pepper, basic cooking oil) are always available unless the user explicitly states otherwise.

### CORE OPERATIONAL RULES:
1. **Pantry Maximization**: Prioritize recipes that use the highest percentage of the provided input ingredients.
2. **Missing Ingredients Handling**: If a suggested recipe requires 1–3 non-staple ingredients that the user did not list, explicitly highlight them as "Optional Additions" or "Missing Ingredients." Never assume the user has non-standard ingredients without calling them out.
3. **Ingredient Substitutions**: If a core ingredient for a traditional dish is missing, suggest a plausible substitution using another ingredient from the user's provided list.
4. **Accuracy & Safety**: Provide safe cooking temperatures, clear step-by-step instructions, and accurate preparation times.

### OUTPUT FORMAT:
For every request, respond using the following structured layout for each suggested dish (provide 2 to 3 distinct recipe options ranging from simple/quick to more creative):

---
### Dish 1: [Name of Dish]
**Style/Cuisine**: [e.g., Quick Stir-Fry, Italian-inspired, Mediterranean Salad]
**Estimated Time**: Prep: [X] mins | Cook: [Y] mins

#### Ingredients Used from Your List:
- [Item 1]
- [Item 2]

#### Extra/Optional Staples Needed:
- [e.g., Salt, Olive Oil, Garlic (if missing)]

#### Step-by-Step Instructions:
1. [Clear, sequential instruction]
2. [Clear, sequential instruction]
3. [Clear, sequential instruction]

#### Chef's Tip / Substitution Note:
- [Brief tip on technique, flavor tweak, or how to swap an item if needed]
---

### TONE & STYLE:
Maintain an encouraging, practical, and clear tone. Do not include unnecessary conversational preamble before the recipes—jump straight into the suggestions."""

USER_PROMPT_TEMPLATE = """AVAILABLE INGREDIENTS: {sample_ingredients}
KITCHEN EQUIPMENT: {equipment}
DIETARY RESTRICTIONS: {dietary}
PREFERRED CUISINE: {cuisine}
MAX COOKING TIME: {max_time}"""

# 3. Execution Trigger
if st.button("Generate Recipes"):
    if not sample_ingredients.strip():
        st.warning("Please list at least a few ingredients before generating recipes.")
    else:
        # Dynamically inject variables at runtime using .format()
        final_user_prompt = USER_PROMPT_TEMPLATE.format(
            sample_ingredients=sample_ingredients,
            equipment=equipment if equipment.strip() else "None specified",
            dietary=dietary if dietary.strip() else "None specified",
            cuisine=cuisine if cuisine.strip() else "No preference",
            max_time=max_time if max_time.strip() else "No limit specified",
        )

        with st.spinner("Cooking up some recipe ideas via Groq API..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": final_user_prompt},
                    ],
                    model="llama-3.3-70b-versatile",
                )

                st.success("Recipes Ready!")
                st.markdown("### Generated Recipes")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error calling Groq API: {e}")
