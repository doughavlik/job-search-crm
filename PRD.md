# Product Requirements Document — Job Search CRM (71340)

## Purpose

A lightweight, mobile-first CRM for managing job search networking — tracking contacts, conversations, companies, and follow-up cadence.

## Core Features

### Contacts
- Fields: full name, LinkedIn URL, phone, email, company (optional association), comments
- Flag: "Propose meeting every 6 weeks" (default: on, toggleable)
- Display: last conversation date + how many weeks ago

### Companies
- Add companies independently
- Optionally associate contacts with a company

### Conversations
- Log notes per contact with a date
- View full conversation history per contact
- Auto-save drafts: notes persist locally on the device until explicitly submitted, so crashes, timeouts, or disconnections do not cause data loss

### Follow-up Alerts
- Email sent to user when a contact is due for a meeting (6-week cadence)
- Email includes: contact info, days overdue for the flagged contact, and a list of all other overdue contacts with days overdue each
- Sent via Gmail using Google App Password

### AI / Agent Access
- All data stored in Supabase (PostgreSQL) with clean schema
- Supabase project URL and API key documented so Claude or other agents can query contact and conversation history directly via REST API
- Enables AI-generated outputs (e.g. thank-you emails) referencing stored data

## Users
Single user (authenticated via Supabase Auth, email/password). No multi-user support required.

## Platforms
- **Primary:** Mobile (iOS 16+ Safari) — optimized for quick, interruptible note entry
- **Secondary:** Desktop browser — functional, not polished

## Constraints
- Zero or near-zero cost (Supabase free tier, GitHub Pages hosting)
- No server-side compute
- No build pipeline
