# Spec: [Feature/Module Name]

**Session**: [Number]  
**Estimated Time**: [Hours]  
**Status**: Draft | In Progress | Implemented | Revised  
**Last Updated**: [Date]

---

## Problem Statement

[What you're trying to learn/build and why. 2-3 sentences max.]

---

## Learning Objectives

- [ ] [Concrete concept to master]
- [ ] [Pattern to apply]
- [ ] [Comparison to make (e.g., async vs threads)]
- [ ] [Something to explain in your own words]

### Pre-Session Knowledge Check

Answer BEFORE starting. Return to them after to measure growth.

1. What do you already know about [core topic]?
   Your answer:
2. What's your biggest uncertainty or gap?
   Your answer:
3. How would you explain [key concept] to someone right now?
   Your answer:

---

## Technical Design

[Simple architecture diagram, bullet points, or flowchart. Keep it visual and concise.]

**Components**:
- [Component 1]: [Purpose]
- [Component 2]: [Purpose]

**Flow**:
```
[Step 1] → [Step 2] → [Step 3]
```

**Key Decisions**:
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [What] | [Chosen option] | [Why this choice] |

### Design Knowledge Check

Before writing code:
1. Why was [key design choice] selected over [alternative]?   Your answer:
2. What would break if you changed [component]?   Your answer:
3. Draw the data flow input → output without looking.   Your answer:

---

## API / Code Contract

[Define the interface - endpoints, function signatures, data structures]

### Endpoints (if applicable)
**Method**: `GET /path/{param}`

**Parameters**:
- `param_name` (type): Description

**Response** (200):
```json
{
  "field": "value"
}
```

**Errors**:
- 400: Description
- 404: Description

### Functions (if applicable)
```python
async def function_name(param: Type) -> ReturnType:
    """What this function does."""
    pass
```

### Data Models (if applicable)
```python
class ModelName(BaseModel):
    field1: str
    field2: int
```

### Contract Knowledge Check

1. Without looking, what does `GET /path/{param}` return on success? On a 404?   Your answer:
2. What does `function_name` accept/return? What happens with bad input?   Your answer:
3. Why does `ModelName` need both fields? What validates them?   Your answer:

---

## Success Criteria

**Code Works**:
- [ ] [Specific feature works]
- [ ] [Test passes]
- [ ] [Edge case handled]

**Understanding Achieved**:
- [ ] Can explain [concept] in own words
- [ ] Know when to use [pattern] vs [alternative]
- [ ] Understand why [decision] was made

### Post-Session Knowledge Check

Answer AFTER the session. Compare to Pre-Session answers.

1. Explain [core concept] in your own words, as if teaching a junior dev.
   Your answer:
2. What's the biggest mistake a developer could make with [pattern]? How do you prevent it?
   Your answer:
3. When would you NOT use [approach learned]? What's the alternative?
   Your answer:
4. Rate your understanding (1–5) and explain the gap:
   - Pre-session: __ / 5
   - Post-session: __ / 5
   - What's still unclear:

---

## Open Questions

- [ ] [Question 1 — will research during implementation]
- [ ] [Question 2 — will ask AI for guidance]
- [ ] [Trade-off to evaluate while coding]

### Resolving Open Questions

After implementation, revisit each:
1. [Question 1]: What did you find?   Your answer:
2. [Question 2]: What guidance did you get?   Your answer:
3. [Trade-off]: Which option and why?   Your answer:

---

## Testing Strategy

**Test Cases**:
- [Happy path]
- [Error case]
- [Edge case]

**Approach**: Unit (mock externals) → Integration (if applicable) → Manual verification

---

## Rails Developer Notes

**Rails equivalent**: [Similar pattern]  
**Key difference**: [How this is different in Python/FastAPI]

---

## Reflection (fill out after implementation)

**What worked well**:
**What was challenging**:
**Would specify differently**:
**Key learning**:

**Spec accuracy**:
- [ ] Matched implementation closely / [ ] Needed significant revision

---

## Commit Message Template

```
[Session X] Implement [feature] per spec #00X

- Add [component]
- Implement [functionality]

Spec: specs/00X-spec-name.md
```

**Notes**: Keep specs ~1-2 pages. Update if design changes. Use spec as AI prompt.
