# API Documentation

This document provides detailed information about the APIs available for interacting with the Message Shortener Agent.

## Web API

The web API provides HTTP endpoints for interacting with the agent from web applications or any HTTP client.

### Base URL

When running locally: `http://localhost:8080`

### Authentication

Currently, the API does not implement authentication. In production, you should implement appropriate authentication mechanisms.

### Endpoints

#### GET /

**Description**: Returns the web interface HTML page.

**Response**: HTML page

**Example**:
```bash
curl http://localhost:8080/
```

#### POST /api/chat

**Description**: Sends a message to the agent and returns the response.

**Request Body**:
```json
{
  "message": "The message you want to shorten",
  "user_id": "web_user",
  "session_id": "optional-session-id-from-previous-request"
}
```

**Parameters**:
- `message` (required): The message text to be shortened
- `user_id` (optional): Identifier for the user (default: "web_user")
- `session_id` (optional): Session ID from a previous request to continue a conversation

**Response**:
```json
{
  "response": "Shortened message from the agent",
  "session_id": "session-id-for-follow-up-requests"
}
```

**Response Fields**:
- `response`: The agent's response (shortened message)
- `session_id`: Session ID to use for follow-up requests in the same conversation

**Example**:
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "This is a very long message that I would like the agent to shorten for me. It contains many unnecessary words and could be much more concise.", "user_id": "web_user"}'
```

**Example Response**:
```json
{
  "response": "Long msg needs shortening. Contains unnecessary words.",
  "session_id": "3256292196344659968"
}
```

### Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Request succeeded
- `400 Bad Request`: Missing required parameters
- `500 Internal Server Error`: Server-side error

Error responses include a JSON body with error details:

```json
{
  "error": "Error message"
}
```

## Command Line Interface

The command line interface provides functionality for deploying and interacting with the agent.

### Deployment Commands

#### Deploy Agent

```bash
poetry run deploy-remote --create
```

**Response**: Outputs the resource ID of the deployed agent

#### List Deployments

```bash
poetry run deploy-remote --list
```

**Response**: Lists all agent deployments with their resource IDs

#### Delete Deployment

```bash
poetry run deploy-remote --delete --resource_id="projects/307552947759/locations/us-central1/reasoningEngines/3174835427156688896"
```

**Parameters**:
- `resource_id` (required): The resource ID of the deployment to delete

### Session Commands

#### Create Session

```bash
poetry run deploy-remote --create_session --resource_id="projects/307552947759/locations/us-central1/reasoningEngines/3174835427156688896"
```

**Parameters**:
- `resource_id` (required): The resource ID of the deployed agent

**Response**: Outputs the session ID for the new session

#### Send Message

```bash
poetry run deploy-remote --send --resource_id="projects/307552947759/locations/us-central1/reasoningEngines/3174835427156688896" --session_id="3256292196344659968" --message="Your message to be shortened"
```

**Parameters**:
- `resource_id` (required): The resource ID of the deployed agent
- `session_id` (required): The session ID from a previous create_session command
- `message` (required): The message to be shortened

**Response**: Outputs the agent's response

## Programmatic API

You can also interact with the agent programmatically using the Vertex AI Python SDK.

### Example Usage

```python
import os
import vertexai
from vertexai import agent_engines

# Initialize Vertex AI
project_id = "your-project-id"
location = "us-central1"

vertexai.init(
    project=project_id,
    location=location,
)

# Agent resource ID
AGENT_RESOURCE_ID = "projects/307552947759/locations/us-central1/reasoningEngines/3174835427156688896"
agent = agent_engines.get(AGENT_RESOURCE_ID)

# Create a session
session = agent.create_session(user_id="your-user-id")
session_id = session['id']

# Send a message
response = agent.query(
    user_id="your-user-id",
    session_id=session_id,
    message="Your message to be shortened",
)

print(response)
```

## Webhook Integration

You can integrate the agent with other applications by creating webhooks that call the API endpoints.

### Example Webhook Integration with Slack

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/slack/shortener', methods=['POST'])
def slack_shortener():
    slack_data = request.form
    message = slack_data.get('text', '')
    user_id = slack_data.get('user_id', 'slack_user')
    
    # Call our agent API
    response = requests.post(
        'http://localhost:8080/api/chat',
        json={
            'message': message,
            'user_id': user_id
        }
    )
    
    agent_response = response.json()
    
    return jsonify({
        'response_type': 'in_channel',
        'text': agent_response['response']
    })

if __name__ == '__main__':
    app.run(port=5000)
```

## Rate Limiting

The API currently does not implement rate limiting. For production use, consider adding rate limiting to prevent abuse.

## Future Improvements

- Authentication and authorization
- Rate limiting
- Response streaming
- Support for attachments and media
- Logging and analytics 