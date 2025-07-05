# Action Repo

This repository is used to trigger GitHub webhook events for integration with a Flask-based webhook receiver (webhook-repo).

## Purpose
- To generate GitHub events (Push, Pull Request, Merge) that are sent to a webhook endpoint.
- The webhook endpoint (in the webhook-repo) receives these events and stores them in MongoDB for further processing and UI display.

## How It Works
1. **Webhook Configuration:**
   - This repository has a webhook configured in its GitHub settings.
   - The webhook points to the Flask app's `/webhook` endpoint (e.g., `https://your-ngrok-url.ngrok-free.app/webhook`).
2. **Event Triggering:**
   - Any push, pull request, or merge action in this repo will trigger a webhook event.
   - The event is sent to the Flask webhook receiver, which processes and stores it.

## How to Test
1. **Push Event:**
   - Make a commit and push to any branch.
2. **Pull Request Event:**
   - Open a new pull request from one branch to another.
3. **Merge Event:**
   - Merge a pull request.

Each of these actions will send a webhook event to the configured endpoint.

## Notes
- No special code or configuration is required in this repo for the webhook to work.
- The webhook must be configured in the GitHub repository settings (Settings > Webhooks).
- The Flask webhook receiver must be running and accessible from the internet (e.g., via ngrok or a public server).

## Example Webhook Payload URL
```
https://your-ngrok-url.ngrok-free.app/webhook
```

Replace `your-ngrok-url` with your actual ngrok subdomain or public server address. 