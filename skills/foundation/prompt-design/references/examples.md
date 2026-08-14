# Prompt Design Examples

## Simple: naming versus showing a format

Weak:
```
Extract the key details from the email and return JSON.
```
Failure observed: keys change between runs, sometimes nested, sometimes flat.

Repaired:
```
Extract details from the email below.

Return exactly this JSON shape, with no text before or after:
{"sender": "", "requested_action": "", "deadline": "", "urgency": "low|medium|high"}

If a field is not present in the email, use null.

###
{email}
###
```
What changed: format shown rather than named, missing value behaviour defined, input delimited.

## Realistic: the dropped second instruction

Original prompt asked the model to (a) classify a support ticket and (b) draft a reply. Classification was correct, replies were generic and often contradicted the classification.

Diagnosis followed Step 6 and stopped at item 7: the task was too large for one prompt. The second action depended on the first, and the model was committing to a reply before its classification was fixed.

Resolution: split into a chain. Prompt 1 returns the category and the evidence spans. Prompt 2 receives the category as input and drafts the reply conditioned on it. See `prompt-chaining-and-workflows`.

Signal worth generalizing: when output quality on task B varies with how confidently task A was resolved, they belong in separate calls.

## Edge case: an instruction that cannot be satisfied

Requirement: "Summarize this contract in 2 sentences and list every obligation of both parties."

These conflict. Two sentences cannot hold a full obligation list, so the model silently picks one and drops the other, and which one it drops varies by input length. No amount of rewording fixes it.

Correct handling under Failure Conditions: stop and put the decision to the user. Either the summary grows, or the obligation list becomes a second output field, or the two become two calls. Reporting the conflict is the deliverable, not a workaround.

## Edge case: empty and out-of-domain input

Every shipped prompt states behaviour for input that is empty, far too long, or outside the intended domain. A prompt that has never been tested on a blank input usually invents content to fill the format it was told to produce, which reads as a confident hallucination. Add an explicit rule:

```
If the input is empty or contains no information relevant to the task,
return {"status": "no_input"} and nothing else.
```
