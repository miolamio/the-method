# Changelog

## 0.1.0 - 2026-11-19

First public release.

- The skill `the-method`: from a Brain Dump it finds the Problem Class, picks a Method and checks it against sources, and applies it to the task as a Plan in `methods/<task-slug>.md`. Three document variants: standard, decision, no-class.
- Guided Walkthrough (`/the-method walk`) and revisions of the Plan or the Method (`/the-method revise`).
- Agents `researcher` and `restater`, and the checking script `check_method.py` for Method documents.
- Three examples in `examples/`, one per variant, written by the skill.
- Known limitation: Evaluation Case 8 (No class fits) passed 1 of 3 runs in the gate run of 2026-11-18 and is excepted from the 2-of-3 rule for `0.1.0`. For a task with no ready Method the skill may write a `standard` document on a weak basis, marked heuristic, where a `no-class` document is expected; more rarely an ordinary task gets a `no-class` document. Not fixed in `0.1.0`; the gate for `1.0.0` keeps the case.
