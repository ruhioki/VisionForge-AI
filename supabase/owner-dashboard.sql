-- VisionForge AI shared authentication and owner-only content management.
-- Run this script in Supabase Dashboard -> SQL Editor after the owner has signed in
-- with GitHub at least once. Never expose a service-role key in browser code.

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

-- Keep this script compatible with site_content tables created by earlier versions.
alter table public.site_content
  add column if not exists label text not null default 'Image Lab · Browser Edition',
  add column if not exists tagline text not null default 'Explore classic computer-vision filters on your phone or laptop.',
  add column if not exists description text not null default 'Explore classic computer-vision filters on your device.',
  add column if not exists footer_text text not null default 'VisionForge AI · Open-source learning project',
  add column if not exists published boolean not null default true,
  add column if not exists updated_at timestamptz not null default now(),
  add column if not exists updated_by uuid references auth.users(id);

-- This table is the actual admin allowlist. Regular users cannot read or modify it.
create table if not exists public.site_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  github_username text not null check (github_username = 'ruhioki'),
  created_at timestamptz not null default now()
);
alter table public.site_admins enable row level security;
revoke all on public.site_admins from anon, authenticated;

-- Add only the Supabase account that has the authorized GitHub identity.
-- If this inserts zero rows, sign in through GitHub once, then rerun this script.
insert into public.site_admins (user_id, github_username)
select distinct u.id, 'ruhioki'
from auth.users u
join auth.identities i on i.user_id = u.id
where lower(coalesce(u.email, '')) = lower('thestromer90@gmail.com')
  and i.provider = 'github'
  and coalesce(
    nullif(lower(i.identity_data->>'user_name'), ''),
    nullif(lower(i.identity_data->>'login'), ''),
    ''
  ) = 'ruhioki'
on conflict (user_id) do update set github_username = excluded.github_username;

-- SECURITY DEFINER lets policies check the private allowlist without exposing it.
create or replace function public.is_site_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.site_admins
    where user_id = auth.uid()
  );
$$;
revoke all on function public.is_site_admin() from public;
grant execute on function public.is_site_admin() to authenticated;

alter table public.site_content enable row level security;
drop policy if exists "Public reads published site content" on public.site_content;
drop policy if exists "Exclusive owner manages site content" on public.site_content;
drop policy if exists "Authorized admins manage site content" on public.site_content;

create policy "Public reads published site content" on public.site_content
  for select to anon, authenticated
  using (published = true);

create policy "Authorized admins manage site content" on public.site_content
  for all to authenticated
  using (public.is_site_admin())
  with check (public.is_site_admin());

grant select on public.site_content to anon, authenticated;
grant insert, update, delete on public.site_content to authenticated;

insert into public.site_content (id, label, tagline, description, footer_text, published)
values (
  'home',
  'Image Lab · Browser Edition',
  'Explore classic computer-vision filters on your phone or laptop.',
  'Explore classic computer-vision filters on your device.',
  'VisionForge AI · Open-source learning project',
  true
)
on conflict (id) do nothing;

-- Non-fatal diagnostic: the script can run before the owner has signed in.
do $$
begin
  if not exists (
    select 1
    from public.site_admins a
    join auth.users u on u.id = a.user_id
    where a.github_username = 'ruhioki'
      and lower(coalesce(u.email, '')) = lower('thestromer90@gmail.com')
  ) then
    raise notice 'Owner not registered yet. Sign in once with the authorized GitHub account, then run this SQL script again.';
  end if;
end
$$;
