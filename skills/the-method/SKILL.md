---
name: the-method
description: Turns a loose description of a goal into a proven way of solving that kind of problem (a Method), applied to the person's case as a Plan, saved in methods/<slug>.md. Use when the person explicitly asks for an approach, a method or an established way to go about a task, or runs /the-method. Not for doing the task itself, quick factual questions, or ordinary planning requests.
allowed-tools: Bash(python3 "${CLAUDE_SKILL_DIR}/scripts/check_method.py" *)
---

# The Method

Take the person's goal, find the kind of problem it is (the Problem Class), choose a reusable Method for that class, and apply it to their task as a Plan. The result is one file, `methods/<slug>.md`. Optionally, walk the person through the Plan step by step.

## Choose the mode

Choose the mode from the request and from the state of `methods/<slug>.md` (its `walkthrough` key and its status line).

| Request | Mode | Read |
|---|---|---|
| A Brain Dump, or no arguments | New run | [discovery.md](discovery.md), [grounding.md](grounding.md), then [format.md](format.md) and [variants.md](variants.md) |
| `walk` | Guided Walkthrough | [walkthrough.md](walkthrough.md), [records.md](records.md) |
| `revise` | Plan Revision or Method Revision | [revision.md](revision.md), [records.md](records.md) |
| `expand <file> S<n>`, e.g. `/the-method expand methods/<slug>.md S3` | Expand a Plan step into its own Method, as a new run in this session | [walkthrough.md](walkthrough.md) |

With no arguments, start a new run. If exactly one document has `walkthrough: in-progress` or `paused`, offer it in one line. If several exist and one is needed, ask which.

Read a file only when you enter its stage. Any write of a document also needs [format.md](format.md) and [variants.md](variants.md).

## New run

1. Run the triviality check (below).
2. Follow [discovery.md](discovery.md): restate the task, name candidate classes, ask one batch of questions, stop before research (unless the person already chose how to proceed), compare Methods.
3. Follow [grounding.md](grounding.md): establish the basis of each candidate, research where needed.
4. Write `methods/<slug>.md` following [format.md](format.md) and [variants.md](variants.md), then run the check.

A Method Revision re-enters steps 2 and 3 through [revision.md](revision.md).

## Triviality check

This is the first step of every run. A task is trivial when all three hold:

- the full answer fits a short reply;
- the person has nothing to carry out;
- the person did not ask for a way of solving it.

For a trivial task, give the short answer, write no document, and offer a Method in one line.

A request that asks how to solve a task of this kind is not trivial; start the full procedure. Starting the skill through the slash command does not by itself count as asking for a way of solving.

## Hard rules

- The person decides. Where a choice belongs to the person, offer it and record their answer.
- A whole Plan is carried out by the person. Guide a Plan step by step; do not execute it end to end.
- A trivial task gets a short answer, not a Method.

## Check after every write

After every write of the document, in every mode (new run, Walkthrough record, Revision), run:

```
python3 "${CLAUDE_SKILL_DIR}/scripts/check_method.py" methods/<slug>.md
```

After a Revision, run it on the live file before reporting the Revision as done.

The script prints `ERROR <rule-name>: <detail>` lines and exits 0 when the document passes, 1 on rule violations, 2 when it could not run. On an error, fix the document and run the script again before showing the result. Files named `<slug>.r<n>.md` are archives; the script skips them.

If Python does not start, check the document by hand against the rule list in [checks.md](checks.md) and tell the person in one line that the script did not run.

## Files

- [discovery.md](discovery.md): the path from Brain Dump to the chosen Method.
- [grounding.md](grounding.md): basis, sources, research, the two agents.
- [format.md](format.md): headings, ids, size limits, frontmatter keys.
- [variants.md](variants.md): the three document skeletons.
- [checks.md](checks.md): the manual check list.
- [records.md](records.md): the `walkthrough` and `revised` keys and record lines.
- [walkthrough.md](walkthrough.md): the Guided Walkthrough.
- [revision.md](revision.md): Plan Revision and Method Revision.
