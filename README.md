# the-method

`the-method` is a Claude Code skill for a goal you cannot yet name a way to reach. You describe the goal loosely (the Brain Dump). The skill finds the Problem Class it belongs to, picks a Method that is proven for that class and checks it against sources, then applies it to your task as a concrete Plan.

## Install

```
claude plugin marketplace add miolamio/the-method
claude plugin install the-method@codegeek-skills
```

## Example

```
/the-method I run a small design studio and need a website, but I don't know where to start
```

The document is written in the language of your Brain Dump. A fragment of the Plan from the Russian example, part of the way through a Walkthrough:

```
- [x] **S2 (M2).** Свести 14 проектов в таблицу: тип, качество фото, есть ли отзыв, «до/после». Отобрать 6–8 сильных, для слабых решить: обрезать, переснять или не брать. Done when: таблица и короткий список готовы к середине декабря.
  - Result: 2026-11-18 - таблица и короткий список готовы со слов автора; материалы Claude не проверял. confirmed by you
- [ ] **S3 (M3).** Нарисовать в Figma карту сайта: главная, проекты (страница-кейс на каждый), услуги с этапами и ценами «от», о студии, контакты с формой. Блог в карту пока не включать. Done when: карта помещается на один экран.
  - Skipped: 2026-11-18 - пропущен по решению автора, причина не указана; карта сайта не составлена.
```

Full examples, one per variant, written by the skill:

- [standard, in Russian, with a Walkthrough in progress](examples/interior-studio-lead-website.md)
- [decision](examples/startup-offer-decision.md)
- [no-class](examples/movement-sound-notation.md)

## What you get

One file, `methods/<task-slug>.md`, with seven sections: Task, Problem Class, Method, Grounding, Assumptions, Plan, Verification.

## Other modes

- Guided Walkthrough: `/the-method walk` takes you through the Plan one step at a time and records each result in the document.
- Revisions: `/the-method revise` changes the Plan, or the Method itself, after something turns out differently than assumed.

## Limits

- The skill does not execute the Plan.
- Lesser-known classes need web search.
- Personal or high-stakes decisions stay with you.
- In a Walkthrough, Claude Code asks for permission on every edit of the document and every run of the checking script, unless your permission mode already allows them. It may also ask once for each of the skill's own files. Accepting edits for the session and allowing the script removes most of these prompts.
- Known limitation of `0.1.0`: for a task with no ready Method, the skill may write a standard document on a weak basis, marked heuristic, where a no-class document fits. More rarely, an ordinary task gets a no-class document.

## Licence

MIT. See `LICENSE`. Method documents the skill writes for you are not covered by it.

## Feedback

Write to [Issues](https://github.com/miolamio/the-method/issues); pull requests are accepted, with no promise on timing.
