import os
import vertexai
from flask import Flask, render_template, request, jsonify
from vertexai import agent_engines

app = Flask(__name__)

# Initialize Vertex AI
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "astra-v1-2025")
location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

print(f"Initializing Vertex AI with project={project_id}, location={location}")
vertexai.init(
    project=project_id,
    location=location,
)

# Your deployed agent's resource ID
AGENT_RESOURCE_ID = "projects/307552947759/locations/us-central1/reasoningEngines/3174835427156688896"
agent = agent_engines.get(AGENT_RESOURCE_ID)

# Dictionary to store user sessions
sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_id = data.get('user_id', 'web_user')
        message = data.get('message')
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        if not session_id:
            # Create a new session
            try:
                session = agent.create_session(user_id=user_id)
                session_id = session['id']
                sessions[session_id] = session
            except Exception as e:
                print(f"Error creating session: {str(e)}")
                return jsonify({"error": f"Failed to create session: {str(e)}"}), 500
        
        # Send message and get response
        responses = []
        try:
            for event in agent.stream_query(
                user_id=user_id,
                session_id=session_id,
                message=message,
            ):
                if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            responses.append(part.text)
                elif isinstance(event, dict) and 'content' in event:
                    if 'parts' in event['content']:
                        for part in event['content']['parts']:
                            if 'text' in part:
                                responses.append(part['text'])
        except Exception as e:
            print(f"Error querying agent: {str(e)}")
            return jsonify({"error": f"Failed to get response from agent: {str(e)}"}), 500
        
        return jsonify({
            'response': ''.join(responses),
            'session_id': session_id
        })
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 