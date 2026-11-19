// Basilica Holiday Home concept demo. Forms are disabled: they show what the live site would do.
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function iso(d) {
    var m = d.getMonth() + 1, day = d.getDate();
    return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
  }
  function parse(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  var fmt = { weekday: "short", day: "numeric", month: "short" };
  function nice(d) { return d.toLocaleDateString("en-IN", fmt); }

  var today = new Date(); today.setHours(0, 0, 0, 0);
  var cin = $("#checkin"), cout = $("#checkout"), nights = $("#nights");

  // Friday to Sunday of this (or next) weekend
  function weekend(offset) {
    var d = new Date(today), dow = d.getDay();
    var toFri = (5 - dow + 7) % 7;
    if (dow === 6) toFri = -1; // already Saturday: start today
    if (dow === 0) toFri = 5; // Sunday: next Friday
    var fri = addDays(d, toFri + offset * 7);
    if (fri < today) fri = today;
    return [fri, addDays(fri, fri.getDay() === 6 ? 1 : 2)];
  }

  function setDates(a, b) { cin.value = iso(a); cout.value = iso(b); update(); }

  function update() {
    cin.min = iso(today);
    if (!cin.value) return;
    var a = parse(cin.value);
    cout.min = iso(addDays(a, 1));
    if (!cout.value || parse(cout.value) <= a) cout.value = iso(addDays(a, 1));
    var b = parse(cout.value);
    var n = Math.round((b - a) / 864e5);
    nights.textContent = nice(a) + " to " + nice(b) + " · " + n + (n === 1 ? " night" : " nights");
    $$(".chip").forEach(function (c) {
      var w = weekend(+c.dataset.weekend);
      c.setAttribute("aria-pressed", String(iso(w[0]) === cin.value && iso(w[1]) === cout.value));
    });
  }

  if (cin && cout) {
    var w0 = weekend(0); setDates(w0[0], w0[1]);
    cin.addEventListener("change", update);
    cout.addEventListener("change", update);
    $$(".chip").forEach(function (c) {
      c.addEventListener("click", function () { var w = weekend(+c.dataset.weekend); setDates(w[0], w[1]); });
    });
  }

  // "Check dates" on a room card picks that stay type
  var type = $("#room-type");
  $$("[data-room]").forEach(function (a) {
    a.addEventListener("click", function () {
      if (type) type.value = a.dataset.room;
      var rooms = $("#rooms-n");
      if (rooms && /br$/.test(a.dataset.room)) rooms.value = "bungalow";
      setTimeout(function () { cin && cin.focus({ preventScroll: true }); }, 450);
    });
  });

  // Demo dialog
  var dlg = $("#demo"), body = $("#demo-body");
  function show(title, text) {
    $("#demo-title").textContent = title;
    body.textContent = text;
    if (dlg && typeof dlg.showModal === "function") dlg.showModal();
    else alert(text);
  }

  var book = $("#book");
  if (book) book.addEventListener("submit", function (e) {
    e.preventDefault();
    var g = $("#guests"), r = $("#rooms-n");
    var a = parse(cin.value), b = parse(cout.value);
    var n = Math.round((b - a) / 864e5);
    show("Your dates, ready for the front desk",
      nice(a) + " to " + nice(b) + " (" + n + (n === 1 ? " night" : " nights") + "), " +
      g.options[g.selectedIndex].text + ", " + r.options[r.selectedIndex].text.toLowerCase() + ", " +
      type.options[type.selectedIndex].text.toLowerCase() + ". " +
      "On the live site you would now see which rooms and bungalows are free with the direct rate, " +
      "pay a deposit or hold the room, and get a WhatsApp confirmation from Basilica. No app commission is charged.");
  });

  // Event enquiry: suggest the space that fits the headcount
  var eg = $("#ev-guests"), fit = $("#ev-fit"), es = $("#ev-space");
  function suggest() {
    var n = parseInt(eg.value, 10);
    if (!n || n < 1) { fit.textContent = ""; return; }
    var s = n <= 70 ? "Orchid (seats 70)" : n <= 200 ? "Tulip (seats 200)" : n <= 400 ? "the Basilica hall (seats 400)" :
      n <= 1000 ? "the Lawn (seats 700, 1,000 standing)" : null;
    fit.textContent = s ? "For " + n + " guests, " + s + " fits best." : "More than 1,000 guests? Talk to us about the Lawn plus a hall.";
  }
  if (eg) { eg.addEventListener("input", suggest); suggest(); }
  var evd = $("#ev-date"); if (evd) evd.min = iso(today);

  var enq = $("#enquiry");
  if (enq) enq.addEventListener("submit", function (e) {
    e.preventDefault();
    var t = $("#ev-type").value, sp = es.value || "a space that fits";
    var when = evd.value ? nice(parse(evd.value)) : "your date";
    show("Your event enquiry",
      t + " for " + (eg.value || "your") + " guests on " + when + ", in " + sp + ". " +
      "On the live site this goes straight to the events team, who check the date and send back package options " +
      "(veg from ₹400 and non-veg from ₹550 a plate) on WhatsApp.");
  });

  // Map loads only on request (no Google requests on page load)
  var ml = $("#map-load");
  if (ml) ml.addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = "https://maps.google.com/maps?q=18.749394,73.392601&z=15&output=embed";
    f.title = "Map showing Basilica Holiday Home in Raiwood, Lonavala";
    f.loading = "lazy";
    f.referrerPolicy = "strict-origin-when-cross-origin";
    var m = $("#map"); m.innerHTML = ""; m.appendChild(f);
  });
})();
