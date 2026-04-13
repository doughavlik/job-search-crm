"""
Weekly follow-up digest — runs every Monday morning via GitHub Actions.
Emails a list of all contacts due or overdue for a meeting this week.
Also writes a markdown summary to the GitHub Actions job summary.

Required environment variables (set as GitHub Actions secrets):
  SUPABASE_URL      — e.g. https://ifzcegsompgglmxmqulc.supabase.co
  SUPABASE_KEY      — service role key (bypasses RLS)
  GMAIL_ADDRESS     — sender Gmail address (optional — only needed for email)
  GMAIL_APP_PASSWORD — Gmail App Password (optional — only needed for email)
  RECIPIENT_EMAIL   — where to send the digest (optional — only needed for email)
"""

import os
import smtplib
import json
import urllib.request
from datetime import date, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "").strip()
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "").strip()

THRESHOLD_DAYS = 42  # 6 weeks


def query_supabase(path, params=""):
    if not SUPABASE_URL:
        raise ValueError("SUPABASE_URL is not set")
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_KEY is not set")
    url = f"{SUPABASE_URL}/rest/v1/{path}{params}"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def write_github_summary(body):
    """Write markdown to GitHub Actions step summary if running in Actions."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "w") as f:
            f.write(body)


def main():
    today = date.today()
    cutoff = today - timedelta(days=THRESHOLD_DAYS)

    # Fetch contacts with follow_up_flag on
    contacts = query_supabase(
        "71340_contacts",
        "?follow_up_flag=eq.true&select=full_name,email,phone,last_conversation_date,company:71340_companies(name)&order=last_conversation_date.asc.nullsfirst"
    )

    # Split into overdue and due-soon (within 7 days of threshold)
    due_soon_cutoff = today - timedelta(days=THRESHOLD_DAYS - 7)
    overdue = []
    due_soon = []

    for c in contacts:
        lcd = c.get("last_conversation_date")
        if lcd is None:
            days_since = None
            overdue.append((c, days_since))
        else:
            last = date.fromisoformat(lcd)
            days_since = (today - last).days
            if days_since >= THRESHOLD_DAYS:
                overdue.append((c, days_since))
            elif days_since >= THRESHOLD_DAYS - 7:
                due_soon.append((c, days_since))

    if not overdue and not due_soon:
        print("No contacts due this week — no email sent.")
        write_github_summary("## Weekly Follow-Up Digest\n\nNo contacts due this week.")
        return

    # Build plain-text body
    lines = [f"Job Search CRM — Weekly Follow-Up Digest ({today.strftime('%B %d, %Y')})", "=" * 60, ""]

    if overdue:
        lines.append(f"OVERDUE ({len(overdue)} contact{'s' if len(overdue) != 1 else ''})")
        lines.append("-" * 40)
        for c, days in overdue:
            company = c.get("company", {}) or {}
            company_name = company.get("name", "") if company else ""
            days_str = f"{days} days" if days is not None else "never contacted"
            lines.append(f"  • {c['full_name']}{' @ ' + company_name if company_name else ''} — {days_str} ago")
        lines.append("")

    if due_soon:
        lines.append(f"DUE THIS WEEK ({len(due_soon)} contact{'s' if len(due_soon) != 1 else ''})")
        lines.append("-" * 40)
        for c, days in due_soon:
            company = c.get("company", {}) or {}
            company_name = company.get("name", "") if company else ""
            days_str = f"{days} days"
            lines.append(f"  • {c['full_name']}{' @ ' + company_name if company_name else ''} — {days_str} ago")
        lines.append("")

    lines.append("Open the app: https://doughavlik.github.io/job-search-crm/")

    body = "\n".join(lines)
    total = len(overdue) + len(due_soon)
    subject = f"[CRM] {total} contact{'s' if total != 1 else ''} need follow-up this week"

    # Always print digest to stdout
    print(body)

    # Build GitHub step summary in markdown
    md_lines = [
        f"## Weekly Follow-Up Digest — {today.strftime('%B %d, %Y')}",
        "",
    ]
    if overdue:
        md_lines.append(f"### Overdue ({len(overdue)} contact{'s' if len(overdue) != 1 else ''})")
        for c, days in overdue:
            company = c.get("company", {}) or {}
            company_name = company.get("name", "") if company else ""
            days_str = f"{days} days" if days is not None else "never contacted"
            md_lines.append(f"- **{c['full_name']}**{' @ ' + company_name if company_name else ''} — {days_str} ago")
        md_lines.append("")
    if due_soon:
        md_lines.append(f"### Due This Week ({len(due_soon)} contact{'s' if len(due_soon) != 1 else ''})")
        for c, days in due_soon:
            company = c.get("company", {}) or {}
            company_name = company.get("name", "") if company else ""
            days_str = f"{days} days"
            md_lines.append(f"- **{c['full_name']}**{' @ ' + company_name if company_name else ''} — {days_str} ago")
        md_lines.append("")
    md_lines.append("[Open the app](https://doughavlik.github.io/job-search-crm/)")

    write_github_summary("\n".join(md_lines))

    # Send email only if Gmail credentials are configured
    if not GMAIL_APP_PASSWORD:
        print("GMAIL_APP_PASSWORD not set — skipping email, digest written to GitHub summary.")
        return

    if not GMAIL_ADDRESS or not RECIPIENT_EMAIL:
        print("GMAIL_ADDRESS or RECIPIENT_EMAIL not set — skipping email.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

    print(f"Digest sent via email: {total} contacts listed.")


if __name__ == "__main__":
    main()
