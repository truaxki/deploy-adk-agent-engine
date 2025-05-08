# Message Shortener Agent

This project deploys a message shortening agent using the Vertex AI Agent Engine. The agent can be interacted with through a command-line interface or a web interface.

## Features

- Message shortening agent built with Google's Agent Development Kit (ADK)
- Deployed to Vertex AI Agent Engine on Google Cloud
- Command-line interface for deployment and interaction
- Web interface for easy interaction with the agent

## Prerequisites

- Python 3.12 or higher
- Poetry for dependency management
- Google Cloud account with Vertex AI API enabled
- Service account with `aiplatform.admin` and `storage.admin` roles

## Setup

### 1. Install Dependencies

```bash
# Install required packages
poetry install
```

### 2. Google Cloud Setup

1. Create a service account with the following roles:
   - `roles/aiplatform.admin`
   - `roles/storage.admin`

2. Download the service account key and save it as `agent-engine-sa-key.json` in the project root.

3. Set environment variables:
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-project-id
   export GOOGLE_CLOUD_LOCATION=us-central1
   export GOOGLE_APPLICATION_CREDENTIALS=./agent-engine-sa-key.json
   ```

### 3. Create a Cloud Storage bucket

```bash
gsutil mb -l us-central1 gs://your-project-id-agent-bucket
export GOOGLE_CLOUD_STAGING_BUCKET=gs://your-project-id-agent-bucket
```

## Usage

### Command-Line Interface

#### Deploy the Agent

```bash
poetry run deploy-remote --create
```

#### List Deployments

```bash
poetry run deploy-remote --list
```

#### Create a Session

```bash
poetry run deploy-remote --create_session --resource_id="your-resource-id"
```

Replace `your-resource-id` with the resource ID from the deployment step.

#### Send a Message

```bash
poetry run deploy-remote --send --resource_id="your-resource-id" --session_id="your-session-id" --message="Your message to be shortened"
```

#### Delete a Deployment

```bash
poetry run deploy-remote --delete --resource_id="your-resource-id"
```

#### Clean Up Failed Deployments

```bash
poetry run cleanup
```

### Web Interface

Start the web interface:

```bash
poetry run web-interface
```

or

```bash
python run_web.py
```

Then open your browser and navigate to `http://localhost:8080`.

## API Documentation

### Web API Endpoints

#### GET /

Renders the web interface HTML page.

#### POST /api/chat

Sends a message to the agent and returns the response.

**Request Body:**
```json
{
  "message": "The message to be shortened",
  "user_id": "web_user",
  "session_id": "optional-session-id"
}
```

- `message`: The message to be shortened
- `user_id`: Identifier for the user (default: "web_user")
- `session_id`: Optional session ID from a previous request

**Response:**
```json
{
  "response": "Shortened message",
  "session_id": "session-id"
}
```

- `response`: The shortened message
- `session_id`: Session ID to use for follow-up requests

## Project Structure

- `adk_short_bot/`: Main agent logic
- `deployment/`: Deployment scripts
  - `local.py`: Local deployment
  - `remote.py`: Vertex AI deployment
  - `cleanup.py`: Cleanup utility
- `templates/`: Web interface templates
- `web_interface.py`: Flask application for web interface
- `run_web.py`: Entry point for web interface

## Development

### Local Testing

Test the agent locally before deployment:

```bash
poetry run deploy-local
```

### Customize the Agent

Modify the `adk_short_bot/agent.py` file to customize the agent's behavior.

## Troubleshooting

### Authentication Issues

If you encounter authentication issues, ensure:
1. The service account key is correctly downloaded and referenced
2. The service account has appropriate roles assigned
3. The Vertex AI API is enabled in your project

### Deployment Failures

If deployment fails:
1. Check Cloud Storage bucket permissions
2. Verify API enablement status
3. Check for quota issues
4. Run the cleanup utility with `poetry run cleanup`

## License

Apache License 2.0 