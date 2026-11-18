-- Run in Supabase Dashboard -> SQL Editor. Never expose a service-role key in the browser.
create table if not exists public.site_content (
  id text primary key check (id = 'home'),
  label text not null default 'Image Lab · Browser Edition',
  tagline text not null default 'Explore classic computer-vision filters on your phone or laptop.',
  description text not null default 'Explore classic computer-vision filters on your device.',
  footer_text text not null default 'VisionForge AI · Open-source learning project',
  published boolean not null default true,
  updated_at timestamptz not null default now(),
  updated_by uuid references auth.users(id)
);
alter table public.site_content enable row level security;
drop policy if exists "Public reads published site content" on public.site_content;
drop policy if exists "Exclusive owner manages site content" on public.site_content;
create policy "Public reads published site content" on public.site_content
  for select to anon, authenticated using (published = true);
create policy "Exclusive owner manages site content" on public.site_content
  for all to authenticated
  using ((auth.jwt() ->> 'email') = 'mo655099@gmail.com')
  with check ((auth.jwt() ->> 'email') = 'mo655099@gmail.com');
grant select on public.site_content to anon, authenticated;
grant insert, update, delete on public.site_content to authenticated;
insert into public.site_content (id, label, tagline, description, footer_text, published)
values ('home','Image Lab · Browser Edition',
'Explore classic computer-vision filters on your phone or laptop.',
'Explore classic computer-vision filters on your device.',
'VisionForge AI · Open-source learning project',true)
on conflict (id) do nothing;
-- RLS is the security boundary; JWT email is verified by Supabase.
-- The id check constraint allows only the single homepage row.
