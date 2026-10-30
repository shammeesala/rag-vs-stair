# Integration Platform Handbook

## 1 Onboarding

### 1.1 Access and accounts
New engineers request access to the integration subscriptions through the platform access portal. Access is granted by group membership, so ask your manager to add you to the integration-engineers group. Production access is read-only for the first ninety days. Service principals are never shared with people; each pipeline gets its own identity.

### 1.2 Local development setup
Clone the integrations monorepo and install Python 3.11 and Java 17. Copy the sample environment file and point it at the development storage account. Run the bootstrap script to create a virtual environment, install pre-commit hooks and download test fixtures. Unit tests should pass before you open your first pull request.

### 1.3 Code review rules
Every pull request needs one approval from a code owner and a green pipeline. Keep changes under four hundred lines when possible and describe how you tested them. Reviewers check error handling, logging and whether personal data could leak into logs. Do not merge your own change on a Friday afternoon.

## 2 Data pipelines

### 2.1 Pipeline architecture
Pipelines read from source systems into a raw layer and publish cleaned tables to a published layer. Each integration is described by a YAML config that lists the source, the target, the load type and the field mappings. The shared framework handles encryption, audit tables and retention so individual pipelines stay small.

### 2.2 Load types
#### 2.2.1 Full load
A full load replaces the whole target table on every run. Use it for small reference data such as locations or job codes where the source cannot tell you what changed.

#### 2.2.2 Incremental merge
An incremental merge reads only rows changed since the last watermark and upserts them by business key. Keep a small overlap window, usually one hour, so late-arriving rows are not missed. The watermark is stored in the audit table after a successful run.

#### 2.2.3 Delete and insert
Delete and insert removes all rows for the affected partition, for example one pay period, and writes the new rows. It is useful when the source sends complete snapshots per partition but has no reliable change timestamps.

### 2.3 Field mappings
Business mappings such as country codes, department names and status values live in an external mapping table, not in code. The framework caches lookups for the duration of a run. When the business adds a new value, update the mapping table instead of shipping a release.

### 2.4 File encryption
Outbound files to vendors are encrypted with PGP using the vendor public key stored in the key vault. Inbound files are decrypted with our private key, which never leaves the vault. Rotate vendor keys when the vendor notifies us and test with a sample file before the next scheduled run.

## 3 Event processing

### 3.1 Event types
Source systems emit many change events, but the platform normalizes them into two canonical events: worker changed and location changed. Downstream consumers only subscribe to canonical events, which keeps them independent of source quirks.

### 3.2 Ordering and partitions
Events for the same worker must be processed in order, so the partition key is the worker identifier. Within a partition the consumer processes events in small batches and commits offsets only after the batch succeeds. Never use a random partition key for change events.

### 3.3 Retries and dead letters
Transient failures such as timeouts or throttling are retried with exponential backoff, up to five attempts. Validation failures are not retried; they go straight to the dead-letter queue with the error reason. Someone on call reviews the dead-letter queue every morning and replays fixed events.

### 3.4 Idempotency
Consumers must be safe to run twice on the same event. Each event carries an event identifier, and the consumer records processed identifiers so a replay does not create duplicate records downstream.

## 4 Operations

### 4.1 Monitoring and alerts
Every service sends traces and metrics through OpenTelemetry. Alert rules are written as code and route to the team chat channel and the paging tool. Page only for customer-visible failures; everything else becomes a ticket.

### 4.2 On-call
The on-call engineer owns the pager for one week, from Monday ten a.m. to the next Monday ten a.m. Acknowledge pages within fifteen minutes. Hand off open incidents in writing at the end of your week.

### 4.3 Incident response
#### 4.3.1 Triage
Start by checking whether the failure is in the source system, our pipeline or the vendor. Look at the latest run in the audit table, then the pipeline logs, then the vendor status page. Declare an incident if payroll or hiring data will be late.

#### 4.3.2 Postmortems
Write a blameless postmortem within five business days for every paged incident. Include the timeline, the root cause, what detection missed and follow-up tasks with owners.

### 4.4 Secrets and key rotation
Service principal secrets expire every ninety days. A scheduled job checks expiry dates and opens a ticket thirty days before a secret expires. Rotate the secret in the key vault and restart the dependent jobs; never paste secrets into tickets or chat.

### 4.5 Cost control
Every resource must carry owner and cost-center tags. Budgets alert the team at eighty percent of the monthly limit. Shut down unused development clusters every Friday.
