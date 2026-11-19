# Guided Walkthrough

In a Walkthrough the person carries out the Plan step by step. The person leads and confirms, Claude checks what it can, and every step has a `Done when:`. All state lives in the document, as record lines and the `walkthrough` key; write them as in [records.md](records.md). Nothing is stored anywhere else. Run the checking script after every write. Document edits follow [format.md](format.md).

## Starting

- Start only when asked. After writing a document, offer a Walkthrough in one line. The person may also ask for it in words or with `/the-method walk methods/<slug>.md`.
- Refuse to walk an archive (`<slug>.r<n>.md`) and point to the live file. A document with `walkthrough: finished` is not walked again; a later change of mind is a new run.
- Before the first step, show the Assumptions and ask whether they still hold.
- A wrong Assumption that touches zero or one step is fixed in place, as under Changing the document below, and the Walkthrough begins. One that touches more than one step pauses the Walkthrough before S1, with a `Paused:` line under S1.

## Resuming

- Take state only from the file. Name the first open step, sum up the closed steps in one or two lines, and ask whether anything changed since last time.
- After a Plan Revision lifts a pause, name the first open step and show for confirmation only the Assumptions that are new or changed.
- Trust hand edits. Take the file as it is. Name each step ticked with no `Result:` line as closed and do not ask for a recheck.

## Working a step

- Offer the first open step by default; the person may take any step. When the chosen step relies on an open earlier step, say so once.
- Check whatever you can observe: files, command output, calculations. Close what you cannot observe on the person's word. Tick a step only on one of these two, and write the `Result:` line.
- The person has the last word and may close a step against your check; the `Result:` line then says the check did not pass.
- A `Done when:` that nobody can observe is a defect of the document. Propose an observable condition; once the person agrees, record it with `Changed:`, then work the step.
- Carry out a step yourself only when asked, one step per request. Show the result, wait for the person's confirmation, then open the next step. The record ends `done by Claude`.
- Asked to do all remaining steps, say that carrying out a whole Plan by itself is outside the skill, and offer to continue step by step.

## Failed steps

- Leave a failed step unticked and write a `Result:` line for every attempt.
- Name one of three causes: an error in carrying the step out (repeat the step); a wrong Assumption (follow its `If wrong:`); a Method that does not fit (the `Switch when:` of an alternative in Choice applies).
- After the second failure on one step, raise whether the Plan is wrong and propose no third attempt. Count across sessions from the records.

## Skipping and returning

- The person may skip any step. Say once what depends on it: later steps and Method steps left without a carried-out step. Do not argue. A skipped step stays unticked and gets a `Skipped:` line.
- Return to a closed step only through `If it fails:` or a try-and-check cycle of a heuristic Method. Untick the step, keep its earlier records, and add the new attempt below them.

## Changing the document

- A change to one Plan step (wording, action or `Done when:`) is made in place with one `Changed:` line. Closed steps stay untouched and `revised` stays unset.
- A wrong Assumption that touches zero or one step moves out of Assumptions into Task `Given:` after the person confirms the corrected fact, even when the fix is made in place.
- Anything larger pauses the Walkthrough with the reason in a `Paused:` line and sets `walkthrough: paused`. Larger means an Assumption that changes several steps, a wrong Method, or a wrong Problem Class. Offer the Revision in one line and never start it yourself; [revision.md](revision.md) holds it.

## Steps that need their own Method

A Plan step marked `Needs its own Method:` is expanded into its own document in only two cases: the person asks (`/the-method expand methods/<slug>.md S<n>`), or the Walkthrough reaches the step.

- On reaching such a step, offer to run the-method on it. The person may decline and work the step without a separate document.
- On agreement, run the skill again in the main session with the discovery stage; never hand it to a subagent, because the person must answer the questions.
- The child's Brain Dump is the parent step's text, its `Done when:`, the parent's Problem Class as context only, and the Given. Show it to the person in one line for confirmation.
- The child run finds the step's own Problem Class through normal discovery. Its slug follows the slug rule in [format.md](format.md). Its Given carries over the parent's Given with the results already recorded.
- Write the child document with its own Walkthrough and link it from the parent step with a `Method:` line. The parent step closes only on its own `Done when:`.

## Finishing

- After the last step, run the `Success check:` from Verification and record it as the final `Result:` item. If it passes, set `walkthrough: finished`. If it fails, follow `If it fails:`.
- The person may stop at any point. The document stays ready to resume with `walkthrough: in-progress`.
- In a decision document the `Process check:` replaces the success check. Rate or recommend no option at any step. `Review on:` stays in the document; set no reminders. When the person has decided, ask whether to record the choice, and record either the choice in the person's own words or only "decision made" with its date, in the Verification `Result:` item.
- In a no-class document, when the last step finds a Problem Class, close the step with the class in its record, offer to run the-method for that class, and link the new document from the step with a `Method:` line. The original Walkthrough ends with its usual check. Finding the class is not a Revision.
