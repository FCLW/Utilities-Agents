/* Minimal SVG charting for the WeatherNext demo.
   No external libraries: nothing to fail to load in front of a customer.

   Conventions follow the dataviz method -- thin marks, hairline recessive
   grid, a 2px surface gap between stacked fills, legend always present for
   >= 2 series, crosshair + tooltip on every time series, and a table-view
   twin rendered by app.js for each chart. */
(function (global) {
  "use strict";

  const NS = "http://www.w3.org/2000/svg";
  // Set from the selected country's dominant zone; a US fleet must not be
  // labelled in Lisbon time.
  let TZ = "UTC";
  let TZ_LABEL = "UTC";
  let dayFmt, dayTimeFmt, weekdayFmt;

  // "Europe/Lisbon" -> "Lisbon", "America/New_York" -> "New York". Used in the
  // table-view column headers so they track the selected country.
  function tzLabel() { return TZ_LABEL; }

  function setTimeZone(tz) {
    TZ = tz || "UTC";
    TZ_LABEL = TZ.split("/").pop().replace(/_/g, " ");
    dayFmt = new Intl.DateTimeFormat("en-GB",
      { day: "numeric", month: "short", timeZone: TZ });
    dayTimeFmt = new Intl.DateTimeFormat("en-GB",
      { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit",
        hour12: false, timeZone: TZ });
    weekdayFmt = new Intl.DateTimeFormat("en-GB", { weekday: "short", timeZone: TZ });
  }
  setTimeZone("UTC");

  function el(name, attrs) {
    const n = document.createElementNS(NS, name);
    if (attrs) for (const k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  function css(name) {
    return getComputedStyle(document.body).getPropertyValue(name).trim();
  }

  // ---------------------------------------------------------------- scales
  function linear(d0, d1, r0, r1) {
    const span = d1 - d0 || 1;
    const f = (v) => r0 + ((v - d0) / span) * (r1 - r0);
    f.invert = (p) => d0 + ((p - r0) / (r1 - r0 || 1)) * span;
    return f;
  }

  function niceTicks(min, max, count) {
    if (max === min) max = min + 1;
    const raw = (max - min) / Math.max(1, count);
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const norm = raw / mag;
    const step = (norm >= 7.5 ? 10 : norm >= 3.5 ? 5 : norm >= 1.5 ? 2 : 1) * mag;
    const out = [];
    // Extend to the first tick at or above max: the axis domain is the last
    // tick, so stopping below max would clip the tallest mark off the plot.
    for (let v = Math.ceil(min / step) * step; ; v += step) {
      out.push(Math.abs(v) < step * 1e-6 ? 0 : v);
      if (v >= max - step * 1e-6) break;
      if (out.length > 200) break;
    }
    return out;
  }

  // ------------------------------------------------------------ formatting
  const fmtNum = (v, d) =>
    v == null || Number.isNaN(v)
      ? "—"
      : v.toLocaleString("en-GB", { minimumFractionDigits: d ?? 0, maximumFractionDigits: d ?? 0 });


  // ---------------------------------------------------------------- tooltip
  const tip = () => document.getElementById("tooltip");

  function showTip(html, ev) {
    const t = tip();
    // Belt and braces alongside the fullscreenchange handler below: if the
    // page is fullscreen and the tooltip is not inside that subtree, it would
    // simply not be painted. Check at the moment it matters.
    const fs = document.fullscreenElement || document.webkitFullscreenElement;
    if (fs && !fs.contains(t)) fs.appendChild(t);
    t.innerHTML = html;
    t.hidden = false;
    const pad = 14, w = t.offsetWidth, h = t.offsetHeight;
    let x = ev.clientX + pad, y = ev.clientY + pad;
    if (x + w > innerWidth - 8) x = ev.clientX - w - pad;
    if (y + h > innerHeight - 8) y = ev.clientY - h - pad;
    t.style.left = Math.max(8, x) + "px";
    t.style.top = Math.max(8, y) + "px";
  }
  function hideTip() { const t = tip(); if (t) t.hidden = true; }

  /* The map's fullscreen control moves the map into the browser's fullscreen
     element, and nothing outside that subtree is painted any more -- including
     this tooltip, which lives on <body>. Re-parent it on the way in and put it
     back on the way out, or hovering a marker in fullscreen shows nothing.
     It is position:fixed, and a fullscreen element fills the viewport, so the
     clientX/clientY placement still lines up. */
  ["fullscreenchange", "webkitfullscreenchange"].forEach((evt) =>
    document.addEventListener(evt, () => {
      const t = tip();
      if (!t) return;
      hideTip();
      (document.fullscreenElement || document.webkitFullscreenElement ||
       document.body).appendChild(t);
    }));

  function tipRows(title, rows) {
    return (
      `<div class="tt-title">${title}</div>` +
      rows.map((r) =>
        `<div class="tt-row"><span class="tt-key">` +
        (r.color ? `<span class="legend-swatch" style="background:${r.color}"></span>` : "") +
        `${r.label}</span><span class="tt-val">${r.value}</span></div>`
      ).join("")
    );
  }

  /* Width of a string as it will actually be drawn.

     A shared canvas context, because the alternative -- guessing a per-character
     width -- is what produced the bug this exists to fix: the y axis had a fixed
     54px left margin, which fits "1,400 MW" and clips "38,538 MW". A fleet of a
     few hundred MW was fine and a national fleet was not, so the axis silently
     lost its labels exactly when the numbers got interesting. */
  let _measureCtx = null;

  function textWidth(str, size, family) {
    try {
      if (!_measureCtx) {
        _measureCtx = document.createElement("canvas").getContext("2d");
      }
      _measureCtx.font = size + "px " + (family || "sans-serif");
      return _measureCtx.measureText(String(str)).width;
    } catch (e) {
      // No canvas (a very old browser, or a hostile sandbox): fall back to a
      // conservative estimate rather than losing the axis entirely.
      return String(str).length * size * 0.62;
    }
  }

  /* Left margin wide enough for every label this axis will draw.

     Call it BEFORE frame(), because the x scale is derived from the margin and
     cannot be corrected afterwards. 9px of it is the gap yAxis leaves between
     the label and the plot; 4px keeps the longest label off the very edge. */
  function axisLeft(ticks, fmt, min) {
    const f = css("--font") || "sans-serif";
    let widest = 0;
    (ticks || []).forEach((t) => {
      const s = fmt ? fmt(t) : fmtNum(t);
      widest = Math.max(widest, textWidth(s, 10.5, f));
    });
    return Math.max(min == null ? 54 : min, Math.ceil(widest) + 9 + 4);
  }

  // ------------------------------------------------------------ chart frame
  function frame(host, height, margin) {
    const width = Math.max(320, host.clientWidth || 720);
    host.textContent = "";
    const svg = el("svg", {
      width, height, viewBox: `0 0 ${width} ${height}`, role: "img",
    });
    host.appendChild(svg);
    const m = Object.assign({ top: 14, right: 18, bottom: 30, left: 54 }, margin);
    return {
      svg, width, height, m,
      iw: width - m.left - m.right,
      ih: height - m.top - m.bottom,
    };
  }

  function yAxis(f, y, ticks, fmt) {
    const g = el("g");
    ticks.forEach((t) => {
      const py = y(t);
      g.appendChild(el("line", {
        x1: f.m.left, x2: f.m.left + f.iw, y1: py, y2: py,
        stroke: css("--grid"), "stroke-width": 1, "shape-rendering": "crispEdges",
      }));
      const lb = el("text", {
        x: f.m.left - 9, y: py + 3.5, "text-anchor": "end",
        fill: css("--muted"), "font-size": 10.5, "font-family": css("--font"),
      });
      lb.textContent = fmt ? fmt(t) : fmtNum(t);
      g.appendChild(lb);
    });
    f.svg.appendChild(g);
  }

  function xTimeAxis(f, x, t0, t1, everyDays) {
    const g = el("g");
    const d = new Date(t0);
    d.setUTCHours(0, 0, 0, 0);
    for (let cur = d.getTime(); cur <= t1; cur += 86400000 * everyDays) {
      if (cur < t0) continue;
      const px = x(cur);
      g.appendChild(el("line", {
        x1: px, x2: px, y1: f.m.top, y2: f.m.top + f.ih,
        stroke: css("--grid"), "stroke-width": 1, "shape-rendering": "crispEdges",
      }));
      const lb = el("text", {
        x: px, y: f.m.top + f.ih + 16, "text-anchor": "middle",
        fill: css("--muted"), "font-size": 10.5, "font-family": css("--font"),
      });
      lb.textContent = dayFmt.format(new Date(cur));
      g.appendChild(lb);
    }
    g.appendChild(el("line", {
      x1: f.m.left, x2: f.m.left + f.iw, y1: f.m.top + f.ih, y2: f.m.top + f.ih,
      stroke: css("--axis"), "stroke-width": 1, "shape-rendering": "crispEdges",
    }));
    f.svg.appendChild(g);
  }

  /* Numeric x axis, for charts whose x is a quantity rather than a date. */
  function xNumAxis(f, x, v0, v1, fmt, label) {
    const g = el("g");
    niceTicks(v0, v1, 8).filter((t) => t >= v0 && t <= v1).forEach((t) => {
      const px = x(t);
      g.appendChild(el("line", {
        x1: px, x2: px, y1: f.m.top, y2: f.m.top + f.ih,
        stroke: css("--grid"), "stroke-width": 1, "shape-rendering": "crispEdges",
      }));
      const lb = el("text", {
        x: px, y: f.m.top + f.ih + 16, "text-anchor": "middle",
        fill: css("--muted"), "font-size": 10.5, "font-family": css("--font"),
      });
      lb.textContent = fmt ? fmt(t) : fmtNum(t);
      g.appendChild(lb);
    });
    g.appendChild(el("line", {
      x1: f.m.left, x2: f.m.left + f.iw, y1: f.m.top + f.ih, y2: f.m.top + f.ih,
      stroke: css("--axis"), "stroke-width": 1, "shape-rendering": "crispEdges",
    }));
    if (label) {
      const t = el("text", {
        x: f.m.left + f.iw / 2, y: f.m.top + f.ih + 30, "text-anchor": "middle",
        fill: css("--muted"), "font-size": 10.5, "font-family": css("--font"),
      });
      t.textContent = label;
      g.appendChild(t);
    }
    f.svg.appendChild(g);
  }

  function pathFrom(pts) {
    return pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(2) + " " + p[1].toFixed(2)).join(" ");
  }

  /* Crosshair layer shared by the time-series charts. `onIndex` returns the
     tooltip HTML for the hovered index; the hit area spans the whole plot so
     the target is never pinpoint. */
  function crosshair(f, x, times, onIndex, marks) {
    const line = el("line", {
      y1: f.m.top, y2: f.m.top + f.ih, stroke: css("--axis"),
      "stroke-width": 1, "shape-rendering": "crispEdges", opacity: 0,
    });
    f.svg.appendChild(line);
    const dots = el("g", { opacity: 0 });
    f.svg.appendChild(dots);

    const hit = el("rect", {
      x: f.m.left, y: f.m.top, width: f.iw, height: f.ih, fill: "transparent",
    });
    f.svg.appendChild(hit);

    function nearest(ev) {
      const r = f.svg.getBoundingClientRect();
      const px = ((ev.clientX - r.left) / r.width) * f.width;
      const t = x.invert(px);
      let lo = 0, hi = times.length - 1;
      while (lo < hi) {
        const mid = (lo + hi) >> 1;
        if (times[mid] < t) lo = mid + 1; else hi = mid;
      }
      if (lo > 0 && Math.abs(times[lo - 1] - t) < Math.abs(times[lo] - t)) lo--;
      return lo;
    }

    hit.addEventListener("mousemove", (ev) => {
      const i = nearest(ev);
      const px = x(times[i]);
      line.setAttribute("x1", px); line.setAttribute("x2", px);
      line.setAttribute("opacity", 1);
      dots.textContent = "";
      (marks ? marks(i) : []).forEach((mk) => {
        dots.appendChild(el("circle", {
          cx: px, cy: mk.y, r: 4, fill: mk.color,
          stroke: css("--surface-1"), "stroke-width": 2,
        }));
      });
      dots.setAttribute("opacity", 1);
      showTip(onIndex(i), ev);
    });
    hit.addEventListener("mouseleave", () => {
      line.setAttribute("opacity", 0);
      dots.setAttribute("opacity", 0);
      hideTip();
    });
  }

  // ------------------------------------------------------- 1. stacked area
  /* rows: [{t:ms, a:Number, b:Number}], a stacked below b. */
  function stackedArea(host, rows, opt) {
    if (!rows.length) { frame(host, opt.height || 300); return; }
    // Ticks before the frame: the left margin is sized from the labels, and the
    // x scale is derived from that margin.
    const times = rows.map((r) => r.t);
    const maxY = Math.max(1, ...rows.map((r) => r.a + r.b));
    const ticks = niceTicks(0, maxY, 5);
    const f = frame(host, opt.height || 300, { left: axisLeft(ticks) });
    const x = linear(times[0], times[times.length - 1], f.m.left, f.m.left + f.iw);
    const y = linear(0, ticks[ticks.length - 1], f.m.top + f.ih, f.m.top);

    yAxis(f, y, ticks);
    xTimeAxis(f, x, times[0], times[times.length - 1], opt.everyDays || 2);

    const base = rows.map((r) => [x(r.t), y(0)]).reverse();
    const lowTop = rows.map((r) => [x(r.t), y(r.a)]);
    const hiTop = rows.map((r) => [x(r.t), y(r.a + r.b)]);

    f.svg.appendChild(el("path", {
      d: pathFrom(lowTop.concat(base)) + " Z",
      fill: opt.colorA, "fill-opacity": 0.9,
    }));
    f.svg.appendChild(el("path", {
      d: pathFrom(hiTop.concat(lowTop.slice().reverse())) + " Z",
      fill: opt.colorB, "fill-opacity": 0.9,
    }));
    // 2px surface gap between the stacked fills (never a border around marks).
    f.svg.appendChild(el("path", {
      d: pathFrom(lowTop), fill: "none",
      stroke: css("--surface-1"), "stroke-width": 2,
    }));

    crosshair(f, x, times,
      (i) => tipRows(dayTimeFmt.format(new Date(times[i])), [
        { label: opt.labelB, color: opt.colorB, value: fmtNum(rows[i].b, 1) + " MW" },
        { label: opt.labelA, color: opt.colorA, value: fmtNum(rows[i].a, 1) + " MW" },
        { label: "Total", value: fmtNum(rows[i].a + rows[i].b, 1) + " MW" },
      ]),
      (i) => [
        { y: y(rows[i].a), color: opt.colorA },
        { y: y(rows[i].a + rows[i].b), color: opt.colorB },
      ]);
  }

  // ---------------------------------------------------------- 2. fan chart
  /* rows: [{t:ms, p10, p50, p90}] -- band + median line, one entity. */
  function fanChart(host, rows, opt) {
    if (!rows.length) { frame(host, opt.height || 300); return; }
    const times = rows.map((r) => r.t);
    const maxY = Math.max(1, ...rows.map((r) => r.p90));
    const ticks = niceTicks(0, maxY, 5);
    const f = frame(host, opt.height || 300, { left: axisLeft(ticks) });
    const x = linear(times[0], times[times.length - 1], f.m.left, f.m.left + f.iw);
    const y = linear(0, ticks[ticks.length - 1], f.m.top + f.ih, f.m.top);

    yAxis(f, y, ticks);
    xTimeAxis(f, x, times[0], times[times.length - 1], opt.everyDays || 2);

    const upper = rows.map((r) => [x(r.t), y(r.p90)]);
    const lower = rows.map((r) => [x(r.t), y(r.p10)]).reverse();
    f.svg.appendChild(el("path", {
      d: pathFrom(upper.concat(lower)) + " Z", fill: opt.color, "fill-opacity": 0.22,
    }));
    f.svg.appendChild(el("path", {
      d: pathFrom(rows.map((r) => [x(r.t), y(r.p50)])),
      fill: "none", stroke: opt.color, "stroke-width": 2,
      "stroke-linejoin": "round", "stroke-linecap": "round",
    }));

    // Capacity reference: a hairline, clearly not a data series.
    if (opt.capacity && opt.capacity <= ticks[ticks.length - 1]) {
      const cy = y(opt.capacity);
      f.svg.appendChild(el("line", {
        x1: f.m.left, x2: f.m.left + f.iw, y1: cy, y2: cy,
        stroke: css("--muted"), "stroke-width": 1, "stroke-dasharray": "1 3",
      }));
      const lb = el("text", {
        x: f.m.left + f.iw, y: cy - 5, "text-anchor": "end",
        fill: css("--muted"), "font-size": 10, "font-family": css("--font"),
      });
      lb.textContent = "installed capacity";
      f.svg.appendChild(lb);
    }

    crosshair(f, x, times,
      (i) => tipRows(dayTimeFmt.format(new Date(times[i])), [
        { label: "P90 (upside)", value: fmtNum(rows[i].p90, 1) + " MW" },
        { label: "P50 (expected)", color: opt.color, value: fmtNum(rows[i].p50, 1) + " MW" },
        { label: "P10 (safe)", value: fmtNum(rows[i].p10, 1) + " MW" },
        { label: "Lead time", value: rows[i].lead_h + " h" },
      ]),
      (i) => [{ y: y(rows[i].p50), color: opt.color }]);
  }

  // -------------------------------------------------------- 3. stacked bars
  /* rows: [{label, sub, a, b, partial}] */
  function stackedBars(host, rows, opt) {
    if (!rows.length) { frame(host, opt.height || 260, { bottom: 40 }); return; }
    const maxY = Math.max(1, ...rows.map((r) => r.a + r.b));
    const ticks = niceTicks(0, maxY, 5);
    const f = frame(host, opt.height || 260,
                    { bottom: 40, left: axisLeft(ticks) });
    const y = linear(0, ticks[ticks.length - 1], f.m.top + f.ih, f.m.top);
    yAxis(f, y, ticks);

    const step = f.iw / rows.length;
    const bw = Math.min(46, step * 0.62);
    const r = 4; // rounded data-end

    rows.forEach((row, i) => {
      const cx = f.m.left + step * (i + 0.5);
      const x0 = cx - bw / 2;
      const yA = y(row.a), yB = y(row.a + row.b), y0 = y(0);
      const g = el("g", { opacity: row.partial ? 0.5 : 1 });

      // lower segment: square top (it butts the segment above), flat base
      g.appendChild(el("rect", { x: x0, y: yA, width: bw, height: Math.max(0, y0 - yA), fill: opt.colorA }));
      // upper segment: rounded top, 2px surface gap below
      const hB = Math.max(0, yA - yB - 2);
      if (hB > 0) {
        const p = el("path", {
          d: `M${x0} ${yB + hB} L${x0} ${yB + r} Q${x0} ${yB} ${x0 + r} ${yB}
              L${x0 + bw - r} ${yB} Q${x0 + bw} ${yB} ${x0 + bw} ${yB + r}
              L${x0 + bw} ${yB + hB} Z`,
          fill: opt.colorB,
        });
        g.appendChild(p);
      }

      const lb = el("text", {
        x: cx, y: f.m.top + f.ih + 15, "text-anchor": "middle",
        fill: css("--muted"), "font-size": 10.5, "font-family": css("--font"),
      });
      lb.textContent = row.label;
      g.appendChild(lb);
      if (row.sub) {
        const s = el("text", {
          x: cx, y: f.m.top + f.ih + 27, "text-anchor": "middle",
          fill: css("--muted"), "font-size": 9.5, "font-family": css("--font"),
        });
        s.textContent = row.sub;
        g.appendChild(s);
      }

      const hit = el("rect", {
        x: cx - step / 2, y: f.m.top, width: step, height: f.ih, fill: "transparent",
      });
      hit.addEventListener("mousemove", (ev) =>
        showTip(tipRows(row.full || row.label, [
          { label: opt.labelB, color: opt.colorB, value: fmtNum(row.b) + " MWh" },
          { label: opt.labelA, color: opt.colorA, value: fmtNum(row.a) + " MWh" },
          { label: "Total", value: fmtNum(row.a + row.b) + " MWh" },
        ].concat(row.partial ? [{ label: "Note", value: "partial day" }] : [])), ev));
      hit.addEventListener("mouseleave", hideTip);
      g.appendChild(hit);
      f.svg.appendChild(g);
    });

    f.svg.appendChild(el("line", {
      x1: f.m.left, x2: f.m.left + f.iw, y1: y(0), y2: y(0),
      stroke: css("--axis"), "stroke-width": 1, "shape-rendering": "crispEdges",
    }));
  }

  // ----------------------------------------------------- 4. horizontal bars
  /* rows: [{label, sub, value, color}] */
  function barsH(host, rows, opt) {
    const rowH = 26;
    // Right margin must fit the widest direct label, or the longest bar's
    // value gets clipped at the plot edge.
    const fmtV = opt.fmt || ((v) => fmtNum(v, 1));
    const widest = rows.reduce((w, r) => Math.max(w, String(fmtV(r.value)).length), 0);
    const m = {
      top: 8, right: Math.max(48, widest * 6.6 + 16),
      bottom: 26, left: opt.labelWidth || 150,
    };
    const f = frame(host, rows.length * rowH + m.top + m.bottom, m);
    if (!rows.length) return;
    const maxV = Math.max(1, ...rows.map((r) => r.value));
    const ticks = niceTicks(0, maxV, 4);
    const x = linear(0, ticks[ticks.length - 1], f.m.left, f.m.left + f.iw);

    ticks.forEach((t) => {
      const px = x(t);
      f.svg.appendChild(el("line", {
        x1: px, x2: px, y1: f.m.top, y2: f.m.top + f.ih,
        stroke: css("--grid"), "stroke-width": 1, "shape-rendering": "crispEdges",
      }));
      const lb = el("text", {
        x: px, y: f.m.top + f.ih + 15, "text-anchor": "middle",
        fill: css("--muted"), "font-size": 10.5, "font-family": css("--font"),
      });
      lb.textContent = fmtNum(t);
      f.svg.appendChild(lb);
    });

    rows.forEach((row, i) => {
      const cy = f.m.top + i * rowH + rowH / 2;
      const h = 13, r = 4;
      const w = Math.max(1, x(row.value) - f.m.left);
      const g = el("g");
      const rr = Math.min(r, w);
      g.appendChild(el("path", {
        d: `M${f.m.left} ${cy - h / 2} L${f.m.left + w - rr} ${cy - h / 2}
            Q${f.m.left + w} ${cy - h / 2} ${f.m.left + w} ${cy - h / 2 + rr}
            L${f.m.left + w} ${cy + h / 2 - rr}
            Q${f.m.left + w} ${cy + h / 2} ${f.m.left + w - rr} ${cy + h / 2}
            L${f.m.left} ${cy + h / 2} Z`,
        fill: row.color || opt.color,
      }));
      const lb = el("text", {
        x: f.m.left - 10, y: cy + 3.5, "text-anchor": "end",
        fill: css("--text-secondary"), "font-size": 11.5, "font-family": css("--font"),
      });
      lb.textContent = row.label;
      g.appendChild(lb);
      // Direct-label the value: few enough rows that this is selective, not noise.
      const vl = el("text", {
        x: f.m.left + w + 8, y: cy + 3.5, fill: css("--text-primary"),
        "font-size": 11.5, "font-weight": 600, "font-family": css("--font"),
      });
      vl.textContent = fmtV(row.value);
      g.appendChild(vl);

      const hit = el("rect", {
        x: f.m.left, y: cy - rowH / 2, width: f.iw, height: rowH, fill: "transparent",
      });
      hit.addEventListener("mousemove", (ev) =>
        showTip(tipRows(row.label, (row.tip || []).concat([
          { label: opt.valueLabel || "Value", color: row.color || opt.color,
            value: fmtV(row.value) },
        ])), ev));
      hit.addEventListener("mouseleave", hideTip);
      g.appendChild(hit);
      f.svg.appendChild(g);
    });
  }

  // ------------------------------------------------------------------- map
  /* Asset locations. Equirectangular with x compressed by cos(mid-latitude),
     so a country is not stretched sideways -- adequate for a fleet spanning a
     country or two, and honest enough at world scale for "where are they".
     It is not a projection for measuring anything.

     `world` is the country-outline file (static/world.json): rings of
     [lon, lat] pairs, pre-simplified per country so Portugal keeps its coast
     while Canada is not 100 KB of Arctic islands. It may be null on the first
     paint -- the map still draws, just without land, and app.js re-renders
     when the fetch lands. */
  function mapPoints(host, rows, opt) {
    const f = frame(host, opt.height || 400,
                    { top: 10, right: 12, bottom: 28, left: 12 });
    if (!rows.length) return;

    // --- bounds: fit the ASSETS, not the countries. Portugal's box would
    // otherwise stretch to the Azores and shrink the mainland to nothing.
    let lo0 = Infinity, lo1 = -Infinity, la0 = Infinity, la1 = -Infinity;
    rows.forEach((r) => {
      lo0 = Math.min(lo0, r.lon); lo1 = Math.max(lo1, r.lon);
      la0 = Math.min(la0, r.lat); la1 = Math.max(la1, r.lat);
    });
    const padLo = Math.max(0.3, (lo1 - lo0) * 0.10);
    const padLa = Math.max(0.3, (la1 - la0) * 0.10);
    lo0 -= padLo; lo1 += padLo; la0 -= padLa; la1 += padLa;

    const kx = Math.cos(((la0 + la1) / 2) * Math.PI / 180) || 1;
    const pw = (lo1 - lo0) * kx, ph = la1 - la0;
    const s = Math.min(f.iw / pw, f.ih / ph);
    const ox = f.m.left + (f.iw - pw * s) / 2;
    const oy = f.m.top + (f.ih - ph * s) / 2;
    const X = (lon) => ox + (lon - lo0) * kx * s;
    const Y = (lat) => oy + (la1 - lat) * s;

    // Clip land to the plot box: outlines run well past the viewport.
    const cid = "mapclip" + Math.random().toString(36).slice(2, 8);
    const defs = el("defs");
    const cp = el("clipPath", { id: cid });
    cp.appendChild(el("rect", {
      x: f.m.left, y: f.m.top, width: f.iw, height: f.ih, rx: 6,
    }));
    defs.appendChild(cp);
    f.svg.appendChild(defs);

    const land = el("g", { "clip-path": `url(#${cid})` });
    f.svg.appendChild(el("rect", {
      x: f.m.left, y: f.m.top, width: f.iw, height: f.ih, rx: 6,
      fill: css("--wash"), stroke: css("--grid"), "stroke-width": 1,
    }));

    if (opt.world && opt.world.features) {
      opt.world.features.forEach((c) => {
        c.r.forEach((ring) => {
          // Cheap bbox cull: most of the planet is off-screen at country zoom.
          let a = Infinity, b = -Infinity, cc = Infinity, dd = -Infinity;
          for (let i = 0; i < ring.length; i++) {
            const p = ring[i];
            if (p[0] < a) a = p[0]; if (p[0] > b) b = p[0];
            if (p[1] < cc) cc = p[1]; if (p[1] > dd) dd = p[1];
          }
          if (b < lo0 || a > lo1 || dd < la0 || cc > la1) return;
          let d = "";
          for (let i = 0; i < ring.length; i++) {
            d += (i ? "L" : "M") + X(ring[i][0]).toFixed(1) + " " + Y(ring[i][1]).toFixed(1);
          }
          land.appendChild(el("path", {
            d: d + "Z", fill: css("--land"), stroke: css("--land-line"),
            "stroke-width": 1, "stroke-linejoin": "round",
          }));
        });
      });
    }
    f.svg.appendChild(land);

    // --- scale bar. km per pixel is 111.32/s regardless of latitude, because
    // the cos() factor is already in the x scale.
    const kmPerPx = 111.32 / s;
    const target = f.iw * 0.18 * kmPerPx;
    const pow = Math.pow(10, Math.floor(Math.log10(target)));
    const barKm = [1, 2, 5, 10].map((n) => n * pow)
      .reduce((best, n) => (Math.abs(n - target) < Math.abs(best - target) ? n : best));
    const barPx = barKm / kmPerPx;
    const bx = f.m.left + 12, by = f.m.top + f.ih - 14;
    const sg = el("g");
    sg.appendChild(el("path", {
      d: `M${bx} ${by - 4}V${by}H${bx + barPx}V${by - 4}`,
      fill: "none", stroke: css("--text-secondary"), "stroke-width": 1.5,
    }));
    const sl = el("text", {
      x: bx + barPx + 6, y: by + 1, fill: css("--muted"),
      "font-size": 10.5, "font-family": css("--font"),
    });
    sl.textContent = (barKm >= 1 ? fmtNum(barKm) : barKm) + " km";
    sg.appendChild(sl);
    f.svg.appendChild(sg);

    // --- markers. Big first, small painted on top, or a single-turbine site
    // vanishes under a neighbouring wind farm.
    const maxV = Math.max(1, ...rows.map((r) => r.value || 0));
    const R = (v) => dotRadius(v, maxV);
    const ordered = rows.slice().sort((a, b) => (b.value || 0) - (a.value || 0));
    const marks = el("g", { "clip-path": `url(#${cid})` });

    ordered.forEach((row) => {
      const cx = X(row.lon), cy = Y(row.lat), r = R(row.value);
      const g = el("g");
      const dot = el("circle", {
        cx, cy, r, fill: row.color, "fill-opacity": 0.82,
        // 2px surface ring: the dataviz rule for marks that overlap.
        stroke: css("--surface-1"), "stroke-width": 2,
      });
      g.appendChild(dot);
      // Hit target is always >= 9px even when the mark is tiny.
      const hit = el("circle", { cx, cy, r: Math.max(9, r + 3), fill: "transparent" });
      hit.addEventListener("mousemove", (ev) => {
        dot.setAttribute("fill-opacity", 1);
        dot.setAttribute("stroke", css("--text-primary"));
        showTip(tipRows(row.label, (row.tip || []).concat([
          { label: "Position", value: row.lat.toFixed(3) + ", " + row.lon.toFixed(3) },
        ])), ev);
      });
      hit.addEventListener("mouseleave", () => {
        dot.setAttribute("fill-opacity", 0.82);
        dot.setAttribute("stroke", css("--surface-1"));
        hideTip();
      });
      g.appendChild(hit);
      marks.appendChild(g);
    });
    f.svg.appendChild(marks);

    /* Selective labels, largest site first: keep one only where it clears the
       labels already kept and stays inside the plot. Same rule as the Google
       renderer, so the two maps read the same. */
    const placed = [];
    ordered.forEach((row) => {
      const cx = X(row.lon), cy = Y(row.lat), r = R(row.value);
      const w = row.label.length * 5.9 + 8;
      const bx = cx + r + 4, by = cy - 7;
      const box = [bx, by, bx + w, by + 14];
      if (box[2] > f.m.left + f.iw - 4 || box[1] < f.m.top + 2 ||
          box[3] > f.m.top + f.ih - 2) return;
      if (placed.some((q) => box[0] < q[2] && box[2] > q[0] &&
                             box[1] < q[3] && box[3] > q[1])) return;
      placed.push([box[0] - 3, box[1] - 2, box[2] + 3, box[3] + 2]);
      const t = el("text", {
        x: bx, y: cy + 3.5, "font-size": 10.5, "font-family": css("--font"),
        fill: css("--text-primary"),
        // Halo: the label sits over land fill and other markers.
        stroke: css("--surface-1"), "stroke-width": 3, "paint-order": "stroke",
        "stroke-linejoin": "round",
      });
      t.textContent = row.label;
      f.svg.appendChild(t);
    });

    // --- size key, bottom-right. Three nested circles read faster than a row.
    const keyVals = [maxV, maxV / 4, maxV / 25].filter((v) => v >= 1);
    const kg = el("g");
    const kx0 = f.m.left + f.iw - 16, ky0 = f.m.top + f.ih - 12;
    keyVals.forEach((v) => {
      const r = R(v);
      kg.appendChild(el("circle", {
        cx: kx0 - 14, cy: ky0 - r, r, fill: "none",
        stroke: css("--axis"), "stroke-width": 1,
      }));
      const t = el("text", {
        x: kx0 - 14 - R(maxV) - 6, y: ky0 - 2 * r + 4, "text-anchor": "end",
        fill: css("--muted"), "font-size": 10, "font-family": css("--font"),
      });
      t.textContent = fmtNum(v, v < 10 ? 1 : 0);
      kg.appendChild(t);
    });
    const kl = el("text", {
      x: kx0, y: ky0 + 12, "text-anchor": "end",
      fill: css("--muted"), "font-size": 10, "font-family": css("--font"),
    });
    kl.textContent = opt.sizeLabel || "MW";
    kg.appendChild(kl);
    f.svg.appendChild(kg);
  }

  // ------------------------------------------------ 5. generic line / band
  /* "Several quantities on one time axis": any number of lines, filled lo/hi
     bands, horizontal reference lines, and markers on flagged hours. Demos 3
     and 6 need the same shape and the demand panels will too, so it is written
     once rather than as near-duplicates of fanChart.

       opt = {
         height, fmt, zero,
         bands:  [{label, color, opacity, rows:[{t, lo, hi}]}],
         lines:  [{label, color, dash, width, rows:[{t, v}]}],
         hlines: [{value, label, color}],
         marks:  [{t, v, color}],
       }

     Every rows array must share one time grid: the crosshair indexes the first
     band or line and reads the rest positionally. */
  function lineChart(host, opt) {
    // Room for the axis caption when the x axis is a labelled quantity.
    const base = opt.xLabel ? { bottom: 46 } : {};
    const bands = opt.bands || [], lines = opt.lines || [], hl = opt.hlines || [];
    const ref = (bands[0] && bands[0].rows) || (lines[0] && lines[0].rows) || [];
    if (!ref.length) { frame(host, opt.height || 300, base); return; }
    const times = ref.map((r) => r.t);
    const t0 = times[0], t1 = times[times.length - 1];

    const vals = [];
    bands.forEach((b) => b.rows.forEach((r) => vals.push(r.lo, r.hi)));
    lines.forEach((l) => l.rows.forEach((r) => vals.push(r.v)));
    hl.forEach((h) => vals.push(h.value));
    const fin = vals.filter((v) => v != null && isFinite(v));
    if (!fin.length) { frame(host, opt.height || 300, base); return; }
    let lo = Math.min(...fin), hi = Math.max(...fin);
    if (opt.zero || lo > 0) lo = Math.min(lo, 0);

    /* Ticks first, then the frame. The left margin has to fit the widest label
       -- national residual load runs to five figures -- and the x scale is
       derived from that margin, so it cannot be widened afterwards. */
    const ticks = niceTicks(lo, hi, 5);
    const f = frame(host, opt.height || 300,
                    Object.assign({}, base, { left: axisLeft(ticks, opt.fmt) }));
    const y = linear(ticks[0], ticks[ticks.length - 1], f.m.top + f.ih, f.m.top);
    const x = linear(t0, t1, f.m.left, f.m.left + f.iw);
    yAxis(f, y, ticks, opt.fmt);
    // The backtest plots against LEAD TIME, not wall-clock time, so the x axis
    // has to be able to be a plain number.
    if (opt.xNumeric) xNumAxis(f, x, t0, t1, opt.xFmt, opt.xLabel);
    else xTimeAxis(f, x, t0, t1, Math.max(1, Math.round((t1 - t0) / 86400000 / 8)));

    bands.forEach((b) => {
      const up = b.rows.map((r) => [x(r.t), y(r.hi)]);
      const dn = b.rows.map((r) => [x(r.t), y(r.lo)]).reverse();
      f.svg.appendChild(el("path", {
        d: pathFrom(up.concat(dn)) + " Z",
        fill: b.color, "fill-opacity": b.opacity == null ? 0.16 : b.opacity,
      }));
    });

    if (opt.zero) {
      f.svg.appendChild(el("line", {
        x1: f.m.left, x2: f.m.left + f.iw, y1: y(0), y2: y(0),
        stroke: css("--axis"), "stroke-width": 1, "shape-rendering": "crispEdges",
      }));
    }

    hl.forEach((h) => {
      const c = h.color || css("--critical");
      f.svg.appendChild(el("line", {
        x1: f.m.left, x2: f.m.left + f.iw, y1: y(h.value), y2: y(h.value),
        stroke: c, "stroke-width": 1.5, "stroke-dasharray": "5 4",
      }));
      if (h.label) {
        const t = el("text", {
          x: f.m.left + f.iw - 4, y: y(h.value) - 5, "text-anchor": "end",
          fill: c, "font-size": 10.5, "font-weight": 600, "font-family": css("--font"),
        });
        t.textContent = h.label;
        f.svg.appendChild(t);
      }
    });

    lines.forEach((l) => {
      const pts = l.rows.filter((r) => r.v != null && isFinite(r.v))
                        .map((r) => [x(r.t), y(r.v)]);
      if (!pts.length) return;
      const a = { d: pathFrom(pts), fill: "none", stroke: l.color,
                  "stroke-width": l.width || 2, "stroke-linejoin": "round",
                  "stroke-linecap": "round" };
      if (l.dash) a["stroke-dasharray"] = l.dash;
      f.svg.appendChild(el("path", a));
    });

    (opt.marks || []).forEach((mk) => {
      f.svg.appendChild(el("circle", {
        cx: x(mk.t), cy: y(mk.v), r: 4.5, fill: mk.color || css("--critical"),
        stroke: css("--surface-1"), "stroke-width": 2,
      }));
    });

    const fmtV = opt.fmt || ((v) => fmtNum(v, 1));
    crosshair(f, x, times, (i) => {
      const rows = [];
      bands.forEach((b) => rows.push({
        label: b.label, color: b.color,
        value: fmtV(b.rows[i].lo) + " – " + fmtV(b.rows[i].hi),
      }));
      lines.forEach((l) => rows.push({
        label: l.label, color: l.color,
        value: l.rows[i] && l.rows[i].v != null ? fmtV(l.rows[i].v) : "—",
      }));
      hl.forEach((h) => rows.push({ label: h.label || "Limit", value: fmtV(h.value) }));
      const title = opt.xNumeric
        ? (opt.xFmt ? opt.xFmt(times[i]) : fmtNum(times[i]))
        : dayTimeFmt.format(new Date(times[i]));
      return tipRows(title, rows);
    }, (i) => lines
      .filter((l) => l.rows[i] && l.rows[i].v != null && isFinite(l.rows[i].v))
      .map((l) => ({ y: y(l.rows[i].v), color: l.color })));
  }

  // -------------------------------------------------- 6. grid-cell heatmap
  /* A choropleth over the forecast's own 0.1 degree cells.

     Sequential encoding, per the dataviz rules: ONE hue, light to dark. Not a
     rainbow -- a rainbow implies categories where there is a magnitude, and
     reverses rank order for colourblind readers. */
  function mix(a, b, t) {
    const p = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
    const [r1, g1, b1] = p(a), [r2, g2, b2] = p(b);
    const c = (x, y) => Math.round(x + (y - x) * t);
    return `rgb(${c(r1, r2)},${c(g1, g2)},${c(b1, b2)})`;
  }

  function gridCells(host, rows, opt) {
    const f = frame(host, opt.height || 420,
                    { top: 10, right: 12, bottom: 34, left: 12 });
    if (!rows.length) return;

    let lo0 = Infinity, lo1 = -Infinity, la0 = Infinity, la1 = -Infinity;
    rows.forEach((r) => {
      lo0 = Math.min(lo0, r.lon); lo1 = Math.max(lo1, r.lon);
      la0 = Math.min(la0, r.lat); la1 = Math.max(la1, r.lat);
    });
    const cd = opt.cellDeg || 0.1;
    lo0 -= cd; lo1 += cd; la0 -= cd; la1 += cd;

    const kx = Math.cos(((la0 + la1) / 2) * Math.PI / 180) || 1;
    const pw = (lo1 - lo0) * kx, ph = la1 - la0;
    const s = Math.min(f.iw / pw, f.ih / ph);
    const ox = f.m.left + (f.iw - pw * s) / 2;
    const oy = f.m.top + (f.ih - ph * s) / 2;
    const X = (lon) => ox + (lon - lo0) * kx * s;
    const Y = (lat) => oy + (la1 - lat) * s;

    f.svg.appendChild(el("rect", {
      x: f.m.left, y: f.m.top, width: f.iw, height: f.ih, rx: 6,
      fill: css("--wash"), stroke: css("--grid"), "stroke-width": 1,
    }));

    const vals = rows.map((r) => r.v).filter((v) => v != null && isFinite(v));
    const vmin = opt.min != null ? opt.min : Math.min(...vals);
    const vmax = opt.max != null ? opt.max : Math.max(...vals);
    const span = (vmax - vmin) || 1;
    const c0 = opt.from || "#eef3fa", c1 = opt.to || "#0f3663";

    const w = Math.max(1.2, cd * kx * s) + 0.4;   // +0.4: hairline seams
    const hgt = Math.max(1.2, cd * s) + 0.4;
    const g = el("g");
    rows.forEach((row) => {
      const t = Math.max(0, Math.min(1, (row.v - vmin) / span));
      const rect = el("rect", {
        x: X(row.lon) - w / 2, y: Y(row.lat) - hgt / 2,
        width: w, height: hgt, fill: mix(c0, c1, t),
        "shape-rendering": "crispEdges",
      });
      rect.addEventListener("mousemove", (ev) =>
        showTip(tipRows(row.label || (row.lat.toFixed(2) + ", " + row.lon.toFixed(2)),
                        row.tip || []), ev));
      rect.addEventListener("mouseleave", hideTip);
      g.appendChild(rect);
    });
    f.svg.appendChild(g);

    // Continuous legend, bottom centre.
    const lw = Math.min(220, f.iw * 0.45), lx = f.m.left + (f.iw - lw) / 2;
    const ly = f.m.top + f.ih + 12;
    const gid = "gr" + Math.random().toString(36).slice(2, 8);
    const defs = el("defs");
    const grad = el("linearGradient", { id: gid, x1: "0", x2: "1", y1: "0", y2: "0" });
    for (let i = 0; i <= 10; i++) {
      grad.appendChild(el("stop", {
        offset: i / 10, "stop-color": mix(c0, c1, i / 10),
      }));
    }
    defs.appendChild(grad);
    f.svg.appendChild(defs);
    f.svg.appendChild(el("rect", {
      x: lx, y: ly, width: lw, height: 8, rx: 2, fill: `url(#${gid})`,
      stroke: css("--axis"), "stroke-width": 0.5,
    }));
    const fmtV = opt.fmt || ((v) => fmtNum(v, 1));
    [[lx, vmin, "start"], [lx + lw, vmax, "end"]].forEach(([x, v, anchor]) => {
      const t = el("text", {
        x, y: ly + 20, "text-anchor": anchor, fill: css("--muted"),
        "font-size": 10.5, "font-family": css("--font"),
      });
      t.textContent = fmtV(v);
      f.svg.appendChild(t);
    });
    if (opt.label) {
      const t = el("text", {
        x: lx + lw / 2, y: ly + 20, "text-anchor": "middle",
        fill: css("--muted"), "font-size": 10.5, "font-family": css("--font"),
      });
      t.textContent = opt.label;
      f.svg.appendChild(t);
    }
  }

  // Area (not radius) tracks capacity, so a 200 MW site does not read as 30x a
  // 7 MW one. Shared by both map renderers so the size key means the same thing.
  function dotRadius(v, maxV) {
    return 3.2 + 10.3 * Math.sqrt(Math.max(0, v || 0) / Math.max(1, maxV));
  }

  // ------------------------------------------------------- Google Maps map
  /* The Maps JavaScript API is the only external dependency on the page, and
     it is deliberately optional: no key, or a failed load, and the caller
     falls back to mapPoints() above. */
  let mapsLoader = null;
  function loadMapsApi(key) {
    if (mapsLoader) return mapsLoader;
    mapsLoader = new Promise((resolve, reject) => {
      if (global.google && global.google.maps) return resolve(global.google.maps);
      // With loading=async the script's own onload fires BEFORE google.maps
      // exists, so readiness has to come from the documented callback.
      const cb = "__wnMapsReady";
      global[cb] = () => resolve(global.google.maps);
      const s = document.createElement("script");
      s.src = "https://maps.googleapis.com/maps/api/js?v=weekly&loading=async" +
              "&callback=" + cb + "&key=" + encodeURIComponent(key);
      s.async = true;
      s.onerror = () => { mapsLoader = null; reject(new Error("Maps JS failed to load")); };
      document.head.appendChild(s);
    });
    return mapsLoader;
  }

  function mapGoogle(host, rows, opt) {
    return loadMapsApi(opt.key).then((maps) => {
      // Cards redraw on every tab switch. Rebuilding the map each time would
      // re-tile and throw away the user's pan/zoom, so keep it when the fleet
      // being plotted has not changed.
      const sig = rows.length + "|" + rows.map((r) => r.label).join("");
      if (host._gmapSig === sig) return;
      host._gmapSig = sig;
      host.textContent = "";

      /* A rejected key, referrer or billing state is reported through this
         global -- NOT through the promise. The script loads, the Map object
         constructs, and Maps paints its own "Oops! Something went wrong" card
         inside the div. Without this hook that error card is what a customer
         would see, so hand back to the SVG map instead. */
      global.gm_authFailure = () => {
        host._gmapSig = null;
        host._gmapFit = null;
        if (opt.onAuthFail) opt.onAuthFail();
      };

      const div = document.createElement("div");
      div.className = "gmap";
      div.style.height = (opt.height || 460) + "px";
      host.appendChild(div);

      const map = new maps.Map(div, {
        mapTypeId: opt.mapTypeId || "hybrid",
        mapTypeControl: true,
        mapTypeControlOptions: { mapTypeIds: ["hybrid", "satellite", "terrain", "roadmap"] },
        streetViewControl: false,
        tilt: 0,
        // Without this, scrolling the page over the map zooms the map instead.
        gestureHandling: "cooperative",
      });
      const bounds = new maps.LatLngBounds();
      rows.forEach((r) => bounds.extend({ lat: r.lat, lng: r.lon }));
      const capZoom = () => maps.event.addListenerOnce(map, "idle", () => {
        // A single-site country would otherwise land at max zoom on a rooftop.
        if (map.getZoom() > 11) map.setZoom(11);
      });
      map.fitBounds(bounds, 56);
      capZoom();
      /* The API resizes itself when the container does, but it keeps the
         centre, not the framing -- so maximising would leave half the fleet
         off-screen. app.js calls this after a resize to re-fit. */
      host._gmapFit = () => { map.fitBounds(bounds, 56); capZoom(); };

      const maxV = Math.max(1, ...rows.map((r) => r.value || 0));
      // Big first so a single-turbine site is not buried under a wind farm.
      const ordered = rows.slice().sort((a, b) => (b.value || 0) - (a.value || 0));

      class Dots extends maps.OverlayView {
        onAdd() {
          this.layer = document.createElement("div");
          this.layer.className = "gmap-dots";
          this.nodes = ordered.map((row) => {
            const d = document.createElement("div");
            d.className = "gmap-dot";
            const r = dotRadius(row.value, maxV);
            d.style.width = d.style.height = 2 * r + "px";
            d.style.background = row.color;
            d.addEventListener("mousemove", (ev) =>
              showTip(tipRows(row.label, (row.tip || []).concat([
                { label: "Position", value: row.lat.toFixed(3) + ", " + row.lon.toFixed(3) },
              ])), ev));
            d.addEventListener("mouseleave", hideTip);
            this.layer.appendChild(d);
            return d;
          });
          this.labels = ordered.map((row) => {
            const t = document.createElement("div");
            t.className = "gmap-label";
            t.textContent = row.label;
            this.layer.appendChild(t);
            return t;
          });
          // overlayMouseTarget, not overlayLayer: the dots take pointer events.
          this.getPanes().overlayMouseTarget.appendChild(this.layer);
        }
        draw() {
          const p = this.getProjection();
          if (!p) return;
          const div = this.getMap().getDiv();
          const vw = div.clientWidth, vh = div.clientHeight;
          const placed = [];
          ordered.forEach((row, i) => {
            const ll = new maps.LatLng(row.lat, row.lon);
            // Two coordinate spaces: the overlay pane is positioned in DIV
            // pixels, but "is this on screen" is a question about CONTAINER
            // pixels. Deriving one from the other via the map centre breaks in
            // fullscreen; ask the projection for both.
            const pt = p.fromLatLngToDivPixel(ll);
            const cp = p.fromLatLngToContainerPixel(ll);
            const r = dotRadius(row.value, maxV);
            this.nodes[i].style.left = pt.x + "px";
            this.nodes[i].style.top = pt.y + "px";

            /* Selective labels: walk the sites largest-first and keep a label
               only where it does not collide with one already kept and the
               marker is actually on screen. Because draw() re-runs on every
               pan and zoom, crowded areas stay clean and zooming in reveals
               the smaller sites -- no fixed "top N" cutoff. */
            const lab = this.labels[i];
            const sx = cp.x, sy = cp.y;
            const w = row.label.length * 6.1 + 10, hgt = 15;
            const box = [sx + r + 5, sy - hgt / 2, sx + r + 5 + w, sy + hgt / 2];
            const onScreen = sx > -20 && sx < vw + 20 && sy > -20 && sy < vh + 20;
            const fits = box[2] < vw - 4 && box[1] > 2 && box[3] < vh - 2;
            const clear = !placed.some((q) =>
              box[0] < q[2] && box[2] > q[0] && box[1] < q[3] && box[3] > q[1]);
            if (onScreen && fits && clear) {
              placed.push([box[0] - 4, box[1] - 3, box[2] + 4, box[3] + 3]);
              lab.style.left = pt.x + r + 5 + "px";
              lab.style.top = pt.y + "px";
              lab.hidden = false;
            } else {
              lab.hidden = true;
            }
          });
        }
        onRemove() { if (this.layer) this.layer.remove(); }
      }
      new Dots().setMap(map);
    });
  }

  global.Charts = {
    stackedArea, fanChart, stackedBars, barsH, lineChart, gridCells,
    mapPoints, mapGoogle,
    fmtNum, css, hideTip, setTimeZone, tzLabel,
    // Accessors, not captured references: setTimeZone() rebuilds them.
    dayFmt: (d) => dayFmt.format(d),
    dayTimeFmt: (d) => dayTimeFmt.format(d),
    weekdayFmt: (d) => weekdayFmt.format(d),
    get timeZone() { return TZ; },
  };
})(window);
