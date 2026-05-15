# Chain-of-Thought vs Self-Consistency Evaluation

## Experiment Summary

Domain: Insurance Claim Approval Reasoning

Total Scenarios Evaluated: 15

Techniques Compared:
1. Direct Prompting
2. Chain-of-Thought (CoT)
3. Self-Consistency (SC)

---

# Accuracy Results

| Technique | Correct Answers | Accuracy |
|---|---|---|
| Direct Prompting | 15 / 15 | 100% |
| Chain-of-Thought (CoT) | 15 / 15 | 100% |
| Self-Consistency (SC) | 15 / 15 | 100% |

---

# Cost Analysis

## Total Cost

| Technique | Total Cost (USD) |
|---|------------------|
| Direct Prompting | $0.00019495      |
| Chain-of-Thought (CoT) | $0.0021899       |
| Self-Consistency (SC) | $0.01091195      |

---

## Average Cost Per Scenario

| Technique | Avg Cost Per Scenario |
|---|-----------------------|
| Direct Prompting | $0.00001300           |
| Chain-of-Thought (CoT) | $0.000145927          |
| Self-Consistency (SC) | $0.00072747           |

---

## Cost Per Correct Answer

Since all approaches achieved 100% accuracy:

| Technique | Cost Per Correct Answer |
|---|---|
| Direct Prompting | $0.00001300 |
| Chain-of-Thought (CoT) | $0.000145927 |
| Self-Consistency (SC) | $0.00072747 |

---

# Observations

## 1. Direct Prompting
Direct prompting achieved perfect accuracy on these relatively simple insurance reasoning scenarios.

Advantages:
- Lowest cost
- Fastest response
- Minimal token usage

Disadvantages:
- May fail on more complex reasoning tasks
- Less reliable for ambiguous or multi-step logic problems

---

## 2. Chain-of-Thought (CoT)
Chain-of-Thought prompting also achieved perfect accuracy while generating intermediate reasoning steps.

Advantages:
- Better reasoning transparency
- Easier debugging and explainability
- More reliable for complex decision-making

Disadvantages:
- Higher token usage
- More expensive than direct prompting

Observation:
The CoT responses clearly demonstrated structured reasoning:
- policy validation
- waiting period checks
- exclusion analysis
- coverage verification

This makes CoT highly useful in regulated domains like insurance and finance.

---

## 3. Self-Consistency
Self-consistency achieved perfect accuracy as well.

Method:
- CoT prompt executed 5 times
- temperature = 0.7
- majority answer selected

Advantages:
- Most robust reasoning strategy
- Reduces random reasoning errors
- Helpful for difficult or ambiguous tasks

Disadvantages:
- Extremely expensive
- 5x higher inference cost
- Increased latency

Observation:
For these simple scenarios, self-consistency did not improve accuracy because the base model already solved all cases correctly.

---

# Final Decision Rule

## Use Direct Prompting When:
- Tasks are simple
- Reasoning depth is low
- Cost and speed matter most
- High throughput systems are needed

Examples:
- basic classification
- simple approvals
- FAQ systems

---

## Use Chain-of-Thought (CoT) When:
- Tasks require multi-step reasoning
- Explainability is important
- Business logic must be transparent
- Errors are moderately costly

Examples:
- insurance claim analysis
- financial decision systems
- medical reasoning
- policy compliance workflows

---

## Use Self-Consistency When:
- Accuracy is extremely critical
- Problems are ambiguous or difficult
- Small reasoning errors are unacceptable
- Extra compute cost is acceptable

Examples:
- legal analysis
- healthcare diagnosis support
- fraud detection
- high-risk financial decisions

---

# Final Conclusion

For this experiment:
- Direct prompting was the most cost-efficient approach.
- Chain-of-Thought improved explainability significantly.
- Self-consistency increased cost substantially without improving accuracy.

Therefore:

1. Default to Direct Prompting for simple reasoning tasks.
2. Use CoT for production reasoning systems requiring transparency.
3. Reserve Self-Consistency only for high-risk or highly ambiguous tasks.