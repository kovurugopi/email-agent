import base64
import os
from email.mime.text import MIMEText

from google.adk.agents.llm_agent import Agent
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'token.json')
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')


def get_gmail_service():
    """Authenticate and return a Gmail API service instance."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email via Gmail.

    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: Plain text email body.

    Returns:
        A dict with status and message id or error.
    """
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message['To'] = to
        message['Subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        sent = service.users().messages().send(
            userId='me', body={'raw': raw}
        ).execute()
        return {"status": "success", "message_id": sent['id']}
    except Exception as e:
        return {"status": "error", "error": str(e)}


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An email assistant that sends emails via Gmail.',
    instruction="""You are an email assistant that can send real emails via Gmail.

When the user asks to send an email:
1. Gather the recipient (to), subject, and body.
2. Confirm all details with the user.
3. Once confirmed, call the send_email tool with the exact details.
4. Report back whether the email was sent successfully.

Always confirm before sending. Never send without explicit user approval.""",
    tools=[send_email],
)
