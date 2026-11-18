import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY } from "./supabase-config.js";

const setText = (selector, value) => {
  const element = document.querySelector(selector);
  if (element && typeof value === "string") element.textContent = value;
};

if (SUPABASE_URL.startsWith("https://") && SUPABASE_PUBLISHABLE_KEY.length > 20) {
  try {
    const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
      auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false }
    });
    const { data, error } = await supabase.from("site_content")
      .select("label,tagline,description,footer_text,published,announcement_text,announcement_enabled,maintenance_mode,maintenance_message")
      .eq("id", "home").maybeSingle();
    if (error) throw error;
    if (data) {
      if (data.published) {
        setText("#site-label", data.label);
        setText("#site-tagline", data.tagline);
        setText("#site-footer-text", data.footer_text);
        const description = document.querySelector('meta[name="description"]');
        if (description && data.description) description.setAttribute("content", data.description);
      }

      const announcement = document.getElementById("site-announcement");
      if (announcement && data.announcement_enabled && data.announcement_text) {
        announcement.textContent = data.announcement_text;
        announcement.hidden = false;
      }

      const workspace = document.querySelector("main.wrap");
      const maintenance = document.getElementById("maintenance-state");
      if (data.maintenance_mode && workspace && maintenance) {
        maintenance.textContent = data.maintenance_message || "VisionForge AI is temporarily undergoing maintenance. Please check back soon.";
        maintenance.hidden = false;
        workspace.hidden = true;
      }
    }
  } catch (error) {
    console.warn("VisionForge content sync unavailable; showing built-in copy.", error);
  }
}
