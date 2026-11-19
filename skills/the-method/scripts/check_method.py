#!/usr/bin/env python3
"""Check Method documents (methods/<slug>.md) against the-method script rules.

Usage: python3 check_method.py FILE [FILE ...]

Prints one line per error: ERROR <rule-name>: <file>: <detail>
Skips archive files named <slug>.r<n>.md.
Exit codes: 0 passes, 1 rule violations, 2 the script could not run.
Standard library only; works on Python 3.8+.
"""
import datetime
import os
import re
import sys

# Rule name -> specification rule it implements.
RULES = {
    "frontmatter-keys": "SS-55",
    "language-code": "SS-56",
    "task-slug": "SS-57",
    "date-format": "SS-58",
    "basis-none": "SS-59",
    "description-confirmed-presence": "SS-60",
    "effectiveness-presence": "SS-61",
    "decision-no-recommendation": "SS-62",
    "not-searched-no-recommendation": "SS-63",
    "walkthrough-value": "SS-64",
    "heading-order": "SS-65",
    "required-labels": "SS-66",
    "empty-optional-field": "SS-67",
    "status-line": "SS-68",
    "fixed-sentences": "SS-69",
    "status-line-marks": "SS-70",
    "fixed-sentence-places": "SS-70",
    "method-step-uncited": "SS-71",
    "step-cites": "SS-72",
    "done-when": "SS-73",
    "duplicate-id": "SS-74",
    "unknown-source-ref": "SS-75",
    "unknown-assumption-ref": "SS-76",
    "source-level": "SS-77",
    "links-in-established": "SS-78",
    "size-limit": "SS-79",
    "paused-line": "SS-80",
    "finished-result": "SS-81",
    "record-label": "SS-82",
    "record-date": "SS-83",
    "record-length": "SS-84",
    "result-ending": "SS-85",
    "skipped-step-ticked": "SS-86",
    "method-link": "SS-87",
}

ARCHIVE_RE = re.compile(r"\.r\d+\.md$")

H2_ORDER = ["Task", "Problem Class", "Method", "Grounding",
            "Assumptions", "Plan", "Verification"]

ENUMS = {
    "method_document": ("1",),
    "variant": ("standard", "decision", "no-class"),
    "basis": ("established-knowledge", "researched-practice",
              "supplied-by-person", "unverified", "none"),
    "description_confirmed": ("yes", "partly", "no"),
    "effectiveness": ("confirmed", "no-checks-found", "not-searched"),
    "heuristic": ("true", "false"),
    "no_recommendation": ("true", "false"),
}
ALWAYS_REQUIRED = ["method_document", "task", "created", "variant", "basis",
                   "heuristic", "no_recommendation"]

# Status line marks for language: en, in the order of the table.
MARK_TEXT = {
    "no-class": "No ready Method found: this is a way to understand the task, "
                "not a proven Method for a class",
    "no_recommendation": "No option is recommended, the decision is yours",
    "unverified": "Unverified",
    "partly": "Description partly confirmed",
    "no": "Description not confirmed",
    "heuristic": "Heuristic",
    "no-checks-found": "No effectiveness checks found",
}
MARK_SEP = " · "

NOCLASS_INTRO = ("No ready Method was found for this task as a whole. These "
                 "steps are the-method's fixed procedure for that case, not a "
                 "Method for a class.")
NOCLASS_STEPS = {
    1: "Settle the goal and the constraints that hold for the whole task, "
       "and have the person confirm them.",
    2: "Split the task into parts and record which parts have a recognisable "
       "Problem Class.",
    3: "For each part without one, run a small trial that can be undone, with "
       "the expected result written down first, and compare.",
    4: "Test again whether one Problem Class fits the whole task. If one "
       "does, run the-method for it. If none does, repeat from M2 or stop "
       "and say so.",
}
RUN_SENTENCE = "Run the-method on this step when you reach it."
NO_OTHER = "No other established Method found."
OUTCOME_TEXT = "not checkable at decision time"
BASIS_NONE_TEXT = "none - the steps are the-method's own procedure"
NOT_SEARCHED_TEXT = ("not searched - common practice, "
                     "not proven effective")
UNCONFIRMED_REASONS = ("search stopped at the limit", "searched, not found",
                       "research declined", "web research unavailable",
                       "source excluded")

RECORD_LABELS = ("Result", "Changed", "Skipped", "Paused", "Method")
RESULT_ENDINGS = ("checked by Claude", "confirmed by you", "done by Claude")
SOURCE_LEVELS = ("primary", "reliable secondary", "weak")

OPTIONAL_LABELS = {
    "Task": ["Given"],
    "Problem Class": ["Other classes in this task"],
    "Method": ["Tool"],
    "Grounding": ["Sources", "Accessed", "Excluded", "Heuristic"],
}
EMPTY_WORDS = ("none", "n/a", "na", "not applicable", "nothing")

DECISION_TASK = ["Decision", "Decider",
                 "Objectives (proposed by the-method; keep or strike)",
                 "Success condition"]
STANDARD_TASK = ["Unknown", "Success condition"]


# ---------------------------------------------------------------- parsing

def count_words(text):
    """Whitespace tokens with at least one letter or digit, markup removed."""
    text = text.replace("**", "").replace("`", "")
    return sum(1 for t in text.split() if any(c.isalnum() for c in t))


def parse_items(lines):
    """Group (lineno, text) lines into top-level list items and plain lines.

    Item: {'no', 'text', 'children': [{'no', 'text'}], 'plain': bool}.
    Wrapped continuation lines are joined to the item or child they follow.
    """
    items = []
    cur = None
    last = None
    for no, raw in lines:
        if not raw.strip():
            continue
        if raw.startswith("- "):
            cur = {"no": no, "text": raw[2:].rstrip(), "children": [],
                   "plain": False}
            items.append(cur)
            last = cur
            continue
        m = re.match(r"^\s+- (.*)$", raw)
        if m and cur is not None:
            ch = {"no": no, "text": m.group(1).rstrip()}
            cur["children"].append(ch)
            last = ch
            continue
        if raw.startswith((" ", "\t")) and last is not None:
            last["text"] += " " + raw.strip()
            continue
        items.append({"no": no, "text": raw.strip(), "children": [],
                      "plain": True})
        cur = None
        last = None
    return items


def split_label(text):
    """'**Label:** value' -> (label, value); None when not a bold label."""
    m = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", text)
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip()


def labeled(items):
    """Map label -> item for bold-labelled top-level list items."""
    out = {}
    for it in items:
        if it["plain"]:
            continue
        sl = split_label(it["text"])
        if sl and sl[0] not in out:
            out[sl[0]] = dict(it, label=sl[0], value=sl[1])
    return out


def is_empty_field(it):
    return not it["value"] and not it["children"]


def strip_id(text):
    return re.sub(r"^\*\*[A-Z]\d+(?: \([^)]*\))?\.\*\*\s*", "", text)


def valid_date(s):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if not m:
        return False
    try:
        datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return False
    return True


def parse_document(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("﻿"):
        text = text[1:]
    lines = text.split("\n")
    doc = {"fm": None, "fm_end": 0, "h1": None, "headings": [],
           "sections": {}, "text": text}
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm = {}
                for raw in lines[1:i]:
                    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", raw)
                    if m:
                        fm[m.group(1)] = re.sub(r"\s+#.*$", "",
                                                m.group(2)).strip()
                doc["fm"] = fm
                start = i + 1
                break
    doc["fm_end"] = start
    current = None
    for idx in range(start, len(lines)):
        raw = lines[idx]
        no = idx + 1
        m = re.match(r"^## (.*?)\s*$", raw)
        if m:
            current = m.group(1)
            doc["headings"].append((current, no))
            doc["sections"].setdefault(current, [])
            continue
        if doc["h1"] is None and current is None and \
                re.match(r"^# \S", raw):
            doc["h1"] = (no, idx)
            doc["h1_idx"] = idx
            continue
        if current is not None:
            doc["sections"][current].append((no, raw))
    doc["lines"] = lines
    return doc


# ------------------------------------------------------------------ rules

class Checker:
    def __init__(self, path, text):
        self.path = path
        self.doc = parse_document(text)
        self.errors = []

    def err(self, rule, detail):
        self.errors.append((rule, detail))

    # -- helpers
    def sec(self, name):
        return self.doc["sections"].get(name, [])

    def items(self, name):
        return parse_items(self.sec(name))

    # -- driver
    def run(self):
        fm = self.doc["fm"]
        if fm is None:
            self.err("frontmatter-keys",
                     "the document has no frontmatter block "
                     "(--- ... --- at the top)")
            return self.errors
        self.fm = fm
        self.variant = fm.get("variant") \
            if fm.get("variant") in ENUMS["variant"] else None
        self.is_en = fm.get("language") == "en"
        self.nr = fm.get("no_recommendation") == "true"
        self.heuristic = fm.get("heuristic") == "true"
        self.decision_fields = (self.variant == "decision" or
                                (self.variant == "no-class" and self.nr))
        self.check_frontmatter()
        self.check_headings()
        self.parse_body()
        self.check_labels()
        self.check_empty_optional()
        self.check_status_line()
        self.check_fixed_sentences()
        self.check_method_plan()
        self.check_grounding()
        self.check_size()
        self.check_records()
        return self.errors

    # -- SS-55 to SS-64
    def check_frontmatter(self):
        fm = self.fm
        for k in ALWAYS_REQUIRED:
            if k not in fm:
                self.err("frontmatter-keys",
                         "required key %s is missing" % k)
        for k, allowed in ENUMS.items():
            if k in fm and fm[k] not in allowed:
                self.err("frontmatter-keys",
                         "%s has value '%s', allowed: %s"
                         % (k, fm[k], " | ".join(allowed)))

        lang = fm.get("language")
        if lang is None or lang == "":
            self.err("language-code", "language is missing")
        elif not re.match(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$", lang):
            self.err("language-code",
                     "language '%s' is not a language code (en, ru, pt-BR)"
                     % lang)

        task = fm.get("task")
        if task is not None and \
                not re.match(r"^[a-z]+(?:-[a-z]+){1,4}$", task):
            self.err("task-slug",
                     "task '%s' must be two to five lowercase Latin words "
                     "joined by hyphens, no digits" % task)

        for k in ("created", "revised"):
            if k in fm and not valid_date(fm[k]):
                self.err("date-format",
                         "%s '%s' is not a date YYYY-MM-DD" % (k, fm[k]))
        if "created" not in fm:
            pass  # reported by frontmatter-keys

        variant = self.variant
        basis = fm.get("basis")
        if variant and basis in ENUMS["basis"]:
            if (basis == "none") != (variant == "no-class"):
                self.err("basis-none",
                         "basis '%s' with variant '%s': none belongs to "
                         "no-class and only to it" % (basis, variant))
        if variant:
            has_dc = "description_confirmed" in fm
            if variant == "no-class" and has_dc:
                self.err("description-confirmed-presence",
                         "description_confirmed must be absent when "
                         "variant is no-class")
            if variant != "no-class" and not has_dc:
                self.err("description-confirmed-presence",
                         "description_confirmed is missing (required unless "
                         "variant is no-class)")
            has_eff = "effectiveness" in fm
            if variant == "no-class" and not self.nr and has_eff:
                self.err("effectiveness-presence",
                         "effectiveness must be absent for no-class unless "
                         "no_recommendation is true")
            if (variant != "no-class" or self.nr) and not has_eff:
                self.err("effectiveness-presence",
                         "effectiveness is missing")
            if variant == "decision" and fm.get("no_recommendation") != \
                    "true" and "no_recommendation" in fm:
                self.err("decision-no-recommendation",
                         "variant decision needs no_recommendation: true")
        if fm.get("effectiveness") == "not-searched" and self.nr:
            self.err("not-searched-no-recommendation",
                     "effectiveness: not-searched with "
                     "no_recommendation: true")
        if "walkthrough" in fm and fm["walkthrough"] not in \
                ("in-progress", "paused", "finished"):
            self.err("walkthrough-value",
                     "walkthrough '%s' is not in-progress, paused or "
                     "finished" % fm["walkthrough"])

    # -- SS-65
    def check_headings(self):
        names = [n for n, _ in self.doc["headings"]]
        if names != H2_ORDER:
            self.err("heading-order",
                     "H2 headings are [%s], expected [%s]"
                     % (", ".join(names), ", ".join(H2_ORDER)))

    def parse_body(self):
        self.task_items = self.items("Task")
        self.pc_items = self.items("Problem Class")
        self.method_items = self.items("Method")
        self.ground_items = self.items("Grounding")
        self.assume_items = self.items("Assumptions")
        self.plan_items = self.items("Plan")
        self.verif_items = self.items("Verification")
        self.fields = {
            "Task": labeled(self.task_items),
            "Problem Class": labeled(self.pc_items),
            "Method": labeled(self.method_items),
            "Grounding": labeled(self.ground_items),
            "Verification": labeled(self.verif_items),
        }
        # Method steps
        self.m_ids = []
        self.m_text = {}
        for no, raw in self.sec("Method"):
            m = re.match(r"^\s*- \*\*M(\d+)\.\*\*\s*(.*)$", raw)
            if m:
                self.m_ids.append(int(m.group(1)))
                self.m_text[int(m.group(1))] = m.group(2).strip()
        # Plan steps
        self.steps = []
        self.step_problems = []
        for it in self.plan_items:
            if it["plain"]:
                continue
            m = re.match(r"^\[( |x|X)\] \*\*(S\d+) \(([^)]*)\)\.\*\*\s*(.*)$",
                         it["text"])
            if not m:
                self.step_problems.append(it)
                continue
            children = it["children"]
            removed = False
            skipped = False
            for ch in children:
                lab = re.match(r"^([^:]*):\s*(.*)$", ch["text"])
                if lab and lab.group(1).strip() == "Skipped":
                    skipped = True
                    if re.match(r"^\S+\s*-\s*removed:", lab.group(2)):
                        removed = True
            self.steps.append({
                "id": m.group(2), "no": it["no"],
                "ticked": m.group(1) in "xX",
                "cites": m.group(3).strip(), "text": m.group(4),
                "children": children, "removed": removed,
                "skipped": skipped})
        # Assumptions
        self.a_ids = []
        for it in self.assume_items:
            m = re.match(r"^\*\*(A\d+)\.\*\*", it["text"]) \
                if not it["plain"] else None
            if m:
                self.a_ids.append(m.group(1))
        # Sources
        self.sources = []
        src = self.fields["Grounding"].get("Sources")
        if src:
            self.sources = src["children"]
        self.r_ids = set()
        for s in self.sources:
            m = re.match(r"^\*\*(R\d+)\.\*\*", s["text"])
            if m:
                self.r_ids.add(m.group(1))
        # Choice
        self.choice_items = []
        seen = False
        for it in self.method_items:
            if it["plain"] and it["text"].startswith("###"):
                seen = re.match(r"^###\s+Choice\s*$", it["text"]) is not None
                if seen:
                    self.has_choice = True
                continue
            if seen:
                self.choice_items.append(it)
        self.has_choice = any(
            it["plain"] and re.match(r"^###\s+Choice\s*$", it["text"])
            for it in self.method_items)

    # -- SS-66
    def check_labels(self):
        variant = self.variant
        if not variant:
            return
        if self.decision_fields:
            task = DECISION_TASK
            verif = ["Outcome", "Process check", "Review on", "If it fails"]
        else:
            task = STANDARD_TASK
            verif = ["Success check", "If it fails"]
        if variant == "no-class":
            pc = ["Class", "Candidates considered",
                  "Parts with recognisable classes"]
            method = ["Steps", "Verify the result"]
            ground = ["Basis", "Rejections rest on", "Searched for",
                      "Unconfirmed"]
        else:
            pc = ["Class", "Recognise it by", "Not this class when",
                  "Boundary", "Candidates considered"]
            method = ["Name", "Applies when", "Steps", "Verify the result",
                      "Depends on"]
            ground = ["Basis", "Rests on", "Description confirmed",
                      "Effectiveness confirmed", "Unconfirmed"]
        if self.heuristic:
            ground = ground + ["Heuristic"]
        req = [("Task", task), ("Problem Class", pc), ("Method", method),
               ("Grounding", ground), ("Verification", verif)]
        for sname, labels in req:
            fields = self.fields[sname]
            for lab in labels:
                if lab not in fields:
                    self.err("required-labels",
                             "section %s lacks the field label '%s:'"
                             % (sname, lab))
                elif is_empty_field(fields[lab]):
                    self.err("required-labels",
                             "section %s: field '%s:' is empty"
                             % (sname, lab))
        if variant == "no-class" and "Unconfirmed" in self.fields["Grounding"] \
                and not self.unconfirmed_entries():
            self.err("required-labels",
                     "no-class Unconfirmed must list at least one entry, "
                     "not Nothing")
        if variant != "no-class" and not self.has_choice:
            self.err("required-labels",
                     "section Method lacks the '### Choice' heading")
        g = self.fields["Grounding"]
        if "Sources" in g and not is_empty_field(g["Sources"]) \
                and "Accessed" not in g:
            self.err("required-labels",
                     "section Grounding has Sources but no 'Accessed:' "
                     "field")

    # -- SS-67
    def check_empty_optional(self):
        for sname, labels in OPTIONAL_LABELS.items():
            fields = self.fields[sname]
            for lab in labels:
                it = fields.get(lab)
                if it is None:
                    continue
                v = it["value"].strip().rstrip(".").lower()
                if is_empty_field(it):
                    self.err("empty-optional-field",
                             "optional field '%s:' in %s has no value; "
                             "leave it out" % (lab, sname))
                elif v in EMPTY_WORDS and not it["children"]:
                    self.err("empty-optional-field",
                             "optional field '%s:' in %s says '%s'; leave "
                             "it out" % (lab, sname, it["value"]))
        for st in getattr(self, "steps", []):
            for ch in st["children"]:
                m = re.match(r"^Needs its own Method:\s*(.*)$", ch["text"])
                if m and not m.group(1).strip():
                    self.err("empty-optional-field",
                             "step %s: 'Needs its own Method:' has no "
                             "value" % st["id"])

    # -- SS-68, SS-70 (marks)
    def expected_marks(self):
        fm = self.fm
        marks = []
        if fm.get("variant") == "no-class":
            marks.append("no-class")
        if fm.get("no_recommendation") == "true":
            marks.append("no_recommendation")
        if fm.get("basis") == "unverified":
            marks.append("unverified")
        if fm.get("description_confirmed") == "partly":
            marks.append("partly")
        if fm.get("description_confirmed") == "no":
            marks.append("no")
        if fm.get("heuristic") == "true":
            marks.append("heuristic")
        if fm.get("effectiveness") == "no-checks-found":
            marks.append("no-checks-found")
        return marks

    def status_line(self):
        """The blockquote line directly under the H1, or None."""
        lines = self.doc["lines"]
        i = self.doc.get("h1_idx")
        if i is None:
            return None
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and lines[j].startswith(">"):
            return lines[j].rstrip()
        return None

    def check_status_line(self):
        marks = self.expected_marks()
        actual = self.status_line()
        if self.doc.get("h1_idx") is None:
            self.err("status-line" if self.is_en else "status-line-marks",
                     "the document has no H1 line")
            return
        if self.is_en:
            expected = ("> " + MARK_SEP.join(MARK_TEXT[m] for m in marks)) \
                if marks else None
            if actual != expected:
                self.err("status-line",
                         "status line is %s, expected %s"
                         % (repr(actual), repr(expected)))
        else:
            if not marks:
                if actual is not None:
                    self.err("status-line-marks",
                             "the frontmatter has no marks, so the status "
                             "line must be left out")
            elif actual is None:
                self.err("status-line-marks",
                         "missing status line with %d marks" % len(marks))
            else:
                body = actual[1:].strip()
                parts = [p for p in body.split(MARK_SEP.strip())
                         if p.strip()] if body else []
                if len(parts) != len(marks):
                    self.err("status-line-marks",
                             "status line has %d marks, the frontmatter "
                             "gives %d (separator ' · ')"
                             % (len(parts), len(marks)))

    # -- SS-69, SS-70 (sentences)
    def fs_error(self, detail):
        self.err("fixed-sentences" if self.is_en else "fixed-sentence-places",
                 detail)

    def check_fixed_sentences(self):
        en = self.is_en
        variant = self.variant

        # no-class Method text and steps
        if variant == "no-class":
            intro = " ".join(it["text"] for it in self.method_items
                             if it["plain"] and
                             not it["text"].startswith("#"))
            if en:
                if intro != NOCLASS_INTRO:
                    self.fs_error("no-class Method text is not the fixed "
                                  "text")
            elif not intro.strip():
                self.fs_error("no-class Method text is missing")
            for n in sorted(NOCLASS_STEPS):
                t = self.m_text.get(n)
                if t is None:
                    self.fs_error("no-class Method has no step M%d" % n)
                elif en and t != NOCLASS_STEPS[n]:
                    self.fs_error("no-class step M%d is not the fixed text"
                                  % n)
                elif not en and not t:
                    self.fs_error("no-class step M%d is empty" % n)
            extra = [n for n in self.m_ids if n not in NOCLASS_STEPS]
            if extra:
                self.fs_error("no-class Method has steps beyond M1-M4: "
                              + ", ".join("M%d" % n for n in extra))

        # "No other established Method found."
        if variant in ("standard", "decision"):
            cands = [it for it in self.choice_items if not it["plain"] and
                     re.match(r"^\*\*[^*]+\*\* - (chosen:|alternative\b|"
                              r"removed:)", it["text"])]
            if len(cands) == 1:
                others = []
                for it in self.choice_items:
                    if it in cands:
                        continue
                    t = it["text"]
                    if not it["plain"] and split_label(t) and \
                            split_label(t)[0] == "Depends on":
                        continue
                    others.append(t)
                if en:
                    if NO_OTHER not in others:
                        self.fs_error("Choice holds one candidate, so it "
                                      "needs the sentence '%s'" % NO_OTHER)
                elif not others:
                    self.fs_error("Choice holds one candidate and no "
                                  "sentence about other Methods")

        # Needs its own Method
        for st in getattr(self, "steps", []):
            for ch in st["children"]:
                m = re.match(r"^Needs its own Method:\s*(.*)$", ch["text"])
                if not m or not m.group(1).strip():
                    continue
                v = m.group(1).strip()
                if en:
                    if not re.match(r"^.+\. " + re.escape(RUN_SENTENCE) +
                                    r"$", v):
                        self.fs_error("step %s: 'Needs its own Method:' "
                                      "must read '<class>. %s'"
                                      % (st["id"], RUN_SENTENCE))
                elif not re.match(r"^\S.*[.!?。]\s+\S", v):
                    self.fs_error("step %s: 'Needs its own Method:' has no "
                                  "fixed sentence after the class"
                                  % st["id"])

        # Outcome
        out = self.fields["Verification"].get("Outcome")
        if out and not is_empty_field(out):
            v = out["value"].strip()
            if en:
                if v.rstrip(".") != OUTCOME_TEXT:
                    self.fs_error("Outcome must read '%s'" % OUTCOME_TEXT)
        elif out is not None and self.decision_fields:
            pass

        g = self.fields["Grounding"]
        # Basis: none
        b = g.get("Basis")
        if variant == "no-class" and b and b["value"]:
            v = b["value"].strip()
            if en:
                if v.rstrip(".") != BASIS_NONE_TEXT:
                    self.fs_error("Basis must read '%s'" % BASIS_NONE_TEXT)
            elif not re.match(r"^none\s+-\s+\S", v):
                self.fs_error("Basis 'none -' has no explanation after it")

        # Description confirmed
        dc = g.get("Description confirmed")
        if dc and dc["value"]:
            if not re.match(r"^(yes|partly|no)\s+-\s+\S", dc["value"]):
                self.fs_error("Description confirmed must read "
                              "'yes | partly | no - <how>'")
        # Effectiveness confirmed
        ef = g.get("Effectiveness confirmed")
        if self.fm.get("effectiveness") == "not-searched" and ef and \
                ef["value"]:
            v = ef["value"].strip()
            if en:
                if v.rstrip(".") != NOT_SEARCHED_TEXT:
                    self.fs_error("Effectiveness confirmed must read '%s' "
                                  "when effectiveness is not-searched"
                                  % NOT_SEARCHED_TEXT)
            elif not re.match(r"^not searched\s+-\s+\S", v):
                self.fs_error("Effectiveness confirmed 'not searched -' has "
                              "no sentence after it")

        # Unconfirmed reasons
        for entry in self.unconfirmed_entries():
            e = entry.strip().rstrip(".").strip()
            if en:
                if not any(e.endswith(r) for r in UNCONFIRMED_REASONS):
                    self.fs_error("Unconfirmed entry does not end with one "
                                  "of the five reasons: '%s'" % entry)
            elif not re.match(r"^\S.*\s-\s+\S", e):
                self.fs_error("Unconfirmed entry has no reason after ' - ': "
                              "'%s'" % entry)

        # same publisher / used at the person's choice (English only)
        if en:
            for s in self.sources:
                if re.search(r"same publisher", s["text"], re.I) and \
                        not re.search(r"same publisher as R\d+", s["text"]):
                    self.fs_error("source line must say 'same publisher as "
                                  "R<n>': '%s'" % s["text"][:60])
            for e in self.excluded_entries():
                if re.search(r"used at the person", e, re.I) and \
                        "used at the person's choice" not in e:
                    self.fs_error("Excluded entry must say 'used at the "
                                  "person's choice'")

    def unconfirmed_entries(self):
        u = self.fields["Grounding"].get("Unconfirmed")
        if not u:
            return []
        entries = []
        inline = u["value"].strip()
        if inline and inline.rstrip(".").lower() != "nothing":
            entries += [p.strip() for p in inline.split(";") if p.strip()]
        entries += [c["text"] for c in u["children"]]
        return entries

    def excluded_entries(self):
        x = self.fields["Grounding"].get("Excluded")
        if not x:
            return []
        entries = []
        if x["value"].strip():
            entries.append(x["value"].strip())
        entries += [c["text"] for c in x["children"]]
        return entries

    # -- SS-71 to SS-74
    def check_method_plan(self):
        for it in self.step_problems:
            self.err("step-cites",
                     "line %d: Plan item is not '- [ ] **S<n> (M<n>).** ...'"
                     % it["no"])
        live = [s for s in self.steps if not s["removed"]]
        cited = set()
        for st in self.steps:
            if st["removed"]:
                continue
            raw = st["cites"]
            if raw == "-":
                if "Why:" not in st["text"]:
                    self.err("step-cites",
                             "step %s cites (-) but has no 'Why:'"
                             % st["id"])
                continue
            parts = [p.strip() for p in raw.split(",")]
            for p in parts:
                m = re.match(r"^M(\d+)$", p)
                if not m:
                    self.err("step-cites",
                             "step %s: '%s' is not an M<n> id or (-)"
                             % (st["id"], p))
                    continue
                n = int(m.group(1))
                cited.add(n)
                if n not in self.m_ids:
                    self.err("step-cites",
                             "step %s cites M%d, which does not exist"
                             % (st["id"], n))
        for n in self.m_ids:
            if n not in cited:
                self.err("method-step-uncited",
                         "M%d is cited by no Plan step" % n)
        for st in self.steps:
            if "Done when:" not in st["text"]:
                self.err("done-when",
                         "step %s has no 'Done when:'" % st["id"])
        seen = set()
        for st in self.steps:
            if st["id"] in seen:
                self.err("duplicate-id", "step id %s appears twice"
                         % st["id"])
            seen.add(st["id"])
        seen = set()
        for a in self.a_ids:
            if a in seen:
                self.err("duplicate-id", "assumption id %s appears twice" % a)
            seen.add(a)
        del live

    # -- SS-75 to SS-78
    def check_grounding(self):
        # R<n> cited in Problem Class, Method, Grounding
        cite_rx = re.compile(r"(?<![\w-])R(\d+)(?![\w])")
        for sname in ("Problem Class", "Method", "Grounding"):
            for no, raw in self.sec(sname):
                t = re.sub(r"\*\*R\d+\.\*\*", "", raw)
                for m in cite_rx.finditer(t):
                    rid = "R" + m.group(1)
                    if rid not in self.r_ids:
                        self.err("unknown-source-ref",
                                 "line %d: %s is cited but no source %s "
                                 "exists" % (no, rid, rid))
        # A<n> cited in Method (Choice), Grounding and Verification. Plan
        # steps and record lines are not scanned: a Revision names a wrong
        # Assumption in a Changed line after it has left Assumptions.
        a_rx = re.compile(r"(?<![\w-])A(\d+)(?![\w])")
        scan = []
        for sname in ("Method", "Grounding", "Verification"):
            scan += [(no, raw) for no, raw in self.sec(sname)]
        a_defined = set(self.a_ids)
        for no, raw in scan:
            t = re.sub(r"\*\*A\d+\.\*\*", "", raw)
            for m in a_rx.finditer(t):
                aid = "A" + m.group(1)
                if aid not in a_defined:
                    self.err("unknown-assumption-ref",
                             "line %d: %s is cited but no Assumption %s "
                             "exists" % (no, aid, aid))
        # source levels
        for s in self.sources:
            t = re.sub(r"\[[^\]]*\]\([^)]*\)", "", s["text"])
            if not re.search(r",\s*(%s)\s*(\(|:|$)"
                             % "|".join(SOURCE_LEVELS), t):
                self.err("source-level",
                         "source has no level (primary | reliable "
                         "secondary | weak): '%s'" % s["text"][:70])
        # links with established knowledge
        if self.fm.get("basis") == "established-knowledge":
            for i, raw in enumerate(self.doc["lines"]):
                if re.search(r"https?://", raw):
                    self.err("links-in-established",
                             "line %d has a link, but basis is "
                             "established-knowledge" % (i + 1))
                    break

    # -- SS-79
    def line_words(self, lines):
        total = 0
        for _, raw in lines:
            if not raw.strip():
                continue
            t = re.sub(r"^\s*(?:- (?:\[[ xX]\] )?)?", "", raw)
            total += count_words(t)
        return total

    def check_size(self):
        def over(what, n, limit):
            self.err("size-limit", "%s has %d words, limit %d"
                     % (what, n, limit))

        limit = 130 if self.decision_fields else 80
        n = self.line_words(self.sec("Task"))
        if n > limit:
            over("Task", n, limit)
        n = self.line_words(self.sec("Problem Class"))
        if n > 150:
            over("Problem Class", n, 150)
        n = self.line_words(self.sec("Method"))
        if n > 220:
            over("Method (with Choice)", n, 220)
        # Grounding without Sources, Excluded, Unconfirmed
        skip = False
        kept = []
        for no, raw in self.sec("Grounding"):
            if raw.startswith("- "):
                skip = re.match(
                    r"^- \*\*(Sources|Excluded|Unconfirmed):\*\*", raw) \
                    is not None
            elif raw.strip() and not raw.startswith((" ", "\t")):
                skip = False
            if not skip:
                kept.append((no, raw))
        n = self.line_words(kept)
        if n > 120:
            over("Grounding (without Sources, Excluded, Unconfirmed)", n,
                 120)
        for s in self.sources:
            n = count_words(strip_id(s["text"]))
            if n > 35:
                over("source line '%s...'" % s["text"][:30], n, 35)
        for e in self.excluded_entries():
            n = count_words(e)
            if n > 35:
                over("Excluded entry '%s...'" % e[:30], n, 35)
        for e in self.unconfirmed_entries():
            n = count_words(e)
            if n > 25:
                over("Unconfirmed entry '%s...'" % e[:30], n, 25)
        a_items = [it for it in self.assume_items
                   if not it["plain"] and re.match(r"^\*\*A\d+\.\*\*",
                                                   it["text"])]
        for it in a_items:
            n = count_words(strip_id(it["text"]))
            if n > 25:
                over("Assumption '%s...'" % it["text"][:20], n, 25)
        if len(a_items) > 7:
            self.err("size-limit", "Assumptions has %d items, at most 7"
                     % len(a_items))
        for st in self.steps:
            n = count_words(st["text"])
            if n > 45:
                over("step %s" % st["id"], n, 45)
        live = [s for s in self.steps if not s["removed"]]
        if not 3 <= len(live) <= 9:
            self.err("size-limit",
                     "Plan has %d steps (removed steps not counted), "
                     "expected 3 to 9" % len(live))
        n = 0
        for it in self.verif_items:
            if self.is_record_item(it):
                continue
            n += count_words(it["text"])
            for ch in it["children"]:
                if not self.is_record_text(ch["text"]):
                    n += count_words(ch["text"])
        if n > 70:
            over("Verification (without record lines)", n, 70)

    @staticmethod
    def is_record_text(text):
        m = re.match(r"^([^:*]*):", text)
        return bool(m) and m.group(1).strip() in RECORD_LABELS

    def is_record_item(self, it):
        return (not it["plain"]) and not it["text"].startswith("**") and \
            self.is_record_text(it["text"])

    # -- SS-80 to SS-87
    def check_records(self):
        recs = []  # (where, label, rest, text, in_plan)
        for st in self.steps:
            for ch in st["children"]:
                if ch["text"].startswith("Needs its own Method:"):
                    continue
                recs.append((st["id"], ch["text"], True, st))
        for it in self.verif_items:
            if it["plain"] or it["text"].startswith("**"):
                continue
            recs.append(("Verification", it["text"], False, None))

        paused_count = 0
        verif_result = False
        for where, text, in_plan, st in recs:
            m = re.match(r"^([^:]*):\s*(.*)$", text)
            label = m.group(1).strip() if m else None
            rest = m.group(2) if m else text
            if label not in RECORD_LABELS:
                self.err("record-label",
                         "%s: record line '%s' does not start with one of "
                         "Result:, Changed:, Skipped:, Paused:, Method:"
                         % (where, text[:40]))
                continue
            if label == "Paused":
                paused_count += 1
            if label == "Result" and not in_plan:
                verif_result = True
            if label != "Method":
                dm = re.match(r"^(\S+)", rest)
                if not dm or not valid_date(dm.group(1).rstrip(",;")):
                    self.err("record-date",
                             "%s: %s line does not start with a date "
                             "YYYY-MM-DD: '%s'" % (where, label, text[:40]))
            if count_words(text) > 25:
                self.err("record-length",
                         "%s: %s line has %d words, limit 25"
                         % (where, label, count_words(text)))
            if label == "Result" and in_plan:
                t = rest.strip().rstrip(".").strip()
                if not any(t.endswith(e) for e in RESULT_ENDINGS):
                    self.err("result-ending",
                             "%s: Result line must end with checked by "
                             "Claude, confirmed by you or done by Claude"
                             % where)
            if label == "Method":
                lm = re.search(r"\]\(([^)\s]+)\)", rest)
                if not lm:
                    self.err("method-link",
                             "%s: Method line has no link" % where)
                else:
                    target = lm.group(1).split("#")[0]
                    base = os.path.dirname(os.path.abspath(self.path))
                    if not target or not os.path.isfile(
                            os.path.join(base, target)):
                        self.err("method-link",
                                 "%s: linked file '%s' does not exist"
                                 % (where, lm.group(1)))
        walk = self.fm.get("walkthrough")
        if walk in ("in-progress", "paused", "finished") or \
                "walkthrough" not in self.fm:
            if (paused_count > 0) != (walk == "paused"):
                self.err("paused-line",
                         "walkthrough is %s but the document has %d "
                         "'Paused:' lines (needs one if and only if paused)"
                         % (walk if walk else "absent", paused_count))
        if walk == "finished" and not verif_result:
            self.err("finished-result",
                     "walkthrough is finished but Verification has no "
                     "'Result:' line")
        for st in self.steps:
            if st["skipped"] and st["ticked"]:
                self.err("skipped-step-ticked",
                         "step %s has a 'Skipped:' line but is ticked"
                         % st["id"])


def check_text(path, text):
    return Checker(path, text).run()


def main(argv):
    files = argv[1:]
    if not files:
        sys.stderr.write("usage: check_method.py FILE [FILE ...]\n")
        return 2
    violations = False
    could_not = False
    for f in files:
        if ARCHIVE_RE.search(os.path.basename(f)):
            continue
        try:
            with open(f, "r", encoding="utf-8") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError) as e:
            sys.stderr.write("cannot read %s: %s\n" % (f, e))
            could_not = True
            continue
        for rule, detail in check_text(f, text):
            sys.stdout.write("ERROR %s: %s: %s\n" % (rule, f, detail))
            violations = True
    if could_not:
        return 2
    return 1 if violations else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as exc:  # the script itself failed
        sys.stderr.write("check_method.py failed: %r\n" % (exc,))
        sys.exit(2)
