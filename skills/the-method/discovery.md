# Discovery

The path from the Brain Dump to one chosen Method. Work in this order; each step is done when its output exists:

triviality check (SKILL.md), restatement, candidate classes, class boundary, several classes, questions, checkpoint, regularity check, research ([grounding.md](grounding.md)), comparison of candidate Methods.

Treat the order as a design judgment, not a proven procedure. Never skip the candidate classes.

## Restate the task

Restate the task as three items: the unknown, the givens, the success condition.

## Candidate Problem Classes

Name 2-3 candidate Problem Classes. Test each against its recognition criteria and against "looks similar but is not" counter-examples. The test may be brief; it is never skipped. Your own confidence in a class is not evidence for it.

## The class boundary

Use the broadest class in which the Method's steps stay the same and only values change. Deep structure of the problem guides recognition of the class; step stability sets its boundary.

Swap-a-noun test: swap a noun in the task. If the steps change, the noun belongs in the class. If the steps do not change, drop the noun from the class.

## Tasks that span several classes

- Classes that are parts of one goal: the Governing Class leads; the other classes become Plan steps marked as needing their own Method (marks in [variants.md](variants.md), expansion in [walkthrough.md](walkthrough.md)).
- Unclear which class applies: treat it as uncertainty and resolve it by a question or an Assumption.
- Independent goals with no shared success condition: the person chooses where to start; each goal gets its own document.
- Compose no hybrid Methods.

## Questions and Assumptions

After the candidate classes exist, restate the task, name the likely Problem Class, and ask in one batch only the questions that could change the Problem Class or the Method. Ask a question only when different answers lead to a different class or Method. There is no limit on the number of questions.

Every point the person does not answer, and every other unconfirmed fact about the task, becomes a recorded Assumption.

## The checkpoint

Stop for confirmation only when a question exists, the candidates remain close, or web research comes next. In every other case continue and record the class as an Assumption.

### The stop before research

Unless the person has already chosen one of the three choices below before the checkpoint is reached (then send no message and carry out that choice), before web research send one short message with four items: the class, the candidates, what model knowledge does not confirm, and what will be searched for. Offer three choices: research (the default), continue without research, or supply sources. Do not mention the Research Limit or any number from it.

What each choice means for research, and what to say when web research is unavailable, is in [grounding.md](grounding.md).

## Regularity check

Ask three questions about the task: can the result be checked, does the same action give the same result, is feedback fast. When two or more answers are no, mark the Method heuristic and prefer candidates with short cycles of trying and checking. When the Method is not marked heuristic, do not record the answers in the document.

The heuristic mark is independent of Grounding: Grounding says where the Method comes from, the mark says how far the environment lets any Method be reliable. Research does not remove the mark.

## Comparing candidate Methods

Collect 2-3 real candidate Methods. If only one established Method exists, say so and invent no other. A suitable tool is part of a candidate, a way to carry out its steps, and is compared like any candidate. A Method that points to a tool is still described, including how to verify the result.

Order of work:

1. Remove candidates whose applicability conditions fail.
2. Research each remaining candidate, at most three, in parallel, when it needs research ([grounding.md](grounding.md)).
3. Compare; remove a candidate for which no basis was found.

Comparison rules:

- Remove a candidate that another candidate beats on every criterion.
- Compare the rest only on criteria where they differ, with no numeric weights and no numeric scores.
- Find the fact the choice depends on. It becomes a question or an Assumption and supplies the condition for switching to an alternative.
- When nothing material separates the candidates, choose the one simplest to carry out and verify, and say the candidates are nearly equal.
- Stop once the next criterion could not change the choice.

## Recommend one Method

Recommend one Method and explain the choice. Name 1-2 alternatives, each with the condition for switching to it and one line on its basis. With only one established Method, name no alternative. The Choice block is in [variants.md](variants.md).

## Personal and high-stakes decisions

A personal or high-stakes decision is a choice that is hard to reverse or seriously affects health, money, legal position, or close relationships. For one:

- Establish what is being decided and who decides.
- Offer a list of possible objectives for the person to check.
- Select a decision method.
- Recommend no option; the decision stays with the person.
- Include consulting a specialist in the Method where needed.

The decision variant is in [variants.md](variants.md); its effectiveness search is in [grounding.md](grounding.md).

## When no class fits

Reach this case only after the normal path, including any research Grounding requires. Do not stretch the nearest class to fit.

After research, the class does not hold when, for every researched candidate, the claim that the Method applies to the task's own kind of object is unconfirmed: `not met: confirmed only for <domain>`, `searched, not found`, or cut off at the limit with no further round. Then write the no-class document, not a standard one with a weak basis. A broader class chosen so that the Method fits changes nothing. A candidate with that claim confirmed and other claims unconfirmed stays a standard document with a weak basis. This test does not apply when web research was unavailable or declined.

1. Say that no ready Method was found.
2. Settle the goal and the task-wide constraints.
3. Split the task into parts whose classes are recognisable.
4. Make small checked trials the first Plan steps.
5. Identify the class again after the trials.

Mark the result as a way to understand the task, not a proven Method for a class. The no-class variant is in [variants.md](variants.md).

## The class is provisional

The class is provisional until the document is finished. Return to the candidates once on any of three events: a correction from the person, research that contradicts the recognition criteria, Plan steps that cannot be made concrete. If the class still fails after that return, tell the person.

Correction of a saved document belongs to [revision.md](revision.md), not here.
