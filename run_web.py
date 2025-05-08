"""Script to run the web interface for the agent."""

import os
from web_interface import app

if __name__ == "__main__":
    # Make sure service account credentials are set
    credentials_file = os.path.join(os.getcwd(), "agent-engine-sa-key.json")
    if os.path.exists(credentials_file):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file
    
    # Set project and location if not already set
    if "GOOGLE_CLOUD_PROJECT" not in os.environ:
        os.environ["GOOGLE_CLOUD_PROJECT"] = "astra-v1-2025"
    
    if "GOOGLE_CLOUD_LOCATION" not in os.environ:
        os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
    
    print("Starting web interface on http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080) 