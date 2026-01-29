# Landing Page Redesign

## Overview

Complete redesign of the hearsay landing page with a balanced approach: equal emphasis on brand identity, podcast discovery, and user conversion. Built with ShadCN components on SvelteKit.

## Visual Direction

- **Background**: Clean white (#ffffff) with light gray sections (#f8f9fa)
- **Text**: Dark gray headings (#1a1a1a), medium gray body (#6b7280)
- **Primary accent**: Blue (#2563eb) for CTAs and interactive elements
- **Typography**: Outfit or Inter (clean sans-serif)
- **Approach**: Minimal, editorial feel matching reference design

## Page Structure

1. Navigation bar (transparent over hero)
2. Hero section (~85vh with featured podcast background)
3. Popular podcasts carousel
4. Features section
5. Footer

---

## Section 1: Navigation Bar

**Behavior**: Overlays hero with transparent/blurred background. Optionally transitions to solid white on scroll.

**Layout**:
- Fixed/sticky at top
- Max-width container (~1200px), centered
- Height: ~64px

**Left side**:
- "hearsay" wordmark in white (over hero), lowercase, medium weight
- Links to home (/)

**Right side (unauthenticated)**:
- "Sign in" - ghost/text button, white text
- "Create account" - primary blue button

**Right side (authenticated)**:
- "Welcome, {email}" - muted white text
- "Dashboard" - ghost button, white
- "Logout" - ghost/outline button

**Mobile (< 768px)**:
- Logo left, hamburger menu right
- Opens as Sheet/dropdown with stacked nav items

**ShadCN components**: Button, Sheet (mobile)

---

## Section 2: Hero Section

**Layout**:
- Full-width, ~85vh height
- Featured podcast artwork as full background image
- Content overlaid on top

**Background**:
- Cover image fills hero area (object-fit: cover)
- Subtle dark overlay for text readability
- Bottom gradient fades from image → white (seamless transition to next section)

**Content overlay**:
- Headline: "track your favorite podcasts." - white/light text, lowercase
- Subtext: Brief value prop in lighter muted white
- CTA buttons:
  - Unauthenticated: "Sign up" (primary blue)
  - Authenticated: "Go to Dashboard" (primary blue)
- Platform badges below: iOS & Android icons with "Coming Soon" Badge overlay, muted white styling

**Data source**:
- Featured podcast from `GET /podcasts/popular` filtered by `is_featured` flag
- Falls back to first popular podcast if none featured

**Responsive (mobile)**:
- Artwork still fills background (may crop)
- Text and CTAs centered
- Smaller headline

**ShadCN components**: Button, Badge

---

## Section 3: Popular Podcasts Carousel

**Layout**:
- White background (seamless from hero fade)
- Padding: ~80px vertical
- Max-width container

**Header**:
- "Popular Podcasts" - clean heading, left-aligned
- "Browse all →" link, right-aligned

**Carousel**:
- Horizontal scrollable row
- ~5-6 cards visible on desktop with partial peek on edges
- Scroll snap behavior
- Left/right arrow buttons on hover (desktop)
- Swipeable on touch devices

**Podcast cards**:
- Square artwork (~150-180px)
- Title below (truncate 1-2 lines)
- Author/publisher in muted text
- Optional: Listen score badge
- Hover: subtle lift + shadow
- Click: navigates to podcast detail or sign-up prompt

**Data source**:
- `GET /podcasts/popular?limit=10`
- Increase limit in +page.server.ts

**Responsive**:
- Fewer visible cards on smaller screens
- Touch-swipeable

**ShadCN components**: Card, Carousel, Badge (optional)

---

## Section 4: Features Section

**Layout**:
- Light gray background (#f8f9fa)
- Padding: ~100px vertical
- Max-width container, centered

**Header**:
- "Why hearsay" - centered heading
- Optional subtext

**Feature cards (3 columns)**:
- Minimal styling (no heavy borders)
- Each contains:
  - Icon (Lucide, line-style, blue or dark gray)
  - Short title
  - 1-2 sentence description

**The three features**:

1. **Never miss an episode**
   - Icon: Bell
   - "Get notified when new episodes drop from your favorite shows"

2. **Your Library**
   - Icon: Library/List
   - "Build and organize your personal podcast collection"

3. **Discovery**
   - Icon: Compass
   - "Find your next favorite podcast with curated recommendations"

**Responsive**: 3 columns → 1 column stacked on mobile

**ShadCN components**: Card (minimal), Lucide icons

---

## Section 5: Footer

**Layout**:
- Dark background (#1a1a1a)
- Padding: ~60px vertical
- Max-width container

**Left side**:
- "hearsay" wordmark in white
- "© 2026 hearsay" below

**Link groups (2-3 columns)**:

**Product**:
- Browse Podcasts
- Dashboard / Sign up

**Company**:
- About
- Contact

**Legal**:
- Privacy Policy
- Terms of Service

**Styling**:
- Links: muted gray (#9ca3af), white on hover
- Clean group separation

**Responsive**: Stack vertically, logo on top, 2-column link grid below

---

## ShadCN Components Required

- Button (multiple variants: default, ghost, outline)
- Card
- Carousel
- Badge
- Sheet (mobile nav)
- NavigationMenu (optional, could use custom)

## Files to Modify

1. `web/src/routes/+page.svelte` - Complete rewrite
2. `web/src/routes/+layout.svelte` - Restyle nav, make transparent over hero
3. `web/src/routes/+page.server.ts` - Increase popular limit, add featured filter
4. `web/src/app.css` or component styles - New color scheme

## Backend Changes

- May need new endpoint or filter: `GET /podcasts/featured` or `?featured=true`
- Current `is_featured` field exists, just needs to be exposed

## Out of Scope

- Mobile app development (just "Coming Soon" badges)
- About/Contact pages (placeholder links for now)
- User authentication flow changes
- Dashboard redesign
