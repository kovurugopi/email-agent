# Email Agent

An AI-powered email assistant built with [Google ADK (Agent Development Kit)](https://google.github.io/adk-docs/) that can send emails through Gmail on your behalf.

## What It Does

This agent uses **Gemini 2.5 Flash** as its LLM and integrates with the **Gmail API** to send emails. When you interact with it:

1. Tell it who to email, the subject, and the body
2. It confirms the details with you
3. Once you approve, it sends the email via your Gmail account

## Prerequisites

- Python 3.10+
- A Google Cloud project with the Gmail API enabled
- OAuth 2.0 credentials for a desktop application

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/kovurugopi/email-agent.git
cd email-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install google-adk google-auth google-auth-oauthlib google-api-python-client
```

### 4. Set up Google OAuth credentials

This project requires a `credentials.json` file from Google Cloud Console:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Gmail API** under "APIs & Services" → "Library"
4. Go to "APIs & Services" → "Credentials"
5. Click "Create Credentials" → "OAuth client ID"
6. Select **Desktop app** as the application type
7. Download the JSON file and save it as `email_agent/credentials.json`

### 5. Set up environment variables

Create a file at `email_agent/.env`:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_google_api_key_here
```

You can get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 6. Authenticate with Gmail

On first run, the agent will open a browser window asking you to authorize Gmail access. This generates a `token.json` file automatically — you don't need to create it manually.

## Usage

```bash
adk run email_agent
```

Then interact with the agent in your terminal. Example:

```
You: Send an email to alice@example.com with subject "Hello" and body "Just checking in!"
Agent: I'd like to confirm the details before sending...
```

## Project Structure

```
email_agent/
├── __init__.py        # Package init
├── agent.py           # Agent definition and Gmail send tool
├── .env               # API keys (not committed)
├── credentials.json   # OAuth client credentials (not committed)
└── token.json         # OAuth token, auto-generated on first auth (not committed)
```

## Security Notes

The following files contain sensitive information and are **excluded from version control** via `.gitignore`:

| File | What it contains | How to get it |
|------|-----------------|---------------|
| `email_agent/.env` | Gemini API key | [Google AI Studio](https://aistudio.google.com/apikey) |
| `email_agent/credentials.json` | OAuth 2.0 client ID/secret | [Google Cloud Console](https://console.cloud.google.com/) → Credentials |
| `email_agent/token.json` | User's Gmail access/refresh token | Auto-generated on first run |

Never commit these files. If you accidentally do, rotate your credentials immediately.

## License

MIT
