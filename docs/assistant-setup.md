# VisionForge AI Assistant setup

The Assistant page adds local developer utilities and an authenticated server-side AI helper. Research mode uses the OpenAI Responses API web-search tool. The OpenAI key is never placed in browser code.

## Deploy the Edge Function

1. Merge the pull request and update your local repository.
2. Use the Supabase CLI linked to project `zidlkybqejipjajhhmfp`.
3. Add a server-side secret; never put it in `web-app/supabase-config.js` or browser JavaScript:

   ```sh
   supabase secrets set OPENAI_API_KEY=your_key_here
   ```

4. Optional model override: `supabase secrets set OPENAI_MODEL=gpt-4.1-mini`.
5. Deploy with `supabase functions deploy assistant`.
6. Confirm Supabase Auth is enabled and the deployed origin is correct. The function validates the bearer token with Supabase Auth before calling OpenAI.
7. Set provider billing/usage limits and monitor function errors before public use.

## Features

- General help, developer troubleshooting, and online research with source links.
- Local JSON formatting, URL encoding/decoding, Unicode-safe Base64 conversion, text diff, timestamp conversion, and UUID generation.
- The existing Image Lab, CivicScan Desk, and 2FA page remain linked.

## Privacy and safety

AI chat requires sign-in. Only the prompt is sent to the server-side assistant; avoid credentials, OTPs, private keys, sensitive identity data, and confidential source code. The function requests `store: false`, but providers can have separate abuse-monitoring/retention policies. Review provider terms.
Search is informational and may be inaccurate. OCR/QR parsing is not proof of document authenticity. Do not use model output to decide eligibility or other high-impact outcomes. This is a prototype, not a production public-sector system; production needs an authorized privacy/security review, access controls, audit and retention policies, rate limits, accessibility testing, and incident response.
