# Service-Tool Framing — Ground Rule

**Date:** 2026-09-15
**Rule:** This is a service tool. Not a consumer product.

---

## What this is

A service-enabled workflow tool:

- produces utility immediately
- operates within a service layer
- does not require a full platform before it is useful

## What this is not

- a standalone consumer product
- a general public app
- something that needs full architecture before it can function

---

## The correct question

**Not:** "How do we build the whole product?"
**Yes:** "How do we make the service tool reliable enough to be useful today?"

---

## The rule

- Tool works → use it, it is real
- Tool broken → fix the tool
- App/UI layer broken → defer it, the service still runs on the working loop
- The service does not depend on the app layer existing

---

## The working loop IS the service interface

```text
speak → get text → refine → copy → use
```

That is the service.
Everything else is infrastructure built around it.

---

*Working flow first. App layer later.*
