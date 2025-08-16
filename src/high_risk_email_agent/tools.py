import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.adk.tools import ToolContext
from solace_ai_connector.common.log import log
from solace_agent_mesh.agent.utils.artifact_helpers import (
    save_artifact_with_metadata,
    DEFAULT_SCHEMA_MAX_KEYS,
)
from solace_agent_mesh.agent.utils.context_helpers import get_original_session_id


async def fun_raise_high_risk_alert(
    risk_message: str,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Send email alert when High Risk score is observed for a customer transaction

    Args:
        nlp: The natural language risk profile details
        tool_context: SAM framework context (provided automatically)
        tool_config: Tool-specific configuration (from config.yaml)

    Returns:
        Status of the email send and the risk profile details
    """
    # --- SMTP Configuration ---
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "XXXXXXXx"   # Replace with your Outlook/Hotmail email
    SMTP_PASSWORD = "XXXXXX"        # Or app password if MFA enabled

    
    
    match = re.search(r"\b(\d+)\b", risk_message)
    log_identifier = "[fun_raise_high_risk_alert]"
    log.info(f"{log_identifier} Processing NLP input: {risk_message}")
    customer_id = int(match.group(1))
    log.info(f"[HistoryAgentExecutor] Fetching data for customer_id={customer_id}")
    # --- Email Content ---
    from_email = SMTP_USER
    to_email = "XXXXXXX"
    subject = "Alert !!! High Risk Transaction Email Alert"
    #body = "Hello,\n\nThis is a test email sent from Python using Outlook SMTP!"

# Create the message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(risk_message, "plain"))

# Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    return {
        "status": "success",
        "history": risk_message,

    }   
