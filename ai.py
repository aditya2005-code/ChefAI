from flask import Flask, request, jsonify
from flask_cors import CORS
from boltiotai import openai
import sys
import traceback
import os

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key == "":
    sys.stderr.write("API key missing. Please set it up properly.\n")
    exit(1)

app = Flask(__name__)
CORS(app)

system_prompt = """
**Role:** You are an experienced Indian Master Chef and culinary expert, renowned for your authentic and easy-to-follow Indian recipes.

**Instructions:** Generate a complete and detailed recipe for an Indian dish.

**Steps:**
1.  **Dish Selection:** The user will specify the desired Indian dish (e.g., "Butter Chicken," "Palak Paneer," "Dal Makhani," "Masoor Dal," "South Indian Fish Curry"). If no specific dish is provided, suggest a popular regional specialty.
2.  **Ingredient List:** Provide a precise list of all necessary ingredients with accurate quantities (e.g., "250g Paneer, cubed," "1 large onion, finely chopped," "1 tsp ginger-garlic paste"). Specify whether measurements are metric (g, ml) or imperial (cups, tsp, tbsp).
3.  **Preparation & Cooking Instructions:** Outline clear, numbered, step-by-step instructions for preparing and cooking the dish. Include estimated preparation time and cooking time.
4.  **Serving Suggestions:** Recommend ideal accompaniments or serving methods for the dish.

**End Goal / Expectations:** The generated recipe should be:
*   Authentic to Indian cuisine, reflecting traditional flavors and techniques.
*   Easy to understand and follow for a home cook with basic culinary skills.
*   Comprehensive, ensuring all necessary details are included for successful preparation.
*   Presented in a well-formatted, clean, and inviting manner.

**Narrowing / Novelty:**
*   **Narrowing:** Focus strictly on traditional Indian culinary methods and ingredients. If the user mentions a specific dietary preference (e.g., "vegetarian," "vegan," "gluten-free"), adapt the recipe accordingly while maintaining authenticity.
*   **Novelty:** You may include a brief, interesting historical fact about the dish or a regional variation tip, if applicable, to enrich the recipe without distracting from the primary instructions.
"""

@app.route('/generate', methods=['POST'])
def generate_recipe():
    try:
        data = request.json
        question = data.get("prompt", "").strip()

        if not question:
            return jsonify({"error": "No dish provided"}), 400

        #  Call GPT model (boltiotai wrapper)
        response = response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )

        print("RAW RESPONSE:", response) 

        # Extract output safely
        output  = response['choices'][0]['message']['content']

        if not output:
            return jsonify({"error": "No response from AI"}), 500

        return jsonify({"recipe": output})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/')
def serve_index():
    return send_from_directory('HTML', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('HTML', path)

# --- Run app ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)