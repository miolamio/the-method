# Manual checks

Use this list only when Python does not start. Tell the person in one line that the script did not run. Check the document by hand against every rule below and fix each failure before showing the result. Skip files named `<slug>.r<n>.md` (archives).

A failure reads `ERROR <rule-name>: <detail>`. Rules marked English-only apply when `language: en`; for other languages apply the rule named beside it. All other rules apply to every language.

Words: tokens separated by spaces, without Markdown markers and without tokens that have no letter or digit (a lone `-`). The id header `**S1 (M1).**`, `**A1.**` or `**R1.**` of a step, Assumption or source is not counted.

## Frontmatter

- `frontmatter-keys`: the file starts with `---` and a closing `---`. Keys `method_document`, `task`, `created`, `variant`, `basis`, `heuristic`, `no_recommendation` are present. Allowed values: `method_document: 1`; `variant`: standard, decision, no-class; `basis`: established-knowledge, researched-practice, supplied-by-person, unverified, none; `description_confirmed`: yes, partly, no; `effectiveness`: confirmed, no-checks-found, not-searched; `heuristic` and `no_recommendation`: true, false.
- `language-code`: `language` is a language code such as `en`, `ru`, `pt-BR`.
- `task-slug`: `task` is two to five lowercase Latin words joined by hyphens, no digits.
- `date-format`: `created`, and `revised` when present, is a real date `YYYY-MM-DD`.
- `basis-none`: `basis: none` if and only if `variant: no-class`.
- `description-confirmed-presence`: `description_confirmed` is absent for `no-class` and present for the other variants.
- `effectiveness-presence`: for `no-class`, `effectiveness` is absent unless `no_recommendation: true`, and then present. For the other variants it is present.
- `decision-no-recommendation`: `variant: decision` has `no_recommendation: true`.
- `not-searched-no-recommendation`: `effectiveness: not-searched` never appears with `no_recommendation: true`.
- `walkthrough-value`: `walkthrough`, when present, is `in-progress`, `paused` or `finished`.

## Structure

- `heading-order`: the H2 headings are exactly Task, Problem Class, Method, Grounding, Assumptions, Plan, Verification, in that order.
- `required-labels`: every required field is present as a top-level list item `- **Label:** value`, with a value or nested items. Required labels by section:
  - Task, standard: Unknown, Success condition. Task, decision (and no-class with `no_recommendation: true`): Decision, Decider, Objectives (proposed by the-method; keep or strike), Success condition.
  - Problem Class, standard and decision: Class, Recognise it by, Not this class when, Boundary, Candidates considered. No-class: Class, Candidates considered, Parts with recognisable classes.
  - Method, standard and decision: Name, Applies when, Steps, Verify the result, Depends on, and the heading `### Choice`. No-class: Steps, Verify the result.
  - Grounding, standard and decision: Basis, Rests on, Description confirmed, Effectiveness confirmed, Unconfirmed. No-class: Basis, Rejections rest on, Searched for, Unconfirmed (at least one entry, not `Nothing`). With `heuristic: true` add Heuristic. If Sources is present, Accessed is present.
  - Verification, standard (and no-class): Success check, If it fails. Decision (and no-class with `no_recommendation: true`): Outcome, Process check, Review on, If it fails.
- `empty-optional-field`: these optional fields are either left out or have a value: Given, Other classes in this task, Tool, Sources, Accessed, Excluded, Heuristic, and a step's `Needs its own Method:`. A value of None, N/A, not applicable or Nothing counts as empty.

## Status line and fixed sentences

- `status-line` (English-only): build the line from the frontmatter. Marks in this order, joined by ` · `, each when its condition holds:
  1. `variant: no-class`: No ready Method found: this is a way to understand the task, not a proven Method for a class
  2. `no_recommendation: true`: No option is recommended, the decision is yours
  3. `basis: unverified`: Unverified
  4. `description_confirmed: partly`: Description partly confirmed
  5. `description_confirmed: no`: Description not confirmed
  6. `heuristic: true`: Heuristic
  7. `effectiveness: no-checks-found`: No effectiveness checks found

  The line is `> ` plus the marks, directly under the H1 (blank lines allowed). With no marks there is no line. It must equal the built one.
- `status-line-marks` (other languages): the status line has as many marks, separated by ` · `, as the frontmatter gives in the table above, and is left out when none applies. The wording is free.
- `fixed-sentences` (English-only): each of these has exactly this text.
  - No-class Method: the line before Steps reads "No ready Method was found for this task as a whole. These steps are the-method's fixed procedure for that case, not a Method for a class." Steps M1 to M4 read, in order:
    - M1. Settle the goal and the constraints that hold for the whole task, and have the person confirm them.
    - M2. Split the task into parts and record which parts have a recognisable Problem Class.
    - M3. For each part without one, run a small trial that can be undone, with the expected result written down first, and compare.
    - M4. Test again whether one Problem Class fits the whole task. If one does, run the-method for it. If none does, repeat from M2 or stop and say so.
    - There is no M5.
  - Choice with only one candidate line holds the line `No other established Method found.`
  - A nested `Needs its own Method: <class>. Run the-method on this step when you reach it.`
  - `Outcome:` reads `not checkable at decision time.`
  - On a no-class document, `Basis:` reads `none - the steps are the-method's own procedure.`
  - `Description confirmed:` reads `yes`, `partly` or `no`, then ` - `, then a reason.
  - With `effectiveness: not-searched`, `Effectiveness confirmed:` reads `not searched - common practice, not proven effective`.
  - Every `Unconfirmed:` entry ends with one of: `search stopped at the limit`, `searched, not found`, `research declined`, `web research unavailable`, `source excluded`. Entries are nested items, or one line split at `;`. `Nothing` has no entries.
  - A source line that mentions "same publisher" says `same publisher as R<n>`. An Excluded entry that mentions "used at the person" says `used at the person's choice`.
- `fixed-sentence-places` (other languages): the same places are filled with text in the Document Language, except that `Description confirmed:` begins `yes | partly | no - `; with `not-searched` the line begins `not searched - ` plus a sentence; on a no-class document `Basis:` begins `none - ` plus an explanation. Also: the no-class Method has an introduction line, non-empty M1 to M4 and no M5; a one-candidate Choice has a sentence line besides the candidate and `Depends on:`; `Needs its own Method: <class>.` has a second sentence; each Unconfirmed entry has ` - ` and a reason.

## Method and Plan

- `method-step-uncited`: every `M<n>` in Method is cited by at least one Plan step. A step removed in a Revision (a `Skipped:` record whose text is `<date> - removed: ...`) does not count as citing.
- `step-cites`: every Plan item reads `- [ ] **S<n> (M1, M2).** ...` (or `[x]`), citing existing `M<n>` ids. A step citing `(-)` has `Why:` in its text. Removed steps are not checked.
- `done-when`: every Plan step, removed ones included, has `Done when:` in its own text.
- `duplicate-id`: no step id and no Assumption id appears twice. Gaps are fine.

## Grounding

- `unknown-source-ref`: every `R<n>` cited in Problem Class, Method or Grounding is defined as a source `**R<n>.**` under Sources.
- `unknown-assumption-ref`: every `A<n>` cited in Method (including Choice), Grounding or Verification is defined in Assumptions. Plan text and record lines are not checked.
- `source-level`: each source under Sources has, after the link, a comma and then exactly one of `primary`, `reliable secondary`, `weak`, followed by ` (`, `:` or the end of the line.
- `links-in-established`: with `basis: established-knowledge` no line in the file contains `http://` or `https://`.

## Size

- `size-limit`: all of these hold.   - Task: at most 80 words; at most 130 for `decision` and for no-class with `no_recommendation: true`.
  - Problem Class: 150. Method including Choice: 220.
  - Grounding: 120, not counting the Sources, Excluded and Unconfirmed items and their nested lines.
  - Each source and each Excluded entry: 35. Each Unconfirmed entry: 25. Each Assumption: 25, at most 7 Assumptions.
  - Plan: 45 words per step, counting the step line only (not nested lines). 3 to 9 steps, not counting removed ones.
  - Verification: 70, not counting a `Result:` list item.

## Walkthrough records

Record lines are the nested items under a Plan step (not `Needs its own Method:`) and top-level non-bold items in Verification.

- `paused-line`: the document has a `Paused:` record if and only if `walkthrough: paused`.
- `finished-result`: with `walkthrough: finished`, Verification has a `Result:` item.
- `record-label`: every record line starts with `Result:`, `Changed:`, `Skipped:`, `Paused:` or `Method:`.
- `record-date`: every record line except `Method:` has a real date `YYYY-MM-DD` right after the label.
- `record-length`: each record line, label and date included, has at most 25 words.
- `result-ending`: each `Result:` under a Plan step ends with `checked by Claude`, `confirmed by you` or `done by Claude` (a final full stop is allowed).
- `skipped-step-ticked`: a step with a `Skipped:` line has an empty checkbox `[ ]`.
- `method-link`: each `Method:` line has a link `[title](path)`, and the file exists, with the path read from the document's folder.
