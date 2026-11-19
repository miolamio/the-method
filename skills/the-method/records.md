# Records and the `walkthrough` and `revised` keys

A Walkthrough keeps all its state in the document, in the `walkthrough` key and in record lines. Revisions use the same lines and the `revised` key. A Revision adds no record label and no section. Run the checking script after every record you write.

## The `walkthrough` key

Absent until a Walkthrough starts. Values:

- `in-progress`: a Walkthrough that is running, or that the person stopped and may resume. A stop has no value of its own.
- `paused`: the document needs revision before the Walkthrough continues. A `Paused:` line is present exactly while the key is `paused`.
- `finished`: the final check in Verification was carried out and recorded. `finished` has no outgoing transition; a later change of mind is a new run.

Transitions:

- `paused` to `in-progress` after a Plan Revision, or when the person lifts the pause. A lifted pause replaces the `Paused:` line with `Changed: <YYYY-MM-DD> - pause lifted by you: <reason>`.
- When the person declines a Revision, leave the document `paused` and mark nothing else.
- After a Method Revision the archive keeps `paused` and its `Paused:` line; the live file starts with no `walkthrough` key.
- `finished` is set only when the success check (or, for a decision, the process check) passed.

## The `revised` key

`revised: <YYYY-MM-DD>` is the date of the last Revision. Set it in a Plan Revision and in a Method Revision. Leave it unset after an in-place single-step change and in a document never revised.

## Record lines

Write progress as dated record lines, never as a log section. Each is a nested list item under a Plan step, added below that step's existing lines. Rewrite a step's own text or `Done when:` only through a `Changed:` line.

````markdown
- [x] **S2 (M2, M3).** <concrete action>. Done when: <condition>.
  - Result: <YYYY-MM-DD> - not met: <reason>. checked by Claude
  - Result: <YYYY-MM-DD> - <short result>. confirmed by you
- [ ] **S3 (M4).** <concrete action>. Done when: <condition>.
  - Changed: <YYYY-MM-DD> - <what was changed in this step and why>
  - Skipped: <YYYY-MM-DD> - <reason>
- [ ] **S4 (M5).** <concrete action>. Done when: <condition>.
  - Needs its own Method: <Problem Class of this step>. Run the-method on this step when you reach it.
  - Method: [<title>](<slug>.md)
  - Paused: <YYYY-MM-DD> - <why the document needs revision>
````

The labels are `Result:`, `Changed:`, `Skipped:`, `Paused:`, `Method:`. They stay English. The text after the label, dates in `YYYY-MM-DD` included, is in the Document Language, whatever language the person writes in during the session. Every record line except `Method:` starts with its date.

- `Result:` for every attempt at a step, met or not. It ends with who closed the step: `checked by Claude`, `confirmed by you` or `done by Claude`. A failed attempt says `not met:` and the reason. When the person closes a step against Claude's check, say the check did not pass. A step may hold several `Result:` lines; never remove an earlier one.
- At the end of Verification, one `Result:` list item in the same form records the final check. Name in it any steps the person skipped; name none removed in a Revision.
- `Changed:` when one step's action or `Done when:` is edited in place, including a `Done when:` nobody could observe rewritten to be observable. It is also the line for Plan Revision edits, `added: <reason>` and `pause lifted by you: <reason>`; [revision.md](revision.md) says which step gets which.
- `Skipped:` when the person skips a step; the checkbox stays empty. A step with records removed in a Plan Revision gets `Skipped: <YYYY-MM-DD> - removed: <reason>`.
- `Method:` links the document written for a step that needed its own Method, and for the last step of a no-class document when a class was found.
- `Paused:` when the Walkthrough pauses for revision. It sits under the step where work stopped, or under S1 when an Assumption fails the check at the start. It is the only record line ever removed, deleted when a Plan Revision completes.
- `[x]` means the step's `Done when:` was checked by Claude or confirmed by the person. A box ticked by hand with no `Result:` line counts as closed.
- A step with a `Skipped:` line is unchecked.
- Each record line is at most 25 words. Record lines count toward no section limit.
- Never renumber or reuse step and Assumption ids, so records stay attached to their step across sessions.
