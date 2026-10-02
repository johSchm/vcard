/*
 * PhD Thesis: canonicalization figure.
 *
 * A wire-frame surface over the input space. The frozen model solves the
 * problem only in the training region (accent color). At test time the
 * queries come from another region, and canonicalization maps all of them
 * to the same canonical spot in the training region, so the model needs no
 * retraining. The figure builds, plays and dismantles itself in a loop like
 * a GIF. It only runs while visible and shows a still frame for
 * prefers-reduced-motion.
 */
(function () {
	"use strict";

	var fig = document.querySelector(".canon-viz");
	if (!fig) return;
	var canvas = fig.querySelector("canvas");
	var ctx = canvas.getContext("2d");
	var steps = fig.querySelectorAll(".canon-viz-step");
	var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

	// --- timeline (ms) -------------------------------------------------------
	// Caption steps: 1800-4400, 4400-7000, 7000-11400 (the last one holds the result).
	var T = {
		build: [0, 1800],      // wire lines draw in one after another
		region: [1800, 2600],  // training region lights up
		test: [4400, 5000],    // test region lights up
		query: 4600,           // first test query appears, the others follow
		path: 7000,            // first query starts its trajectory
		travel: 1800,          // duration of one trajectory
		stagger: 100,          // delay between two queries
		hold: 11400,           // start of the dismantling, 2 s after "canonical form" appears (9400)
		unbuild: 1500,         // duration of the dismantling
		loop: 13200
	};

	// --- surface -------------------------------------------------------------
	var N = 30;                                   // grid lines per direction
	var R = 0.6;                                  // radius of the orbit
	var TQ = -35 * Math.PI / 180;                 // angle of the test region
	var TC = 145 * Math.PI / 180;                 // angle of the training region
	var C = [R * Math.cos(TC), R * Math.sin(TC)]; // training region, canonical spot
	var Q = [R * Math.cos(TQ), R * Math.sin(TQ)]; // test region
	// test queries, as offsets from the center of the test region
	var QUERIES = [[0, 0], [0.16, 0.05], [-0.12, 0.13], [0.05, -0.17],
		[-0.16, -0.07], [0.12, -0.12], [-0.02, 0.2]].map(function (o) {
		return [Q[0] + o[0], Q[1] + o[1]];
	});

	function bump(x, y, p, s) {
		var dx = x - p[0], dy = y - p[1];
		return Math.exp(-(dx * dx + dy * dy) / s);
	}
	function height(x, y) {
		return 0.07 * Math.sin(3 * x + 0.5) * Math.cos(2.5 * y) +
			0.04 * Math.sin(5 * x - 2 * y + 1) * Math.cos(4 * y + 0.3) +
			0.06 * (x * x + y * y) -
			0.3 * bump(x, y, C, 0.12) +
			0.12 * bump(x, y, Q, 0.07) +
			0.12 * bump(x, y, [0.15, -0.75], 0.04) -
			0.1 * bump(x, y, [0.3, 0.75], 0.05) +
			0.1 * bump(x, y, [-0.75, -0.45], 0.05) -
			0.08 * bump(x, y, [-0.15, -0.2], 0.04);
	}
	function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
	function smooth(a, b, v) { v = clamp((v - a) / (b - a)); return v * v * (3 - 2 * v); }
	function easeInOut(v) { return v < 0.5 ? 2 * v * v : 1 - Math.pow(-2 * v + 2, 2) / 2; }
	function phase(span, t) { return clamp((t - span[0]) / (span[1] - span[0])); }
	// 1 inside the training / test region, 0 outside, smooth in between
	function solved(x, y) { return 1 - smooth(0.22, 0.36, Math.hypot(x - C[0], y - C[1])); }
	function tested(x, y) { return 1 - smooth(0.22, 0.34, Math.hypot(x - Q[0], y - Q[1])); }

	// grid points, then the 2N wire lines (rows first, then columns)
	var grid = [];
	for (var i = 0; i < N; i++) {
		grid.push([]);
		for (var j = 0; j < N; j++) {
			var x = -1 + 2 * j / (N - 1), y = -1 + 2 * i / (N - 1);
			grid[i].push({ x: x, y: y, z: height(x, y), s: solved(x, y), f: tested(x, y) });
		}
	}
	var lines = [];
	for (i = 0; i < N; i++) lines.push(grid[i]);
	for (j = 0; j < N; j++) lines.push(grid.map(function (row) { return row[j]; }));

	// trajectory of a query: it turns along the orbit towards the training
	// region and its radius settles, so all queries meet at the canonical spot
	function trajectory(q, u) {
		var a0 = Math.atan2(q[1], q[0]), r0 = Math.hypot(q[0], q[1]);
		var a = a0 + (TC - a0) * u, r = r0 + (R - r0) * easeInOut(u);
		var x = r * Math.cos(a), y = r * Math.sin(a);
		return { x: x, y: y, z: height(x, y) + 0.015 };
	}

	// --- projection ----------------------------------------------------------
	var AZ = 0.61, SWAY = 0.12;        // azimuth and its slow sway (rad)
	var TILT = 0.6, LIFT = 0.85;      // vertical squash of the floor, height scale
	var W = 0, H = 0, scale = 1, ox = 0, oy = 0;

	function raw(p, az) {
		var ca = Math.cos(az), sa = Math.sin(az);
		var xr = p.x * ca - p.y * sa, yr = p.x * sa + p.y * ca;
		return { x: xr, y: yr * TILT - p.z * LIFT, d: (yr + 1.45) / 2.9 };
	}
	function proj(p, az) {
		var r = raw(p, az);
		return { x: ox + scale * r.x, y: oy + scale * r.y, d: r.d };
	}
	function at(p, az) { return proj({ x: p[0], y: p[1], z: height(p[0], p[1]) + 0.015 }, az); }

	function resize() {
		var dpr = window.devicePixelRatio || 1;
		W = canvas.clientWidth; H = canvas.clientHeight;
		canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
		ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
		// fit the surface for every azimuth of the sway
		var b = [Infinity, Infinity, -Infinity, -Infinity];
		[AZ - SWAY, AZ, AZ + SWAY].forEach(function (az) {
			grid.forEach(function (row) {
				row.forEach(function (p) {
					var r = raw(p, az);
					b[0] = Math.min(b[0], r.x); b[1] = Math.min(b[1], r.y);
					b[2] = Math.max(b[2], r.x); b[3] = Math.max(b[3], r.y);
				});
			});
		});
		var pad = 16;
		scale = Math.min((W - 2 * pad) / (b[2] - b[0]), (H - 2 * pad) / (b[3] - b[1]));
		ox = W / 2 - scale * (b[0] + b[2]) / 2;
		oy = H / 2 - scale * (b[1] + b[3]) / 2;
	}

	// --- colors --------------------------------------------------------------
	function rgb(hex) {
		hex = hex.trim().replace("#", "");
		if (hex.length === 3) hex = hex.replace(/./g, "$&$&");
		var n = parseInt(hex, 16);
		return [n >> 16 & 255, n >> 8 & 255, n & 255];
	}
	var ACCENT = rgb(getComputedStyle(document.documentElement).getPropertyValue("--accent") || "#20c997");
	var FAIL = [239, 111, 108];
	var FONT = getComputedStyle(document.body).fontFamily;
	function rgba(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }
	function mix(a, b, v) { return [0, 1, 2].map(function (k) { return Math.round(a[k] + (b[k] - a[k]) * v); }); }

	// --- drawing -------------------------------------------------------------
	function dot(p, r, c, a) {
		ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, 2 * Math.PI);
		ctx.fillStyle = rgba(c, a); ctx.fill();
	}
	function ring(p, r, c, a) {
		ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, 2 * Math.PI);
		ctx.strokeStyle = rgba(c, a); ctx.lineWidth = 1.25; ctx.stroke();
	}
	function label(text, p, dx, dy, a, align) {
		if (a <= 0) return;
		ctx.font = "500 12px " + FONT;
		ctx.textAlign = align || "left";
		ctx.textBaseline = "middle";
		ctx.fillStyle = "rgba(255,255,255," + 0.8 * a + ")";
		ctx.fillText(text, p.x + dx, p.y + dy);
	}

	function draw(t, az) {
		ctx.clearRect(0, 0, W, H);
		var keep = 1 - clamp((t - T.hold) / (T.unbuild * 0.5));  // fade of the overlays
		var unbuild = clamp((t - T.hold) / T.unbuild);
		var build = easeInOut(phase(T.build, t));
		var region = easeInOut(phase(T.region, t)) * keep;
		var gone = easeInOut(clamp((t - T.path) / T.travel));    // queries leaving
		var test = easeInOut(phase(T.test, t)) * (1 - 0.65 * gone) * keep;

		// wire lines: drawn in sequence, dismantled in reverse order
		var L = lines.length, spread = 8;
		var P = lines.map(function (line) { return line.map(function (p) { return proj(p, az); }); });
		ctx.lineCap = "round";
		for (var k = 0; k < L; k++) {
			var prog = Math.min(
				clamp((build * (L + spread) - k) / spread),
				clamp(((1 - easeInOut(unbuild)) * (L + spread) - k) / spread));
			if (prog <= 0) continue;
			var segs = prog * (N - 1);
			for (var s = 0; s < segs; s++) {
				var a = P[k][s], b = P[k][s + 1], f = Math.min(1, segs - s);
				var bx = a.x + (b.x - a.x) * f, by = a.y + (b.y - a.y) * f;
				var near = (a.d + b.d) / 2, base = 0.07 + 0.2 * near;
				var hot = (lines[k][s].s + lines[k][s + 1].s) / 2 * region;
				var bad = (lines[k][s].f + lines[k][s + 1].f) / 2 * test;
				ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(bx, by);
				if (hot > 0.01) {
					ctx.strokeStyle = rgba(ACCENT, (0.3 + 0.6 * near) * hot + base * (1 - hot));
					ctx.lineWidth = 1 + 0.5 * hot;
				} else if (bad > 0.01) {
					ctx.strokeStyle = rgba(FAIL, (0.2 + 0.4 * near) * bad + base * (1 - bad));
					ctx.lineWidth = 1 + 0.3 * bad;
				} else {
					ctx.strokeStyle = "rgba(255,255,255," + base + ")";
					ctx.lineWidth = 1;
				}
				ctx.stroke();
			}
		}

		var c = at(C, az);
		label("training region", c, 0, -scale * 0.36, region, "center");
		label("test region", at(Q, az), 0, -scale * 0.34, easeInOut(phase(T.test, t)) * keep, "center");

		// test queries: pop in one after another and wait with a gentle pulse
		var travelled = [];
		QUERIES.forEach(function (q, n) {
			var qa = clamp((t - T.query - n * T.stagger) / 400) * keep;
			if (qa <= 0) return;
			var p = at(q, az);
			var u = easeInOut(clamp((t - T.path - n * T.stagger) / T.travel));
			if (u <= 0) {
				var pulse = ((t - T.query - n * T.stagger) % 1300) / 1300;
				ring(p, 3.5 + 8 * pulse, FAIL, 0.5 * (1 - pulse) * qa);
				dot(p, 3.5, FAIL, qa);
				return;
			}
			ring(p, 3, FAIL, 0.45 * qa);                       // where the query came from
			travelled.push({ q: q, u: u, start: p, a: qa });
		});

		// canonicalization: every query travels to the same canonical spot
		if (travelled.length) {
			var pa = keep, samples = 80;
			ctx.setLineDash([3, 4]);
			ctx.lineWidth = 1.25;
			ctx.strokeStyle = "rgba(255,255,255," + 0.45 * pa + ")";
			travelled.forEach(function (m) {
				ctx.beginPath(); ctx.moveTo(m.start.x, m.start.y);
				var end = Math.ceil(m.u * samples);
				for (var n = 1; n <= end; n++) {
					var p = proj(trajectory(m.q, Math.min(m.u, n / samples)), az);
					ctx.lineTo(p.x, p.y);
				}
				ctx.stroke();
				m.head = proj(trajectory(m.q, m.u), az);
			});
			ctx.setLineDash([]);
			travelled.forEach(function (m) {
				var h = trajectory(m.q, m.u);
				dot(m.head, 3.5, mix(FAIL, ACCENT, solved(h.x, h.y)), pa);
			});

			var mid = proj(trajectory(Q, 0.5), az);
			label("canonicalization", mid, 0, 22, clamp(gone * 3) * pa, "center");

			var arrived = clamp((t - T.path - T.travel - (QUERIES.length - 1) * T.stagger) / 900);
			if (arrived > 0) {
				if (arrived < 1) ring(c, 4.5 + 16 * arrived, ACCENT, 0.7 * (1 - arrived) * pa);
				label("canonical form", c, -12, 10, arrived * pa, "right");
			}
		}
	}

	function setStep(t) {
		var active = t >= T.region[0] && t < T.test[0] ? 0 :
			t >= T.test[0] && t < T.path ? 1 :
			t >= T.path && t < T.hold ? 2 : -1;
		for (var i = 0; i < steps.length; i++) steps[i].classList.toggle("is-active", i === active);
	}

	// --- loop ----------------------------------------------------------------
	var running = false, visible = false, start = null, elapsed = 0, raf = 0;

	function still() {
		draw(T.hold - 1, AZ);
		for (var i = 0; i < steps.length; i++) steps[i].classList.add("is-active");
	}
	function frame(now) {
		if (start === null) start = now - elapsed;
		elapsed = now - start;
		var t = elapsed % T.loop;
		draw(t, AZ + SWAY * Math.sin(elapsed / 4000));
		setStep(t);
		raf = requestAnimationFrame(frame);
	}
	function update() {
		var go = visible && !reduce.matches && !document.hidden;
		if (go && !running) { running = true; start = null; raf = requestAnimationFrame(frame); }
		if (!go && running) { running = false; cancelAnimationFrame(raf); }
		if (reduce.matches) still();
	}

	resize();
	if (reduce.matches) still();
	new ResizeObserver(function () {
		resize();
		if (reduce.matches) still();
		else if (!running) draw(elapsed % T.loop, AZ + SWAY * Math.sin(elapsed / 4000));
	}).observe(canvas);
	new IntersectionObserver(function (entries) {
		visible = entries[0].isIntersecting;
		update();
	}, { threshold: 0.25 }).observe(canvas);
	document.addEventListener("visibilitychange", update);
	if (reduce.addEventListener) reduce.addEventListener("change", update);
})();
