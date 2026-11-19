# Format of the Method document

Read this file with [variants.md](variants.md) whenever you write or edit a document. Run the checking script after every write.

## File

- Write one Markdown file per task: `methods/<task-slug>.md`. Create `methods/` in the working directory when absent.
- Never overwrite a file. When `methods/<slug>.md` exists on a new run, offer a Revision of that document or ask the person for a distinguishing word in the slug.
- The slug is two to five English words in lowercase Latin letters, joined by hyphens, with no digits, whatever the language of the Brain Dump. Take the words from the Unknown (standard), the Decision field (decision) or the Task's goal as restated (no-class).
- `<slug>.r<n>.md` files are archives of Method Revisions, not live documents.
- The document has no short form. A simple document on model knowledge runs 750-800 words, a researched one 1000-1150. A task too small for it is handled by the triviality check in [discovery.md](discovery.md).
- Order: frontmatter, H1, status line, then the seven H2 sections: Task, Problem Class, Method, Grounding, Assumptions, Plan, Verification. Method holds `### Choice` in the standard and decision variants.

## Rules for every variant

- Fixed parts: frontmatter keys, the seven H2 headings, `### Choice`, bold field labels, the ids. The H1 is written in the Document Language.
- Leave an optional field out when it is empty. Write a field that is not optional every time. Write nothing like "None" or "not applicable" for an optional field.
- Problem Class, Method and Grounding are the reusable part; Task, Assumptions, Plan and Verification belong to the one task.
- Keep every value of this task out of Method, Choice included: names, numbers, dates, files from the Task. Class terms and tool names belong there. A `Depends on:` line that names an Assumption id is not a task value.
- Every Plan step cites the Method steps it carries out, as in `S3 (M3, M4)`; every Method step is cited by at least one step; several steps may cite one Method step.
- A step that serves no Method step cites `(-)` and gives `Why:` (setup, a risk check, a specialist, the person's own goal such as understanding).
- A step removed in a Revision that has records counts neither toward the 3-9 steps nor toward citation of Method steps. A step the person skipped counts toward both.
- Write each check once. Method's `Verify the result` checks any task of the class. Verification holds only what is specific to this task. A step's `Done when:` covers that step and leaves out the final check.
- Plan steps are checkboxes (`- [ ]`) with a permanent id and a `Done when:`.
- The status line repeats the marks without reasons. Give reasons once, in Grounding.

## Ids

`M<n>` Method steps, `S<n>` Plan steps, `A<n>` Assumptions, `R<n>` sources. Step ids and Assumption ids are unique, need not be consecutive, and are permanent: never renumber or reuse one. A new step takes the next unused number and sits where it belongs in the order; the file may read S1, S2, S3, S9, S5.

## Frontmatter

Keys in this order:

```yaml
---
method_document: 1
language: <code, e.g. en | ru | pt-BR>
task: <task-slug>
created: <YYYY-MM-DD>
revised: <YYYY-MM-DD>                            # optional
variant: standard | decision | no-class
basis: established-knowledge | researched-practice | supplied-by-person | unverified | none
description_confirmed: yes | partly | no
effectiveness: confirmed | no-checks-found | not-searched
heuristic: true | false
no_recommendation: true | false
walkthrough: in-progress | paused | finished     # optional
---
```

- `language`: any language code, no list of supported languages. `created` is kept across a Method Revision. `revised` and `walkthrough` are in [records.md](records.md).
- `basis` holds one value. `none` goes with `variant: no-class` and only with it. For researched practice combined with person-supplied material, [grounding.md](grounding.md) names the value.
- `description_confirmed`: left out for `no-class`. `yes` when every key claim met its source threshold or, for established knowledge, the independent restatement agreed on every step and applicability condition; `partly` when some did; `no` when none did. The `restater` running on the same model does not lower the mark.
- When the main session made the restatement itself because subagents were unavailable: `partly`, `basis` stays `established-knowledge`, and the `Description confirmed:` line carries `restated by the main session, not independent` in its how slot.
- When research stops at the Research Limit with claims missing: `partly` or `no`, with the missing claims under `Unconfirmed:`. No extra key or mark exists for the limit.
- `effectiveness`: left out for `no-class` unless `no_recommendation: true`. `not-searched` never goes with `no_recommendation: true`. A decision document searches for studies, so it takes `confirmed` or `no-checks-found`. With `not-searched` the Grounding line reads `Effectiveness confirmed: not searched - common practice, not proven effective`.
- `heuristic: true` marks a heuristic Method, decided by [discovery.md](discovery.md). Research does not remove it. With `false`, do not record the regularity-check answers; with `true`, `Heuristic:` gives the reason.
- `no_recommendation` is `true` for `decision`; it may be `true` for `no-class` when the task is a personal or high-stakes choice.

## Status line

One blockquote line directly under the H1, built from the frontmatter. Write the marks in this order, joined by " · "; omit the line when no mark applies. The frontmatter is the truth where the two differ. `not-searched` has no mark.

| Condition | Mark (`language: en`) |
|---|---|
| `variant: no-class` | No ready Method found: this is a way to understand the task, not a proven Method for a class |
| `no_recommendation: true` | No option is recommended, the decision is yours |
| `basis: unverified` | Unverified |
| `description_confirmed: partly` | Description partly confirmed |
| `description_confirmed: no` | Description not confirmed |
| `heuristic: true` | Heuristic |
| `effectiveness: no-checks-found` | No effectiveness checks found |

## Size limits

| Section | Limit |
|---|---|
| Task | 80 words; 130 for decision |
| Problem Class | 150 words |
| Method, with Choice | 220 words |
| Grounding, without Sources, Excluded and Unconfirmed | 120 words |
| Sources | 35 words per source |
| Excluded | 35 words per entry |
| Unconfirmed | 25 words per entry |
| Assumptions | 25 words each, at most 7 |
| Plan | 45 words per step, 3-9 steps |
| Verification | 70 words |

The whole document has no limit. Record lines sit outside the limits.

## Language

- Set the Document Language once, at creation, from the Brain Dump. A mixed Brain Dump gives the language of most of it, with no question; English terms inside text in another language change nothing. Records and Revision edits use it even when the person writes otherwise. A different language takes a new run.
- The person's request for another language applies to text, never to labels. Decline a request to translate labels in one sentence saying the check reads them.
- Chat replies follow the person's language.
- English in every document: frontmatter keys and values; the seven H2 headings and `### Choice`; every field label, the text up to and including its colon; record labels `Result:`, `Changed:`, `Skipped:`, `Paused:`, `Method:`; the ids and the name `the-method`; the enumerated values below.
- In the Document Language: the H1, all text written for the task, the whole status line (each mark translated), and the fixed sentences with their label left English. Use ordinary words of the language for Problem Class, Method, Plan and Assumption.
- Keep source and publisher names in the original language. State claims in the Document Language with no translated direct quotes. Copy the `researcher`'s claims and `Unconfirmed:` reasons without rewriting.
- Enumerated values, always English: `checked by Claude`, `confirmed by you`, `done by Claude`, `not met:`, `primary`, `reliable secondary`, `weak`, `threshold met`, `chosen:`, `removed:`, `rejected:`, `alternative`, `your answer:`, `nothing material:`, `yes`, `partly`, `no` after `Description confirmed:`, `no checks found` and `not searched` after `Effectiveness confirmed:`, `None.`, `Nothing`, `None found`.

## Fixed sentences

For `language: en` write the exact text; in any other language keep the meaning, fill every place, and keep the number and order of status marks.

- No-class Method text and steps M1-M4 ([variants.md](variants.md)).
- `Needs its own Method: <Problem Class of this step>. Run the-method on this step when you reach it.` In Russian: `Needs its own Method: <класс>. Запустите the-method на этом шаге, когда дойдёте до него.`
- `No other established Method found.`
- `not checkable at decision time` in `Outcome:`.
- `the steps are the-method's own procedure.` after `Basis: none -`.
- The five `Unconfirmed:` reasons ([variants.md](variants.md)).
- `restated by the main session, not independent`.
- `common practice, not proven effective`.
- `same publisher as R<n>` and `used at the person's choice`.
