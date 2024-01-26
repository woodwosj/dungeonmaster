from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate-plot', methods=['POST'])
def generate_plot():
    data = request.json
    # Construct the prompt using the provided data
    prompt = {
        "theme": data.get('theme', ''),
        "storyIdea": data.get('storyIdea', ''),
        "numPlayers": data.get('numPlayers', ''),
        "characterLevels": data.get('characterLevels', ''),
        "setting": data.get('setting', '')
    }
    
    # Construct the messages list for the chat
    messages = [
        {"role": "system", "content": "You are a dungeon master creating a plot for a D&D game."},
        {"role": "user", "content": f"Create a plot with the theme {prompt['theme']}, based on {prompt['storyIdea']}, for {prompt['numPlayers']} players at level {prompt['characterLevels']} in a {prompt['setting']} setting."}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the correct GPT-4 model identifier
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        # Assuming the response structure is similar to GPT-3's ChatCompletion
        plot = response['choices'][0]['message']['content']
        return jsonify({'plot': plot}), 200
    except Exception as e:
        print(f"An error occurred: {e}")  # Logging the exception
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
