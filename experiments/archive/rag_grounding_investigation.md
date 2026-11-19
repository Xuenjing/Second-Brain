# RAG Grounding Investigation

## Purpose

Investigate whether the remaining RAG answer-grounding errors can be improved through prompt structure, context size, answerability checks, or a larger local language model.

The retrieval pipeline was already considered stable enough for this investigation:

- Embedding model: `intfloat/multilingual-e5-small`
- Semantic threshold: `0.82`
- Top-k: `5`
- Identifier-aware hybrid ranking enabled
- Production retrieval evaluation:
  - Top-1: `34/36 (94.4%)`
  - Top-5: `35/36 (97.2%)`

The main remaining generation issue was a semantic property mismatch, especially:

- Context contains **lunch** information.
- Question asks about **dinner**.
- The model sometimes reuses lunch times as if they were dinner times.

---

## Baseline

Model:

`Qwen/Qwen3-1.7B`

Generation settings:

- `do_sample = False`
- deterministic generation
- `max_new_tokens = 200`

Baseline grounding evaluation:

- Retrieval: `11/11 PASS`
- Generation: `13/15 PASS`

Remaining failures:

1. `När serverar Matsal 18 middag?`
   - Context contains lunch hours.
   - Model incorrectly answers with the lunch hours as dinner hours.

2. `När öppnar Huvudmatsalen för middag?`
   - Context contains lunch hours.
   - Model answers with lunch information instead of reporting that dinner information is missing.

This became the reference baseline for the investigation.

---

## Experiment 1: Move grounding rules to the system prompt

Grounding rules were moved from the user prompt to the system prompt while keeping retrieval and test cases unchanged.

Initial evaluation appeared as:

- Generation: `11/15`

However, two failures were false negatives caused by the evaluator:

- `Har Niklas ett telefonnummer?`
- Model answer: `Nej.`

The evaluator originally expected the phrase `inget telefonnummer`, even though `Nej.` was correct.

The evaluator was updated to allow multiple valid forms for these cases.

After correcting the evaluator:

- Generation: `13/15 PASS`

The same two lunch/dinner failures remained.

### Conclusion

Moving grounding rules to the system prompt did not solve the grounding problem, but it provided a clean and reasonable prompt structure.

---

## Experiment 2: Add stricter grounding instructions

Additional instructions were added, including rules such as:

- verify that the context contains the exact requested fact
- do not substitute information from another property, event, category, or time period
- treat related but different information as missing

Result:

- Retrieval: `11/11 PASS`
- Generation: `12/15 PASS`

New regression:

- Question: `Har Niklas ett telefonnummer?`
- Context states that Niklas has no phone number.
- Model answered: `Ja.`

The two lunch/dinner failures also remained.

### Conclusion

Adding more grounding rules made the smaller model less reliable.

More prompt instructions did not improve grounding and introduced a new regression.

The experiment was rolled back.

---

## Experiment 3: Context size — Top-5 vs Top-1

The two known meal-mismatch questions were tested with:

- full Top-5 context
- only the Top-1 retrieval result

### Matsal 18

Question:

`När serverar Matsal 18 middag?`

Top-5 answer:

`Matsal 18 serverar middag mellan klockan 10:30 och 13:30.`

Top-1 answer:

`Matsal 18 serverar lunch mellan klockan 10:30 och 13:30.`

Top-1 reduced the severity of the hallucination: the model no longer changed lunch into dinner.

### Huvudmatsalen

Question:

`När öppnar Huvudmatsalen för middag?`

Both Top-5 and Top-1 answered with lunch information.

### Conclusion

Additional similar context can increase semantic interference in some cases, but reducing context to Top-1 does not solve the general grounding issue.

---

## Experiment 4: Full evaluation with Top-1 context

The full 15-question evaluation was run using only the highest-ranked retrieval result as generation context.

Result:

- Retrieval: `11/11 PASS`
- Generation: `12/15 PASS`

Failures:

1. paraphrased Niklas negation question
2. Matsal 18 dinner mismatch
3. Huvudmatsalen dinner mismatch

### Conclusion

Top-1 context is worse overall than the Top-5 baseline.

Important information or useful redundancy can exist outside the highest-ranked result.

---

## Experiment 5: Full evaluation with Top-3 context

The same evaluation was run with Top-3 context.

Result:

- Retrieval: `11/11 PASS`
- Generation: `12/15 PASS`

Failures included:

- a new Huvudmatsalen paraphrase failure where the model echoed the question
- Matsal 18 dinner mismatch
- Huvudmatsalen dinner mismatch

### Conclusion

Top-3 did not improve grounding.

The production Top-5 approach remains the strongest tested context size.

---

## Experiment 6: Two-stage RAG answerability check

A separate first model call was introduced.

Pipeline:

1. retrieve Top-5 context
2. ask Qwen to classify the question as:
   - `SUPPORTED`
   - `NOT_SUPPORTED`
3. only generate a normal answer when classified as `SUPPORTED`

Result:

- Retrieval: `11/11 PASS`
- Support check: `12/15 PASS`
- Generation: `12/15 PASS`

Important classification errors:

### Niklas negation

Question:

`Finns det något telefonnummer till Niklas?`

The context explicitly states that Niklas has no phone number.

The support checker returned:

`NOT_SUPPORTED`

This was incorrect because the question is answerable from the negative fact.

### Matsal 18 dinner

Context contains only lunch information.

The support checker returned:

`SUPPORTED`

### Huvudmatsalen dinner

Context contains only lunch information.

The support checker returned:

`SUPPORTED`

### Conclusion

The answerability step reproduced the same semantic mistakes as normal generation.

Adding a second LLM call increased complexity and latency without improving accuracy.

---

## Experiment 7: Qwen3-4B

The baseline evaluation was repeated with:

`Qwen/Qwen3-4B`

No other intended changes were made.

Result:

- Retrieval: `11/11 PASS`
- Generation: `12/15 PASS`
- Total evaluation time: approximately `150 s`

For comparison, Qwen3-1.7B completed the baseline evaluation in approximately `60 s`.

Failures:

1. Negation contradiction:
   - `Ja, Niklas har inte ett telefonnummer.`

2. Language drift:
   - a correct negation answer was produced in Chinese instead of Swedish

3. Huvudmatsalen dinner mismatch:
   - lunch opening time was presented as dinner opening time

The Matsal 18 dinner case improved, but new failures appeared elsewhere.

### Conclusion

Qwen3-4B did not provide a net grounding improvement in this evaluation.

It was substantially slower and changed the error profile rather than eliminating the grounding problem.

---

## Overall Findings

The strongest tested configuration remains:

- Qwen3-1.7B
- deterministic generation
- Top-5 retrieval context
- concise grounding rules
- current production E5 + hybrid retrieval

Result:

- Retrieval: `11/11 PASS`
- Generation: `13/15 PASS`

The remaining failures are consistent semantic-property grounding errors.

The model sometimes treats closely related information as if it answered the requested property, for example:

- lunch vs dinner

The investigation did **not** find evidence that the issue can be reliably solved by:

- moving instructions between user/system prompts
- adding more grounding rules
- reducing context to Top-1
- reducing context to Top-3
- adding a separate LLM answerability check
- switching from Qwen3-1.7B to Qwen3-4B

The results suggest that the remaining issue is primarily a model-level grounding limitation rather than a simple retrieval, prompt-placement, sampling, or context-size problem.

---

## Recommendation

Keep the current production approach for now:

- Qwen3-1.7B
- Top-5 context
- deterministic generation
- concise grounding instructions

Do not add more prompt rules or a second LLM support-check stage at this point.

Possible future improvements should be investigated separately, for example:

- deterministic post-retrieval / pre-generation validation
- structured knowledge representation for properties and entities
- stronger models or external/internal AI providers
- larger and more diverse grounding evaluation datasets

These should be treated as separate implementation or research tickets rather than extending the current investigation.

---

## Ticket Conclusion

The grounding investigation is complete.

The current RAG pipeline is not perfectly grounded, but the remaining known failures have been isolated and investigated across multiple controlled experiments.

The current Qwen3-1.7B + Top-5 configuration remains the best overall tested trade-off between:

- answer quality
- stability
- latency
- implementation complexity

The remaining grounding limitation should be documented rather than addressed through additional prompt complexity in this ticket.
