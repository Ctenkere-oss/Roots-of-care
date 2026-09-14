/* =============================================================
   ROOTS OF CARE — site scripts
   Vanilla JavaScript, no dependencies. Loaded with "defer".
   Every block is independent: if an element is not present on
   the page, that block simply does nothing.
   ============================================================= */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------
     1) STICKY HEADER — shrinks slightly on scroll
     --------------------------------------------------------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------------------------------------------------
     2) FULL-SCREEN MOBILE MENU
     --------------------------------------------------------- */
  var toggle = document.querySelector(".nav-toggle");
  var mobileNav = document.getElementById("nav-mobile");

  function closeMenu() {
    if (!toggle || !mobileNav) return;
    toggle.setAttribute("aria-expanded", "false");
    mobileNav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
  }

  if (toggle && mobileNav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      mobileNav.classList.toggle("is-open", !open);
      document.body.classList.toggle("nav-open", !open);
      if (!open) {
        var first = mobileNav.querySelector("a, button");
        if (first) first.focus();
      }
    });

    // Escape closes the menu
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        closeMenu();
        toggle.focus();
      }
    });

    // Clicking any link closes the menu
    mobileNav.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeMenu();
    });

    // Back to desktop width: close it
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1000) closeMenu();
    });
  }

  /* ---------------------------------------------------------
     3) SOFT FADE-IN ON SCROLL
     (disabled when the visitor asks for reduced motion)
     --------------------------------------------------------- */
  var revealables = document.querySelectorAll(".reveal");
  if (revealables.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(revealables, function (el) {
        el.classList.add("is-visible");
      });
    } else {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              io.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
      );
      Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });
    }
  }

  /* ---------------------------------------------------------
     4) SERVICES PAGE CATEGORY FILTERS
     --------------------------------------------------------- */
  var filterBar = document.querySelector("[data-filters]");
  if (filterBar) {
    var buttons = filterBar.querySelectorAll(".filter-btn");
    var items = document.querySelectorAll("[data-category]");
    var groups = document.querySelectorAll("[data-group]");

    filterBar.addEventListener("click", function (e) {
      var btn = e.target.closest(".filter-btn");
      if (!btn) return;
      var filter = btn.getAttribute("data-filter");

      Array.prototype.forEach.call(buttons, function (b) {
        b.setAttribute("aria-pressed", String(b === btn));
      });

      Array.prototype.forEach.call(items, function (item) {
        var match = filter === "all" || item.getAttribute("data-category") === filter;
        item.hidden = !match;
      });

      // Hide any category block that has become empty
      Array.prototype.forEach.call(groups, function (group) {
        var visible = group.querySelectorAll("[data-category]:not([hidden])").length;
        group.hidden = visible === 0;
      });
    });
  }

  /* ---------------------------------------------------------
     5) BOOKING PAGE — calendar embed or fallback
     The fallback block is visible by default, so the page still
     works with JavaScript disabled. As soon as a real calendar
     embed is pasted into #booking-embed (an <iframe> with a src
     that no longer contains "[["), the embed is shown instead.
     --------------------------------------------------------- */
  var embed = document.getElementById("booking-embed");
  var fallback = document.getElementById("booking-fallback");
  if (embed && fallback) {
    var iframe = embed.querySelector("iframe");
    var src = iframe ? (iframe.getAttribute("src") || "") : "";
    var configured = !!iframe && src !== "" &&
                     src.indexOf("[[") === -1 &&
                     src.indexOf("about:blank") !== 0;

    var showFallback = function () {
      embed.hidden = true;
      fallback.hidden = false;
    };

    if (configured) {
      embed.hidden = false;
      fallback.hidden = true;

      var loaded = false;
      iframe.addEventListener("load", function () { loaded = true; });
      iframe.addEventListener("error", showFallback);
      // Safety net: if the calendar never loads, go back to the fallback.
      window.setTimeout(function () { if (!loaded) showFallback(); }, 8000);
    } else {
      showFallback();
    }
  }

  /* ---------------------------------------------------------
     6) CONTACT FORM
     While no form service is connected (the action attribute
     still contains "[["), we block the submission and show
     the instructions plus the email fallback.
     --------------------------------------------------------- */
  var form = document.querySelector("[data-contact-form]");
  if (form) {
    form.addEventListener("submit", function (e) {
      var action = form.getAttribute("action") || "";
      if (action === "" || action.indexOf("[[") !== -1) {
        e.preventDefault();
        var note = form.querySelector("[data-form-note]");
        if (note) {
          note.hidden = false;
          note.setAttribute("role", "status");
          note.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        }
      }
    });
  }

  /* ---------------------------------------------------------
     7) COOKIE BANNER — Québec Law 25 / PIPEDA friendly
     No non-essential cookie is dropped before a choice is made.
     Declining is exactly as easy as accepting (same button,
     same visual weight). The choice is kept for 6 months.
     TO CONNECT AN ANALYTICS TOOL (e.g. Google Analytics):
     put its code inside loadAnalytics() below. It will only
     ever run after an explicit consent.
     --------------------------------------------------------- */
  var KEY = "roc-consent";
  var banner = document.getElementById("cookie-banner");

  function loadAnalytics() {
    /* <-- PASTE the analytics snippet here (optional).
       Example:
       var s = document.createElement("script");
       s.src = "https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX";
       s.async = true;
       document.head.appendChild(s);
    */
  }

  function readConsent() {
    try {
      var raw = window.localStorage.getItem(KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      // Consent expires after 6 months, so the choice is renewed
      if (!data.ts || Date.now() - data.ts > 1000 * 60 * 60 * 24 * 183) return null;
      return data.value;
    } catch (err) { return null; }
  }

  function writeConsent(value) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify({ value: value, ts: Date.now() }));
    } catch (err) { /* private browsing: ignore */ }
  }

  if (banner) {
    var choice = readConsent();
    if (choice === null) {
      banner.classList.add("is-visible");
    } else if (choice === "accepted") {
      loadAnalytics();
    }

    banner.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-consent]");
      if (!btn) return;
      var value = btn.getAttribute("data-consent");
      writeConsent(value);
      banner.classList.remove("is-visible");
      if (value === "accepted") loadAnalytics();
    });
  }

  // Lets the privacy page reopen the banner so a visitor can change their mind
  var reopen = document.querySelector("[data-consent-reopen]");
  if (reopen && banner) {
    reopen.addEventListener("click", function (e) {
      e.preventDefault();
      try { window.localStorage.removeItem(KEY); } catch (err) {}
      banner.classList.add("is-visible");
      banner.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
    });
  }

  /* ---------------------------------------------------------
     8) CURRENT YEAR IN THE FOOTER
     --------------------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
