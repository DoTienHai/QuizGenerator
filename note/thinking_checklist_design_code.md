# Thinking Checklist: Design & Code Quality

**Purpose**: Universal framework for self-evaluation of software design and code quality  
**Created**: 2026-03-15  
**Scope**: General principles applicable to any project

---

## Table of Contents

- [Design Thinking Questions](#design-thinking-questions)
- [Code Quality Questions](#code-quality-questions)
- [Architecture Questions](#architecture-questions)
- [Testing & Validation](#testing--validation)
- [User Experience & Accessibility](#user-experience--accessibility)
- [Security & Robustness](#security--robustness)
- [Quick Decision Framework](#quick-decision-framework)

---

## Design Thinking Questions

### 1. Problem Understanding

**Do I understand the problem?**
- ✅ What is the core problem being solved?
- ✅ Who is the user?
- ✅ What is the user's pain point?
- ✅ Why is this important?
- ✅ What are the constraints?

### 2. Requirement Clarity

**Are requirements clear and complete?**
- ✅ What does "done" look like?
- ✅ Are all requirements documented?
- ✅ Are there conflicting requirements?
- ✅ What are the acceptance criteria?
- ✅ Are scope boundaries defined?

### 3. Solution Design

**Is the design thoughtful?**
- ✅ Is this the simplest solution?
- ✅ Does it solve the actual problem (not symptoms)?
- ✅ Are there simpler alternatives?
- ✅ What are the trade-offs?
- ✅ Was the design discussed/reviewed before coding?

### 4. Scalability & Flexibility

**Is the design future-proof?**
- ✅ Can it handle growth (more data, more users)?
- ✅ Is it flexible for future changes?
- ✅ Are assumptions documented?
- ✅ What would break if scale increases 10x?
- ✅ Can components be replaced later?

### 5. Separation of Concerns

**Is the design properly separated?**
- ✅ Does each component have one responsibility?
- ✅ Are concerns clearly separated?
- ✅ Is the data flow obvious?
- ✅ Can components be tested independently?
- ✅ Is coupling minimized?

### 6. Naming & Clarity

**Are concepts clearly named?**
- ✅ Do names accurately describe what things do?
- ✅ Are names consistent across the system?
- ✅ Would a new developer understand?
- ✅ Are abbreviations avoided?
- ✅ Do names avoid ambiguity?

---

## Code Quality Questions

### 1. Correctness

**Does the code work?**
- ✅ Does it do what it's supposed to do?
- ✅ Are all test cases passing?
- ✅ Are edge cases handled?
- ✅ Are there known bugs?
- ✅ Does it handle errors gracefully?

### 2. Readability

**Is the code easy to understand?**
- ✅ Would a new developer understand it?
- ✅ Are variable/function names clear?
- ✅ Is logic straightforward?
- ✅ Are there confusing sections?
- ✅ Do comments explain "why" not "what"?

### 3. Maintainability

**Is the code easy to change?**
- ✅ Can I change one thing without breaking others?
- ✅ Are dependencies clear?
- ✅ Is the code organized logically?
- ✅ Can I easily find what I need?
- ✅ Are similar things grouped together?

### 4. DRY Principle (Don't Repeat Yourself)

**Is there unnecessary duplication?**
- ✅ Do I see the same code in multiple places?
- ✅ Can common logic be extracted?
- ✅ Are patterns repeated?
- ✅ Could functions be reused?
- ✅ Is there boilerplate that could be eliminated?

### 5. KISS Principle (Keep It Simple, Stupid)

**Is this the simplest solution?**
- ✅ Is the code overly complex?
- ✅ Could it be simpler?
- ✅ Are there unnecessary abstractions?
- ✅ Is clever code actually clever or just confusing?
- ✅ Can I explain it in 2 minutes?

### 6. Code Smell Detection

**Are there warning signs?**
- ✅ Functions > 30 lines (too long)?
- ✅ Parameters > 5 (too many)?
- ✅ Nesting > 3 levels deep?
- ✅ Classes with too many responsibilities?
- ✅ Hard-coded values everywhere?
- ✅ Inconsistent formatting?
- ✅ Magic numbers without explanation?

### 7. Performance

**Is performance acceptable?**
- ✅ Does it run fast enough?
- ✅ Are there obvious inefficiencies?
- ✅ N+1 query problems?
- ✅ Unnecessary loops or iterations?
- ✅ Memory usage reasonable?
- ✅ Could algorithms be optimized?

### 8. Error Handling

**Are errors handled properly?**
- ✅ Are exceptions caught appropriately?
- ✅ Do error messages help debug?
- ✅ Are exceptions re-thrown when needed?
- ✅ Is there graceful degradation?
- ✅ Are errors logged?

---

## Architecture Questions

### 1. Layering & Structure

**Is architecture clean?**
- ✅ Are layers clearly separated?
- ✅ Do dependencies flow downward only?
- ✅ Is coupling minimized?
- ✅ Are there circular dependencies?
- ✅ Is the structure understandable?

### 2. Module Organization

**Is the codebase organized?**
- ✅ Can I find things easily?
- ✅ Are modules focused?
- ✅ Is the folder structure logical?
- ✅ Are related things grouped?
- ✅ Is the structure self-documenting?

### 3. Dependencies

**Are dependencies well-managed?**
- ✅ Are external dependencies necessary?
- ✅ Are versions pinned?
- ✅ Can dependencies be replaced?
- ✅ Are there unnecessary dependencies?
- ✅ Is dependency tree clean?

### 4. Interfaces & Contracts

**Are contracts clear?**
- ✅ Are input/output types known?
- ✅ Are assumptions documented?
- ✅ Is the contract stable?
- ✅ Can contracts be versioned?
- ✅ Are breaking changes communicated?

### 5. Configuration

**Is configuration externalized?**
- ✅ Are secrets in the code?
- ✅ Can config change without recompiling?
- ✅ Are environment-specific settings handled?
- ✅ Is configuration documented?
- ✅ Is there a single source of truth?

---

## Testing & Validation

### 1. Test Coverage

**Is the code tested?**
- ✅ Are critical paths tested?
- ✅ Are edge cases tested?
- ✅ Is there unit test coverage?
- ✅ Are there integration tests?
- ✅ Are there acceptance tests?

### 2. Test Quality

**Are tests good?**
- ✅ Do tests verify behavior (not implementation)?
- ✅ Are tests maintainable?
- ✅ Do they catch real bugs?
- ✅ Are there flaky tests?
- ✅ Is test code clean?

### 3. Edge Cases & Boundaries

**Are edge cases handled?**
- ✅ Empty input?
- ✅ Null/undefined values?
- ✅ Maximum values?
- ✅ Negative numbers?
- ✅ Concurrent access?
- ✅ Out of memory?

### 4. Data Validation

**Is input validated?**
- ✅ All user input validated?
- ✅ Types checked?
- ✅ Ranges enforced?
- ✅ Format validated?
- ✅ Constraints checked?

---

## User Experience & Accessibility

### 1. User Flow

**Is the user journey logical?**
- ✅ Can user accomplish goals easily?
- ✅ Are next steps obvious?
- ✅ Is error recovery easy?
- ✅ Are there dead ends?
- ✅ Is the path intuitive?

### 2. Feedback & Responsiveness

**Does the system respond to users?**
- ✅ Are actions acknowledged?
- ✅ Is feedback clear?
- ✅ Are errors explained?
- ✅ Is success indicated?
- ✅ Are users informed of progress?

### 3. Consistency

**Is the experience consistent?**
- ✅ Do similar actions work similarly?
- ✅ Is terminology consistent?
- ✅ Is styling consistent?
- ✅ Are patterns repeated?
- ✅ Are there surprising exceptions?

### 4. Accessibility

**Is the system accessible to all?**
- ✅ Can it be used with keyboard only?
- ✅ Works with screen readers?
- ✅ Color not the only information source?
- ✅ Text is readable (contrast, size)?
- ✅ Works on mobile devices?

### 5. Documentation

**Is usage documented?**
- ✅ Is there user help?
- ✅ Are error messages clear?
- ✅ Is onboarding supported?
- ✅ Are workflows explained?
- ✅ Is support available?

---

## Security & Robustness

### 1. Input Handling

**Is all input treated as untrusted?**
- ✅ Is user input validated?
- ✅ Are there injection attacks possible?
- ✅ Is data sanitized?
- ✅ Are file uploads safe?
- ✅ Are limits enforced?

### 2. Data Protection

**Is sensitive data protected?**
- ✅ Is data encrypted at rest?
- ✅ Is data encrypted in transit?
- ✅ Are secrets protected?
- ✅ Are logs sanitized?
- ✅ Is access controlled?

### 3. Error Information Leakage

**Are errors revealing secrets?**
- ✅ Are stack traces exposed?
- ✅ Do errors reveal system details?
- ✅ Are file paths leaked?
- ✅ Are usernames enumerated?
- ✅ Are error messages safe?

### 4. Robustness

**Does system fail gracefully?**
- ✅ What happens on network failure?
- ✅ What happens on database failure?
- ✅ What happens on resource exhaustion?
- ✅ Is there recovery?
- ✅ Are services degraded safely?

### 5. Monitoring & Logging

**Is system visibility adequate?**
- ✅ Are critical events logged?
- ✅ Are errors alerting?
- ✅ Is performance monitored?
- ✅ Are logs analyzable?
- ✅ Is there observability?

---

## Quick Decision Framework

### When in Doubt, Ask:

| Question | Purpose |
|----------|---------|
| **Why?** | Do I understand the reason? |
| **Who?** | Who uses this? What's their need? |
| **What?** | What exactly needs to happen? |
| **How?** | Is there a simpler way? |
| **Where?** | Where does this belong architecturally? |
| **When?** | When is this needed? Is it premature? |
| **What if?** | What breaks if I change this? |
| **Is this YAGNI?** | Do I need this now or "might" need it? |
| **Is this over-engineered?** | Could it be simpler? |
| **What would I change?** | If I rewrote this, what would be different? |

---

## Decision Checklist

**Before finalizing design:**
- ✅ Problem Understanding (5 Qs)
- ✅ Requirement Clarity (5 Qs)
- ✅ Solution Design (5 Qs)
- ✅ Separation of Concerns (5 Qs)

**Before code review:**
- ✅ Above + Code Quality (8 Qs)
- ✅ Architecture (5 Qs)
- ✅ Security (5 Qs)

**Before deployment:**
- ✅ All above + Testing (4 Qs)
- ✅ UX/Accessibility (5 Qs)
- ✅ Robustness (5 Qs)

---

## Key Principles Summary

1. **SOLID Principles**
   - Single Responsibility: 1 reason to change
   - Open/Closed: Open for extension, closed for modification
   - Liskov Substitution: Subtypes are substitutable
   - Interface Segregation: Clients depend on specific interfaces
   - Dependency Inversion: Depend on abstractions, not concretions

2. **DRY**: Don't Repeat Yourself
3. **KISS**: Keep It Simple, Stupid
4. **YAGNI**: You Aren't Gonna Need It
5. **Clean Code**: Code is read more than written

---

## Red Flags

**Watch out for:**
- ❌ "We'll refactor later" (often doesn't happen)
- ❌ "Just this one hack" (spreads like wildfire)
- ❌ Huge functions/classes
- ❌ No tests
- ❌ Hard-coded values everywhere
- ❌ No documentation
- ❌ Circular dependencies
- ❌ Magic numbers
- ❌ Inconsistent patterns
- ❌ "It works, don't touch it"

---

## Green Flags

**Strive for:**
- ✅ Clear naming
- ✅ Small focused functions
- ✅ Good test coverage
- ✅ Documented assumptions
- ✅ Consistent patterns
- ✅ Easy to navigate code
- ✅ Separated concerns
- ✅ Error handling
- ✅ Clear data flow
- ✅ Flexible to change
