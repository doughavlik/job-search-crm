# Job Search CRM — Claude Agent Reference

## App
Hosted at: https://doughavlik.github.io/job-search-crm/
GitHub repo: https://github.com/doughavlik/job-search-crm

## Supabase Access

**Project URL:** `https://ifzcegsompgglmxmqulc.supabase.co`
**Anon key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmemNlZ3NvbXBnZ2xteG1xdWxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2MDkzMDksImV4cCI6MjA4OTE4NTMwOX0.akXCmDSJ_GNq7MD0PIPtQcRusIWlBuqpLvskjICvewQ`

For agent queries (bypasses RLS), use the Management API:

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/ifzcegsompgglmxmqulc/database/query" \
  -H "Authorization: Bearer <sbp_token_from_credentials.md>" \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR SQL HERE"}'
```

## Table Schema

All tables use a `71340_` prefix.

### 71340_contacts
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK, auto-generated |
| full_name | text | Required |
| linkedin_url | text | Optional |
| phone | text | Optional |
| email | text | Optional |
| company_id | uuid | FK → 71340_companies.id, nullable |
| comments | text | Optional freeform notes |
| follow_up_flag | boolean | Default true — include in 6-week cadence |
| last_conversation_date | date | Cached from latest conversation; updated on note submit |
| created_at | timestamptz | Auto |

### 71340_companies
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK, auto-generated |
| name | text | Required |
| created_at | timestamptz | Auto |

### 71340_conversations
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK, auto-generated |
| contact_id | uuid | FK → 71340_contacts.id, CASCADE delete |
| note | text | Required |
| date | date | Required, defaults to today |
| created_at | timestamptz | Auto |

## Example Queries

**List all contacts with their company and last conversation:**
```sql
SELECT c.full_name, co.name AS company, c.last_conversation_date, c.follow_up_flag
FROM "71340_contacts" c
LEFT JOIN "71340_companies" co ON co.id = c.company_id
ORDER BY c.last_conversation_date ASC NULLS FIRST;
```

**List overdue contacts (no conversation in 6+ weeks):**
```sql
SELECT full_name, last_conversation_date,
  CURRENT_DATE - last_conversation_date AS days_since
FROM "71340_contacts"
WHERE follow_up_flag = true
  AND (last_conversation_date IS NULL OR last_conversation_date < CURRENT_DATE - INTERVAL '42 days')
ORDER BY last_conversation_date ASC NULLS FIRST;
```

**Get all conversations for a contact:**
```sql
SELECT cv.date, cv.note
FROM "71340_conversations" cv
JOIN "71340_contacts" c ON c.id = cv.contact_id
WHERE c.full_name ILIKE '%Name Here%'
ORDER BY cv.date DESC;
```

**List contacts due this week (for weekly digest):**
```sql
SELECT full_name, email, last_conversation_date,
  CURRENT_DATE - last_conversation_date AS days_since
FROM "71340_contacts"
WHERE follow_up_flag = true
  AND last_conversation_date < CURRENT_DATE - INTERVAL '35 days'
ORDER BY last_conversation_date ASC NULLS FIRST;
```

## Deployment
- GitHub Pages auto-deploys on push to `main`
- Email notifications run via GitHub Actions on a weekly cron (Mondays 8am CT)
- No build step — `index.html` is the entire frontend
