/* Chapter 5 explorers for the CurrentCourseGuide (Day 10–11 lecture topics and the §5.1–5.7 textbook previews):
   VSEPR shapes with and without lone pairs, polar molecules, hybrid orbitals, σ and π bonds, chirality, and
   molecular orbital diagrams. Classic script loaded after explorers.js; adds to window.Explorers.mount.
   Data come from verification/CurrentCourseGuide/ch5_data.py (GUIDE_DATA.ch5; Lewis drawings from the checked
   structures in lewis.py). In node, module.exports gives the pure calculations (tested by test_explorers_ch5.js). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory(require("./explorers.js"));
  else factory(root.Explorers);
})(typeof self !== "undefined" ? self : this, function (X) {
  "use strict";
  var U = X.ui, mount = X.mount;
  var MINUS = "−", RAD = Math.PI / 180, TET = Math.acos(-1 / 3) / RAD;

  /* ================================================================ pure calculations */
  var C = {};
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function len(a) { return Math.sqrt(dot(a, a)); }
  function unit(a) { var L = len(a); return [a[0] / L, a[1] / L, a[2] / L]; }
  function addv(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
  function mul(a, k) { return [a[0] * k, a[1] * k, a[2] * k]; }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  C.unit = unit;
  C.angle = function (a, b) { return Math.acos(Math.max(-1, Math.min(1, dot(unit(a), unit(b))))) / RAD; };

  C.EPG = { 1: "", 2: "linear", 3: "trigonal planar", 4: "tetrahedral", 5: "trigonal bipyramidal", 6: "octahedral" };
  C.MG = { "2-0": "linear", "3-0": "trigonal planar", "3-1": "bent (angular)", "4-0": "tetrahedral", "4-1": "trigonal pyramidal",
    "4-2": "bent (angular)", "5-0": "trigonal bipyramidal", "5-1": "seesaw", "5-2": "T-shaped", "5-3": "linear",
    "6-0": "octahedral", "6-1": "square pyramidal", "6-2": "square planar", "6-3": "T-shaped" };
  C.MAXLP = { 2: 0, 3: 1, 4: 2, 5: 3, 6: 3 };

  // ---- VSEPR electron-domain directions (y up, x right, z toward the viewer). Ligands fill the non-lone-pair
  // positions in order. opt.angle draws a stated bond angle (O3 117°, CH2O 118°, NH3 107°, H2O 104.5°, BrF5 85°);
  // opt.axial puts one SN 5 lone pair on an axial site; opt.adjacent puts two SN 6 lone pairs at 90°;
  // opt.frame "B" orients an SN 4 shape with two domains below and two above (H2O, CH2Cl2).
  C.domains = function (sn, nlp, opt) {
    opt = opt || {};
    var dirs = [], lp = [], site = [];
    function put(v, isLp, s) { dirs.push(v); lp.push(!!isLp); site.push(s || ""); }
    var a;
    if (sn === 1) put([1, 0, 0], false);
    else if (sn === 2) { put([-1, 0, 0], false); put([1, 0, 0], false); }
    else if (sn === 3) {
      a = (opt.angle || 120) * RAD;
      put([0, 1, 0], nlp >= 1);
      put([-Math.sin(a / 2), -Math.cos(a / 2), 0], false);
      put([Math.sin(a / 2), -Math.cos(a / 2), 0], false);
    } else if (sn === 4) {
      if (nlp === 2 || opt.frame === "B") {
        a = (opt.angle || TET) * RAD;
        var b = TET * RAD;
        put([-Math.sin(a / 2), -Math.cos(a / 2), 0], false);
        put([Math.sin(a / 2), -Math.cos(a / 2), 0], false);
        put([0, Math.cos(b / 2), Math.sin(b / 2)], nlp >= 1);
        put([0, Math.cos(b / 2), -Math.sin(b / 2)], nlp >= 2);
      } else {
        a = (opt.angle || TET) * RAD;
        var s2 = 2 / 3 * (1 - Math.cos(a)), st = Math.sqrt(s2), ct = Math.sqrt(1 - s2);
        put([0, 1, 0], nlp >= 1);
        [0, 120, 240].forEach(function (p) { put([st * Math.sin(p * RAD), -ct, st * Math.cos(p * RAD)], false); });
      }
    } else if (sn === 5) {
      var E = [[-1, 0, 0], [0.5, 0, Math.sqrt(3) / 2], [0.5, 0, -Math.sqrt(3) / 2]];
      var ax = !!opt.axial && nlp >= 1, ne = ax ? nlp - 1 : nlp;
      var eqLP = ne === 0 ? [] : ne === 1 ? [0] : ne === 2 ? [1, 2] : [0, 1, 2];
      put([0, 1, 0], ax, "axial"); put([0, -1, 0], false, "axial");
      E.forEach(function (v, i) { put(v, eqLP.indexOf(i) >= 0, "equatorial"); });
    } else if (sn === 6) {
      var P = [[0, 1, 0], [0, -1, 0], [-1, 0, 0], [1, 0, 0], [0, 0, 1], [0, 0, -1]];
      if (opt.angle && nlp === 1) {         // base atoms tilt toward the apex, away from the lone pair (BrF5)
        a = opt.angle * RAD;
        P = [[0, 1, 0], [0, -1, 0], [-Math.sin(a), Math.cos(a), 0], [Math.sin(a), Math.cos(a), 0], [0, Math.cos(a), Math.sin(a)], [0, Math.cos(a), -Math.sin(a)]];
      }
      var idx = nlp === 0 ? [] : nlp === 1 ? [1] : nlp === 2 ? (opt.adjacent ? [1, 2] : [0, 1]) : [1, 4, 5];
      P.forEach(function (v, i) { put(v, idx.indexOf(i) >= 0, ""); });
    }
    return { dirs: dirs, lp: lp, site: site };
  };

  C.shapeInfo = function (sn, nlp, opt) {
    opt = opt || {};
    var d = C.domains(sn, nlp, opt), atoms = [], i, j, c = { lplp: 0, lpbp: 0, bpbp: 0 }, set = {}, lpSites = [];
    for (i = 0; i < d.dirs.length; i++) { if (d.lp[i]) lpSites.push(d.site[i]); else atoms.push(d.dirs[i]); }
    for (i = 0; i < d.dirs.length; i++) for (j = i + 1; j < d.dirs.length; j++) {
      if (Math.abs(C.angle(d.dirs[i], d.dirs[j]) - 90) < 1) c[d.lp[i] && d.lp[j] ? "lplp" : !d.lp[i] && !d.lp[j] ? "bpbp" : "lpbp"]++;
    }
    for (i = 0; i < atoms.length; i++) for (j = i + 1; j < atoms.length; j++) set[(Math.round(C.angle(atoms[i], atoms[j]) * 10) / 10).toFixed(1)] = 1;
    var variant = (!!opt.axial && sn === 5 && nlp >= 1) || (!!opt.adjacent && sn === 6 && nlp === 2);
    return { epg: C.EPG[sn], mg: variant ? null : C.MG[sn + "-" + nlp], observed: !variant, contacts: c, lpSites: lpSites.sort(),
      angles: Object.keys(set).map(Number).sort(function (x, y) { return x - y; }), domains: d };
  };

  // ---- polarity: bond dipoles point toward the more electronegative atom, length ∝ Δχ (a stand-in); vector sum
  C.dipole = function (m, chi) {
    var d = C.domains(m.sn, m.lp, { angle: m.angle, frame: m.frame }), bonds = [], net = [0, 0, 0], unknown = false, li = 0;
    for (var i = 0; i < d.dirs.length; i++) {
      if (d.lp[i]) continue;
      var x = m.ligands[li], u = unit(d.dirs[i]), dc = null;
      if (chi[m.center] === undefined || chi[x] === undefined) { unknown = true; net = addv(net, u); }
      else { dc = Math.round((chi[x] - chi[m.center]) * 100) / 100; net = addv(net, mul(u, dc)); }
      bonds.push({ el: x, dir: u, dchi: dc, order: m.orders[li] });
      li++;
    }
    var mag = len(net);
    if (mag < 1e-9) { net = [0, 0, 0]; mag = 0; }
    return { bonds: bonds, net: net, mag: mag, polar: mag > 1e-6, unknown: unknown, domains: d };
  };

  // ---- hybrid orbitals: ground state (Hund's rule), hybrids (lone pairs, then one electron per σ bond),
  // unhybridized p (one electron per π bond, the rest empty)
  C.HYB = { 2: "sp", 3: "sp2", 4: "sp3" };
  C.hybridize = function (h) {
    var p = [0, 0, 0], n, hyb = [], unh = [], roles = [], proles = [];
    for (n = 0; n < h.p; n++) p[n % 3]++;
    for (n = 0; n < h.lp; n++) { hyb.push(2); roles.push({ kind: "lp" }); }
    h.sigma.forEach(function (s) { hyb.push(1); roles.push({ kind: "sigma", partner: s }); });
    h.pi.forEach(function (s) { unh.push(1); proles.push({ kind: "pi", partner: s }); });
    while (unh.length < 4 - h.sn) { unh.push(0); proles.push({ kind: "empty" }); }
    return { hyb: C.HYB[h.sn], ground: [h.s].concat(p), hybrids: hyb, unhybridized: unh, roles: roles, proles: proles,
      unpairedGround: (h.s === 1 ? 1 : 0) + p.filter(function (x) { return x === 1; }).length, bonds: h.sigma.length + h.pi.length };
  };
  C.hybHTML = function (k) { return k === "sp" ? "sp" : "sp<sup>" + k.slice(2) + "</sup>"; };
  C.hybText = function (k) { return k === "sp" ? "sp" : "sp" + (k === "sp2" ? "²" : "³"); };

  C.sigmaPi = function (bonds) { var s = 0, p = 0; bonds.forEach(function (b) { s += 1; p += b[2] - 1; }); return { sigma: s, pi: p }; };

  // ---- chirality: four groups on the corners of a tetrahedron (group i at TETRA[i]); the mirror image reflects x
  C.TETRA = (function () {
    var r = Math.sqrt(8) / 3, out = [[0, 1, 0]];
    [0, 120, 240].forEach(function (p) { out.push([r * Math.sin(p * RAD), -1 / 3, r * Math.cos(p * RAD)]); });
    return out;
  })();
  C.mirror = function (v) { return [-v[0], v[1], v[2]]; };
  C.rotateAbout = function (v, axis, deg) {                      // Rodrigues' rotation formula
    var k = unit(axis), t = deg * RAD, c = Math.cos(t), s = Math.sin(t);
    return addv(addv(mul(v, c), mul(cross(k, v), s)), mul(k, dot(k, v) * (1 - c)));
  };
  C.nearest = function (v) {
    var best = 0, bd = 1e9;
    C.TETRA.forEach(function (p, i) { var d = len(addv(v, mul(p, -1))); if (d < bd) { bd = d; best = i; } });
    return best;
  };
  C.matchCount = function (groups, dirs) {                        // dirs[i]: where the mirror image's group i points now
    var n = 0;
    dirs.forEach(function (v, i) { if (groups[C.nearest(v)] === groups[i]) n++; });
    return n;
  };
  C.superimposable = function (groups) {                         // all 12 proper rotations: 120° turns about two bonds
    var start = C.TETRA.map(C.mirror), queue = [start], seen = {}, count = 0;
    function key(ds) { return ds.map(C.nearest).join(""); }
    seen[key(start)] = 1;
    while (queue.length) {
      var ds = queue.shift();
      count++;
      if (C.matchCount(groups, ds) === 4) return true;
      for (var ax = 0; ax < 2; ax++) {
        var nx = ds.map(function (v) { return C.rotateAbout(v, C.TETRA[ax], 120); }), k = key(nx);
        if (!seen[k]) { seen[k] = 1; queue.push(nx); }
      }
    }
    C._lastOrbit = count;
    return false;
  };
  C.chiral = function (groups) { var s = {}; groups.forEach(function (g) { s[g] = 1; }); return Object.keys(s).length === 4; };

  // ---- MO diagrams: aufbau over the levels, Hund's rule inside a degenerate level, at most 2 per orbital
  C.moFill = function (orders, type, n) {
    var left = n, levels = [];
    orders[type].forEach(function (o) {
      var deg = o[2], k = Math.min(left, 2 * deg), boxes = [], e;
      left -= k;
      for (e = 0; e < deg; e++) boxes.push(0);
      for (e = 0; e < k; e++) boxes[e % deg]++;
      levels.push({ name: o[0], bonding: o[1], boxes: boxes, n: k });
    });
    if (left > 0) return null;
    var b = 0, a = 0, unp = 0;
    levels.forEach(function (L) { L.boxes.forEach(function (x) { if (L.bonding) b += x; else a += x; if (x === 1) unp++; }); });
    return { levels: levels, bonding: b, antibonding: a, bo: (b - a) / 2, unpaired: unp,
      config: levels.filter(function (L) { return L.n; }).map(function (L) { return "(" + L.name + ")" + L.n; }).join("") };
  };
  C.moCapacity = function (orders, type) { return orders[type].reduce(function (t, o) { return t + 2 * o[2]; }, 0); };
  C.moCharges = function (sp, orders) {
    var cap = C.moCapacity(orders, sp.order), V = sp.valence[0] + sp.valence[1], out = [];
    for (var q = -2; q <= 2; q++) if (V - q >= 1 && V - q <= cap) out.push(q);
    return out;
  };
  C.moHTML = function (name) { var m = name.match(/^([σπ]\*?)(\w+)$/); return m ? m[1] + "<sub>" + m[2] + "</sub>" : name; };
  C.configHTML = function (fill) {
    return fill.levels.filter(function (L) { return L.n; }).map(function (L) { return "(" + C.moHTML(L.name) + ")<sup>" + L.n + "</sup>"; }).join("");
  };
  C.boText = function (x) { return Math.abs(x - Math.round(x)) < 1e-9 ? String(Math.round(x)) : (Math.round(x * 10) / 10).toFixed(1); };

  /* ================================================================ 3-D drawing (browser and node: strings only) */
  C.rotate = function (v, yaw, pitch) {                           // turn about y (yaw), then tilt about x (pitch)
    var a = yaw * RAD, b = pitch * RAD, ca = Math.cos(a), sa = Math.sin(a), cb = Math.cos(b), sb = Math.sin(b);
    var x = v[0] * ca + v[2] * sa, z = -v[0] * sa + v[2] * ca, y = v[1];
    return [x, y * cb - z * sb, y * sb + z * cb];
  };
  var ATOM = { H: "#FFFFFF", C: "#3A3F47", N: "#2F5DB8", O: "#C8332B", F: "#5FA83A", Cl: "#1E7A3C", Br: "#8B3A1A", I: "#6B3FA0",
    S: "#D9A51A", P: "#E07B00", B: "#E8A07A", Be: "#8FB35A", Xe: "#2B8C9E", A: "#5B6472", X: "#C3CAD4", G: "#E4E7EC" };
  var LP_FILL = "rgba(123,91,214,0.26)", LP_LINE = "#6A4BC4", BOND = "#8A94A3", HYB = "#1baf7a", PORB = "#2a78d6";
  function f1(x) { return (Math.round(x * 10) / 10).toFixed(1); }
  function halo(extra) { return " style='paint-order:stroke;stroke:#FCFCFB;stroke-width:4px;stroke-linejoin:round" + (extra ? ";" + extra : "") + "'"; }
  function ink(hex) { return U && U.inkOn ? U.inkOn(hex) : "#17212E"; }
  function slerp(u, v, t) {
    var om = C.angle(u, v) * RAD, s = Math.sin(om);
    if (s < 1e-6) {                                               // 180°: go round through a perpendicular
      var w = len(cross(u, [0, 0, 1])) > 0.1 ? unit(cross([0, 0, 1], u)) : unit(cross([0, 1, 0], u));
      return unit(addv(mul(u, Math.cos(t * Math.PI)), mul(w, Math.sin(t * Math.PI))));
    }
    return addv(mul(u, Math.sin((1 - t) * om) / s), mul(v, Math.sin(t * om) / s));
  }
  /* o: {s, cx, cy, yaw, pitch, atoms:[{p, el, label, r, fill, ring}], bonds:[{a, b, order}], lobes:[{at, dir, len, w, fill,
     line, dots, dash}], arrows:[{p0, p1, col, w, cross, dash, off, label}], arcs:[{c, u, v, r, label}]} -> SVG markup */
  C.scene = function (o) {
    var items = [], top = [];
    function P(v) { var r = C.rotate(v, o.yaw, o.pitch); return { x: o.cx + o.s * r[0], y: o.cy - o.s * r[1], z: r[2] }; }
    (o.bonds || []).forEach(function (b) {
      var A = P(b.a), B = P(b.b), dx = B.x - A.x, dy = B.y - A.y, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
      var f = 1 + 0.1 * (A.z + B.z) / 2, col = b.col || BOND, g = "", offs, w;
      if (b.order === 3) { offs = [-6, 0, 6]; w = 3; } else if (b.order === 2) { offs = [-4.2, 4.2]; w = 3.6; } else if (b.order === 1.5) { offs = [-3.6, 3.6]; w = 3.6; } else { offs = [0]; w = 6.5; }
      offs.forEach(function (k, i) {
        g += "<line x1='" + f1(A.x + nx * k) + "' y1='" + f1(A.y + ny * k) + "' x2='" + f1(B.x + nx * k) + "' y2='" + f1(B.y + ny * k) + "' style='stroke:" + col +
          ";stroke-width:" + f1(w * f) + ";stroke-linecap:round" + (b.order === 1.5 && i === 1 ? ";stroke-dasharray:5 5" : "") + "'/>";
      });
      items.push({ z: Math.min(A.z, B.z) - 0.001, svg: g });      // behind both of its atoms: each sphere covers its own end
    });
    (o.lobes || []).forEach(function (l) {
      var st0 = l.start === undefined ? 0.14 : l.start, A = P(addv(l.at, mul(l.dir, st0))), T = P(addv(l.at, mul(l.dir, st0 + l.len))), M = P(addv(l.at, mul(l.dir, st0 + l.len * 0.5)));
      var dx = T.x - A.x, dy = T.y - A.y, proj = Math.hypot(dx, dy) / (o.s * l.len), th = Math.atan2(dy, dx) / RAD;
      var rx = o.s * l.len * (0.2 + 0.3 * proj), ry = o.s * (l.w || 0.17), g = "<g transform='rotate(" + f1(th) + " " + f1(M.x) + " " + f1(M.y) + ")'>" +
        "<ellipse cx='" + f1(M.x) + "' cy='" + f1(M.y) + "' rx='" + f1(rx) + "' ry='" + f1(ry) + "' style='fill:" + (l.fill || LP_FILL) + ";stroke:" + (l.line || LP_LINE) + ";stroke-width:1.2" + (l.dash ? ";stroke-dasharray:4 3" : "") + "'/>";
      if (l.dots === 2) g += "<circle cx='" + f1(M.x) + "' cy='" + f1(M.y - 4) + "' r='2.4' style='fill:#17212E'/><circle cx='" + f1(M.x) + "' cy='" + f1(M.y + 4) + "' r='2.4' style='fill:#17212E'/>";
      else if (l.dots === 1) g += "<circle cx='" + f1(M.x) + "' cy='" + f1(M.y) + "' r='2.4' style='fill:#17212E'/>";
      g += "</g>";
      if (l.label) g += "<text class='direct-label' x='" + f1(T.x + (dx >= 0 ? 6 : -6)) + "' y='" + f1(T.y + (dy >= 0 ? 12 : -4)) + "' text-anchor='" + (dx >= 0 ? "start" : "end") + "'" + halo() + ">" + l.label + "</text>";
      items.push({ z: P(l.at).z - 0.002, svg: g });                // behind its own atom, so the symbol stays readable
    });
    (o.atoms || []).forEach(function (a) {
      var A = P(a.p), f = 1 + 0.12 * A.z, r = (a.r || 15) * f, fill = a.fill || ATOM[a.el] || ATOM.G, txt = a.label === undefined ? a.el : a.label;
      var fs = (txt.length > 2 ? 10 : txt.length === 2 ? 12.5 : 14) * Math.min(1.15, f);
      var g = (a.ring ? "<circle cx='" + f1(A.x) + "' cy='" + f1(A.y) + "' r='" + f1(r + 4) + "' style='fill:none;stroke:" + a.ring + ";stroke-width:2.5'/>" : "") +
        "<circle cx='" + f1(A.x) + "' cy='" + f1(A.y) + "' r='" + f1(r) + "' style='fill:" + fill + ";stroke:#17212E;stroke-width:1'/>" +
        "<text x='" + f1(A.x) + "' y='" + f1(A.y + fs * 0.36) + "' text-anchor='middle' style='fill:" + ink(fill) + ";font-size:" + f1(fs) + "px;font-weight:600'>" + txt + "</text>";
      items.push({ z: A.z, svg: g });
    });
    (o.arrows || []).forEach(function (w) {
      var A = P(w.p0), B = P(w.p1), dx = B.x - A.x, dy = B.y - A.y, L = Math.hypot(dx, dy);
      if (L < 2) return;
      var ux = dx / L, uy = dy / L, nx = -uy, ny = ux, k = w.off || 0, x0 = A.x + nx * k, y0 = A.y + ny * k, x1 = B.x + nx * k, y1 = B.y + ny * k;
      var hw = (w.w || 2.5) * 2.2 + 2, hl = hw * 1.5, bx = x1 - ux * hl, by = y1 - uy * hl, g = "";
      g += "<line x1='" + f1(x0) + "' y1='" + f1(y0) + "' x2='" + f1(bx) + "' y2='" + f1(by) + "' style='stroke:" + w.col + ";stroke-width:" + (w.w || 2.5) + (w.dash ? ";stroke-dasharray:5 4" : "") + "'/>" +
        "<path d='M" + f1(x1) + " " + f1(y1) + " L" + f1(bx + nx * hw / 2) + " " + f1(by + ny * hw / 2) + " L" + f1(bx - nx * hw / 2) + " " + f1(by - ny * hw / 2) + " Z' style='fill:" + w.col + "'/>";
      if (w.cross) { var cx = x0 + ux * Math.min(10, L * 0.25), cy = y0 + uy * Math.min(10, L * 0.25); g += "<line x1='" + f1(cx + nx * 6) + "' y1='" + f1(cy + ny * 6) + "' x2='" + f1(cx - nx * 6) + "' y2='" + f1(cy - ny * 6) + "' style='stroke:" + w.col + ";stroke-width:" + (w.w || 2.5) + "'/>"; }
      if (w.label) g += "<text class='direct-label strong' x='" + f1(x1 + nx * 12 + ux * 6) + "' y='" + f1(y1 + ny * 12 + uy * 6 + 4) + "' text-anchor='middle'" + halo() + ">" + w.label + "</text>";
      top.push(g);
    });
    (o.arcs || []).forEach(function (ac) {
      var pts = [], i, r = ac.r || 0.36;
      for (i = 0; i <= 16; i++) { var q = P(addv(ac.c, mul(slerp(unit(ac.u), unit(ac.v), i / 16), r))); pts.push([q.x, q.y]); }
      var mid = P(addv(ac.c, mul(slerp(unit(ac.u), unit(ac.v), 0.5), r + 0.2)));
      top.push("<path d='" + U.linePath(pts) + "' style='fill:none;stroke:#17212E;stroke-width:1.3'/>" +
        "<text class='direct-label strong' x='" + f1(mid.x) + "' y='" + f1(mid.y + 4) + "' text-anchor='middle'" + halo() + ">" + ac.label + "</text>");
    });
    items.sort(function (a, b) { return a.z - b.z; });
    return items.map(function (x) { return x.svg; }).join("") + top.join("");
  };

  /* ================================================================ shared view helpers (browser only) */
  var el = U && U.el;
  function tag(t) {
    return t === "lecture" ? "<span class='pill-label lecture'>Lecture example</span>" :
      t === "textbook" ? "<span class='pill-label preview'>Textbook example</span>" : "<span class='pill-label'>New example</span>";
  }
  function srcText(p) { return p.src ? " <span class='source-inline'>(" + p.src + ")</span>" : ""; }
  function degText(v) { return (v < 0 ? MINUS : "") + Math.abs(v) + "°"; }
  function angleText(v) { return (Math.abs(v - Math.round(v)) < 0.05 ? String(Math.round(v)) : v.toFixed(1)) + "°"; }
  // two view sliders plus drag-to-turn on the drawing
  function viewControls(ui, tid, st, redraw) {
    var yaw = U.slider(ui.controls, { label: "Turn left or right", testid: tid + "-yaw", min: -180, max: 180, step: 5, value: st.yaw, format: degText, onInput: function (v) { st.yaw = v; redraw(); } });
    var pitch = U.slider(ui.controls, { label: "Tilt toward you", testid: tid + "-pitch", min: -90, max: 90, step: 5, value: st.pitch, format: degText, onInput: function (v) { st.pitch = v; redraw(); } });
    var drag = null;
    ui.view.style.touchAction = "pan-y";
    ui.view.addEventListener("pointerdown", function (e) {
      if (e.button !== 0 || !e.target.closest || !e.target.closest("svg")) return;
      drag = { x: e.clientX, y: e.clientY, yaw: st.yaw, pitch: st.pitch };
      if (ui.view.setPointerCapture) ui.view.setPointerCapture(e.pointerId);
    });
    ui.view.addEventListener("pointermove", function (e) {
      if (!drag) return;
      var y = drag.yaw + (e.clientX - drag.x) * 0.6, p = Math.max(-90, Math.min(90, drag.pitch + (e.clientY - drag.y) * 0.6));
      st.yaw = ((y + 540) % 360) - 180; st.pitch = p;
      yaw.set(Math.round(st.yaw)); pitch.set(Math.round(st.pitch));
      redraw();
    });
    function end() { drag = null; }
    ui.view.addEventListener("pointerup", end); ui.view.addEventListener("pointercancel", end);
    return { set: function (y, p) { st.yaw = y; st.pitch = p; yaw.set(y); pitch.set(p); } };
  }
  // electron spins as drawn arrows (font arrows render inconsistently): n = 0, 1 (up), or 2 (up and down)
  function spins(cx, cy, n) {
    function arrow(x, up) {
      var t = cy - 8, b = cy + 8, h = up ? t : b, k = up ? 4.5 : -4.5;
      return "<path d='M" + x + " " + (up ? b : t) + " V" + h + " M" + (x - 3.6) + " " + (h + k) + " L" + x + " " + h + " L" + (x + 3.6) + " " + (h + k) + "' style='fill:none;stroke:#17212E;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round'/>";
    }
    return n === 1 ? arrow(cx, true) : n === 2 ? arrow(cx - 5, true) + arrow(cx + 5, false) : "";
  }
  // a "your results so far" table: rows appear only for cases the student has already explored
  function seenTable(head, rows, empty) {
    return rows.length ? U.tableHTML(head, rows) : "<p class='table-note'>" + empty + "</p>";
  }
  function viewCaption(lobes) { return "<p class='xp-caption'>Drag the model or use the sliders to turn it." + (lobes ? " Purple lobes are lone pairs." : "") + "</p>"; }

  /* ================================================================ m20 / m21: VSEPR */
  mount.vsepr = function (host, D) {
    var V = D.ch5.vsepr, mode = host.getAttribute("data-mode") === "lone" ? "lone" : "bonds", tid = "vsepr-" + mode;
    var presets = V.presets.filter(function (p) { return p.mode === mode || p.mode === "both"; }), byKey = {};
    V.presets.forEach(function (p) { byKey[p.key] = p; });
    var st = mode === "lone" ? { sn: 4, lp: 1, preset: "NH3", showLP: true, axial: false, adjacent: false, yaw: 25, pitch: 15 }
      : { sn: 4, lp: 0, preset: "CCl4", showLP: true, axial: false, adjacent: false, yaw: 25, pitch: 15 };
    var ui = U.shell(host, mode === "lone" ? {
      title: "Explorer: lone pairs and molecular shape",
      intro: "Choose a steric number and how many of its electron pairs are lone pairs, or pick a molecule. Then hide the lone pairs: what is left is the molecular geometry, the atoms only.",
      source: "Source: Day 10 p.14–26 (ozone 117°, ammonia 107°, water 104.5°; SN 5 lone pairs go equatorial; SN 6 lone pairs sit opposite; the summary table). Textbook preview §5.2 and Table 5.1 (PDF p.237–243): counting 90° repulsions, SO₂, SF₄, BrF₃, XeF₂, BrF₅'s 85°, XeF₄. I₃⁻ is a new example. The 3-D drawing is this guide's rendering of the VSEPR shapes."
    } : {
      title: "Explorer: steric number and shape",
      intro: "Pick a steric number, or one of the lecture's molecules. Turn the model and compare its angles with the flat Lewis structure, which draws every bond at 90° or 180°.",
      source: "Source: Day 10 p.7–13 (steric number; the five shapes and their angles; CO₂, BF₃, CCl₄, PF₅, SF₆; formaldehyde's about 118°). Textbook §5.2, Fig. 5.3 (PDF p.234). The 3-D drawing is this guide's rendering of the VSEPR shapes."
    });
    U.radios(ui.controls, { label: "Steric number (SN)", testid: tid + "-sn", value: String(st.sn), options: [["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"], ["6", "6"]], onChange: function (v) {
      st.sn = +v; st.lp = Math.min(st.lp, C.MAXLP[st.sn]); st.preset = null; buildLP(); draw(); } });
    var lpBox = el("div"), togBox = el("div", { class: "xp-controls" });
    ui.controls.appendChild(lpBox); ui.controls.appendChild(togBox);
    var snRadios = host.querySelectorAll("input[name='rg-" + tid + "-sn']");
    function buildLP() {
      lpBox.innerHTML = ""; togBox.innerHTML = "";
      if (mode === "lone") {
        var opts = [];
        for (var k = 0; k <= C.MAXLP[st.sn]; k++) opts.push([String(k), String(k)]);
        U.radios(lpBox, { label: "Lone pairs on the central atom", testid: tid + "-lp", value: String(st.lp), options: opts, onChange: function (v) { st.lp = +v; st.preset = null; buildLP(); draw(); } });
        U.checkbox(togBox, { label: "Show the lone pairs", testid: tid + "-showlp", value: st.showLP, onChange: function (v) { st.showLP = v; draw(); } });
        if (st.sn === 5 && st.lp >= 1) U.checkbox(togBox, { label: "Put one lone pair in an axial position instead", testid: tid + "-axial", value: st.axial, onChange: function (v) { st.axial = v; st.preset = null; draw(); } });
        if (st.sn === 6 && st.lp === 2) U.checkbox(togBox, { label: "Put the two lone pairs next to each other (90° apart) instead of opposite", testid: tid + "-adjacent", value: st.adjacent, onChange: function (v) { st.adjacent = v; st.preset = null; draw(); } });
      }
      Array.prototype.forEach.call(snRadios, function (r) { r.checked = +r.value === st.sn; });
    }
    var view = viewControls(ui, tid, st, function () { draw(true); });
    U.presetButtons(ui, tid, presets.map(function (p) { return [p.label + (p.tag === "lecture" ? "" : p.tag === "textbook" ? " (textbook)" : " (new)"), p.key]; }), function (k) {
      var p = byKey[k]; st.preset = k; st.sn = p.sn; st.lp = p.lp; st.axial = false; st.adjacent = false; buildLP(); draw(); });

    function c90(c) { return (c.lplp ? c.lplp + " lone pair–lone pair and " : "") + c.lpbp + " lone pair–bond"; }
    function arcsFor(atoms, p, lp) {
      var pairs = [], seen = {}, i, j, out = [], vals = [];
      for (i = 1; i < atoms.length; i++) for (j = i + 1; j < atoms.length; j++) pairs.push([i, j, C.angle(atoms[i].p, atoms[j].p)]);
      if (p && p.angle) {
        // the stated angle, between two identical ligands (formaldehyde's H–C–H, not H–C=O)
        var hit = pairs.filter(function (q) { return Math.abs(q[2] - p.angle) < 0.6 && atoms[q[0]].el === atoms[q[1]].el; })[0];
        return hit ? [{ c: [0, 0, 0], u: atoms[hit[0]].p, v: atoms[hit[1]].p, label: angleText(p.angle) }] : [];
      }
      pairs.forEach(function (q) { var k = Math.round(q[2] * 10) / 10; if (!seen[k]) { seen[k] = q; vals.push(k); } });
      vals.sort(function (a, b) { return a - b; });
      var show = vals.length > 1 ? vals.filter(function (v) { return v !== 180; }) : vals;
      var exact = lp === 0 || (st.sn === 6 && lp === 2 && !st.adjacent) || (st.sn === 5 && lp === 3 && !st.axial);
      show.forEach(function (k) {
        var q = seen[k];
        out.push({ c: [0, 0, 0], u: atoms[q[0]].p, v: atoms[q[1]].p, label: (exact || k === 180 ? "" : st.sn === 6 && lp === 3 ? "≈ " : "&lt; ") + angleText(k) });
      });
      return out;
    }
    function draw(fast) {
      var p = st.preset ? byKey[st.preset] : null;
      var opt = { axial: st.axial && st.sn === 5 && st.lp >= 1, adjacent: st.adjacent && st.sn === 6 && st.lp === 2, angle: p ? p.angle : null };
      var info = C.shapeInfo(st.sn, st.lp, opt), d = info.domains;
      var atoms = [{ p: [0, 0, 0], el: p ? p.center : "A", r: 18 }], bonds = [], lobes = [], li = 0;
      d.dirs.forEach(function (v, i) {
        if (d.lp[i]) { if (mode === "bonds" || st.showLP) lobes.push({ at: [0, 0, 0], dir: v, len: 0.95, w: 0.2, dots: 2 }); return; }
        var e = p ? p.ligands[li] : "X", o = p ? p.orders[li] : 1;
        li++;
        atoms.push({ p: v, el: e, r: e === "H" ? 11 : 15 });
        bonds.push({ a: [0, 0, 0], b: v, order: o });
      });
      var arcs = arcsFor(atoms, p, st.lp), nAt = atoms.length - 1;
      var aria = (p ? p.label + ": " : "") + "steric number " + st.sn + ", " + nAt + " atom" + (nAt === 1 ? "" : "s") + " and " + st.lp + " lone pair" + (st.lp === 1 ? "" : "s") + "; " + (info.mg || "an arrangement that is not observed");
      ui.view.innerHTML = U.svgWrap(520, 330, aria, C.scene({ s: 108, cx: 260, cy: 168, yaw: st.yaw, pitch: st.pitch, atoms: atoms, bonds: bonds, lobes: lobes, arcs: arcs })) + viewCaption(lobes.length);
      if (fast) return;
      var who = p ? tag(p.tag) + " <strong>" + p.html + "</strong>" + srcText(p) + ": " : "";
      var count = "SN " + st.sn + " = " + nAt + " bonded atom" + (nAt === 1 ? "" : "s") + " + " + st.lp + " lone pair" + (st.lp === 1 ? "" : "s");
      var msg;
      if (!info.observed) {
        var pref = C.shapeInfo(st.sn, st.lp, {});
        msg = count + ". At 90° this arrangement has " + c90(info.contacts) + " contacts; the observed arrangement has " + c90(pref.contacts) + (info.contacts.lplp && !pref.contacts.lplp ? " (no lone pair–lone pair contacts)" : "") +
          ". Electron pairs 90° apart repel most, and two lone pairs most of all (textbook PDF p.238, p.241), so this arrangement is <strong>not observed</strong>: the observed shape is " + pref.mg + " (" + (st.sn === 5 ? "Day 10 p.22–23" : "Day 10 p.25") + ").";
      } else if (st.lp === 0) {
        msg = count + ": the electron-pair geometry and the molecular geometry are both <strong>" + info.epg + "</strong>.";
      } else {
        msg = count + ": electron-pair geometry <strong>" + info.epg + "</strong>; molecular geometry (atoms only) <strong>" + info.mg + "</strong>.";
        if (st.sn === 5) msg += " Lone pairs take equatorial positions: an equatorial lone pair has 2 neighbors at 90°, an axial one would have 3 (textbook PDF p.241).";
        if (st.sn === 6 && st.lp === 2) msg += " The two lone pairs sit opposite each other (Day 10 p.25).";
        if (st.sn === 6 && st.lp === 1) msg += " All six positions are equivalent, so it doesn't matter which one the lone pair takes (Day 10 p.24).";
      }
      if (mode === "lone" && st.lp && !st.showLP) msg += " Lone pairs hidden: what is left is the molecular geometry, which “describes relative positions of atoms only” (Day 10 p.14).";
      ui.readout.innerHTML = who + msg + (p ? " " + p.angleText.charAt(0).toUpperCase() + p.angleText.slice(1) + "." + (p.note ? " " + p.note : "") : "");
      var epAngles = { 2: "180°", 3: "120°", 4: "109.5°", 5: "120° and 90°", 6: "90°" }[st.sn];
      var kv = [["Steric number", st.sn], ["Bonded atoms + lone pairs", nAt + " + " + st.lp], ["Electron-pair geometry", info.epg], ["Molecular geometry", info.mg || "not observed"],
        ["Electron-pair angles (Day 10 p.26)", epAngles],
        [p && p.angle ? "Angles between bonded atoms (as drawn)" : "Angles between bonded atoms (ideal)", info.angles.map(function (a) { return angleText(a); }).join(", ") +
          (!(p && p.angle) && st.lp && info.observed && !(st.sn === 6 && st.lp === 2) && !(st.sn === 5 && st.lp === 3) ? "; lone pairs make the real angles smaller" : "")]];
      if (st.sn >= 5 && st.lp) kv.push(["Pairs at 90° to a lone pair", info.contacts.lplp + " lone pair, " + info.contacts.lpbp + " bonding"]);
      U.kvSet(ui.kv, kv);
      ui.table.innerHTML = U.tableHTML(["Number of electron domains", "Electron pair geometry", "# of lone pairs", "Molecular geometry", "Ideal bond angles"],
        V.profTable.map(function (r) { return r.map(String); })) +
        "<p class='table-note'>The professor's summary table, Day 10 p.26 (“See-saw” as printed). It has no row for SN 5 with 3 lone pairs (linear), which Day 10 p.23 shows. It lists SN 6 with 3 lone pairs as T-shaped, a case the textbook says we will not encounter (Table 5.1, PDF p.240). Its angle column gives the electron-pair angles; lone pairs make the real angles smaller (107°, 104.5°: Day 10 p.18–19).</p>";
    }
    buildLP();
    draw();
    view.set(st.yaw, st.pitch);
  };

  /* ================================================================ m22: polar molecules */
  mount.dipoles = function (host, D) {
    var M = D.ch5.dipoles, chi = D.ch5.chi, byKey = {}, seen = {}, st = { key: "H2O", net: false, yaw: 30, pitch: 16 };
    M.forEach(function (m) { byKey[m.key] = m; });
    var ui = U.shell(host, { title: "Explorer: polar bonds, polar molecules",
      intro: "Pick a molecule. Each arrow is a bond dipole pointing toward the more electronegative atom. Predict whether the arrows cancel, then show their vector sum.",
      source: "Source: Day 10 p.27–31 and Day 11 p.6–8 (CO₂, CF₄, H₂O; CHCl₃ and CCl₃F; Table 5.2's measured dipole moments); χ values from Day 9 p.17. Textbook §5.3 (PDF p.243–246): CH₂O, CH₂Cl₂, H₂S. The other molecules are new examples with their VSEPR shapes." });
    var sel = U.select(ui.controls, { label: "Molecule", testid: "dip-mol", value: st.key, options: M.map(function (m) { return [m.key, m.label + (m.tag === "lecture" ? "  (lecture)" : m.tag === "textbook" ? "  (textbook)" : "")]; }), onChange: function (v) { st.key = v; draw(); } });
    var cb = U.checkbox(ui.controls, { label: "Show the net dipole (the vector sum)", testid: "dip-net", value: st.net, onChange: function (v) { st.net = v; draw(); } });
    viewControls(ui, "dip", st, function () { draw(true); });
    U.presetButtons(ui, "dip", [["CO₂", "CO2"], ["CF₄", "CF4"], ["H₂O", "H2O"], ["CHCl₃", "CHCl3"], ["CCl₃F", "CCl3F"]], function (k) { st.key = k; sel.value = k; draw(); });
    function dirWords(m, r) {                                     // e.g. "toward the F atoms", "toward S"
      if (r.bonds.every(function (b) { return b.dchi < 0; })) return "toward " + m.center;
      var els = [], n = 0;
      r.bonds.forEach(function (b) { if (b.dchi > 0 && dot(b.dir, r.net) > 0) { n++; if (els.indexOf(b.el) < 0) els.push(b.el); } });
      return "toward the " + els.join(" and ") + (n > 1 ? " atoms" : " atom");
    }
    // Where to draw the net dipole: try spots along and beside its direction through the atoms' centroid (water's
    // lands between the H atoms, as on Day 10 p.31) and keep the first one clear of every atom, bond, and bond-dipole
    // arrow; otherwise draw it beside the molecule.
    function placeNet(r, atoms, bonds, arrows, K) {
      var S = 118, dir = unit(r.net), half = Math.max(0.3, len(r.net) * K * 0.6), cen = [0, 0, 0];
      atoms.forEach(function (a) { cen = addv(cen, mul(a.p, 1 / atoms.length)); });
      function scr(v) { var q = C.rotate(v, st.yaw, st.pitch); return [q[0] * S, -q[1] * S]; }
      function ptSeg(p, a, b) {
        var dx = b[0] - a[0], dy = b[1] - a[1], L2 = dx * dx + dy * dy || 1, t = Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2));
        return Math.hypot(p[0] - a[0] - dx * t, p[1] - a[1] - dy * t);
      }
      function cross2(a, b, c) { return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]); }
      function segSeg(a, b, c, d) {
        if (cross2(a, b, c) * cross2(a, b, d) < 0 && cross2(c, d, a) * cross2(c, d, b) < 0) return 0;
        return Math.min(ptSeg(a, c, d), ptSeg(b, c, d), ptSeg(c, a, b), ptSeg(d, a, b));
      }
      function offset(seg, k) {
        var dx = seg[1][0] - seg[0][0], dy = seg[1][1] - seg[0][1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
        return [[seg[0][0] + nx * k, seg[0][1] + ny * k], [seg[1][0] + nx * k, seg[1][1] + ny * k]];
      }
      var obstacles = bonds.map(function (b) { return [scr(b.a), scr(b.b)]; }).concat(arrows.map(function (w) { return offset([scr(w.p0), scr(w.p1)], w.off || 0); }));
      var tries = [], sh = [-0.35, 0.35, 0, -0.7], ks = [0, 28, -28, 52, -52];
      sh.forEach(function (a) { ks.forEach(function (k) { tries.push([a, k]); }); });
      for (var i = 0; i < tries.length; i++) {
        var c = addv(cen, mul(dir, tries[i][0])), p0 = addv(c, mul(dir, -half)), p1 = addv(c, mul(dir, half)), seg = offset([scr(p0), scr(p1)], tries[i][1]);
        var clear = atoms.every(function (a) { return ptSeg(scr(a.p), seg[0], seg[1]) > (a.r || 15) + 6; }) &&
          obstacles.every(function (o) { return segSeg(seg[0], seg[1], o[0], o[1]) > 8; });
        if (clear) return { p0: p0, p1: p1, col: U.SERIES[1], w: 4, cross: true, off: tries[i][1], label: "net" };
      }
      var right = -1e9;                                             // beside the molecule, on the right
      atoms.forEach(function (a) { right = Math.max(right, C.rotate(a.p, st.yaw, st.pitch)[0]); });
      var m3 = C.rotate(C.rotate([right + 0.75, 0, 0], 0, -st.pitch), -st.yaw, 0);   // undo the tilt, then the turn
      return { p0: addv(m3, mul(dir, -half)), p1: addv(m3, mul(dir, half)), col: U.SERIES[1], w: 4, cross: true, off: 0, label: "net" };
    }
    function draw(fast) {
      var m = byKey[st.key], r = C.dipole(m, chi), d = r.domains, K = 0.42;
      var atoms = [{ p: [0, 0, 0], el: m.center, r: m.center === "H" ? 11 : 17 }], bonds = [], lobes = [], arrows = [], li = 0;
      var shift = m.sn === 1 ? [-0.5, 0, 0] : [0, 0, 0];
      atoms[0].p = shift;
      d.dirs.forEach(function (v, i) {
        if (d.lp[i]) { lobes.push({ at: shift, dir: v, len: 0.85, w: 0.18, dots: 2 }); return; }
        var b = r.bonds[li++], end = addv(shift, v);
        atoms.push({ p: end, el: b.el, r: b.el === "H" ? 11 : 15 });
        bonds.push({ a: shift, b: end, order: b.order });
        var dc = b.dchi === null ? 0.9 : b.dchi;                   // unknown χ (Xe): equal arrows of nominal length
        if (Math.abs(dc) > 1e-9) {
          var mid = addv(shift, mul(v, 0.5)), half = mul(v, Math.abs(dc) * K / 2);
          var p0 = dc > 0 ? addv(mid, mul(half, -1)) : addv(mid, half), p1 = dc > 0 ? addv(mid, half) : addv(mid, mul(half, -1));
          arrows.push({ p0: p0, p1: p1, col: U.SERIES[0], w: 2.4, cross: true, off: 13, dash: b.dchi === null });
        }
      });
      if (st.net && r.mag > 1e-6) arrows.push(placeNet(r, atoms, bonds, arrows, K));
      var aria = m.label + ": " + r.bonds.map(function (b) { return m.center + "–" + b.el + " bond dipole " + (b.dchi === null ? "of unknown size" : "Δχ " + Math.abs(b.dchi).toFixed(1)); }).join("; ") + (st.net ? "; " + (r.polar ? "net dipole present" : "bond dipoles cancel") : "");
      ui.view.innerHTML = U.svgWrap(520, 320, aria, C.scene({ s: 118, cx: 260, cy: 160, yaw: st.yaw, pitch: st.pitch, atoms: atoms, bonds: bonds, lobes: lobes, arrows: arrows })) +
        "<div class='legend-row'><span class='lg'><span class='lg-sw' style='background:" + U.SERIES[0] + "'></span>bond dipole (length ∝ Δχ)</span>" + (st.net ? "<span class='lg'><span class='lg-sw' style='background:" + U.SERIES[1] + ";height:6px'></span>net dipole</span>" : "") + "</div>" +
        "<p class='xp-caption'>Arrow lengths use Δχ as a stand-in for each bond dipole (a background model). It predicts the direction and whether the arrows cancel, not the size of the dipole moment: CCl₃F's arrows add up to more than CHCl₃'s, yet Table 5.2 gives 0.45 D and 1.01 D (Day 11 p.8).</p>";
      if (fast) return;
      var bondTxt = [], listed = {};
      r.bonds.forEach(function (b) { var k = m.center + "–" + b.el; if (listed[k]) return; listed[k] = 1; bondTxt.push(k + (b.dchi === null ? ": no χ for " + m.center + " in the course table" : ": Δχ = " + Math.abs(b.dchi).toFixed(1) + (Math.abs(b.dchi) <= 0.4 ? " (essentially nonpolar)" : ""))); });
      var who = tag(m.tag) + " <strong>" + m.html + "</strong>" + srcText(m) + ". ";
      var mu = m.mu !== null ? "Measured: μ = " + m.mu.toFixed(2) + " D (" + m.muSrc + ")." : "";
      var msg;
      if (!st.net) msg = "Predict first: do these bond dipoles cancel? Then switch on “Show the net dipole”.";
      else if (r.unknown) msg = "<strong>Nonpolar</strong>: the course table gives no χ for Xe, but the four Xe–F bond dipoles are identical and point to the corners of a square, so they cancel whatever their size (the lone pairs above and below the square cancel too).";
      else if (!r.polar) msg = "<strong>Nonpolar</strong>: each bond is polar, but the bond dipoles are perfectly opposed and cancel" + (m.key === "CO2" ? " (Day 10 p.29)" : m.key === "CF4" ? " (Day 10 p.30)" : "") + ".";
      else msg = "<strong>Polar</strong>: the bond dipoles don't cancel, so the molecule has a net dipole" + (m.dir ? ", pointing " + m.dir + ". " : "; in this model it points " + dirWords(m, r) + ". ") + mu + (m.key === "H2O" ? " (Day 10 p.31: “the dipole moments are not perfectly opposed.”)" : "");
      if (st.net && !r.polar && m.mu === null && !r.unknown) msg += " Its dipole moment is 0.";
      ui.readout.innerHTML = who + msg;
      U.kvSet(ui.kv, [["Shape", (m.sn === 1 ? "diatomic" : (m.lp ? C.MG[m.sn + "-" + m.lp] : C.EPG[m.sn]))], ["Bonds", bondTxt.join("; ")],
        ["Sum of the Δχ arrows", st.net ? (r.unknown ? "0 by symmetry" : r.mag.toFixed(2) + " (model units)") : "?"], ["Measured μ", m.mu !== null ? m.mu.toFixed(2) + " D" : "not given in the course materials"]]);
      if (st.net) seen[m.key] = 1;
      ui.table.innerHTML = seenTable(["Molecule", "Shape", "Sum of Δχ arrows (model)", "Polar?", "Measured μ (D)"], M.filter(function (x) { return seen[x.key]; }).map(function (x) {
        var q = C.dipole(x, chi); return [x.html, x.sn === 1 ? "diatomic" : x.lp ? C.MG[x.sn + "-" + x.lp] : C.EPG[x.sn], q.unknown ? "0 (symmetry)" : q.mag.toFixed(2), q.polar ? "polar" : "nonpolar", x.mu !== null ? x.mu.toFixed(2) : "—"]; }),
        "Each molecule you check with “Show the net dipole” is added here.") +
        "<p class='table-note'>Measured values: Table 5.2 (Day 11 p.8) and the textbook's H₂S value (PDF p.246). Only the direction and the cancellation come from the model.</p>";
      cb.checked = st.net;
    }
    draw();
  };

  /* ================================================================ m23: hybrid orbitals */
  mount.hybrid = function (host, D) {
    var H = D.ch5.hybrid, byKey = {}, seen = {}, st = { key: "C-CH4", stage: "ground", promote: false };
    H.forEach(function (h) { byKey[h.key] = h; });
    var ui = U.shell(host, { title: "Explorer: hybrid orbitals, box by box",
      intro: "Pick an atom in a molecule. Start from its ground-state boxes, mix the orbitals it needs (one hybrid per electron domain), then see which orbitals hold lone pairs, make σ bonds, and make π bonds.",
      source: "Source: Day 11 p.9–25 (valence bond theory; the methane problem, p.11; hybridization, p.12–16; CH₂O, N₂H₂, C₂H₂, C₂H₄, p.18–25; the rules, p.20). Textbook §5.4 (PDF p.247–253): CO₂ (Sample Ex. 5.5). BF₃, BeCl₂, PCl₃, and HCN are new examples worked with the same rules. The orbital sketch is schematic, not to scale." });
    var sel = U.select(ui.controls, { label: "Atom", testid: "hyb-atom", value: st.key, options: H.map(function (h) { return [h.key, h.label + (h.tag === "lecture" ? "  (lecture)" : h.tag === "textbook" ? "  (textbook)" : "")]; }), onChange: function (v) { st.key = v; st.promote = false; draw(); } });
    var stageR = U.radios(ui.controls, { label: "Step", testid: "hyb-stage", value: st.stage, options: [["ground", "1. the ground-state atom"], ["mix", "2. hybridize: mix orbitals"], ["bond", "3. make the bonds"]], onChange: function (v) { st.stage = v; draw(); } });
    var promoBox = el("div"); ui.controls.appendChild(promoBox);
    U.presetButtons(ui, "hyb", [["C in CH₄", "C-CH4"], ["N in NH₃", "N-NH3"], ["O in H₂O", "O-H2O"], ["C in CH₂O", "C-CH2O"], ["C in C₂H₂", "C-C2H2"]], function (k) { st.key = k; sel.value = k; st.promote = false; draw(); });
    function boxes(x, y, list, labels, cls) {
      var g = "";
      list.forEach(function (n, i) {
        var bx = x + i * 46;
        g += "<rect x='" + bx + "' y='" + y + "' width='40' height='30' rx='2' style='fill:" + (cls === "hyb" ? "#E3F5EC" : cls === "p" ? "#E4EEFA" : cls === "s" ? "#FFF2C2" : "#FFFFFF") + ";stroke:#17212E;stroke-width:1.2'/>" +
          spins(bx + 20, y + 15, n);
        if (labels && labels[i]) g += "<text class='direct-label' x='" + (bx + 20) + "' y='" + (y + 44) + "' text-anchor='middle'>" + labels[i][0] + "</text>" + (labels[i][1] ? "<text class='direct-label' x='" + (bx + 20) + "' y='" + (y + 56) + "' text-anchor='middle'>" + labels[i][1] + "</text>" : "");
      });
      return g;
    }
    function sup(k) { return k === "sp" ? "sp" : "sp<tspan class='sup' dy='-6'>" + k.slice(2) + "</tspan><tspan dy='6'>​</tspan>"; }
    function draw() {
      var h = byKey[st.key], r = C.hybridize(h), n = h.shell, W = 560, Hh = 300, g = "";
      var canPromote = r.unpairedGround < r.bonds;
      promoBox.innerHTML = "";
      if (canPromote) U.checkbox(promoBox, { label: "Why not promote an electron instead?", testid: "hyb-promote", value: st.promote, onChange: function (v) { st.promote = v; draw(); } });
      else st.promote = false;
      // energy axis
      g += "<line x1='22' y1='250' x2='22' y2='40' style='stroke:#6B7686;stroke-width:1.2'/><path d='M22 34 l-5 9 h10 z' style='fill:#6B7686'/>" +
        "<text class='axis-label' transform='translate(14 150) rotate(-90)' text-anchor='middle'>energy</text>";
      // ground state
      var gs = r.ground, yS = 210, yP = 110;
      g += "<text class='direct-label strong' x='40' y='28'>" + h.el + " atom" + (st.promote ? ", one 2s electron promoted" : ", ground state") + "</text>";
      var sCount = st.promote ? gs[0] - 1 : gs[0], pList = gs.slice(1);
      if (st.promote) { var moved = false; pList = pList.map(function (x) { if (!moved && x === 0) { moved = true; return 1; } return x; }); }
      g += boxes(40, yS, [sCount], [[n + "s", ""]], "s") + boxes(110, yP, pList, [["", ""], [n + "p", ""], ["", ""]], "p");
      if (st.stage !== "ground") {
        g += "<path d='M268 160 h44' style='stroke:#17212E;stroke-width:1.6'/><path d='M318 160 l-9 -5 v10 z' style='fill:#17212E'/>" +
          "<text class='direct-label strong' x='290' y='150' text-anchor='middle'>hybridize</text>";
        var yH = r.hyb === "sp3" ? 150 : r.hyb === "sp2" ? 156 : 162;
        var roleLab = r.roles.map(function (q) { return q.kind === "lp" ? ["lone", "pair"] : ["σ with", q.partner.orb.replace(/sp([23])/, function (_, d) { return "sp" + (d === "2" ? "²" : "³"); })]; });
        var pLab = r.proles.map(function (q) { return q.kind === "pi" ? ["π with", q.partner.el + " p"] : ["empty", ""]; });
        g += "<text class='direct-label strong' x='330' y='" + (yH - 10) + "'>" + r.hybrids.length + " " + sup(r.hyb) + " hybrid" + (r.hybrids.length > 1 ? "s" : "") + "</text>" + boxes(330, yH, r.hybrids, st.stage === "bond" ? roleLab : null, "hyb");
        if (r.unhybridized.length) g += "<text class='direct-label strong' x='" + (330 + r.hybrids.length * 46 + 14) + "' y='" + (yP - 10) + "'>unhybridized " + n + "p</text>" + boxes(330 + r.hybrids.length * 46 + 14, yP, r.unhybridized, st.stage === "bond" ? pLab : null, "p");
      }
      var aria = h.label + ": ground state " + n + "s" + gs[0] + " " + n + "p" + (gs[1] + gs[2] + gs[3]) + (st.stage !== "ground" ? "; " + r.hybrids.length + " " + C.hybText(r.hyb) + " hybrid orbitals holding " + r.hybrids.join(", ") + " electrons" + (r.unhybridized.length ? "; " + r.unhybridized.length + " unhybridized p orbitals holding " + r.unhybridized.join(", ") : "") : "");
      var sketch = st.stage === "ground" ? "" : U.svgWrap(560, 250, "Sketch of the " + C.hybText(r.hyb) + " hybrid orbitals" + (r.unhybridized.length ? " and the unhybridized p orbitals" : ""), orbitalSketch(h, r));
      ui.view.innerHTML = U.svgWrap(W, Hh, aria, g) + sketch + (st.stage === "bond" ? "<div class='lw-row'>" + h.lewis + "</div>" : "") +
        (st.stage !== "ground" ? "<p class='xp-caption'>Boxes colored as on the slides (Day 11 p.13): gold 2s, blue 2p, green hybrids. In the sketch, green: hybrid orbitals; blue: unhybridized p orbitals (a filled blue lobe holds one electron for a π bond; an outline is empty). Sketch not to scale.</p>" : "");
      var hy = C.hybHTML(r.hyb), mixes = r.hyb === "sp3" ? "one " + n + "s + three " + n + "p" : r.hyb === "sp2" ? "one " + n + "s + two " + n + "p" : "one " + n + "s + one " + n + "p";
      var msg;
      if (st.promote) msg = "Promoting a " + n + "s electron gives " + (r.unpairedGround + 2) + " unpaired electrons, but in orbitals of different shapes and directions: one spherical " + n + "s and " + n + "p orbitals at 90° to each other. Bonds made from them would not be equivalent. For methane the professor's verdict: “that's not what methane <strong>looks</strong> like! We need four equivalent bonds pointing to the vertices of a tetrahedron!” (Day 11 p.11). Hybridization mixes the orbitals instead (Day 11 p.12–13); the textbook never uses a promotion step (PDF p.247–248).";
      else if (st.stage === "ground") msg = h.el + " has " + (h.s + h.p) + " valence electrons: " + n + "s<sup>" + h.s + "</sup>" + (h.p ? " " + n + "p<sup>" + h.p + "</sup>" : "") + ", with " + r.unpairedGround + " unpaired. " + (canPromote ? "But " + h.el + " makes " + r.bonds + " bonds here. How?" : "It makes " + r.bonds + " bond" + (r.bonds > 1 ? "s" : "") + " here (" + h.sigma.length + " σ" + (h.pi.length ? " + " + h.pi.length + " π" : "") + ").");
      else if (st.stage === "mix") msg = "SN of " + h.el + " = " + h.sigma.length + " bonded atom" + (h.sigma.length > 1 ? "s" : "") + " + " + h.lp + " lone pair" + (h.lp === 1 ? "" : "s") + " = " + h.sn + ", so it needs " + h.sn + " hybrid orbitals (“the number of hybridized orbitals equals the steric number of the atom”, Day 11 p.12): mix " + mixes + " → " + h.sn + " " + hy + " orbitals" + (r.unhybridized.length ? ", leaving " + r.unhybridized.length + " " + n + "p unhybridized" : "") + ". The same " + (h.s + h.p) + " electrons go into the new boxes.";
      else msg = "Lone pairs sit in hybrid orbitals; each σ bond is a head-on overlap of a hybrid with the partner's orbital (H uses its 1s); each π bond is a side-to-side overlap of unhybridized p orbitals (Day 11 p.20). " + h.el + " in " + h.molecule + ": " + h.sigma.length + " σ bond" + (h.sigma.length > 1 ? "s" : "") + (h.pi.length ? ", " + h.pi.length + " π bond" + (h.pi.length > 1 ? "s" : "") : "") + (h.lp ? ", " + h.lp + " lone pair" + (h.lp > 1 ? "s" : "") : "") + (r.unhybridized.indexOf(0) >= 0 ? "; its empty p orbital" + (r.unhybridized.filter(function (x) { return x === 0; }).length > 1 ? "s stay" : " stays") + " empty (" + h.el + " has fewer than eight valence electrons here)" : "") + ".";
      ui.readout.innerHTML = tag(h.tag) + " " + h.label + srcText(h) + ". " + msg;
      U.kvSet(ui.kv, [["Steric number", h.sn], ["Hybridization", hy], ["Hybrid orbitals", h.sn], ["Unhybridized p orbitals", 4 - h.sn], ["σ bonds", h.sigma.length], ["π bonds", h.pi.length], ["Lone pairs", h.lp]]);
      if (st.stage !== "ground") seen[h.key] = 1;
      ui.table.innerHTML = seenTable(["Atom", "SN", "Hybridization", "Geometry of the hybrids", "Angle between hybrids"], H.filter(function (x) { return seen[x.key]; }).map(function (x) {
        return [x.label, x.sn, C.hybHTML(C.HYB[x.sn]), C.EPG[x.sn], { 2: "180°", 3: "120°", 4: "109.5°" }[x.sn]]; }), "Each atom you hybridize (step 2 or 3) is added here.") +
        "<p class='table-note'>Hybridization based on steric number: SN 2 sp, SN 3 sp<sup>2</sup>, SN 4 sp<sup>3</sup> (Day 11 p.24, Table 5.3; the slide's sp<sup>3</sup> row says “Trigonal planar” for 3 σ bonds, where the textbook's Table 5.3 and Day 10 p.18 say trigonal pyramidal).</p>";
      stageR.set(st.stage);
    }
    function orbitalSketch(h, r) {
      var d = C.domains(h.sn, 0, {}).dirs, lobes = [], atoms = [{ p: [0, 0, 0], el: h.el, r: 15 }], bondsArr = [];
      var pAxes = h.sn === 2 ? [[0, 1, 0], [0, 0, 1]] : h.sn === 3 ? [[0, 0, 1]] : [];
      // lone pairs on the upper hybrids (as the slides draw NH3 and H2O), σ bonds on the others
      var order = h.sn === 4 && h.lp === 2 ? [2, 3, 0, 1] : d.map(function (_, i) { return i; });
      if (h.sn === 4 && h.lp === 2) d = C.domains(4, 2, {}).dirs;
      r.roles.forEach(function (q, k) {
        var v = d[order[k]];
        if (q.kind === "lp") lobes.push({ at: [0, 0, 0], dir: v, len: 0.95, w: 0.2, fill: "rgba(27,175,122,0.30)", line: "#127A55", dots: st.stage === "bond" ? 2 : 0, label: st.stage === "bond" ? "lone pair" : "" });
        else {
          lobes.push({ at: [0, 0, 0], dir: v, len: 0.95, w: 0.2, fill: "rgba(27,175,122,0.30)", line: "#127A55", dots: st.stage === "bond" ? 1 : 0 });
          if (st.stage === "bond") { var pe = mul(v, 1.32); atoms.push({ p: pe, el: q.partner.el, r: q.partner.el === "H" ? 11 : 14 }); }
        }
      });
      pAxes.forEach(function (ax, k) {
        var e = r.unhybridized[k], col = e ? "rgba(42,120,214,0.34)" : "rgba(255,255,255,0.6)";
        [ax, mul(ax, -1)].forEach(function (v) { lobes.push({ at: [0, 0, 0], dir: v, len: 0.78, w: 0.17, fill: col, line: "#1F5FB0", dash: !e }); });
      });
      return C.scene({ s: 82, cx: 280, cy: 125, yaw: 28, pitch: 18, atoms: atoms, bonds: bondsArr, lobes: lobes });
    }
    draw();
  };

  /* ================================================================ m24: σ and π bonds */
  mount.sigmaPi = function (host, D) {
    var S = D.ch5.sigmaPi, byKey = {}, st = { key: "CH2O", color: false, reveal: false };
    S.forEach(function (s) { byKey[s.key] = s; });
    var ui = U.shell(host, { title: "Explorer: count the σ and π bonds",
      intro: "Every bond contains one σ bond; a double bond adds one π bond and a triple bond adds two. Count them first, then color the bonds and check each atom's hybridization.",
      source: "Source: Day 11 p.17–26 (formaldehyde, diazene, acetylene, ethylene, acrolein, benzene; σ bonds green and π bonds blue, as on p.19 and p.23). Textbook §5.4–5.5 (PDF p.249–255): CO₂, N₂. Other molecules are new examples. Each atom's hybridization follows from its steric number (Day 11 p.12, p.24)." });
    var sel = U.select(ui.controls, { label: "Molecule", testid: "sp-mol", value: st.key, options: S.map(function (s) { return [s.key, s.label.replace(/<[^>]+>/g, "") + (s.tag === "lecture" ? "  (lecture)" : s.tag === "textbook" ? "  (textbook)" : "")]; }), onChange: function (v) { st.key = v; draw(); } });
    var c1 = U.checkbox(ui.controls, { label: "Color the σ and π bonds", testid: "sp-color", value: st.color, onChange: function (v) { st.color = v; draw(); } });
    var c2 = U.checkbox(ui.controls, { label: "Show the counts and each atom's hybridization", testid: "sp-reveal", value: st.reveal, onChange: function (v) { st.reveal = v; draw(); } });
    U.presetButtons(ui, "sp", [["formaldehyde", "CH2O"], ["diazene", "N2H2"], ["acetylene", "C2H2"], ["ethylene", "C2H4"]], function (k) { st.key = k; sel.value = k; draw(); });
    function draw() {
      var s = byKey[st.key], c = C.sigmaPi(s.bonds);
      ui.view.innerHTML = "<p class='xp-caption'>" + tag(s.tag) + " " + s.label + (s.src ? " <span class='source-inline'>(" + s.src + ")</span>" : "") + "</p><div class='lw-row'>" + (st.color ? s.colored : s.plain) + "</div>" +
        (st.color ? "<div class='legend-row'><span class='lg'><span class='lg-sw' style='background:#0F8A5F'></span>σ bond (green)</span><span class='lg'><span class='lg-sw' style='background:#2a78d6;height:5px'></span>π bond (blue, thicker)</span></div>" : "") +
        (st.key === "HCOOH" && st.reveal ? "<p class='bg'>The steric-number rule gives the O–H oxygen sp<sup>3</sup> (2 bonded atoms + 2 lone pairs). Because one of its lone pairs can spread into the C=O π bond, more advanced treatments describe that oxygen as sp<sup>2</sup>. Use the course's rule.</p>" : "") +
        (st.key === "C6H6" ? "<p class='connection'>One Kekulé structure is drawn. In benzene the π electrons are spread over the whole ring, above and below it (Day 11 p.26): the orbital picture of its resonance (Day 9 p.12–13).</p>" : "");
      var single = s.bonds.filter(function (b) { return b[2] === 1; }).length, dbl = s.bonds.filter(function (b) { return b[2] === 2; }).length, tri = s.bonds.filter(function (b) { return b[2] === 3; }).length;
      ui.readout.innerHTML = st.reveal ? "<strong>" + c.sigma + " σ and " + c.pi + " π</strong>: " + [single ? single + " single bond" + (single > 1 ? "s" : "") + " (σ)" : "", dbl ? dbl + " double bond" + (dbl > 1 ? "s" : "") + " (σ + π each)" : "", tri ? tri + " triple bond" + (tri > 1 ? "s" : "") + " (σ + 2 π each)" : ""].filter(Boolean).join(", ") + "."
        : "Count the σ bonds and the π bonds, then check with “Show the counts”.";
      U.kvSet(ui.kv, [["σ bonds", st.reveal ? c.sigma : "?"], ["π bonds", st.reveal ? c.pi : "?"], ["Bonds drawn", s.bonds.length]]);
      ui.table.innerHTML = U.tableHTML(["Atom", "Bonded atoms", "Lone pairs", "Steric number", "Hybridization", "π bonds it makes"], s.atoms.map(function (a) {
        return st.reveal ? [a.desc, a.bonded, a.lp, a.sn, C.hybHTML(a.hyb), a.pi] : [a.desc, a.bonded, a.lp, "?", "?", "?"]; })) +
        "<p class='table-note'>Steric number = bonded atoms + lone pairs; SN 2 → sp, 3 → sp<sup>2</sup>, 4 → sp<sup>3</sup>. A π bond needs an unhybridized p orbital on both atoms, so an sp<sup>3</sup> atom makes none.</p>";
      if (st.reveal) ui.details.open = true;
      c1.checked = st.color; c2.checked = st.reveal;
    }
    draw();
  };

  /* ================================================================ t5-6: chirality */
  mount.chirality = function (host, D) {
    var G = D.ch5.chirality, text = {}, seen = {}, st = { groups: G.presets[0].groups.slice(), turned: null, axis: 0, anim: false };
    G.groups.forEach(function (g) { text[g.key] = g.text; });
    var ui = U.shell(host, { title: "Explorer: is it superimposable on its mirror image?",
      intro: "Choose the four groups on a tetrahedral carbon. The right-hand model is its mirror image. Turn the mirror image about one of its bonds and try to make every group land on the same group in the original.",
      source: "Source: carvone, Day 10 p.6 (lecture; the slide names chiral molecules but gives no definition). Textbook preview §5.6 (PDF p.255–260): chirality, the reflect-and-rotate test with CHBrClF and CHBr₂Cl (Fig. 5.40, PDF p.257), alanine (Fig. 5.41, PDF p.260), carvone's stereocenter (PDF p.257–258)." });
    var POS = ["top", "front", "back right", "back left"], sels = [];
    POS.forEach(function (name, i) {
      sels.push(U.select(ui.controls, { label: "Group " + (i + 1) + " (" + name + ")", testid: "chi-g" + i, value: st.groups[i], options: G.groups.map(function (g) { return [g.key, g.text]; }), onChange: function (v) { st.groups[i] = v; st.turned = null; draw(); } }));
    });
    var axisSel = U.select(ui.controls, { label: "Turn the mirror image about its bond to", testid: "chi-axis", value: "0", options: POS.map(function (n, i) { return [String(i), "group " + (i + 1)]; }), onChange: function (v) { st.axis = +v; } });
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    U.button(row, "Turn 120°", "btn-chi-turn", function () { turn(); });
    U.button(row, "Reset the mirror image", "btn-chi-reset", function () { st.turned = null; draw(); });
    U.presetButtons(ui, "chi", G.presets.map(function (p) { return [p.label, p.key]; }), function (k) {
      var p = G.presets.filter(function (x) { return x.key === k; })[0]; st.groups = p.groups.slice(); st.turned = null; st.preset = k;
      sels.forEach(function (s, i) { s.value = st.groups[i]; }); draw(); });
    function current() { return st.turned || C.TETRA.map(C.mirror); }
    function turn() {
      var from = current(), axis = from[st.axis], to = from.map(function (v) { return C.rotateAbout(v, axis, 120); });
      if (U.reduceMotion || !window.requestAnimationFrame) { st.turned = to; draw(); return; }
      var t0 = null;
      function step(t) {
        if (t0 === null) t0 = t;
        var k = Math.min(1, (t - t0) / 600), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        st.turned = from.map(function (v) { return C.rotateAbout(v, axis, 120 * e); });
        draw(k < 1);
        if (k < 1) window.requestAnimationFrame(step); else { st.turned = to; draw(); }
      }
      window.requestAnimationFrame(step);
    }
    var GCOL = ["#F2C14E", "#7FB7E6", "#E88C7D", "#9ED29A", "#C7A5E0", "#F5A3C7", "#BFC6CF"];
    function colorOf(key) { var keys = []; st.groups.forEach(function (g) { if (keys.indexOf(g) < 0) keys.push(g); }); return GCOL[keys.indexOf(key) % GCOL.length]; }
    function model(center, dirs, groups, ringIdx) {
      var atoms = [{ p: center, el: "C", r: 15 }], bonds = [];
      dirs.forEach(function (v, i) {
        var e = addv(center, mul(v, 1.0)), g = groups[i], t = text[g];
        atoms.push({ p: e, el: g, label: t.length > 4 ? String(i + 1) : t, fill: g === "H" ? "#FFFFFF" : colorOf(g), r: t.length > 4 ? 14 : 16, ring: ringIdx && ringIdx[i] ? ringIdx[i] : null });
        bonds.push({ a: center, b: e, order: 1 });
      });
      return { atoms: atoms, bonds: bonds };
    }
    function draw(fast) {
      var g = st.groups, mirrorDirs = current(), chiral = C.chiral(g), matches = st.turned ? C.matchCount(g, mirrorDirs) : null;
      var ok = mirrorDirs.map(function (v, i) { return g[C.nearest(v)] === g[i]; });
      var left = model([-1.55, 0, 0], C.TETRA, g), right = model([1.55, 0, 0], mirrorDirs, g, st.turned ? ok.map(function (x) { return x ? "#0F7B4B" : "#B42318"; }) : null);
      var svg = C.scene({ s: 74, cx: 280, cy: 140, yaw: 0, pitch: 12, atoms: left.atoms.concat(right.atoms), bonds: left.bonds.concat(right.bonds) }) +
        "<line x1='280' y1='24' x2='280' y2='256' style='stroke:#6B7686;stroke-width:1.5;stroke-dasharray:6 5'/><text class='direct-label' x='280' y='272' text-anchor='middle'>mirror</text>" +
        "<text class='direct-label strong' x='165' y='272' text-anchor='middle'>molecule</text><text class='direct-label strong' x='395' y='272' text-anchor='middle'>mirror image" + (st.turned ? ", turned" : "") + "</text>";
      var long = g.filter(function (k) { return text[k].length > 4; });
      ui.view.innerHTML = U.svgWrap(560, 282, "A tetrahedral carbon with " + g.map(function (k) { return text[k]; }).join(", ") + ", beside its mirror image", svg) +
        (long.length ? "<p class='xp-caption'>Numbered spheres: " + g.map(function (k, i) { return text[k].length > 4 ? (i + 1) + " = " + text[k] : ""; }).filter(Boolean).join("; ") + ".</p>" : "") +
        (st.turned ? "<p class='xp-caption'>Rings on the mirror image: green where the group matches the original's group in that position, red where it doesn't.</p>" : "");
      if (fast) return;
      var groupsTxt = g.map(function (k) { return text[k]; }).join(", ");
      var verdict = chiral ? "All four groups are different, so no turn lines the mirror image up with the original: the molecule is <strong>chiral</strong> (not superimposable on its mirror image), and the carbon is a stereocenter."
        : "Two groups are the same, so some turn makes the mirror image land exactly on the original: the molecule is <strong>achiral</strong>.";
      ui.readout.innerHTML = (st.turned ? matches + " of 4 positions match after turning. " : "") + (st.turned && matches === 4 ? "The mirror image is the same molecule. " : "") + verdict + (st.preset === "carvone" && chiral ? " For carvone the two ring branches are both CH<sub>2</sub> at first, but one side of the ring leads to C=C and the other to C=O (textbook PDF p.257–258). (+)-carvone smells of caraway and (−)-carvone of spearmint (Day 10 p.6)." : "");
      U.kvSet(ui.kv, [["Groups", groupsTxt], ["Different groups", Object.keys(g.reduce(function (o, k) { o[k] = 1; return o; }, {})).length + " of 4"], ["Matching positions now", st.turned ? matches + " of 4" : "turn the mirror image to test"], ["Verdict", chiral ? "chiral" : "achiral"]]);
      if (st.turned) seen[g.join("|")] = 1;
      ui.table.innerHTML = seenTable(["Groups", "Chiral?"], Object.keys(seen).map(function (k) { var gs = k.split("|"); return [gs.map(function (x) { return text[x]; }).join(", "), C.chiral(gs) ? "chiral" : "achiral"]; }),
        "Each set of groups you test by turning the mirror image is added here.");
    }
    draw();
  };

  /* ================================================================ t5-7: MO diagrams */
  mount.moDiagram = function (host, D) {
    var M = D.ch5.mo, byKey = {}, seen = {}, st = { key: "O2", q: 0 };
    M.species.forEach(function (s) { byKey[s.key] = s; });
    var ui = U.shell(host, { title: "Explorer: molecular orbital diagrams",
      intro: "Pick a diatomic molecule or ion. Electrons fill the molecular orbitals from the bottom up (aufbau), one per orbital before any pair up (Hund), two per orbital at most (Pauli). Then read off the bond order and the unpaired electrons.",
      source: "Source: lecture, Day 11 p.27 (O₂'s magnetism) and Day 12 p.8–11: H₂, H₂⁻, He₂, the bond-order formula, and the textbook's Fig. 5.50 with both energy orders (π<sub>2p</sub> below σ<sub>2p</sub> for Li<sub>2</sub>–N<sub>2</sub>, above it for O<sub>2</sub>–Ne<sub>2</sub>). Textbook preview §5.7 (PDF p.262–269): ions of the diatomics (Sample Ex. 5.8) and NO (Fig. 5.52). Energies are schematic." });
    var sel = U.select(ui.controls, { label: "Molecule", testid: "mo-species", value: st.key, options: M.species.map(function (s) { return [s.key, s.label]; }), onChange: function (v) { st.key = v; st.q = 0; buildCharge(); draw(); } });
    var qBox = el("div"); ui.controls.appendChild(qBox);
    function buildCharge() {
      qBox.innerHTML = "";
      var qs = C.moCharges(byKey[st.key], M.orders);
      if (qs.indexOf(st.q) < 0) st.q = 0;
      U.radios(qBox, { label: "Charge", testid: "mo-charge", value: String(st.q), options: qs.map(function (q) { return [String(q), q === 0 ? "0 (neutral)" : (q > 0 ? "+" : MINUS) + Math.abs(q)]; }), onChange: function (v) { st.q = +v; draw(); } });
    }
    U.presetButtons(ui, "mo", [["O₂ (Day 11 p.27; Day 12 p.11)", ["O2", 0]], ["N₂ (Day 12 p.11)", ["N2", 0]], ["B₂ (Day 12 p.11)", ["B2", 0]], ["He₂ (Day 12 p.9)", ["He2", 0]], ["NO", ["NO", 0]], ["O₂²⁻", ["O2", -2]]], function (p) {
      st.key = p[0]; sel.value = p[0]; st.q = p[1]; buildCharge(); draw(); });
    function label(name) { var m = name.match(/^([σπ]\*?)(\w+)$/); return m[1] + "<tspan class='sub' dy='4'>" + m[2] + "</tspan><tspan dy='-4'>​</tspan>"; }
    function spinBox(x, y, n) {
      return "<rect x='" + x + "' y='" + (y - 13) + "' width='30' height='26' rx='2' style='fill:#FFFFFF;stroke:#17212E;stroke-width:1.1'/>" +
        spins(x + 15, y, n);
    }
    function draw() {
      var sp = byKey[st.key], type = sp.order, n = sp.valence[0] + sp.valence[1] - st.q, fill = C.moFill(M.orders, type, n);
      var W = 560, Hh = 380, g = "", one = type === "1s", hetero = sp.atoms[0] !== sp.atoms[1];
      // schematic energies (y down) for each MO and the atomic orbitals
      var Y = one ? { "σ1s": 250, "σ*1s": 110 } : type === "low" ? { "σ2s": 330, "σ*2s": 270, "π2p": 190, "σ2p": 160, "π*2p": 95, "σ*2p": 50 }
        : { "σ2s": 330, "σ*2s": 270, "σ2p": 200, "π2p": 165, "π*2p": 95, "σ*2p": 50 };
      var AO = one ? [{ n: "1s", y: 180 }] : [{ n: "2s", y: 300 }, { n: "2p", y: 130 }], shiftL = hetero ? -10 : 0, shiftR = hetero ? 14 : 0;
      var xL = 70, xR = 430, xM = 250;
      // atomic orbitals (electrons only for neutral species)
      [[xL, sp.atoms[0], sp.valence[0], shiftL], [xR, sp.atoms[1], sp.valence[1], shiftR]].forEach(function (side) {
        var x = side[0], e = side[2], left = e;
        g += "<text class='direct-label strong' x='" + (x + (one ? 15 : 45)) + "' y='" + (Hh - 8) + "' text-anchor='middle'>" + side[1] + " atom</text>";
        AO.forEach(function (a) {
          var nb = a.n === "2p" ? 3 : 1, y = a.y + side[3], fillAO = [], k;
          var take = a.n === "2p" ? Math.max(0, left) : Math.min(2, left);
          left -= take;
          for (k = 0; k < nb; k++) fillAO.push(0);
          for (k = 0; k < take; k++) fillAO[k % nb]++;
          for (k = 0; k < nb; k++) g += st.q === 0 ? spinBox(x + k * 32, y, fillAO[k]) : spinBox(x + k * 32, y, 0);
          g += x === xL ? "<text class='tick' x='" + (x - 6) + "' y='" + (y + 4) + "' text-anchor='end'>" + a.n + "</text>"
            : "<text class='tick' x='" + (x + nb * 32 + 4) + "' y='" + (y + 4) + "'>" + a.n + "</text>";
        });
      });
      // molecular orbitals
      fill.levels.forEach(function (L) {
        var y = Y[L.name], nb = L.boxes.length, x0 = xM - (nb * 32) / 2 + 1;
        L.boxes.forEach(function (b, k) { g += spinBox(x0 + k * 32, y, b); });
        g += "<text class='tick strong' x='" + (x0 + nb * 32 + 8) + "' y='" + (y + 4) + "'>" + label(L.name) + "</text>";
        // correlation lines to the atomic orbitals they come from
        var src = /1s/.test(L.name) ? "1s" : /2s/.test(L.name) ? "2s" : "2p", ao = AO.filter(function (a) { return a.n === src; })[0];
        if (ao) {
          var nbA = src === "2p" ? 3 : 1;
          g += "<line class='landmark' x1='" + (xL + nbA * 32) + "' y1='" + (ao.y + shiftL) + "' x2='" + (x0 - 2) + "' y2='" + y + "' style='stroke-dasharray:3 3'/>" +
            "<line class='landmark' x1='" + (x0 + nb * 32) + "' y1='" + y + "' x2='" + (xR - 2) + "' y2='" + (ao.y + shiftR) + "' style='stroke-dasharray:3 3'/>";
        }
      });
      g += "<text class='direct-label strong' x='" + xM + "' y='" + (Hh - 8) + "' text-anchor='middle'>molecule (valence MOs)</text>" +
        "<line x1='22' y1='" + (Hh - 40) + "' x2='22' y2='30' style='stroke:#6B7686;stroke-width:1.2'/><path d='M22 24 l-5 9 h10 z' style='fill:#6B7686'/><text class='axis-label' transform='translate(14 " + (Hh / 2) + ") rotate(-90)' text-anchor='middle'>energy</text>";
      var name = sp.label + (st.q ? U.uniSup((Math.abs(st.q) > 1 ? Math.abs(st.q) : "") + (st.q > 0 ? "+" : MINUS)) : "");
      var nameHTML = U.ion(sp.label, st.q).replace(/₂/g, "<sub>2</sub>");
      ui.view.innerHTML = U.svgWrap(W, Hh, name + " molecular orbital diagram: " + fill.config + ", bond order " + C.boText(fill.bo) + ", " + fill.unpaired + " unpaired electrons", g) +
        (st.key === "O2" && st.q === 0 ? "<p class='xp-caption'>Compare O<sub>2</sub>'s Lewis structure (Day 8 p.20), with every electron paired:</p><div class='lw-row'>" + M.o2Lewis + "</div>" : "") +
        (st.q !== 0 ? "<p class='xp-caption'>For an ion the atomic-orbital boxes are left empty: count the electrons from the atoms' valence electrons and the charge.</p>" : "");
      var mag = fill.unpaired ? "<strong>paramagnetic</strong> (attracted to a magnetic field)" : "<strong>diamagnetic</strong> (no unpaired electrons)";
      var msg = nameHTML + ": " + sp.valence[0] + " + " + sp.valence[1] + (st.q ? (st.q > 0 ? " − " + st.q : " + " + (-st.q)) + " (charge)" : "") + " = " + n + " valence electrons → " + C.configHTML(fill) +
        ". Bond order = ½(" + fill.bonding + " − " + fill.antibonding + ") = <strong>" + C.boText(fill.bo) + "</strong>" + (fill.bo === 0 ? ": no net bond, so it is not expected to exist" : "") + ". " + fill.unpaired + " unpaired electron" + (fill.unpaired === 1 ? "" : "s") + ": " + mag + ".";
      if (st.key === "O2" && st.q === 0) msg += " This is the Day 11 p.27 puzzle: liquid O<sub>2</sub> sticks to a magnet, which Lewis structures, VSEPR, and valence bond theory all fail to predict. The two unpaired electrons sit in the two π*<sub>2p</sub> orbitals, the pair circled in red on Day 12 p.11.";
      if (st.key === "NO") msg += " The textbook orders NO's orbitals like O<sub>2</sub>'s (Fig. 5.52, PDF p.268).";
      ui.readout.innerHTML = msg;
      U.kvSet(ui.kv, [["Valence electrons", n], ["Bonding electrons", fill.bonding], ["Antibonding electrons", fill.antibonding], ["Bond order", C.boText(fill.bo)], ["Unpaired electrons", fill.unpaired], ["Magnetism", fill.unpaired ? "paramagnetic" : "diamagnetic"]]);
      seen[st.key + ":" + st.q] = 1;
      var rows = [];
      M.species.forEach(function (x) { C.moCharges(x, M.orders).forEach(function (q) {
        if (!seen[x.key + ":" + q]) return;
        var f = C.moFill(M.orders, x.order, x.valence[0] + x.valence[1] - q);
        rows.push([U.ion(x.label, q).replace(/₂/g, "<sub>2</sub>"), x.valence[0] + x.valence[1] - q, C.boText(f.bo), f.unpaired, f.unpaired ? "paramagnetic" : "diamagnetic"]); }); });
      ui.table.innerHTML = seenTable(["Species", "Valence e⁻", "Bond order", "Unpaired e⁻", "Magnetism"], rows, "") +
        "<p class='table-note'>The species you have looked at so far. The textbook's values: Fig. 5.50 (PDF p.266; shown on Day 12 p.11) for the neutral homonuclear molecules, Sample Ex. 5.8 for their cations (PDF p.267), Fig. 5.52 for NO (PDF p.268).</p>";
    }
    buildCharge();
    draw();
  };

  X.calcCh5 = C;
  return { calc: C };
});
