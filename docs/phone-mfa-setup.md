# VisionForge AI phone MFA setup

The app supports Supabase Auth phone-factor enrollment and a second-factor challenge during sign-in. This is **not active for every account until a phone factor is enrolled and verified**, and SMS delivery will not work until the Supabase project has an SMS provider configured.

## Configure Supabase before testing

1. Open the Supabase project dashboard for VisionForge AI.
2. In **Authentication → Providers / Phone**, enable phone authentication/MFA as supported by your project settings.
3. Configure a supported SMS provider and its credentials in the Supabase dashboard. Keep provider secrets in Supabase settings only. Never commit them to GitHub or put them in `web-app/supabase-config.js`.
4. Review OTP expiry, SMS rate limits, abuse protection, and any provider restrictions before production use.
5. In **Authentication → URL Configuration**, allow the deployed app URL, including `https://ruhioki.github.io/VisionForge-AI/security.html` and `https://ruhioki.github.io/VisionForge-AI/login.html`.
6. Deploy the current branch/PR, sign in to the app, open **Account security · Phone 2FA**, enter a phone number in international format (for example `+91...`), and verify the SMS code.
7. Sign out and sign in again. The login page should ask for the second factor before routing to the app.

## Important behavior and limitations

- Phone MFA is opt-in until a user enrolls and verifies a factor. Once enrolled, login checks Supabase's authenticator assurance level and requires a second-factor challenge.
- If a verified phone factor is enrolled, SMS is used for the challenge. If a TOTP authenticator factor is enrolled instead, the login flow accepts its current code.
- SMS is weaker than passkeys or authenticator-app TOTP because phone numbers can be ported or SIM-swapped. For government or high-impact deployments, prefer passkeys/WebAuthn or TOTP where feasible and establish an approved account-recovery process.
- This is a browser client. The database and Supabase Auth enforce access; never trust a client-side role flag alone.
- Do not use this prototype with real identity documents or sensitive public records until an authorized organization has reviewed hosting, data retention, access controls, audit requirements, privacy obligations, accessibility, and incident response.
- A phone number is personal information. Collect it only with consent and for a documented purpose. Do not write it to logs or a custom table unnecessarily.
