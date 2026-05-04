# Code Reviewer

Review the code changes in the current working directory or the files provided as arguments.

## Instructions

You are performing a thorough code review. Follow these steps:

### 1. Identify What to Review
- If arguments are provided (`$ARGUMENTS`), review those specific files
- Otherwise, run `git diff HEAD` to see recent changes, or review files the user has mentioned

### 2. Review Criteria

Evaluate each file or change against the following:

**Correctness**
- Does the logic do what it's supposed to?
- Are there off-by-one errors, null/undefined issues, or incorrect conditionals?
- Are all edge cases handled?

**Security**
- No XSS vulnerabilities (unsanitized innerHTML, eval, etc.)
- No sensitive data exposed in client-side code
- No unsafe use of external input

**Performance**
- No unnecessary DOM manipulation or reflows in loops
- No blocking operations on the main thread
- Assets and data fetching are reasonably efficient

**Maintainability**
- Code follows existing patterns in the project
- No unnecessary complexity or over-engineering
- Variable and function names are clear

**Project-Specific (Wordineer)**
- Static HTML/CSS/JS only — no framework dependencies introduced
- Changes work with `tool-engine.js` and existing build system (`build.py`)
- SEO-relevant elements (title, meta description, headings) are correct
- No regressions to `global.css` shared styles

### 3. Output Format

Provide your review in this structure:

**Summary**
One paragraph describing what was reviewed and the overall quality.

**Issues** (if any)
List each issue with:
- Severity: `critical` | `warning` | `suggestion`
- File and line reference
- What the problem is
- How to fix it

**Looks Good**
Call out anything done particularly well.

**Verdict**
`APPROVE` / `REQUEST CHANGES` / `NEEDS DISCUSSION`
