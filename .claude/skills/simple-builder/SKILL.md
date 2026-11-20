---
name: simple-builder
description: Enforces radical simplicity, flat logic, and plain-language explanations whenever building software, writing code, designing Excel formulas, or structuring workflows. Activate automatically for all development, logic, spreadsheet, and architecture requests.
---

# Simple Builder Guidelines

Whenever you build, write, design, or explain any logic, code, spreadsheet, or system, follow these strict rules:

## 1. Core Principles
- **Choose the simplest working solution:** Avoid over-engineering, premature abstraction, and unnecessary dependencies.
- **Keep logic flat:** Eliminate deeply nested `if/else` blocks, complex ternary chains, and convoluted formulas. Use early returns, guard clauses, or small helper steps instead.
- **One job per piece:** Each function, script, Excel column, or module must do exactly one clear thing.
- **Use obvious names:** Name variables, functions, and columns in plain English (e.g., `total_after_discount` instead of `calcVal2`).

## 2. Domain-Specific Rules
- **Code & Architecture:** Favor standard libraries, linear top-to-bottom execution, and minimal files. Only introduce classes, frameworks, or design patterns when a simple function cannot handle the requirement.
- **Excel & Data Logic:** Break complex formulas into labeled helper columns or use `LET` with readable variable names. Never write giant nested `IF` formulas.
- **Explanations:** Explain how things work using everyday words and short sentences. Start with the big picture in 1–2 sentences before showing details.

## 3. Output Format
1. **Plain-English Summary:** 1–2 sentences explaining what the build does and why this approach is the simplest.
2. **The Build:** Clean, minimal, copy-pasteable code, formula, or structure with brief comments only where logic isn't immediately obvious.
3. **How It Flows:** A short bulleted walkthrough of Step 1 -> Step 2 -> Step 3.
