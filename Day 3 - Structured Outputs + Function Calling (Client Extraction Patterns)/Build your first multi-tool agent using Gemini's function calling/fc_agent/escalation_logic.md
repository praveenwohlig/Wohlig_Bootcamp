# Escalation Logic

The customer-service agent uses escalation logic to transfer sensitive or high-risk conversations to a human support representative.

---

# Escalation Triggers

The agent escalates when any of the following conditions are detected:

## 1. Angry or Abusive Customers

Examples:
- "This is unacceptable."
- "Worst support ever."
- "I'm extremely frustrated."

Reason:
High emotional intensity may require human empathy and intervention.

---

## 2. Legal Threats

Examples:
- "I will file a complaint."
- "I will take legal action."
- "I'm contacting consumer court."

Reason:
Legal issues should always be handled by trained human representatives.

---

## 3. Disputed Orders

Examples:
- Damaged delivery
- Wrong item received
- Missing package claims

Reason:
Disputed orders often require manual verification and approval workflows.

---

## 4. Refund Conflicts

Examples:
- Refund denied disputes
- Refund delays
- Multiple refund complaints

Reason:
Complex refund handling may require human approval.

---

## 5. Multiple Failed Support Attempts

Examples:
- "I've contacted support 5 times."
- "Nobody helped me."
- "Still unresolved after many requests."

Reason:
Repeated unresolved cases indicate escalation priority.

---

# Context Passed During Escalation

When escalation happens, the agent sends structured context to the human support system.

The following information is included:

- Order ID
- Customer complaint summary
- Detected sentiment
- Previous tool outputs
- Dispute details
- Escalation reason

---

# Example Escalation Flow

## User Input

"If my refund is not processed today, I will file a legal complaint."

---

## Tool Called

escalate_to_human(
    reason="Customer threatened legal action regarding refund delay"
)

---

## Tool Response

{
  "status": "ESCALATED",
  "message": "A human support agent will contact the customer shortly.",
  "reason": "Customer threatened legal action regarding refund delay"
}

---

# Escalation Design Goal

The escalation system is designed to:

- Protect customer experience
- Prevent unsafe automated handling
- Ensure sensitive cases reach humans quickly
- Maintain professional support workflows