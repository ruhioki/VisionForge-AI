import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY } from "./supabase-config.js";
if (SUPABASE_URL.startsWith("https://") && SUPABASE_PUBLISHABLE_KEY.length > 20) {
  try {
    const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
      auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false }
    });
    const { data, error } = await supabase.from("site_content")
      .select("label, tagline, description, footer_text")
      .eq("id", "home").eq("published", true).maybeSingle();
    if (error) throw error;
    if (data) {
      const label = document.getElementById("site-label");
      const tagline = document.getElementById("site-tagline");
      const footer = document.getElementById("site-footer-text");
      const description = document.querySelector('meta[name="description"]');
      if (label) label.textContent = data.label;
      if (tagline) tagline.textContent = data.tagline;
      if (footer) footer.textContent = data.footer_text;
      if (description) description.setAttribute("content", data.description);
    }
  } catch (error) {
    console.warn("VisionForge content sync unavailable; showing built-in copy.", error);
  }
}
