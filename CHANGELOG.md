# Changelog

## 2026-04-04

### Fixed: Follow-up checkbox unresponsive on iPhone

The global CSS rule `input { -webkit-appearance: none }` was stripping native rendering from all input elements, including checkboxes. On iOS Safari, this made the "Propose meeting every 6 weeks" checkbox completely unresponsive.

**Fix:** Added an overriding rule `input[type="checkbox"] { -webkit-appearance: checkbox; appearance: checkbox; }` to restore native checkbox rendering on all platforms.

### Added: Edit and delete past logged conversations

Users can now edit and delete previously logged conversations from the contact detail screen.

**Changes:**
- Each conversation entry now shows **Edit** and **Delete** buttons inline.
- **Edit:** Opens the note screen pre-filled with the existing date and note text. The date field is editable, allowing the user to correct the conversation date. Saving updates the record in Supabase.
- **Delete:** Prompts for confirmation, then deletes the conversation from Supabase.
- After any edit or delete, `last_conversation_date` on the contact is recalculated from the remaining conversations (rather than blindly set to the edited date), ensuring it always reflects the true most-recent conversation.

**New functions:** `editConvo(id)`, `deleteConvo(id)`, `updateLastConvoDate(contactId)`
