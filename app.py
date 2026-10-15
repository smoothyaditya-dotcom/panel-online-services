from flask import Flask, render_template_string

app = Flask(__name__)

# Edit this list. Set "live": True when a product is ready to sell.
# "qr" = QR image in the static folder, "upi_link" = opens the user's UPI app.
PRODUCTS = [
    {
        "name": "Product 1",
        "price": "₹30",
        "desc": "Write one clear sentence about what this does for the buyer.",
        "live": True,
        "qr": "/static/upi-qr-rs30.png",
        "upi_link": "upi://pay?pa=7276052050@fam&pn=My%20Shop&am=30.00&cu=INR&tn=Product%20payment",
    },
    {
        "name": "Product 2",
        "price": "₹00",
        "desc": "Coming soon.",
        "live": False,
    },
    {
        "name": "Product 3",
        "price": "₹00",
        "desc": "Coming soon.",
        "live": False,
    },
]

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>My Shop</title>
  <style>
    :root { --ink:#14213d; --muted:#5b6475; --line:#d9dde5; --accent:#1d4ed8; --bg:#ffffff; }
    @media (prefers-color-scheme: dark) {
      :root { --ink:#eef1f7; --muted:#a3adc2; --line:#2b3550; --accent:#6d9bff; --bg:#0e1424; }
    }
    * { box-sizing: border-box; }
    body { margin:0; font-family: Georgia, serif; color:var(--ink); background:var(--bg); line-height:1.5; }
    main { position:relative; z-index:1; max-width: 640px; margin: 0 auto; padding: 32px 20px 64px; }
    h1 { font-size: 2rem; margin: 0 0 8px; }
    .sub { color: var(--muted); margin: 0 0 32px; }
    .item { border-top: 1px solid var(--line); padding: 20px 0; }
    .item h2 { margin: 0; font-size: 1.25rem; }
    .price { font-weight: bold; margin: 4px 0; }
    .item p { color: var(--muted); margin: 8px 0 14px; }
    .buy { display:inline-block; padding: 12px 22px; background: var(--accent); color:#fff;
           text-decoration:none; border-radius: 6px; font-family: system-ui, sans-serif; }
    .buy:focus-visible { outline: 3px solid var(--ink); outline-offset: 2px; }
    .soon { color: var(--muted); font-family: system-ui, sans-serif; }
    .qrbox { margin-top: 18px; }
    .qrbox img { display:block; background:#fff; padding:8px; border:1px solid var(--line); border-radius:6px; margin-bottom:8px; }

    /* 3D cylinder: popup for 3 seconds, then it rolls behind the page */
    #intro-bg { position:fixed; inset:0; z-index:100; background:#0a0405;
                transition: opacity .9s ease; animation: failsafe .5s 9s forwards; }
    #intro-bg.gone { opacity:0; pointer-events:none; }
    #cyl { position:fixed; inset:0; width:100%; height:100%; z-index:101; pointer-events:none; display:block; }
    #cyl.back { z-index:0; }
    #intro-info { position:fixed; left:0; right:0; bottom:max(18px, env(safe-area-inset-bottom)); z-index:102;
                  text-align:center; font-family:system-ui, sans-serif; font-size:15px; line-height:1.5;
                  color:#f3d9d3; pointer-events:none; transition: opacity .5s ease; animation: failsafe .5s 9s forwards; }
    #intro-info b { font-size:19px; }
    #intro-info.gone { opacity:0; }
    @keyframes failsafe { to { opacity:0; visibility:hidden; } }
  </style>
</head>
<body>
  <div id="intro-bg" aria-hidden="true"></div>
  <div id="intro-info" aria-hidden="true"><b>Ø 6.0 mm × 84 mm</b><br>Circumference 18.8 mm</div>
  <canvas id="cyl" aria-hidden="true"></canvas>

  <main>
    <h1>My Shop</h1>
    <p class="sub">Write one short line about who you are and what you make.</p>
    {% for p in products %}
    <section class="item">
      <h2>{{ p.name }}</h2>
      <div class="price">{{ p.price }}</div>
      <p>{{ p.desc }}</p>
      {% if p.live %}
        <a class="buy" href="{{ p.upi_link }}">Pay with UPI app</a>
        <div class="qrbox">
          <img src="{{ p.qr }}" alt="Scan to pay 30 rupees" width="220" height="220">
          <div class="soon">Or scan this QR with any UPI app</div>
        </div>
      {% else %}
        <span class="soon">Available soon</span>
      {% endif %}
    </section>
    {% endfor %}
  </main>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  {% raw %}
  <script>
  (function () {
    var bg = document.getElementById('intro-bg');
    var info = document.getElementById('intro-info');
    var canvas = document.getElementById('cyl');

    function abandon() {
      bg.style.display = 'none';
      info.style.display = 'none';
      canvas.style.display = 'none';
    }
    if (typeof THREE === 'undefined') { abandon(); return; }

    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    } catch (e) { abandon(); return; }

    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var R = 3, L = 84; // millimetres: diameter 6.0, length 84

    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(30, 1, 1, 1000);
    scene.add(new THREE.AmbientLight(0xffffff, 0.85));
    var key = new THREE.DirectionalLight(0xffffff, 0.9);
    key.position.set(-40, 60, 80);
    scene.add(key);

    var side = new THREE.MeshStandardMaterial({ roughness: 0.45, metalness: 0.05, transparent: true });
    var cap = new THREE.MeshStandardMaterial({ color: 0x1a0a0c, roughness: 0.7, transparent: true });
    var mesh = new THREE.Mesh(new THREE.CylinderGeometry(R, R, L, 64, 1), [side, cap, cap]);
    var tilt = new THREE.Group();
    tilt.add(mesh);
    var pose = new THREE.Group();
    pose.rotation.x = 0.3;
    pose.add(tilt);
    scene.add(pose);

    function layout() {
      var w = window.innerWidth, h = window.innerHeight, aspect = w / h;
      renderer.setSize(w, h, false);
      camera.aspect = aspect;
      camera.updateProjectionMatrix();
      var a = (aspect < 1 ? 62 : 18) * Math.PI / 180; // angle from horizontal
      tilt.rotation.z = -(Math.PI / 2 - a);
      var halfW = (L / 2) * Math.cos(a) + R * Math.sin(a);
      var halfH = (L / 2) * Math.sin(a) + R * Math.cos(a);
      var t = Math.tan(camera.fov * Math.PI / 360);
      var d = Math.max(halfH / t, halfW / (t * aspect)) / 0.86 + R;
      camera.position.set(0, 0, d);
    }

    function clamp01(x) { return Math.max(0, Math.min(1, x)); }
    function ease(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }

    var T_IN = 0.9, T_HOLD = 3.0, T_OUT = 3.9;
    var BG_SCALE = 0.72, BG_OPACITY = 0.38;
    var started = false, faded = false, finished = false;
    var t0 = 0, last = 0, lastDraw = 0, spin = 0, lastY = window.scrollY || 0;

    function setLook(scale, opacity) {
      pose.scale.set(scale, scale, scale);
      side.opacity = opacity;
      cap.opacity = opacity;
    }

    function finish() {
      finished = true;
      bg.style.display = 'none';
      info.style.display = 'none';
      canvas.className = 'back';
      setLook(BG_SCALE, BG_OPACITY);
    }

    function frame(now) {
      var t = (now - t0) / 1000;
      var dt = Math.min(0.05, (now - last) / 1000);
      last = now;

      if (!finished) {
        var p = ease(clamp01(t / T_IN));
        var q = ease(clamp01((t - T_HOLD) / (T_OUT - T_HOLD)));
        setLook((0.6 + 0.4 * p) * (1 - (1 - BG_SCALE) * q), p * (1 - (1 - BG_OPACITY) * q));
        spin += (0.9 + 3.5 * (1 - p)) * dt;
        if (!faded && t >= T_HOLD) {
          faded = true;
          bg.className = 'gone';
          info.className = 'gone';
        }
        if (t >= T_OUT) { finish(); }
      } else {
        spin += 0.6 * dt;
        if (now - lastDraw < 33) { requestAnimationFrame(frame); return; }
      }

      var y = window.scrollY || 0;
      spin += (y - lastY) * 0.01;
      lastY = y;
      lastDraw = now;

      mesh.rotation.y = spin;
      renderer.render(scene, camera);
      requestAnimationFrame(frame);
    }

    function begin() {
      if (started) { return; }
      started = true;
      layout();
      if (reduce) {
        finish();
        renderer.render(scene, camera);
        window.addEventListener('resize', function () { layout(); renderer.render(scene, camera); });
        return;
      }
      window.addEventListener('resize', layout);
      t0 = performance.now();
      last = t0;
      requestAnimationFrame(frame);
    }

    function useTexture(tex) {
      tex.encoding = THREE.sRGBEncoding;
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      side.map = tex;
      side.needsUpdate = true;
      begin();
    }

    function fallbackTexture() {
      var c = document.createElement('canvas');
      c.width = 512;
      c.height = 512;
      var g = c.getContext('2d');
      var grad = g.createLinearGradient(0, 0, 512, 512);
      grad.addColorStop(0, '#5a0d12');
      grad.addColorStop(1, '#14080a');
      g.fillStyle = grad;
      g.fillRect(0, 0, 512, 512);
      useTexture(new THREE.CanvasTexture(c));
    }

    // Your image is wrapped once around the tube and stretched over its full length.
    new THREE.TextureLoader().load('/static/product.jpg', useTexture, undefined, fallbackTexture);
  })();
  </script>
  {% endraw %}
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE, products=PRODUCTS)


@app.route("/health")
def health():
    # Tiny page used by the keep-alive workflow
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
  
