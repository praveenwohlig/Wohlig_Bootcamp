# Test Queries

## Single-Tool Queries

### 1. Order Status
User:
What's the status of order #1002?

Expected Tool:
- get_order

---

### 2. Shipping Details
User:
Track shipping for order #1015

Expected Tool:
- get_shipping

---

### 3. Refund Policy
User:
What is the refund policy for electronics products?

Expected Tool:
- check_refund_policy

---

# Multi-Tool Queries

### 4. Refund Eligibility + Policy
User:
Can I get a refund for order #1003 and what is the policy?

Expected Tools:
- get_order
- check_refund_policy

---

### 5. Delayed Shipment Investigation
User:
My order #1010 is delayed. What's happening and can I cancel it?

Expected Tools:
- get_shipping
- get_order

---

### 6. Wrong Item Complaint
User:
I received the wrong item for order #1019. What are my options?

Expected Tools:
- get_order
- check_refund_policy

---

# Multi-Turn Conversations

### 7. Delivery + Return Conversation

User:
Where is order #1006?

Follow-up:
Can I return it after delivery?

Expected Tools:
- get_shipping
- check_refund_policy

---

### 8. Damaged Product Conversation

User:
My order #1013 arrived damaged.

Follow-up:
Can you help me get a replacement?

Expected Tools:
- get_order
- escalate_to_human

---

# Escalation Queries

### 9. Angry Customer Escalation

User:
I've contacted support multiple times for order #1004 and still no refund. This is unacceptable.

Expected Tool:
- escalate_to_human

---

### 10. Legal Threat Escalation

User:
If my refund for order #1013 is not processed today, I will file a legal complaint.

Expected Tool:
- escalate_to_human