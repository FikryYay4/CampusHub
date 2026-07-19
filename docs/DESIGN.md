# Design System Inspired by Itemku

## 1. Visual Theme & Atmosphere

Itemku's design system embodies a modern, trustworthy digital marketplace centered around gaming and digital goods commerce. The aesthetic combines a vibrant primary blue palette with clean, professional neutrals to create an accessible yet energetic environment. The visual language emphasizes clarity and security—critical for an e-commerce platform handling transactions. Subtle shadows and carefully calibrated spacing foster a sense of depth and organization, while the bold typography hierarchy guides users through product discovery and purchasing workflows. The overall impression is contemporary, approachable, and commerce-focused, balancing gamified visual elements with enterprise-grade reliability.

**Key Characteristics**
- Vibrant blue primary system establishing trust and energy
- Clean neutral foundation (`#E5E7EB`, `#000000`, `#FFFFFF`) for readability
- Rounded component corners (`8px` radius) softening technical appearance
- Layered elevation system with subtle shadows for depth
- Strong typographic contrast using Exo and Exo 2 families
- Accent yellow badges (`#FFC107` implied) for calls-to-action and status
- High contrast text-to-background ratios ensuring accessibility

## 2. Color Palette & Roles

### Primary
- **Primary Blue** (`#2C77D2`): Main interactive elements, primary CTAs, navigation highlights, and core brand identity
- **Primary Dark Blue** (`#1859AA`): Pressed states, secondary emphasis, hover interactions
- **Primary Light Blue** (`#307FE2`): Alternative primary state, interactive feedback

### Accent Colors
- **Bright Accent Blue** (`#215EA9`): Tertiary interactive states and supporting highlights
- **Pale Blue** (`#CBDFF8`): Light backgrounds for subtle emphasis zones
- **Sky Blue** (`#CFE5FF`): Hover states and progressive disclosure backgrounds
- **Ultra Light Blue** (`#D9E2FC`): Tertiary backgrounds and disabled states
- **Ghost Blue** (`#EAF2FC`): Faint backgrounds for information sections

### Interactive
- **Button Primary** (`#2C77D2`): Standard button backgrounds, primary actions
- **Button Hover** (`#1859AA`): Button hover and pressed states
- **Link Text** (`#2C77D2`): Hyperlink text color, matching primary blue

### Neutral Scale
- **Black** (`#000000`): Primary text, headings, body copy
- **Text Charcoal** (`#474747`): Secondary text, body emphasis
- **Text Gray** (`#909090`): Tertiary text, subtle labels
- **Text Dark** (`#1B1B1B`): High-contrast text for accessibility
- **White** (`#FFFFFF`): Text on dark backgrounds, card backgrounds

### Surface & Borders
- **Light Gray Border** (`#E5E7EB`): Primary border color, divider lines, subtle separators
- **Medium Gray** (`#E2E2E2`): Secondary borders, secondary dividers
- **Card Background** (`#FFFFFF`): Product cards, content containers
- **Transparent Black** (`#0000`): Overlay backgrounds, transparent masks

### Semantic / Status
- **Error Red** (`#E42B2B`): Error states, validation failures, dangerous actions, discount strike-through text

## 3. Typography Rules

### Font Family
- **Primary Font**: Exo (headings, navigation, UI text) with fallback stack: `Exo, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- **Secondary Font**: Exo 2 (body text, descriptions) with fallback stack: `Exo 2, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- **Monospace / Accent**: Helvetica (buttons, labels, metadata) with fallback stack: `Helvetica, Arial, sans-serif`

### Hierarchy

| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|------|--------|-------------|----------------|-------|
| Display / H1 | Exo | 32px | 700 | 48px | 0px | Hero headlines, page titles |
| Heading / H2 | Exo | 24px | 700 | 36px | 0px | Section headers, category titles |
| Subheading / H3 | Exo | 20px | 700 | 30px | 0px | Subsection headers, card titles |
| Body / Large | Exo 2 | 16px | 400 | 24px | 0px | Main body text, product descriptions |
| Body / Base | Exo 2 | 14px | 400 | 21px | 0px | Standard body copy, card labels |
| Link | Exo | 12px | 400 | 18px | 0px | Hyperlinks, action text |
| Button / Primary | Helvetica | 12px | 700 | 18px | 0px | Standard button labels |
| Button / Large | Exo | 16px | 700 | 24px | 0px | Large CTA buttons |
| Button / Medium | Exo | 14px | 700 | 21px | 0px | Medium action buttons |
| Caption / Small | Helvetica | 12px | 400 | 21px | 0px | Metadata, timestamps, helpers |
| Code / Mono | Helvetica | 12px | 400 | 18px | 0px | Inline code, technical text |

### Principles
- **Hierarchy through weight**: Rely primarily on font weight (400 vs. 700) rather than size variance for efficiency
- **Generous line height**: 1.5× font size minimum ensures readability in dense product grids
- **Semantic consistency**: Use Exo for UI-facing content (buttons, labels) and Exo 2 for narrative body copy
- **Accessibility**: Maintain minimum 16px for body text on small screens; scale up proportionally
- **Link styling**: Links inherit primary blue (`#2C77D2`) with no underline; underline appears on hover

## 4. Component Stylings

### Buttons

#### Primary Button
- **Background**: `#2C77D2`
- **Text Color**: `#FFFFFF`
- **Font Family**: Exo
- **Font Size**: `16px`
- **Font Weight**: 700
- **Padding**: `10px 12px`
- **Border Radius**: `8px`
- **Border**: none
- **Height**: `44px`
- **Line Height**: `24px`
- **Hover State**: Background `#1859AA`, shadow `rgba(0, 0, 0, 0.1) 0px 4px 12px`
- **Active/Pressed**: Background `#0F3A7D`, transform `scale(0.98)`
- **Disabled**: Background `#D9E2FC`, text color `#909090`, cursor `not-allowed`

#### Secondary Button (Medium)
- **Background**: `#2C77D2`
- **Text Color**: `#FFFFFF`
- **Font Family**: Exo
- **Font Size**: `14px`
- **Font Weight**: 700
- **Padding**: `8px 8px`
- **Border Radius**: `8px`
- **Border**: none
- **Height**: `36px`
- **Line Height**: `21px`
- **Hover State**: Background `#1859AA`
- **Active/Pressed**: Background `#0F3A7D`

#### Ghost Button (Rounded, White Text)
- **Background**: transparent
- **Text Color**: `#FFFFFF`
- **Font Family**: Exo
- **Font Size**: `12px`
- **Font Weight**: 400
- **Padding**: `0px`
- **Border Radius**: `9999px`
- **Border**: none
- **Height**: auto
- **Line Height**: `18px`
- **Hover State**: Background `rgba(255, 255, 255, 0.1)`, text color `#FFFFFF`

#### Compact Button (Small)
- **Background**: `#307FE2`
- **Text Color**: `#FFFFFF`
- **Font Family**: Helvetica
- **Font Size**: `12px`
- **Font Weight**: 700
- **Padding**: `0px`
- **Border Radius**: `3px`
- **Border**: `1px solid #307FE2`
- **Height**: `28px`
- **Width**: `99px`
- **Line Height**: `18px`
- **Hover State**: Background `#215EA9`, border `1px solid #215EA9`

### Cards & Containers

#### Product Card (Image + Content)
- **Background**: transparent (outer wrapper)
- **Border Radius**: `8px`
- **Box Shadow**: `rgba(0, 0, 0, 0.1) 0px 2px 4px 0px, rgba(0, 0, 0, 0.05) 0px 6px 16px 0px`
- **Height**: `364px`
- **Width**: `160px`
- **Image Wrapper**:
  - Background: transparent
  - Border Radius: `4px 4px 0px 0px`
  - Height: `212px`
  - Width: `160px`
- **Content Wrapper**:
  - Background: `#FFFFFF`
  - Padding: `8px`
  - Border Radius: `0px 0px 4px 4px`
  - Height: `152px`
  - Width: `160px`
  - Text Color: `#000000`
  - Font Family: Exo
  - Font Size: `12px`
  - Line Height: `18px`
- **Hover State**: Box shadow increases to `rgba(0, 0, 0, 0.15) 0px 4px 8px 0px, rgba(0, 0, 0, 0.08) 0px 8px 20px 0px`, transform `translateY(-2px)`

#### Badge (Featured, New Release, Discount)
- **Background**: `#FFC107` (inferred from visual)
- **Text Color**: `#000000`
- **Font Family**: Helvetica
- **Font Size**: `11px`
- **Font Weight**: 700
- **Padding**: `4px 8px`
- **Border Radius**: `4px`
- **Line Height**: `16px`
- **Position**: Absolute, top-left or top-right of card

#### Section Container
- **Background**: `#FFFFFF` or `#EAF2FC` (light section)
- **Padding**: `24px` or `48px`
- **Border Radius**: `0px`
- **Border**: `1px solid #E5E7EB` (bottom border for separation)

### Inputs & Forms

#### Text Input
- **Background**: `#FFFFFF`
- **Text Color**: `#000000`
- **Font Family**: Exo
- **Font Size**: `16px`
- **Font Weight**: 400
- **Padding**: `10px 12px`
- **Border Radius**: `0px` (or `4px` for modern variant)
- **Border**: `1px solid #E5E7EB`
- **Line Height**: `24px`
- **Height**: auto (minimum `44px`)
- **Placeholder Color**: `#909090`
- **Focus State**: Border `1px solid #2C77D2`, box shadow `0px 0px 0px 3px rgba(44, 119, 210, 0.1)`
- **Error State**: Border `1px solid #E42B2B`, text color `#E42B2B`
- **Disabled State**: Background `#E5E7EB`, color `#909090`, cursor `not-allowed`

#### Compact Input (Small)
- **Background**: `#FFFFFF`
- **Text Color**: `#000000`
- **Font Family**: Exo
- **Font Size**: `12px`
- **Font Weight**: 400
- **Padding**: `6px 8px`
- **Border Radius**: `0px`
- **Border**: `1px solid #E5E7EB`
- **Height**: `18px`
- **Line Height**: `18px`

#### Search Input (Hero)
- **Background**: `#FFFFFF`
- **Text Color**: `#000000`
- **Font Family**: Exo
- **Font Size**: `16px`
- **Font Weight**: 400
- **Padding**: `10px 16px`
- **Border Radius**: `4px`
- **Border**: none
- **Height**: `44px`
- **Width**: `100%` (or responsive)
- **Box Shadow**: none (or subtle)
- **Placeholder**: "Cari Game, Diamond, Hero…" in `#909090`
- **Focus State**: Box shadow `0px 0px 0px 3px rgba(44, 119, 210, 0.1)`, border `1px solid #2C77D2`

### Navigation

#### Top Navigation Bar
- **Background**: `#2C77D2` (primary blue gradient to `#1859AA` possible)
- **Padding**: `8px 16px`
- **Height**: `64px`
- **Display**: Flex, align-items center
- **Text Color**: `#FFFFFF`
- **Font Family**: Exo
- **Font Size**: `14px`

#### Navigation Links
- **Text Color**: `#FFFFFF`
- **Font Weight**: 400
- **Padding**: `8px 16px`
- **Border Radius**: `4px`
- **Hover State**: Background `rgba(255, 255, 255, 0.1)`
- **Active State**: Background `rgba(255, 255, 255, 0.2)`, text color `#FFFFFF`
- **Font Size**: `12px`
- **Line Height**: `18px`

#### Breadcrumb Navigation
- **Separator**: `/` in `#909090`
- **Text Color**: `#474747`
- **Font Family**: Exo
- **Font Size**: `12px`
- **Font Weight**: 400
- **Active Link**: Text `#2C77D2`, weight 700
- **Spacing**: `8px` around separator

### Badges & Labels

#### Status Badge (Discount %)
- **Background**: `#E42B2B`
- **Text Color**: `#FFFFFF`
- **Font Family**: Helvetica
- **Font Size**: `11px`
- **Font Weight**: 700
- **Padding**: `4px 8px`
- **Border Radius**: `3px`
- **Display**: Inline-block
- **Line Height**: `16px`

#### Info Badge
- **Background**: `#EAF2FC`
- **Text Color**: `#2C77D2`
- **Font Family**: Exo
- **Font Size**: `12px`
- **Font Weight**: 400
- **Padding**: `6px 12px`
- **Border Radius**: `4px`
- **Line Height**: `18px`

## 5. Layout Principles

### Spacing System
The spacing system is based on an `8px` base unit, scaled in multiples: `4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `48px`, `80px`, `84px`, `128px`.

- **Micro spacing** (`4px`): Tight element grouping, icon-to-text gaps
- **Small spacing** (`8px`): Component internal padding (buttons, inputs, badges)
- **Standard spacing** (`12px`, `16px`): Default gap between inline elements, label-to-input distance
- **Section spacing** (`24px`, `48px`): Vertical rhythm between content sections, container padding
- **Large spacing** (`80px`, `84px`, `128px`): Major layout breaks, full-width sections, hero-to-content transitions

### Grid & Container
- **Max Width**: `1200px` for main content grid (recommended)
- **Column Strategy**: 12-column grid system inferred; product cards at `160px` width suggest 6–8 columns on desktop
- **Gutter**: `12px` to `16px` between columns
- **Section Patterns**:
  - Hero section: Full width with `128px` vertical padding
  - Product grid: 6–12 column layout with `12px` gap, centered max-width container
  - Footer: 4-column layout with `24px` gutter
  - Hero search: Full width, centered with `48px` padding top/bottom

### Whitespace Philosophy
Whitespace is leveraged strategically to guide user attention and reduce cognitive load. Product cards employ breathing room within the `160px × 364px` bounds. Content sections maintain substantial vertical gaps (`24px`–`48px`) to separate distinct sections (game offers, gift cards, top-up options). The navigation bar anchors the top with compact spacing (`8px` padding), while hero regions employ generous white space to position search and messaging prominently. This approach fosters clarity in a commerce-heavy interface.

### Border Radius Scale
- **None** (`0px`): Input fields, navigation bars, full-width sections
- **Tight** (`3px`): Compact buttons, small badges
- **Standard** (`4px`): Badges, small card corners, dividers
- **Medium** (`8px`): Primary buttons, main cards, product containers
- **Pill** (`9999px`): Ghost buttons, rounded action buttons, circular icons

## 6. Depth & Elevation

| Level | Treatment | Use |
|-------|-----------|-----|
| Flat (L0) | No shadow | Input fields, text, backgrounds, flat backgrounds |
| Raised (L1) | `rgba(0, 0, 0, 0.1) 0px 2px 4px 0px, rgba(0, 0, 0, 0.05) 0px 6px 16px 0px` | Product cards, standard containers, normal state |
| Lifted (L2) | `rgba(0, 0, 0, 0.15) 0px 4px 8px 0px, rgba(0, 0, 0, 0.08) 0px 8px 20px 0px` | Card hover, interactive elevations, modals |
| Floating (L3) | `rgba(0, 0, 0, 0.2) 0px 6px 16px 0px, rgba(0, 0, 0, 0.1) 0px 12px 32px 0px` | Dropdowns, tooltips, context menus |
| Modal (L4) | `rgba(0, 0, 0, 0.3) 0px 8px 24px 0px` | Full-screen overlays, modal windows, critical dialogs |

**Shadow Philosophy**: Shadows are used minimally and subtly to provide depth without overwhelming the interface. The two-layer shadow approach (outer + inner blur) creates dimensional separation between z-index levels. On hover, shadows increase to signal interactivity. Flat surfaces (inputs, text, backgrounds) avoid shadows entirely to maintain clarity. The overall effect is modern and clean, prioritizing content over decorative depth.

## 7. Do's and Don'ts

### Do
- Use `#2C77D2` as the primary CTA color for all major actions (purchase, checkout, explore)
- Maintain at least `44px` height for touch targets on mobile devices
- Apply `8px` border radius to primary buttons and card containers
- Employ Exo font for all UI-facing elements (buttons, labels, headings) and Exo 2 for body narratives
- Group related inputs with `12px` horizontal gap and `16px` vertical gap
- Use `#E42B2B` exclusively for error states, discounts, and danger scenarios
- Stack product cards in a 6-column grid on desktop, responsive down to 2–3 columns on mobile
- Include focus states (blue ring) on all interactive elements for keyboard navigation
- Ensure text contrast ratios meet WCAG AA standards (4.5:1 for body, 3:1 for large text)
- Render badges and status indicators with `#FFC107` yellow background for high visibility

### Don't
- Mix primary button colors—never use secondary blues (`#1859AA`, `#215EA9`) for primary CTAs
- Apply shadows to input fields or flat background surfaces; reserve shadows for cards and elevated containers
- Use font sizes smaller than `12px` for body text, except in captions and metadata
- Nest border radius values inconsistently; use `8px` or `4px` standards
- Create spacing between elements less than `8px` unless justifying micro-interactions
- Place interactive elements with less than `44px` height on mobile (except in compact tables or lists)
- Use color alone to convey status; always pair with icon, text, or pattern
- Override the navigation bar background from primary blue (`#2C77D2`)—maintain brand consistency
- Apply multiple shadows on a single element; use only one elevation level per component state
- Reduce line height below `1.4×` font size for readability

## 8. Responsive Behavior

### Breakpoints

| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | `< 640px` | 1–2 column product grids, full-width inputs, stacked navigation, `16px` base padding |
| Tablet | `640px` – `1024px` | 2–4 column product grids, sidebar navigation optional, `20px` base padding |
| Desktop | `1024px` – `1440px` | 6 column product grids, fixed navigation, `24px` base padding, max-width containers active |
| Large Desktop | `> 1440px` | 8+ column grids (optional), full-width sections, `48px` padding on hero |

### Touch Targets
- **Minimum touch target**: `44px × 44px` (buttons, links, interactive elements)
- **Icon + text combination**: `40px` height minimum, with `8px` padding around icon
- **Dense lists** (product grids): `48px` row height for checkbox/radio rows
- **Spacing between targets**: Minimum `8px` to prevent accidental taps

### Collapsing Strategy
- **Product cards**: Scale from `160px` width (desktop) → `140px` (tablet) → `100%` max-width (mobile, single column)
- **Navigation**: Collapse horizontal menu into hamburger icon below `768px`
- **Hero search**: Full-width at all breakpoints; reduce padding from `128px` (desktop) to `48px` (mobile)
- **Buttons**: Maintain `44px` height at all breakpoints; reduce padding left/right on mobile (`8px` vs. `12px` desktop)
- **Typography**: Scale headings down `4px`–`8px` on mobile (h2 from `24px` → `20px`, h3 from `20px` → `16px`)
- **Grid gaps**: Reduce from `12px` (desktop) to `8px` (mobile) for tighter spacing
- **Sections**: Full-bleed on mobile; center with max-width container on desktop

## 9. Agent Prompt Guide

### Quick Color Reference
- **Primary CTA** (`#2C77D2`): Primary Blue — all main buttons, interactive elements, links
- **Primary CTA Hover** (`#1859AA`): Primary Dark Blue — button hover and pressed states
- **Background** (`#FFFFFF`): White — card and container backgrounds
- **Text Primary** (`#000000`): Black — headings, body text
- **Text Secondary** (`#474747`): Charcoal — secondary copy, meta text
- **Border / Divider** (`#E5E7EB`): Light Gray — dividers, input borders, subtle separations
- **Error / Danger** (`#E42B2B`): Error Red — errors, validation failures, discount strike-through
- **Accent Badge** (`#FFC107`): Bright Yellow (inferred) — "New", "Featured", discount badges
- **Overlay / Disabled** (`#D9E2FC`): Ultra Light Blue — disabled states, secondary backgrounds
- **Navigation Background** (`#2C77D2`): Primary Blue — top bar, header sections

### Iteration Guide
1. **All primary buttons must use `#2C77D2` background with `#FFFFFF` text**; hover shifts to `#1859AA`.
2. **Button padding and height are strictly `8px–12px` padding with `36px`–`44px` height**; no exceptions for consistency.
3. **Cards are `160px` wide with `8px` radius; shadow is always `rgba(0, 0, 0, 0.1) 0px 2px 4px 0px, rgba(0, 0, 0, 0.05) 0px 6px 16px 0px`**.
4. **Font sizes are locked to the hierarchy table**: Headings `24px`, body `16px`, labels `12px`; no arbitrary sizes.
5. **Spacing uses base `8px` increments**: `8px`, `16px`, `24px`, `48px` are standard; `12px` for gaps.
6. **Input fields have no border-radius** (or `4px` for modern variant); borders are always `#E5E7EB`.
7. **Navigation bar is always `#2C77D2` background with white text, `64px` height minimum**.
8. **Product grid is 6 columns on desktop, responsive down to 2–3 on mobile; never stack single column above tablet**.
9. **All interactive elements must have focus ring**: `0px 0px 0px 3px rgba(44, 119, 210, 0.1)` on focus.
10. **Error state is exclusively `#E42B2B`; use for validation, discount strike-through, and danger actions**.
11. **Accessible line-height is always 1.4×–1.5× font size**; never reduce below `1.3×` for readability.
12. **Touch targets minimum `44px × 44px`** on all devices; test on mobile before shipping.