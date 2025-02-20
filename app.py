from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Define intents with example utterances and responses.
intents = {
    "greeting": {
        "utterances": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?"
        ]
    },
    "order_pizza": {
        "utterances": ["order a pizza", "i want to order a pizza", "pizza please", "get me a pizza"],
        "responses": [
            "Sure! What size pizza would you like? (small, medium, or large)",
            "Great! Do you have a preference for size? (small, medium, large)"
        ],
        # Define potential entity keywords for demonstration.
        "entities": {
            "size": ["small", "medium", "large"],
            "topping": ["pepperoni", "mushroom", "cheese", "veggie"]
        }
    },
    "goodbye": {
        "utterances": ["bye", "goodbye", "see you later"],
        "responses": [
            "Goodbye! Have a great day!",
            "See you later!"
        ]
    }
}

def identify_intent(user_message):
    """Identify the intent based on whether an utterance is a substring of the message."""
    user_message = user_message.lower()
    for intent, data in intents.items():
        for utter in data.get("utterances", []):
            if utter in user_message:
                return intent
    return None

def extract_entities(user_message, intent):
    """Extract simple entities for a given intent based on keyword matching."""
    user_message = user_message.lower()
    entities_found = {}
    
    if intent == "order_pizza":
        # Check for size entity
        for size in intents[intent]["entities"]["size"]:
            if size in user_message:
                entities_found["size"] = size
                break
        # Check for topping entity (if mentioned)
        for topping in intents[intent]["entities"]["topping"]:
            if topping in user_message:
                entities_found["topping"] = topping
                break
    return entities_found

def generate_response(intent, entities):
    """Generate a response based on the intent and any extracted entities."""
    responses = intents[intent]["responses"]
    response = random.choice(responses)
    
    # For order_pizza, customize the response if entities are detected.
    if intent == "order_pizza":
        if entities.get("size") and entities.get("topping"):
            response = f"Great! I'll order you a {entities['size']} pizza with {entities['topping']}."
        elif entities.get("size"):
            response = f"Okay, a {entities['size']} pizza. Do you have a topping preference?"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    intent = identify_intent(message)
    if intent:
        entities = extract_entities(message, intent)
        response = generate_response(intent, entities)
    else:
        response = "I'm sorry, I didn't understand that. Could you rephrase?"
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
