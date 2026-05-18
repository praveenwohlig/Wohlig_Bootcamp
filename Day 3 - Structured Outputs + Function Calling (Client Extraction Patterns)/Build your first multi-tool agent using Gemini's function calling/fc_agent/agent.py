from google.adk.agents import Agent
from dotenv import load_dotenv
import os

from .tools import (
    get_order,
    get_shipping,
    check_refund_policy,
    escalate_to_human
)

# Load environment variables
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

SYSTEM_PROMPT = """
You are a customer support AI agent.

Rules:
- Use tools whenever needed.
- Help users with order tracking, shipping, refunds, and disputes.
- Escalate to a human agent when:
    1. Customer is angry or abusive
    2. Legal threats are mentioned
    3. Refund disputes cannot be resolved
    4. Multiple support failures are mentioned
- Be professional, concise, and helpful.
"""

# Root Agent
root_agent = Agent(
    model=MODEL_NAME,
    name="customer_support_agent",
    description="AI customer service agent with function calling support.",
    instruction=SYSTEM_PROMPT,
    tools=[
        get_order,
        get_shipping,
        check_refund_policy,
        escalate_to_human
    ]
)

# Export agent
agent = root_agent