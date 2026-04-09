# Rigorous Session Template

**Use this template for Sessions 2-6**  
**Pattern**: Incremental micro-steps, hands-on experimentation

---

## Session X: [Topic Name] ([Time] hours)

**Spec**: `specs/00X-[topic].md`  
**Approach**: Build incrementally, break intentionally, learn deeply

---

## 🎯 Core Principle

```
Don't ask "Do Session X" - that generates everything at once.
Instead: Work through micro-steps, typing and testing each one.
```

---

## 📋 Micro-Step Breakdown

### Before You Start

**Setup**:
```bash
mkdir sessionX_work
cd sessionX_work
touch progress.md
```

**Review**:
- Read Session X in plan.md
- Review spec: `specs/00X-[topic].md`
- Note: Prerequisites from previous sessions

**Pre-Session Knowledge Check** (answer before writing any code):

1. What do you already know about [session topic]?
   Your answer:

2. What concept from the previous session directly applies here?
   Your answer:

3. What's your biggest uncertainty going in?
   Your answer:

Return to these after completing Step XG to measure your growth.

---

### Step XA: [Simplest Foundation] (10-15 min)

**Pre-Step Knowledge Check** (answer before generating code):
- What do you expect this code to do?
- What's one thing that could go wrong?

**Prompt**:
```
Generate the simplest [key concept] example that:
- [Requirement 1]
- [Requirement 2]
- Includes timing/logging/output to observe behavior

Keep under 20 lines. Add comments explaining [core concept].
```

**Your Tasks**:
1. Read generated code carefully
2. **Type it yourself** - don't copy-paste
3. Predict output before running
4. Run and compare to prediction
5. Note surprises or confusions

**Break It Challenge**:
```
Ask: "Show me what happens if I:"
1. [Remove/modify key element]
2. [Try wrong type/value]
3. [Skip required step]

Try each - read error - understand why.
```

**Concept Check** (answer without looking at code, then verify):
- [Question 1]: What does [key element] actually do?
  Your answer:
- [Question 2]: Why does this work this way and not [alternative]?
  Your answer:
- [Question 3]: When in real code would you use this pattern?
  Your answer:

**Confidence rating**: __ / 5 — What would push it higher?

**Mark**: `[x] Step XA` in progress.md

---

### Step XB: [Add Complexity Layer 1] (15-20 min)

**Pre-Step Knowledge Check** (answer before generating code):
- How does [new concept from XB] relate to what you built in XA?
- What will change in behavior? What will stay the same?

**Prompt**:
```
Extend Step XA to include [new concept/pattern].

Show:
- [Specific requirement 1]
- [Specific requirement 2]
- Comparison to previous approach

Generate ONLY the new/modified parts - I'll integrate.
```

**Your Tasks**:
1. Integrate new code into your file
2. Run both old and new versions
3. Compare behavior/output
4. Measure timing if applicable

**Experiment Yourself**:
```
Before asking AI, try:
- [Variation 1]
- [Variation 2]
- [Edge case]

If stuck after 10 min, ask for hints.
```

**Concept Check** (answer before asking AI to verify):
- Why is [new approach] different from XA? Not just what changed — why does it matter?
  Your answer:
- When would I stay with the XA approach vs use the XB approach?
  Your answer:
- What trade-offs did you observe (timing, complexity, readability)?
  Your answer:

**Confidence rating**: __ / 5

**Mark**: `[x] Step XB`

---

### Step XC: [Add Complexity Layer 2] (20-25 min)

**Pre-Step Knowledge Check** (answer before generating code):
- What gap does [XC concept] fill that XA and XB didn't cover?
- Predict: how will this change error behavior?

**Prompt**:
```
Add [advanced concept] to the example.

Requirements:
- [Specific behavior 1]
- [Specific behavior 2]
- Error handling for [scenario]

Keep incremental - build on step XB.
```

**Your Tasks**:
1. Type new additions
2. Test each piece separately
3. Integrate step-by-step
4. Debug issues yourself first

**Break It Challenge**:
```
Test edge cases:
- [Edge case 1] - what breaks?
- [Edge case 2] - how to handle?
- [Edge case 3] - graceful degradation?
```

**Concept Check** (answer before asking AI to verify):
- How does [XC concept] interact with what you built in XA and XB?
  Your answer:
- What new failure mode did this step expose?
  Your answer:
- Where might this pattern break in a production environment?
  Your answer:

**Confidence rating**: __ / 5

**Mark**: `[x] Step XC`

---

### Step XD: [Real-World Integration] (25-30 min)

**Pre-Step Knowledge Check** (answer before generating code):
- How do the XA–XC patterns map to a real application you've seen or used?
- What concerns emerge when moving from example code to production code?

**Prompt**:
```
Show how steps XA-XC would work in a real [application context].

Example:
- Step XA pattern in [real scenario 1]
- Step XB pattern in [real scenario 2]
- Complete mini-project combining all concepts

Generate structure/skeleton - I'll fill in details.
```

**Your Tasks**:
1. Study the real-world example
2. Identify patterns from earlier steps
3. Note new considerations (security, performance, etc.)
4. Ask about anything unclear

**Deep Dive**:
```
Ask: "Find a real open-source project using [this pattern].
Explain how professionals structure this differently than my learning code."
```

**Concept Check** (answer before asking AI):
- How does this learning code differ from what you'd ship in production?
  Your answer:
- What's missing from your XA–XC examples that the real-world version has?
  Your answer:
- What would you add to make this production-ready?
  Your answer:

**Confidence rating**: __ / 5

**Mark**: `[x] Step XD`

---

### Step XE: [Build Your Own Challenge] (30-45 min)

**Pre-Step Knowledge Check** (before writing a single line):
- Can you describe the full solution approach without looking at earlier steps?
- Which step (XA–XD) will be hardest to replicate? Why?

**Challenge** (Do YOURSELF first - no AI):
```
Create [mini-project] that combines all concepts:

Requirements:
- [Requirement 1 - uses step XA concept]
- [Requirement 2 - uses step XB concept]
- [Requirement 3 - uses step XC concept]
- [Requirement 4 - error handling]
- [Requirement 5 - testing]

Build incrementally:
1. [Sub-task 1]
2. [Sub-task 2]
3. [Sub-task 3]
```

**Sub-task Knowledge Check** (after each sub-task, before the next):
- Sub-task 1 done: What assumption did you make that could be wrong?
- Sub-task 2 done: Does this behave the same as step XB? Why or why not?
- Sub-task 3 done: What error would a real user trigger that your code doesn't handle yet?

**Your Tasks**:
1. Spend 20-30 min building yourself
2. Refer to earlier steps when needed
3. Debug your own bugs first
4. After completing, ask AI for code review

**AI Review** (only after building):
```
Ask: "Review my [mini-project] code.

What could improve:
- Code structure
- Error handling  
- Performance
- Readability
- Production readiness

[Paste your code]"
```

**Post-Build Concept Check**:
- Did you need AI help? For which parts? What does that reveal about gaps?
  Your answer:
- Explain your key design decisions in 2-3 sentences.
  Your answer:
- What would you do differently if you rebuilt this from scratch right now?
  Your answer:

**Confidence rating**: __ / 5

**Mark**: `[x] Step XE - CRITICAL STEP`

---

### Step XF: [Testing & Validation] (20-25 min)

**Pre-Step Knowledge Check** (before writing tests):
- What behavior are you most uncertain about? Write a test for that first.
- What's a realistic bad input or failure that a user could trigger?

**Prompt**:
```
Show me how to test the code from step XE.

Include:
- Unit tests for [component 1]
- Integration test for [workflow]
- Mock [external dependency]
- Test error cases

Keep under 40 lines total.
```

**Your Tasks**:
1. Type tests yourself
2. Run them - do they pass?
3. Intentionally break code - do tests catch it?
4. Add your own test cases

**Test-Driven Learning**:
```
Try TDD:
1. Write test for new feature (fails)
2. Implement feature
3. Test passes
4. Refactor

Do this for 2-3 small features.
```

**Concept Check** (answer before asking AI):
- What's hard to test here? What does that tell you about the design?
  Your answer:
- Did your tests catch the intentional breakage? If not, what's missing?
  Your answer:
- When would you mock vs use real implementations?
  Your answer:

**Confidence rating**: __ / 5

**Mark**: `[x] Step XF`

---

### Step XG: [Concept Self-Test] (15-20 min)

**Test Yourself** (answer BEFORE asking AI — no looking at previous steps):

1. **[Core concept question]**
   Your answer:
   
2. **[Pattern comparison question]**
   Your answer:
   
3. **[When to use question]**
   Your answer:
   
4. **[Trade-offs question]**
   Your answer:
   
5. **[Real-world application question]**
   Your answer:

6. **[Connection to previous session question]**
   Your answer:

**After Answering**:
```
Ask AI: "I answered these questions about [topic]:
1. [Your answer]
2. [Your answer]
...

Critique my understanding. What's missing or wrong?"
```

**Code From Scratch**:
```
Without looking at previous code, write:

[Specific small project that combines key concepts]

Can you do it? Time yourself.
```

**Post-Scratch Concept Check**:
- Where did you get stuck? What specifically caused the friction?
  Your answer:
- Compared to your Pre-Session answers, what changed most?
  Your answer:
- What question do you still have that this session didn't fully answer?
  Your answer:

**Final confidence ratings**:
| Concept | Pre-session | Post-session | Gap explanation |
|---------|-------------|--------------|-----------------|
| [Concept 1] | __ / 5 | __ / 5 | |
| [Concept 2] | __ / 5 | __ / 5 | |
| [Concept 3] | __ / 5 | __ / 5 | |

**Mark**: `[x] Step XG`

---

## 🎯 Session Completion Checklist

### Code Quality
- [ ] All steps XA-XG completed
- [ ] Typed code yourself (minimal copy-paste)
- [ ] Broke and fixed code in each step
- [ ] Added your own variations
- [ ] Tests written and passing

### Knowledge Check Coverage
- [ ] Answered Pre-Session check before starting
- [ ] Answered Pre-Step check before each step (XA–XF)
- [ ] Answered Concept Check after each step (XA–XF)
- [ ] Completed XG self-test without looking at notes
- [ ] Filled in confidence rating table in XG
- [ ] Post-session answers differ meaningfully from pre-session answers

### Conceptual Understanding
- [ ] Can explain [core concept 1] without notes
- [ ] Understand [pattern 1] vs [pattern 2] trade-offs
- [ ] Know when to use [approach from this session]
- [ ] Can debug common errors
- [ ] Can write code from scratch

### Application
- [ ] Completed step XE challenge independently
- [ ] Code review made sense and improved code
- [ ] Connected to previous sessions
- [ ] Ready for next session

### Reflection
- [ ] Updated LEARNING_LOG.md honestly
- [ ] Documented struggles and victories
- [ ] Listed remaining questions
- [ ] Compared time to estimate

---

## ⏱️ Time Tracking

| Step | Estimated | Actual | Notes |
|------|-----------|--------|-------|
| XA | 10-15 min | _____ | |
| XB | 15-20 min | _____ | |
| XC | 20-25 min | _____ | |
| XD | 25-30 min | _____ | |
| XE | 30-45 min | _____ | |
| XF | 20-25 min | _____ | |
| XG | 15-20 min | _____ | |
| Buffer | Variable | _____ | |
| **Total** | **[X]h** | **_____** | |

---

## 🔄 Iteration Protocol

**When stuck**:
1. Spend 5 min debugging yourself
2. Re-read error message carefully
3. Check previous steps for patterns
4. Google the error
5. Ask AI with context (after trying)

**When confident**:
1. Add more challenging variations
2. Combine with previous sessions
3. Research advanced patterns
4. Help others learn

---

## 📝 Adaptation Notes

**For each session, customize**:
- Step topics (XA, XB, etc.) to match learning objectives
- Challenges to match difficulty level
- Time estimates based on complexity
- Prerequisites from earlier sessions

**Keep consistent**:
- Incremental building approach
- Type-it-yourself requirement
- Break-and-fix methodology
- Build-your-own challenge
- Self-test before AI verification

---

**This template ensures**:
- Deep, hands-on learning
- Conceptual understanding, not just code
- Ability to build without AI assistance
- Production-ready thinking
- Measurable progress
