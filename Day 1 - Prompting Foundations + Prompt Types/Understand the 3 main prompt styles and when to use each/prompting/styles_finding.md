# Prompt Style Evaluation Findings

## Accuracy Table

| Prompt Style | Accuracy |
|---|---|
| Zero-shot | 87.5% |
| Few-shot | 87.5% |
| Role-based | 93.8% |

---

## Examples Where Prompt Styles Worked Well

### Zero-shot Success
Ticket:
> "I returned my shoes two weeks ago via FedEx, but I haven't seen the credit on my statement yet. Tracking says it was delivered."

Predicted:
> Refund

Actual:
> Refund

Why:
> The ticket used clear and direct wording, making it easy to classify correctly without examples.

### Few-shot Success
Ticket:
> "I returned my shoes two weeks ago via FedEx, but I haven't seen the credit on my statement yet. Tracking says it was delivered."

Predicted:
> Refund

Actual:
> Refund

Why:
> The examples provided in the prompt helped the model understand the category pattern.

### Role-based Success
Ticket:
> "I returned my shoes two weeks ago via FedEx, but I haven't seen the credit on my statement yet. Tracking says it was delivered."

Predicted:
> Refund

Actual:
> Refund

Why:
> The professional role instruction improved consistency and reasoning.

---

## Examples Where Prompt Styles Failed

### Zero-shot Failure
Ticket:
> "I paid for overnight shipping, but it’s been three days and the order is still 'Processing.' Can I get my shipping fee back?"

Predicted:
> Refund

Actual:
> Shipping

Reason:
> The model misunderstood the intent because the ticket wording was ambiguous.

### Few-shot Failure
Ticket:
> "I paid for overnight shipping, but it’s been three days and the order is still 'Processing.' Can I get my shipping fee back?"

Predicted:
> Refund

Actual:
> Shipping

Reason:
> Even with examples, the model focused on secondary context instead of the main request.

### Role-based Failure
Ticket:
> "I accidentally ordered two of the same blender. Can I get a refund for the duplicate before it ships?"

Predicted:
> Order Change

Actual:
> Refund

Reason:
> The ticket contained overlapping intents, causing the model to choose the wrong category.

---

## Conclusion

Role-based prompting achieved the highest accuracy with 93.8% because assigning a professional support analyst role improved consistency and reasoning.

Both Zero-shot and Few-shot prompting achieved 87.5% accuracy. Zero-shot worked well for straightforward tickets, while Few-shot benefited from example-based guidance.

Overall:
- Use Zero-shot prompting for simple and direct classification tasks.
- Use Few-shot prompting when categories are similar or require examples.
- Use Role-based prompting when high accuracy and consistent reasoning are important.