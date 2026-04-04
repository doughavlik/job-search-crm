# Tech Stack — Job Search CRM (71340)

## Frontend
Single-file static app (`index.html`) built with vanilla HTML, CSS, and JavaScript. No build step, no framework. Mobile-first layout optimized for iOS 16+ Safari.

**Draft persistence:** Notes-in-progress saved to `localStorage` on every keystroke. Synced to Supabase only on explicit submit. Survives crashes, disconnections, and interrupted sessions.

## Database
Supabase (PostgreSQL) on the free tier. All objects namespaced with a `71340_` prefix.

Key tables:
- `71340_contacts` — contact records with follow-up flag and last-conversation cache
- `71340_companies` — company records
- `71340_conversations` — notes + date, linked to a contact

REST API publicly queryable with the anon key (RLS enforces read access post-login). Enables direct access from Claude and other AI agents.

## Authentication & Access
Supabase Auth (email/password) for the web UI. Row Level Security on all tables.

## Hosting
GitHub Pages (static, free). Auto-deploys on push to `main`.

## Email Notifications
Python script (run via GitHub Actions scheduled workflow, free tier) sends follow-up reminder emails via Gmail SMTP using a Google App Password. No separate email service required.

## AI Agent Access
Supabase REST API + documented schema allows Claude (or any agent) to:
- Query contacts and conversation history
- Generate outputs (e.g., thank-you emails) from stored notes

## Languages
HTML, CSS, JavaScript (frontend) · Python (email notification script) · SQL (Supabase schema)

## Cost
All components free: Supabase free tier, GitHub Pages, GitHub Actions (2,000 min/month free).
