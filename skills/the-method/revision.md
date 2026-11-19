# Revision

A Revision corrects a saved document whose Task is unchanged. Record lines, the `revised` key and the `walkthrough` transitions are in [records.md](records.md); write the document as in [format.md](format.md) and [variants.md](variants.md). Run the checking script on the live file after every Revision, before reporting it done.

## Is it a Revision

- A changed Unknown or Success condition is a new run with a new slug. For a decision document, a changed Decision, Decider or Success condition is a new run. Leave the old document as it is and say so instead of revising.
- A document with `walkthrough: finished` is not revised; a later change of mind is a new run.
- A change to one Plan step is not a Revision, inside or outside a Walkthrough: edit in place with one `Changed:` line and leave `revised` unset.
- A wrong Assumption that touches zero or one step is handled the same way and still moves from Assumptions to Task `Given:`.
- Anything touching more than one step, or replacing the Method or the Problem Class, is a Revision. Keep the Task and the person's earlier answers; a Revision never restarts from a blank Brain Dump.
- Refuse to revise an archive (`<slug>.r<n>.md`) and point to the live file.

## Entry and the message

- The entry is `/the-method revise methods/<slug>.md` or a request in words, with or without a Walkthrough ever started. A paused Walkthrough offers a Revision in one line. Never start one yourself.
- Before editing, send one message that names what turned out wrong, which kind of Revision follows, and what will be kept. Wait for the person's agreement, then edit.
- The person may decline: the document stays `paused` for as long as they like, with nothing else marked. The person may instead lift a pause without revising: replace the `Paused:` line with `Changed: <date> - pause lifted by you: <reason>` and return to `in-progress`.

## Choosing the kind

The document has two halves: the reusable part (Problem Class, Method, Grounding) and the one-task part (Task, Assumptions, Plan, Verification).

- Plan Revision: the Problem Class and Method hold, an Assumption was wrong, and more than one step changes. It edits this file in place, and only Assumptions, Plan, Verification and Task `Given:` (plus the `Depends on:` line in Choice, below).
- Method Revision: the Method or the Problem Class is replaced. A switch to an alternative already listed in Choice is a Method Revision, because Grounding, the marks and the `M<n>` ids change with it.

## Plan Revision

- A wrong Assumption leaves Assumptions. The corrected fact, confirmed by the person, goes into Task under `Given:`. When `Given:` outgrows the Task limit, condense older facts.
- Never edit a closed step's text or records. When its result no longer holds and the same step must be redone as written, untick it and keep its records. When a different action is needed, add a new step and leave the closed one closed.
- Rewrite, add or remove open steps. Number new steps by the id rules in [format.md](format.md).
- Each rewritten or unticked step gets a `Changed:` line naming the wrong Assumption and the change. An added step gets `Changed: <date> - added: <reason>`.
- A removed step that has records (a `Method:` line included) stays, unticked, with `Skipped: <date> - removed: <reason>`. Delete a removed step that has no records.
- When a removed Assumption is cited by `Depends on:` in Choice, correct that line too, since the checking script requires every cited `A<n>` to exist: delete the removed id, and when no `A<n>` is left write `your answer: <the corrected fact>`. This is the one edit to Choice a Plan Revision makes.
- Set `revised`. The section limits apply to the revised text unchanged.
- Leaving `paused`: when the revised file passes the checking script and the person has seen a short summary of the changes, delete the `Paused:` line and set `walkthrough: in-progress`. The reason survives in the `Changed:` lines. Then resume as in [walkthrough.md](walkthrough.md).

## Method Revision

1. Rename the live file to `methods/<slug>.r<n>.md`, where n counts up from 1 with each Method Revision. Never edit the archive again; it keeps whatever state it had. Do not depend on git for it.
2. Restart from the earliest broken point with the normal rules and no shortcuts: read [discovery.md](discovery.md) and [grounding.md](grounding.md) and follow them. They are the only source of those rules.
   - A wrong Problem Class goes back to class recognition with the failed class excluded. When nothing fits, the result is a no-class document.
   - A switch to a listed alternative gets full Grounding, including the checkpoint before research.
3. Derive the heuristic check and every mark again.
4. Write the new document at `methods/<slug>.md`, the live file. Keep the original `created:` and set `revised:`.
5. State the reason for the change where the format has a place for it: the old Method in Choice as `removed:`, or the old class under `Candidates considered:` as `rejected:`, each with its reason.
6. Start the Plan at S1, with no steps, ticks or records carried over. Write what the person already achieved into Task under `Given:`; do not repeat it in the new Plan.
7. Leave out the `walkthrough` key and offer a Walkthrough in one line.

Before a second Method Revision of one task (a `<slug>.r1.md` exists), raise whether the Task is misstated or no class fits, and offer a new run or the no-class variant. The number of Revisions has no cap.

## Child documents

- Never edit or delete a child document (linked by a `Method:` line) in a Revision; a child is revised only through its own Revision.
- After a Method Revision a child stays linked from the archive only.
- When a step of the new Plan needs its own Method for the same Problem Class, offer to link the existing child instead of writing another.

## No-class documents

Finding a class at the last step of a no-class document is not a Revision; follow the route in [walkthrough.md](walkthrough.md), a new document for that class.
