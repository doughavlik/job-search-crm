# Design Feedback — Job Search CRM (71340)

## What's Working Well
The core design is well-scoped. The mobile-first, offline-resilient note entry solves a real pain point. Using Supabase as the data layer for AI agent access is smart — it avoids building a separate API. The 6-week follow-up flag is actionable and the email alert keeps the system useful even when you're not actively logging in.

---

## Option 1: Minor Tweaks

**Email alert timing:** Rather than emailing on the exact due date, consider a weekly digest every Monday morning listing all contacts due or overdue that week. Less noise, more actionable.

**Conversation quick-capture:** Add a one-tap "I just talked to [name]" button on each contact card that opens a blank note with today's date pre-filled. Reduces friction for the most common mobile action.

**AI access documentation:** Add a `CLAUDE.md` to the repo that specifies the Supabase URL, table schema, and example queries. This makes it immediately usable from any Claude Code session without re-explaining the schema each time.

---

## Option 2: More Dramatic Rethinking

**Use a voice-first note capture instead of typing.** On mobile, speaking a 30-second note is faster and less error-prone than typing while standing in a parking lot. The Web Speech API (Safari-supported) could transcribe speech to text and auto-save. This changes the primary input model but fits your described use case much better than a text area.

**Consider Notion or Airtable as the database instead of Supabase.** Both have free tiers, mobile apps already built, and APIs that Claude can query. You'd skip building the frontend entirely and focus only on the email alerts and AI integration layer. Tradeoff: less control, dependent on a third-party product.
