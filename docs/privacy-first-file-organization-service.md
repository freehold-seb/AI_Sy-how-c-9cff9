# Privacy-First File Organization Service

## Service concept

Kepler should first be evaluated as a supervised service for organizing disordered personal files, not as an unattended consumer product. The operator and customer agree on scope, inspection depth, prohibited locations, proposed actions, and retention before processing begins. The default delivery model is local processing, dry-run recommendations, customer review, and explicit approval for any mutation.

The service may eventually support intimate images, medical records, financial documents, and other sensitive material. That possibility raises the required standard: sensitive content must be minimized, isolated, access-controlled, auditable, and deleted according to an agreed policy.

## Non-negotiable boundaries

- Local processing is preferred; sending file names, metadata, or content to a remote model requires separate, informed consent.
- Collect the least information needed for the selected inspection level.
- Treat filename, metadata, extracted text, thumbnails, embeddings, logs, and backups as potentially sensitive data.
- Default to dry-run. No rename, move, copy, or deletion occurs without scoped confirmation.
- Uncertain classifications go to customer review, not an irreversible action.
- Customer content is not used for model training or retained beyond the agreed delivery and deletion window.
- Every operator and process receives only the access required for the current engagement.

## Major risks

1. **Unauthorized disclosure:** operators, remote APIs, logs, temporary files, or backups expose sensitive content.
2. **Excessive inspection:** content is opened when filenames or metadata would have been sufficient.
3. **Misclassification:** files are placed in harmful, embarrassing, or misleading categories.
4. **Destructive action:** collisions, incorrect moves, or deletions cause data loss.
5. **Scope escape:** links, mounted drives, cloud folders, archives, or hidden directories are scanned without consent.
6. **Residual data:** thumbnails, caches, embeddings, reports, or backups survive the promised deletion date.
7. **Weak access control:** customer files or reports are available to unauthorized people or processes.
8. **Ambiguous consent:** a customer cannot tell what the system will inspect or change.
9. **Legal and contractual exposure:** handling intimate, medical, financial, or third-party data creates jurisdiction-specific obligations.
10. **Unverifiable claims:** confidentiality or accuracy is promised without technical evidence and an incident process.

## Smallest fixture-only proof of concept

Use only synthetic files under `tests/fixtures/`. Do not copy or derive fixtures from real personal files.

1. Create synthetic document, image, audio, archive, duplicate, unknown, and deliberately sensitive-labelled fixtures.
2. Define four inspection levels: filename only, filename plus metadata, extracted text, and image/content analysis. Only the first two are enabled initially.
3. Record allowed roots, forbidden roots, allowed actions, retention, and review requirements in a synthetic intake record.
4. Produce a deterministic dry-run manifest containing source, proposed destination, reason, confidence, inspection level, and review requirement.
5. Route conflicts, unknowns, sensitive labels, and low-confidence results to review without moving them.
6. Require explicit confirmation for fixture execution and validate the result against the expected schema.
7. Generate a redacted audit report and prove that temporary analysis artifacts are removed.

The proof succeeds when repeated runs produce the expected manifest, no forbidden path is read, no content analysis occurs above the selected level, uncertain files remain untouched, fixture execution is reversible, and the audit contains no fixture contents.

## Deferred product work

The booking website, customer accounts, payment handling, uploads, remote AI processing, and the full intake questionnaire remain deferred. They should begin only after the fixture trial, threat model, data lifecycle, and legal review establish a service that can make defensible privacy promises.
