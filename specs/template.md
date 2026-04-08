# Spec: [Feature/Module Name]

**Session**: [Number]  
**Estimated Time**: [Hours]  
**Status**: Draft | In Progress | Implemented | Revised  
**Last Updated**: [Date]

---

## Problem Statement

[What you're trying to learn/build and why. Keep this to 2-3 sentences.]

**Example**: Learn async fundamentals by building examples that demonstrate event loops, coroutines, and concurrent execution. This will provide the foundation for understanding FastAPI's async capabilities.

---

## Learning Objectives

[Specific concepts you'll understand after completing this session]

- [ ] [Concrete concept to master]
- [ ] [Pattern to apply]
- [ ] [Comparison to make (e.g., async vs threads)]
- [ ] [Something to explain in your own words]

**Example**:
- [ ] Understand how event loops manage concurrent tasks
- [ ] Know when to use `await` vs `asyncio.gather()` vs `asyncio.create_task()`
- [ ] Compare concurrent vs parallel vs sequential execution
- [ ] Explain why async helps with I/O but not CPU-intensive work

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

---

## Success Criteria

[Concrete, testable outcomes. Mix of code working AND conceptual understanding.]

**Code Works**:
- [ ] [Specific feature works - be precise]
- [ ] [Test passes]
- [ ] [Edge case handled]

**Understanding Achieved**:
- [ ] Can explain [concept] in own words
- [ ] Know when to use [pattern] vs [alternative]
- [ ] Understand why [decision] was made

**Example**:
- [ ] Async examples show measurable timing improvement for I/O
- [ ] Can trace execution order of concurrent tasks
- [ ] Tests pass: sequential vs concurrent execution
- [ ] Can explain event loop to another developer

---

## Open Questions

[Things you're unsure about - to research or decide during implementation. It's OK to not know!]

- [ ] [Question 1 - will research during implementation]
- [ ] [Question 2 - will ask AI for guidance]
- [ ] [Trade-off to evaluate while coding]

**Example**:
- [ ] Should we use threads instead of async for this use case?
- [ ] How do we handle API timeouts gracefully?
- [ ] What's the real-world difference between `gather()` and `as_completed()`?

---

## Testing Strategy

[What to test and how. Don't need to write tests yet, just plan the approach.]

**Test Cases**:
1. [Happy path test]
2. [Error case test]
3. [Edge case test]

**Approach**:
- Unit tests: [What to mock, what to test]
- Integration tests: [If applicable]
- Manual tests: [How to verify it works]

**Example**:
- Unit test: Mock async sleep, verify concurrent execution
- Manual test: Run with print statements, observe timing
- Error test: Remove `await`, verify it raises TypeError

---

## Implementation Notes

[Optional: Technical details, constraints, or reminders for implementation phase]

**Key Patterns to Use**:
- [Pattern 1]
- [Pattern 2]

**Libraries/Tools**:
- [Library name]: [Purpose]

**References**:
- [Link to docs]
- [Tutorial reference]

---

## Rails Developer Notes

[Optional: How this compares to Rails patterns. Helps bridge mental models.]

**Rails equivalent**: [Similar pattern in Rails]  
**Key difference**: [How this is different in Python/FastAPI]

**Example**:
- **Rails**: Uses thread pools (Puma) for concurrency
- **FastAPI**: Uses async event loop (single-threaded cooperative multitasking)
- **When to use**: Rails for simple CRUD, FastAPI for high-concurrency I/O

---

## Reflection (Fill out after implementation)

**What worked well**:
- [Thing that went smoothly]

**What was challenging**:
- [Difficult concept or bug]

**Spec accuracy**:
- [ ] Spec matched implementation closely
- [ ] Spec needed significant revision
- [ ] Open questions answered: [How]

**Would specify differently**:
- [What you'd change in the spec knowing what you know now]

**Key learnings**:
- [Most important thing you learned]

---

## Commit Message Template

```
[Session X] Implement [feature] per spec #00X

- Add [component 1]
- Implement [functionality]
- Tests: [what was tested]

Spec: specs/00X-spec-name.md
```

---

**Notes**:
- Keep specs lightweight (~1-2 pages max)
- Update spec if design changes during implementation
- It's OK to have open questions - you're learning!
- Use spec as prompt for AI code generation
- Focus on understanding, not perfect documentation
