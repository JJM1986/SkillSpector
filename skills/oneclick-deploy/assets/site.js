/* Offline widgets for oneclick-deploy scaffolds. Expects window.SITE. */
(function () {
  var SITE = window.SITE || { trade: "Fachbetrieb", faq: {}, rates: { hourly: 65, per_km: 0.8 } };

  function show(el, text) {
    if (!el) return;
    el.hidden = false;
    el.textContent = text;
  }

  var lead = document.getElementById("lead-form");
  if (lead) {
    lead.addEventListener("submit", function (event) {
      event.preventDefault();
      var name = event.target.name.value.trim();
      show(
        document.getElementById("lead-status"),
        "Danke " + name + ", Ihre Anfrage an " + SITE.trade + " wurde lokal vorgemerkt (kein Versand)."
      );
      event.target.reset();
    });
  }

  var booking = document.getElementById("booking-form");
  if (booking) {
    booking.addEventListener("submit", function (event) {
      event.preventDefault();
      var form = event.target;
      var entry = {
        date: form.date.value,
        slot: form.slot.value,
        name: form.name.value.trim(),
      };
      try {
        var key = "oneclick-booking:" + SITE.trade;
        var existing = JSON.parse(localStorage.getItem(key) || "[]");
        existing.push(entry);
        localStorage.setItem(key, JSON.stringify(existing));
      } catch (err) {
        /* ignore */
      }
      show(
        document.getElementById("booking-status"),
        "Termin vorgemerkt: " + entry.date + " um " + entry.slot + " für " + entry.name + "."
      );
      form.reset();
    });
  }

  var quote = document.getElementById("quote-form");
  if (quote) {
    quote.addEventListener("submit", function (event) {
      event.preventDefault();
      var form = event.target;
      var hours = Number(form.hours.value) || 0;
      var km = Number(form.km.value) || 0;
      var rates = SITE.rates || { hourly: 65, per_km: 0.8 };
      var total = hours * rates.hourly + km * rates.per_km;
      var result = document.getElementById("quote-result");
      if (result) {
        result.textContent =
          "Orientierung: ca. " + total.toFixed(0) + " € (netto, unverbindlich) für " + SITE.trade + ".";
      }
    });
  }

  var material = document.getElementById("material-form");
  if (material) {
    material.addEventListener("submit", function (event) {
      event.preventDefault();
      var form = event.target;
      var sqm = Number(form.sqm.value) || 0;
      var coats = Number(form.coats.value) || 1;
      var liters = Math.ceil((sqm * coats) / 10);
      var result = document.getElementById("material-result");
      if (result) {
        result.textContent = "Geschätzt ca. " + liters + " Liter Farbe.";
      }
    });
  }

  function hasToken(text, tokens) {
    for (var i = 0; i < tokens.length; i++) {
      if (text.indexOf(tokens[i]) >= 0) return true;
    }
    return false;
  }

  var faq = document.getElementById("faq-form");
  if (faq) {
    faq.addEventListener("submit", function (event) {
      event.preventDefault();
      var q = String(event.target.q.value || "").toLowerCase();
      var hints = SITE.faq || {};
      var answer = hints.default || "Bitte nutzen Sie das Kontaktformular.";
      // Prefer specific emergency tokens; bare "not" matches unrelated German stems.
      if (hasToken(q, ["notdienst", "notfall", "24h", "dringend"])) {
        answer = hints.notdienst || answer;
      } else if (hasToken(q, ["preis", "kost"])) {
        answer = hints.preis || answer;
      } else if (hasToken(q, ["termin", "buch"])) {
        answer = hints.termin || answer;
      }
      var box = document.getElementById("faq-answer");
      if (box) box.textContent = answer;
    });
  }
})();
