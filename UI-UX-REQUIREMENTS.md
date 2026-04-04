# UI/UX Requirements — Job Search CRM (71340)

## Mobile-First Principles
- Touch targets minimum 44px. No hover-only interactions.
- Single-column layout. Large readable font (16px minimum body text).
- Forms optimized for thumb input: fields stacked vertically, no small dropdowns.

## Contacts List (Home Screen)
- Contacts sorted by urgency: overdue for meeting shown first, then by last-conversation date (oldest first).
- Each contact card shows: name, company, last conversation date, "X weeks ago", and a visual overdue indicator (e.g. red dot) if past 6-week threshold.
- Each contact card includes a one-tap **"I just talked to [name]"** quick-capture button that opens a blank note with today's date pre-filled. This is the primary mobile action and must be prominently accessible without navigating to the contact detail view.

## Note Entry
- Dedicated note screen per contact — minimal UI, just a text area and a date field (defaulting to today).
- Auto-save to `localStorage` on every keystroke. Clear indicator that a draft is saved locally.
- Submit button explicitly syncs to Supabase.

## Navigation
- Bottom navigation bar (mobile-friendly): Contacts | Companies | Add Contact.
- Minimal transitions; no animations that slow the app.

## Desktop
- Same single-column layout constrained to ~480px centered. Functional, not redesigned.
