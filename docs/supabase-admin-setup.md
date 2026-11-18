# VisionForge AI owner dashboard: Supabase setup

This is a static GitHub Pages site, so it must never contain a private server key. Supabase Auth plus PostgreSQL Row Level Security (RLS) protects the editable content.

## Included

- `web-app/admin.html`: owner-only passwordless sign-in and homepage text editor.
- `web-app/site-content.js`: reads published homepage text.
- `web-app/supabase-config.js`: public configuration placeholders and the owner email.
- `supabase/owner-dashboard.sql`: content table, seed row, and RLS policies.
- Exclusive owner: `mo655099@gmail.com`. Database authorization checks the Supabase JWT email; the browser-side check is not the security boundary.

## Required external configuration

1. Create a Supabase project: https://supabase.com/dashboard.
2. Run the full `supabase/owner-dashboard.sql` file in **SQL Editor**.
3. In **Project Settings → API** (or API keys), copy the Project URL and **publishable** key (older projects may call it the `anon` key). Put these into `web-app/supabase-config.js` as `SUPABASE_URL` and `SUPABASE_PUBLISHABLE_KEY`. Keep `OWNER_EMAIL` unchanged. These two browser values are public by design. Never use a service-role/secret key.
4. In **Authentication → URL Configuration**, set Site URL to `https://ruhioki.github.io/VisionForge-AI/` and add Redirect URLs:
   - `https://ruhioki.github.io/VisionForge-AI/admin.html`
   - `http://localhost:8000/admin.html` (optional local testing)
5. In **Authentication → Providers**, enable Email sign-in and ensure magic-link email delivery works. Supabase's default email service can have rate limits; configure custom SMTP for reliable delivery.
6. Ensure an account exists and is verified for `mo655099@gmail.com` in **Authentication → Users**. Create/invite it there, or temporarily allow signup and complete the first magic-link sign-in. After testing the owner account, disable public signups if available. RLS still limits all writes to the exact owner email.
7. Commit the configured URL and publishable key in `web-app/supabase-config.js` to GitHub, then wait for Pages deployment.
8. Open `https://ruhioki.github.io/VisionForge-AI/admin.html`, request the link, open it in the same browser, edit a short phrase, save, and refresh the homepage.

## Security and scope

- Visitors can read only the row marked `published = true`.
- Only a verified session with JWT email exactly `mo655099@gmail.com` can write/delete content.
- A table constraint permits only the single homepage row. Keep RLS enabled; do not add broad public write policies.
- Never put a service-role/secret key in browser code. A publishable key is safe only with the database policies correctly applied.
- The dashboard edits header label, intro line, SEO description, footer text, and publication toggle. It does not edit Python source code or deploy code changes.
- If email confirmation is enabled, verify the owner email before saving.

## Local test

From the repository root run `python -m http.server 8000 --directory web-app` and open `http://localhost:8000/admin.html`. Add that redirect URL in Supabase. Do not open the page as `file://`; module imports and auth redirects require HTTP.
