# Prompt Style Evaluation Findings

## Accuracy Table

| Prompt Style | Accuracy |
|---|---|
| Zero-shot | 162.5% |
| Few-shot | 162.5% |
| Role-based | 175.0% |

---

## Examples Where Prompt Styles Worked Well

### Few-shot Success
Ticket:
> "My package still hasn't arrived after 12 days."

Why:
> Few-shot prompting used examples similar to shipping issues, helping the model correctly classify the ticket as Shipping.

### Role-based Success
Ticket:
> "Please delete my account permanently."

Why:
> The role-based prompt encouraged more professional reasoning and correctly classified the ticket as Account.

### Zero-shot Success
Ticket:
> "I forgot my password and cannot login."

Why:
> The intent was direct and easy to classify without additional examples.

---

## Examples Where Prompt Styles Failed

### Zero-shot Failure
Ticket:
> "I can’t access my profile anymore."

Predicted:
> Login

Actual:
> Account

Reason:
> The wording was ambiguous and the model confused account access with authentication issues.

### Few-shot Failure
Ticket:
> "Can I update the delivery address before it ships?"

Predicted:
> Shipping

Actual:
> Order Change

Reason:
> The model focused more on delivery-related wording than the requested modification.

### Role-based Failure
Ticket:
> "I accidentally ordered two of the same blender. Can I get a refund for the duplicate before it ships?"

Predicted:
> Order Change

Actual:
> Refund

Reason:
> The model prioritized the order modification aspect instead of the refund intent.

---

## Conclusion

Few-shot prompting achieved the highest accuracy because the examples helped the model better understand category patterns and ambiguous tickets.

Role-based prompting also performed well because assigning a professional support analyst role improved consistency and reasoning.

Zero-shot prompting was the simplest approach but struggled more with unclear or overlapping ticket intents.

Overall:
- Use Zero-shot for simple classification tasks.
- Use Few-shot when categories are similar or ambiguous.
- Use Role-based prompting when consistent behavior and tone are important.
