-- VisionForge AI shared authentication and owner-only app controls.
-- Run in Supabase SQL Editor after the authorized owner has signed in with GitHub.
-- Never expose a service-role key in browser code.

create table if not exists public.site_content (
  id text primary key check (id = 'home'),
  label text not null default 'Image Lab · Browser Edition',
  tagline text not null default 'Explore classic computer-vision filters on your phone or laptop.',
  description text not null default 'Explore classic computer-vision filters on your device.',
  footer_text text not null default 'VisionForge AI · Open-source learning project',
  published boolean not null default true,
  announcement_text text not null default '',
  announcement_enabled boolean not null default false,
  maintenance_mode boolean not null default false,
  maintenance_message text not null default 'VisionForge AI is temporarily undergoing maintenance. Please check back soon.',
  updated_at timestamptz not null default now(),
  updated_by uuid references auth.users(id)
);

-- Add missing columns without replacing existing content or the existing home row.
alter table public.site_content
  add column if not exists label text not null default 'Image Lab · Browser Edition',
  add column if not exists tagline text not null default 'Explore classic computer-vision filters on your phone or laptop.',
  add column if not exists description text not null default 'Explore classic computer-vision filters on your device.',
  add column if not exists footer_text text not null default 'VisionForge AI · Open-source learning project',
  add column if not exists published boolean not null default true,
  add column if not exists announcement_text text not null default '',
  add column if not exists announcement_enabled boolean not null default false,
  add column if not exists maintenance_mode boolean not null default false,
  add column if not exists maintenance_message text not null default 'VisionForge AI is temporarily undergoing maintenance. Please check back soon.',
  add column if not exists updated_at timestamptz not null default now(),
  add column if not exists updated_by uuid references auth.users(id);

-- The private allowlist is never directly readable or writable by browser roles.
create table if not exists public.site_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  github_username text not null check (github_username = 'ruhioki'),
  created_at timestamptz not null default now()
);
alter table public.site_admins enable row level security;
revoke all on public.site_admins from public, anon, authenticated;

-- Register only the Supabase user with the expected email and GitHub username.
insert into public.site_admins (user_id, github_username)
select distinct u.id, 'ruhioki'
from auth.users u
join auth.identities i on i.user_id = u.id
where lower(coalesce(u.email, '')) = lower('thestromer90@gmail.com')
  and i.provider = 'github'
  and coalesce(nullif(lower(i.identity_data->>'user_name'), ''),
               nullif(lower(i.identity_data->>'login'), ''), '') = 'ruhioki'
on conflict (user_id) do update set github_username = excluded.github_username;

create or replace function public.is_site_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.site_admins a
    where a.user_id = auth.uid()
      and a.github_username = 'ruhioki'
  );
$$;
revoke all on function public.is_site_admin() from public, anon;
grant execute on function public.is_site_admin() to authenticated;

alter table public.site_content enable row level security;

-- Remove all existing site_content policies so no older permissive policy can bypass this allowlist.
do $$
declare p record;
begin
  for p in
    select policyname from pg_policies
    where schemaname = 'public' and tablename = 'site_content'
  loop
    execute format('drop policy if exists %I on public.site_content', p.policyname);
  end loop;
end
$$;

create policy "Public reads published site content" on public.site_content
  for select to anon, authenticated using (published = true);

-- Require a verified second factor for privileged owner writes.
-- Existing owner sessions at AAL1 must enroll/verify MFA before saving admin changes.
create policy "Authorized owner manages site content" on public.site_content
  for all to authenticated
  using (public.is_site_admin() and (select auth.jwt() ->> 'aal') = 'aal2')
  with check (public.is_site_admin() and (select auth.jwt() ->> 'aal') = 'aal2');

revoke all on public.site_content from public;
grant select on public.site_content to anon, authenticated;
grant insert, update, delete on public.site_content to authenticated;

insert into public.site_content
  (id, label, tagline, description, footer_text, published)
values
  ('home', 'Image Lab · Browser Edition',
   'Explore classic computer-vision filters on your phone or laptop.',
   'Explore classic computer-vision filters on your device.',
   'VisionForge AI · Open-source learning project', true)
on conflict (id) do nothing;

do $$
begin
  if not exists (
    select 1 from public.site_admins a
    join auth.users u on u.id = a.user_id
    where a.github_username = 'ruhioki'
      and lower(coalesce(u.email, '')) = lower('thestromer90@gmail.com')
  ) then
    raise notice 'Owner not registered. Sign in with GitHub account ruhioki, then rerun this SQL.';
  end if;
end
$$;

-- SQL Editor verification: this checks registration, not the browser JWT's live admin result.
select exists (
  select 1 from public.site_admins a
  join auth.users u on u.id = a.user_id
  where a.github_username = 'ruhioki'
    and lower(coalesce(u.email, '')) = lower('thestromer90@gmail.com')
) as authorized_owner_registered;
