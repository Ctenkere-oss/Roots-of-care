# Roots of Care — Beauty Services

A complete, ready-to-publish website for a loc, natural hair and henna studio
in Montréal.

It is a **plain static website**: HTML, CSS and a single small JavaScript file.
No frameworks, no build step required, no database, no server code. Every page
is a normal `.html` file you can open by double-clicking it.

---

## 1. What you get

```
site/                          ← THIS FOLDER IS THE WEBSITE. Upload it as-is.
├── index.html                 Home
├── hair.html                  Hair & Locs
├── henna.html                 Henna
├── services.html              Services, prices & durations (with filters)
├── booking.html               Booking — holds the calendar embed
├── about.html                 About
├── contact.html               Contact form + details + hours
├── booking-policies.html      Booking policies ($20 deposit, 24 h notice)
├── privacy-policy.html        Privacy policy (Québec Law 25 / PIPEDA)
├── terms.html                 Terms of use
├── 404.html                   Error page, in brand colours
├── robots.txt                 Search engine instructions
├── sitemap.xml                Page list for Google
└── assets/
    ├── css/styles.css         ALL the styling, one file
    ├── js/main.js             ALL the scripts, one file
    └── img/                   Logo, icons, share image, image placeholders

src/          Page content only (used by the optional build script — see §10)
tools/        The optional build script
```

---

## 2. Publish it

The site is a folder of files, so almost any host works. Pick one:

| Where | How | Notes |
|---|---|---|
| **Netlify** (easiest) | netlify.com → drag the `site` folder onto the upload box | Free tier, free SSL, custom domain in a few clicks |
| **Cloudflare Pages** | Connect this Git repo, or upload the folder | Free, very fast, free SSL |
| **Vercel** | Import the repo, set the output directory to `site` | Free tier, free SSL |
| **Any cPanel / FTP host** | Upload the **contents** of `site/` into `public_html` | Enable SSL in the host panel |
| **10Web / TenWeb** | Publish to a temporary URL first (Netlify is fine), then use their *import from URL* feature | Their importer reads a live site, not a ZIP |
| **Wix** | Not recommended | Wix cannot import an HTML site. You would have to rebuild the design by hand in their editor. |

Whatever you choose, upload the **contents** of `site/` to the web root, so the
home page ends up at `https://yourdomain.com/index.html`.

You handle hosting, SSL and email — nothing in these files depends on a
specific host.

---

## 3. Checklist — what still needs to be filled in

Everything left to supply is marked in the pages like this: `[[PRICE]]`.
They show up on the page with a dashed underline, so they are easy to spot.

Open the files in any text editor and use **Find & Replace**.

### Already filled in from the Setmore page

These came across from `rootsofcare.setmore.com` and need no further work:

- Email `rootsofcare.vv@gmail.com`, everywhere it appears
- The booking policy: non-refundable $20 deposit, e-transfer, 3-hour window,
  24-hour cancellation notice
- Booking platform named as Setmore in the privacy policy
- 7 services with confirmed prices and durations: No Retwist Styles,
  Small and Medium Men's Twists, Henna one hand and one arm sleeve,
  Jagua one hand and one arm sleeve
- The founder section on the About page: Yamiley's name, her Haitian and
  Cuban roots, and her photograph (`assets/img/yamile-henna.webp`)
- Instagram and Snapchat links, in the footer of every page, in the mobile
  menu, on the contact page, on the booking page, and in the structured data

### Essentials (the site is not ready to launch without these)

- [ ] **`[[PRICE]]` and `[[DURATION]]`** — the remaining 20 services in
      `services.html` (the 7 above already have real numbers). Format:
      `$120` or `from $120`, and `3 h` or `90 min`.
- [ ] **`[[PHONE]]`** — footer of every page, plus contact and booking.
      If you'd rather not publish a number, delete the whole line instead.
- [ ] **`[[HOURS]]`** — seven days in `contact.html`, left blank for now.
      Write `Closed` for days you don't work. (Setmore showed a 22:00
      closing time but not the full week.)
- [ ] **`[[CALENDAR_URL]]`** — `https://rootsofcare.setmore.com` (see §5).
- [ ] **`[[NEIGHBOURHOOD / AREA]]`** — the part of Montréal you serve
      (`about.html`, `contact.html`).
- [ ] **Surname on the privacy policy** (optional). The page names Yamiley
      as the person in charge of personal information. A full legal name is
      stronger there, but a first name is workable.

### Content

- [ ] **`[[TESTIMONIAL 1–3]]`** and **`[[FIRST NAME]]`** — three client
      reviews on the home page. Two or three sentences each reads best.
      (The Setmore page shows one 5-star review — worth asking that client
      for a sentence.)
- [ ] **About page wording** — the founder story in `about.html` was written
      from what you told me. Read it through and change anything that
      doesn't sound like you; it's your voice on the page, not mine.

### Privacy policy specifics

- [ ] **`[[HOSTING PROVIDER]]`** — whoever you host with.
- [ ] **`[[FORM SERVICE]]`** — the contact form service you connect (§6).
- [ ] **`[[ANALYTICS TOOL, or "none"]]`** — write `none` if you don't add one.

### Images

- [ ] **Logo** — see §4.
- [ ] **Photos** — 22 image slots still to fill. Each is a cream
      placeholder marked with the size it wants, and each has an HTML
      comment above it saying what the photo should show. See §7.
      The founder portrait on the About page is already the real thing.

---

## 4. Replace the logo

Right now the logo is drawn with web fonts as a stand-in. To use the real one:

1. Save your logo as `site/assets/img/logo-roots-of-care.svg`
   (or `.png` with a transparent background — then adjust the file name below).
2. In each HTML file, find the block that starts with
   `<!-- LOGO — to use the real logo file, replace the inline <svg> below with:`
   and follow the instruction there: delete the `<svg>…</svg>` block and paste
   the `<img>` tag shown in the comment.
   - In the **header** of every page (small version)
   - In the **hero** of `index.html` (large version)
   - In the **footer** of every page (light version — use a white/off-white
     logo file here, since the footer is brown)
3. Replace the icons too, if you have them:
   `assets/img/favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`,
   and `og-roots-of-care.png` (the 1200 × 630 image shown when the site is
   shared on social media).

---

## 5. Connect the booking calendar

This is the one piece the site cannot do on its own — it needs your booking
platform (Fresha, Square Appointments, Acuity, Setmore, Booksy, Calendly…).

1. Open `site/booking.html` and find the big comment block titled
   `BOOKING CALENDAR AREA`. Full step-by-step instructions are in there.
2. In Setmore, look for the section about adding booking to your own website
   — usually under Settings → *Booking Page*, or *Apps & Integrations*. It
   offers both an embed snippet and a plain link
   (`https://rootsofcare.setmore.com`).
3. Either paste the `<iframe>` code it gives you inside
   `<div id="booking-embed">`, **or** just replace `[[CALENDAR_URL]]` with your
   booking link in the two places it appears on that page.
4. Setmore does not collect the deposit, so the booking page explains the
   e-transfer step instead. If you ever move to a platform that can take the
   $20 at the time of booking, simplify that section to match.

**Until you do this**, the booking page automatically shows a fallback block
with a "Book on our platform" button, an Instagram DM link and your email, so
the page is never broken or empty.

---

## 6. Connect the contact form

The contact form needs a service to deliver the messages (a static site can't
send email by itself). All of these have a free tier and take about two
minutes:

- [Formspree](https://formspree.io)
- [Web3Forms](https://web3forms.com)
- [Basin](https://usebasin.com)

Create a form there, copy the URL it gives you, and in `site/contact.html`
replace `[[FORM_ENDPOINT]]` in the line `action="[[FORM_ENDPOINT]]"`.

Until then, pressing *Send message* shows a polite note with your email and
Instagram instead of failing silently. Remember to add the service name to
`[[FORM SERVICE]]` in the privacy policy.

---

## 7. Replace the photos

Every image slot has an HTML comment right above it, like:

```html
<!-- REPLACE IMAGE: warm studio / atmosphere shot. 1200 x 800 px, landscape. -->
```

To swap one in:

1. Save your photo into `site/assets/img/` (WebP or JPG, and please compress
   it — aim for under 300 KB each; [squoosh.app](https://squoosh.app) is free).
2. Change the `src="…"` to point at your file.
3. Update the `alt="…"` text to describe the photo — it matters for
   accessibility and for Google.
4. Update `width` and `height` to your image's real pixel size, so the page
   doesn't jump while loading.

Sizes used: `1200 × 800` (landscape), `900 × 1200` (portrait),
`960 × 1200` (tall), `1000 × 1000` (square gallery tiles).

---

## 8. Change colours or fonts

All colours live at the very top of `site/assets/css/styles.css`, in the
`:root` block. Change a value there and the whole site follows.

```css
--brand-cream:    #E9E5DC;   /* page background   */
--brand-card:     #F4F1EA;   /* cards, alt sections */
--brand-brown:    #7A5647;   /* headings, buttons */
--brand-taupe:    #AD9686;   /* decorative lines  */
--brand-ink:      #3B322C;   /* body text         */
--brand-offwhite: #FBF9F5;   /* text on brown     */
```

Fonts are set just below, in the same block. They come from Google Fonts —
Josefin Sans (headings), Lato (body) and Parisienne (the script accents). To
swap one, change the `<link>` tags in the `<head>` of each page and the
`--font-*` values.

---

## 9. Before you launch — SEO & housekeeping

- [ ] **Set your real domain.** The files currently reference
      `https://www.rootsofcare.ca`. Search & replace it everywhere (including
      `sitemap.xml` and `robots.txt`) if your domain is different.
- [ ] **Add your phone, email and opening hours to the structured data.**
      Near the bottom of the `<head>` of every page there is a
      `application/ld+json` block with a comment saying exactly what to add.
      This is what makes Google show your hours and click-to-call.
- [ ] **Submit `sitemap.xml`** in [Google Search Console](https://search.google.com/search-console).
- [ ] **Create a Google Business Profile** for the studio and link it to the
      site — for a local business this moves the needle more than anything
      on the site itself.
- [ ] **Add the site link to the Instagram bio.**
- [ ] **Have the legal pages looked over.** The privacy policy and terms were
      written for a small Québec business and cover Law 25 and PIPEDA, but
      they describe the tools *you* end up using, so they need your details
      filled in — and a professional review if anything about your setup is
      unusual.

### One thing to be aware of: French

This site is English only, as requested. Québec's *Charter of the French
Language* generally expects a commercial website aimed at Québec consumers to
be available in French, and at least as prominently as any other language.
It is worth checking whether it applies to you — and the site is already
built to take a French version without rework. See §10.

---

## 10. Optional: the build script

You do **not** need this. `site/` is a finished website you can edit directly.

It exists so the shared parts (header, footer, `<head>` tags, cookie banner)
stay identical across all pages. If you'd rather work that way:

```bash
python3 tools/build.py      # regenerates everything in site/
```

Page content lives in `src/pages/en/*.html`; the shell lives in
`tools/build.py`.

> ⚠️ Running the build **overwrites** `site/`. Pick one way of working: either
> edit `site/` directly and never run the build, or edit `src/` and rebuild.

### Adding a second language later

The builder is already language-aware:

1. Copy `src/pages/en/` to `src/pages/fr/` and translate the content files.
2. In `tools/build.py`, add `"fr"` to `LANGS`, add French slugs to `SLUGS`
   (e.g. `"home": {"en": "index.html", "fr": "fr/index.html"}`), and add a
   `"fr"` block to `LABELS` and `UI`.
3. Uncomment the language-switcher note in the `header()` function and add the
   FR/EN links.

`hreflang` tags, the sitemap and all internal links are generated from that
configuration, so they update themselves.

---

## 11. What's already handled

- **Mobile first** — tested at 375 px, 768 px and 1440 px; no horizontal
  scrolling at any width.
- **Accessibility** — keyboard navigation throughout, visible focus outlines,
  a skip link, labels on every form field, `alt` text on every image, and
  colour contrast at WCAG AA (a few readable brown tones were derived from the
  palette for this; they're documented in the CSS).
- **Motion** — gentle fade-ins only, and they switch off automatically for
  anyone who has "reduce motion" enabled.
- **Cookie banner** — declining is exactly as easy as accepting, and nothing
  non-essential runs before a choice is made. To add analytics later, put the
  snippet inside `loadAnalytics()` in `assets/js/main.js` — it will only ever
  run after consent.
- **SEO** — unique title and description per page, Montréal-focused keywords,
  `HairSalon` structured data, Open Graph and Twitter share cards, canonical
  URLs, `sitemap.xml` and `robots.txt`.
- **Performance** — no frameworks, no trackers, one stylesheet, one script,
  lazy-loaded images with fixed dimensions.

---

Website by Alpha Marketing Studio.
