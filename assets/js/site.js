/* Hamza Ishtiaq — portfolio interactions (no dependencies) */
(function () {
  "use strict";

  var doc = document.documentElement;
  var CAL_LINK = "hamza-ishtiaq-03cjw0/bookacall";
  var CAL_NS = "bookacall";
  var EMAIL = "hamzaishtiaq2491@gmail.com";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  window.__siteReady = true;

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    initHeader();
    initMobileMenu();
    initReveal();
    initCal();
    initWorksIndex();
    initCopy();
    initContactForm();
    initYear();
  });

  /* ---------- Header: solid background once the page scrolls ---------- */
  function initHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var update = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    };
    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  /* ---------- Mobile menu ---------- */
  function initMobileMenu() {
    var toggle = document.querySelector(".menu-toggle");
    var menu = document.getElementById("mobile-menu");
    if (!toggle || !menu) return;

    function setOpen(open) {
      doc.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      if (open) {
        menu.removeAttribute("inert");
        var first = menu.querySelector("a");
        if (first) first.focus({ preventScroll: true });
      } else {
        menu.setAttribute("inert", "");
      }
    }

    toggle.addEventListener("click", function () {
      setOpen(!doc.classList.contains("menu-open"));
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && doc.classList.contains("menu-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 860 && doc.classList.contains("menu-open")) setOpen(false);
    });
  }

  /* ---------- Reveal on scroll ---------- */
  function initReveal() {
    var items = [].slice.call(document.querySelectorAll("[data-reveal]"));
    if (!items.length) return;
    if (reduceMotion || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Cal.com booking modal ----------
     Links keep their real cal.com href, so they still work without JS.
     The embed script only loads the first time someone shows intent. */
  function initCal() {
    var triggers = document.querySelectorAll("[data-cal]");
    if (!triggers.length) return;
    var initialised = false;

    function loadCal() {
      if (initialised) return;
      initialised = true;
      (function (C, A, L) {
        var p = function (a, ar) { a.q.push(ar); };
        var d = C.document;
        C.Cal = C.Cal || function () {
          var cal = C.Cal, ar = arguments;
          if (!cal.loaded) {
            cal.ns = {}; cal.q = cal.q || [];
            d.head.appendChild(d.createElement("script")).src = A;
            cal.loaded = true;
          }
          if (ar[0] === L) {
            var api = function () { p(api, arguments); };
            var namespace = ar[1];
            api.q = api.q || [];
            if (typeof namespace === "string") {
              cal.ns[namespace] = cal.ns[namespace] || api;
              p(cal.ns[namespace], ar);
              p(cal, ["initNamespace", namespace]);
            } else p(cal, ar);
            return;
          }
          p(cal, ar);
        };
      })(window, "https://app.cal.com/embed/embed.js", "init");
      window.Cal("init", CAL_NS, { origin: "https://app.cal.com" });
      window.Cal.ns[CAL_NS]("ui", {
        theme: "dark",
        styles: { branding: { brandColor: "#111111" } },
        hideEventTypeDetails: false,
        layout: "month_view"
      });
    }

    [].forEach.call(triggers, function (el) {
      el.addEventListener("pointerenter", loadCal, { once: true });
      el.addEventListener("focus", loadCal, { once: true });
      el.addEventListener("touchstart", loadCal, { once: true, passive: true });
      el.addEventListener("click", function (e) {
        // Let people open the booking page in a new tab if they want to.
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return;
        e.preventDefault();
        loadCal();
        window.Cal.ns[CAL_NS]("modal", {
          calLink: CAL_LINK,
          config: { layout: "month_view", theme: "dark" }
        });
      });
    });
  }

  /* ---------- Works index: filters + floating preview ---------- */
  function initWorksIndex() {
    var list = document.querySelector(".index-list");
    if (!list) return;
    var rows = [].slice.call(list.querySelectorAll(".index-row"));

    // Filters
    var buttons = [].slice.call(document.querySelectorAll(".filter-btn"));
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var filter = btn.getAttribute("data-filter");
        buttons.forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
        rows.forEach(function (row) {
          var cats = (row.getAttribute("data-category") || "").split(" ");
          row.hidden = !(filter === "all" || cats.indexOf(filter) !== -1);
        });
      });
    });

    // Floating preview that follows the cursor (desktop only)
    var preview = document.querySelector(".hover-preview");
    if (!preview || !window.matchMedia("(hover: hover) and (min-width: 861px)").matches) return;
    var img = preview.querySelector("img");
    var url = preview.querySelector(".browser__url span");
    var x = 0, y = 0, cx = 0, cy = 0, raf = null, active = false;

    function loop() {
      cx += (x - cx) * (reduceMotion ? 1 : 0.16);
      cy += (y - cy) * (reduceMotion ? 1 : 0.16);
      // Sit just right of the cursor so the project name stays readable; flip left near the edge.
      var w = preview.offsetWidth || 380;
      var left = cx + 36 + w > window.innerWidth - 16 ? cx - 36 - w : cx + 36;
      preview.style.transform = "translate3d(" + left + "px," + (cy - 130) + "px,0)";
      if (active || Math.abs(x - cx) > 0.5 || Math.abs(y - cy) > 0.5) raf = requestAnimationFrame(loop);
      else raf = null;
    }

    rows.forEach(function (row) {
      row.addEventListener("mouseenter", function (e) {
        var src = row.getAttribute("data-preview");
        if (src && img.getAttribute("src") !== src) img.setAttribute("src", src);
        if (url) url.textContent = row.getAttribute("data-domain") || "";
        if (!active) { cx = x = e.clientX; cy = y = e.clientY; }
        active = true;
        preview.classList.add("is-active");
        if (!raf) raf = requestAnimationFrame(loop);
      });
      row.addEventListener("mouseleave", function () {
        active = false;
        preview.classList.remove("is-active");
      });
    });
    list.addEventListener("mousemove", function (e) {
      x = e.clientX;
      y = e.clientY;
      if (!raf) raf = requestAnimationFrame(loop);
    });
    // Preload preview images so the swap is instant
    rows.forEach(function (row) {
      var src = row.getAttribute("data-preview");
      if (src) { var i = new Image(); i.src = src; }
    });
  }

  /* ---------- Copy email ---------- */
  function initCopy() {
    [].forEach.call(document.querySelectorAll("[data-copy]"), function (btn) {
      btn.addEventListener("click", function () {
        var text = btn.getAttribute("data-copy");
        var label = btn.querySelector("span");
        var done = function () {
          if (!label) return;
          var original = label.textContent;
          label.textContent = "Copied!";
          setTimeout(function () { label.textContent = original; }, 1800);
        };
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
        } else {
          fallbackCopy(text);
          done();
        }
      });
    });
  }
  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) { /* ignore */ }
    document.body.removeChild(ta);
  }

  /* ---------- Contact form (FormSubmit AJAX) ---------- */
  function initContactForm() {
    var form = document.getElementById("contact-form");
    if (!form) return;
    // With JS we show friendlier inline messages; without JS the browser's own checks still apply.
    form.noValidate = true;
    var status = document.getElementById("form-status");
    var submit = form.querySelector('button[type="submit"]');
    var submitLabel = submit ? submit.innerHTML : "";

    // Arriving back from the no-JS fallback redirect
    if (/[?&]sent=1/.test(window.location.search)) {
      showStatus("success", "<strong>Thanks — your message is on its way!</strong> I'll get back to you soon.");
    }

    function showStatus(type, html) {
      if (!status) return;
      status.className = "form-status form-status--" + type + " is-visible";
      var icon = type === "success"
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
        : type === "error"
          ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>'
          : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>';
      status.innerHTML = icon + "<div>" + html + "</div>";
    }

    function mailtoLink(data) {
      var body = data.message + "\n\n— " + data.name + " (" + data.email + ")" + (data.service ? "\nProject type: " + data.service : "");
      return "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Project inquiry from " + data.name) + "&body=" + encodeURIComponent(body);
    }

    function setBusy(busy) {
      if (!submit) return;
      submit.disabled = busy;
      submit.innerHTML = busy ? '<span class="spinner" aria-hidden="true"></span> Sending…' : submitLabel;
    }

    function markInvalid(field, invalid) {
      if (field) field.setAttribute("aria-invalid", String(invalid));
    }

    form.addEventListener("input", function (e) {
      if (e.target.getAttribute("aria-invalid") === "true") markInvalid(e.target, false);
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var nameEl = form.elements.namedItem("name");
      var emailEl = form.elements.namedItem("email");
      var msgEl = form.elements.namedItem("message");
      var serviceEl = form.querySelector('input[name="service"]:checked');
      var honey = form.elements.namedItem("_honey");

      var data = {
        name: nameEl.value.trim(),
        email: emailEl.value.trim(),
        message: msgEl.value.trim(),
        service: serviceEl ? serviceEl.value : ""
      };

      // Validate
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email);
      markInvalid(nameEl, !data.name);
      markInvalid(emailEl, !emailOk);
      markInvalid(msgEl, !data.message);
      if (!data.name) { nameEl.focus(); showStatus("error", "Please tell me your name."); return; }
      if (!emailOk) { emailEl.focus(); showStatus("error", "Please enter a valid email address so I can reply."); return; }
      if (!data.message) { msgEl.focus(); showStatus("error", "Please add a short message about your project."); return; }

      // Bots fill the hidden field — pretend it worked and do nothing.
      if (honey && honey.value) {
        showStatus("success", "<strong>Thanks — your message is on its way!</strong>");
        form.reset();
        return;
      }

      setBusy(true);
      showStatus("info", "Sending your message…");

      var controller = "AbortController" in window ? new AbortController() : null;
      var timer = setTimeout(function () { if (controller) controller.abort(); }, 15000);

      fetch("https://formsubmit.co/ajax/" + EMAIL, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          name: data.name,
          email: data.email,
          "project type": data.service || "Not specified",
          message: data.message,
          _subject: "New project inquiry from " + data.name,
          _template: "table",
          _captcha: "false",
          _autoresponse: "Thanks for reaching out! I've received your message and will get back to you soon. — Hamza"
        }),
        signal: controller ? controller.signal : undefined
      })
        .then(function (res) {
          return res.json().catch(function () { return {}; }).then(function (json) {
            return { ok: res.ok, json: json };
          });
        })
        .then(function (result) {
          clearTimeout(timer);
          var success = result.ok && String(result.json.success) === "true";
          if (!success) throw new Error(result.json.message || "Request failed");
          form.reset();
          showStatus("success", "<strong>Thanks, " + escapeHtml(data.name.split(" ")[0]) + " — your message is on its way!</strong> I'll get back to you soon. Keep an eye on your inbox.");
        })
        .catch(function () {
          clearTimeout(timer);
          showStatus(
            "error",
            "<strong>Sorry, your message didn't send.</strong> Please <a href=\"" + mailtoLink(data) + "\">email me directly</a> at " + EMAIL + " — your message is already filled in."
          );
        })
        .then(function () { setBusy(false); });
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- Footer year ---------- */
  function initYear() {
    var y = String(new Date().getFullYear());
    [].forEach.call(document.querySelectorAll("[data-year]"), function (el) { el.textContent = y; });
  }
})();
