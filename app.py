from flask import Flask, render_template_string

app = Flask(__name__)

# Products catalog: Set "live": True when ready to sell
PRODUCTS = [
    {
        "id": 1,
        "name": "Product 1",
        "price": "₹30",
        "image": "/static/panel_artwork.jpg",
        "live": True,
        "qr": "/static/upi-qr-rs30.png",
        "upi_link": "upi://pay?pa=7276052050@fam&pn=PANEL%20OFFICIAL&am=30.00&cu=INR&tn=Panel%20Payment",
    },
    {
        "id": 2,
        "name": "Product 2",
        "price": "₹99",
        "image": "/static/panel_artwork.jpg",
        "live": False,
        "qr": "",
        "upi_link": "",
    },
    {
        "id": 3,
        "name": "Product 3",
        "price": "₹149",
        "image": "/static/panel_artwork.jpg",
        "live": False,
        "qr": "",
        "upi_link": "",
    },
]

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PANEL OFFICIAL</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #070304;
      --card-bg: rgba(20, 10, 14, 0.78);
      --card-border: rgba(255, 30, 60, 0.22);
      --accent-red: #ff1e3c;
      --accent-gradient: linear-gradient(135deg, #ff1744 0%, #b70020 100%);
      --text-main: #f8fafc;
      --text-sub: #94a3b8;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg);
      background-image: 
        radial-gradient(at 15% 15%, rgba(255, 23, 68, 0.18) 0px, transparent 60%),
        radial-gradient(at 85% 85%, rgba(180, 0, 30, 0.12) 0px, transparent 60%);
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: var(--text-main);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* 3D Intro Background Overlay */
    #intro-bg {
      position: fixed;
      inset: 0;
      z-index: 100;
      background: #090305;
      transition: opacity 0.9s cubic-bezier(0.4, 0, 0.2, 1);
      animation: failsafe 0.5s 9s forwards;
    }
    #intro-bg.gone {
      opacity: 0;
      pointer-events: none;
    }

    /* 3D Cylinder Canvas Layer */
    #cyl {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 101;
      pointer-events: none;
      display: block;
      transition: z-index 0.1s ease;
    }
    #cyl.back {
      z-index: 0;
    }

    @keyframes failsafe {
      to { opacity: 0; visibility: hidden; }
    }

    /* Page Layout */
    .container {
      position: relative;
      z-index: 10;
      max-width: 680px;
      margin: 0 auto;
      padding: 40px 16px 80px;
    }

    /* Animated Brand Title */
    .brand-header {
      text-align: center;
      margin-bottom: 36px;
    }

    .brand-title {
      font-size: 2.85rem;
      font-weight: 800;
      letter-spacing: 2.5px;
      background: linear-gradient(90deg, #ff1744, #ff758c, #ff1744);
      background-size: 200% auto;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: shine 4s linear infinite;
      text-shadow: 0 0 35px rgba(255, 23, 68, 0.45);
    }

    @keyframes shine {
      to { background-position: 200% center; }
    }

    .verified-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-top: 8px;
      padding: 4px 14px;
      background: rgba(255, 23, 68, 0.12);
      border: 1px solid rgba(255, 23, 68, 0.35);
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 700;
      color: #ff5252;
      letter-spacing: 0.5px;
    }

    /* Catalog & Cards */
    .catalog {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      overflow: hidden;
      backdrop-filter: blur(14px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.55);
      transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .card:hover {
      transform: translateY(-3px);
      border-color: rgba(255, 23, 68, 0.5);
      box-shadow: 0 16px 36px rgba(255, 23, 68, 0.25);
    }

    .image-wrapper {
      width: 100%;
      height: 220px;
      background: #120406;
      overflow: hidden;
    }

    .image-wrapper img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }

    .card:hover .image-wrapper img {
      transform: scale(1.04);
    }

    .card-body {
      padding: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .card-details h2 {
      font-size: 1.35rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 4px;
    }

    .price-tag {
      font-size: 1.45rem;
      font-weight: 800;
      color: #ff3366;
    }

    .action-group {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    /* Buttons */
    .btn {
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: 700;
      padding: 10px 18px;
      border-radius: 10px;
      border: none;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }

    .btn-upi {
      background: var(--accent-gradient);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(255, 23, 68, 0.35);
    }

    .btn-upi:hover {
      opacity: 0.95;
      transform: scale(1.02);
      box-shadow: 0 6px 18px rgba(255, 23, 68, 0.55);
    }

    .btn-qr {
      background: rgba(255, 255, 255, 0.08);
      color: #e2e8f0;
      border: 1px solid rgba(255, 255, 255, 0.16);
    }

    .btn-qr:hover {
      background: rgba(255, 255, 255, 0.14);
      border-color: rgba(255, 255, 255, 0.3);
    }

    .btn-disabled {
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-sub);
      cursor: not-allowed;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Pop-up Modal */
    .modal-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.82);
      backdrop-filter: blur(8px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .modal-backdrop.active {
      display: flex;
    }

    .modal-box {
      background: #140609;
      border: 1px solid rgba(255, 23, 68, 0.35);
      padding: 28px 24px;
      border-radius: 20px;
      text-align: center;
      max-width: 320px;
      width: 100%;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.85);
      position: relative;
    }

    .modal-box h3 {
      font-size: 1.15rem;
      margin-bottom: 4px;
      color: #ffffff;
    }

    .modal-box p {
      font-size: 0.82rem;
      color: var(--text-sub);
      margin-bottom: 16px;
    }

    .modal-box img {
      width: 210px;
      height: 210px;
      border-radius: 12px;
      background: #ffffff;
      padding: 8px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    }

    .close-btn {
      position: absolute;
      top: 12px;
      right: 14px;
      background: none;
      border: none;
      color: var(--text-sub);
      font-size: 1.4rem;
      cursor: pointer;
    }

    .close-btn:hover { color: #fff; }
  </style>
</head>
<body>

  <!-- Fullscreen 3D Intro & Animated Background -->
  <div id="intro-bg" aria-hidden="true"></div>
  <canvas id="cyl" aria-hidden="true"></canvas>

  <div class="container">
    <header class="brand-header">
      <h1 class="brand-title">PANEL OFFICIAL</h1>
      <div class="verified-badge">● INSTANT DELIVERY ACTIVE</div>
    </header>

    <div class="catalog">
      {% for p in products %}
      <div class="card">
        <div class="image-wrapper">
          <img src="{{ p.image }}" alt="{{ p.name }}" loading="lazy">
        </div>
        <div class="card-body">
          <div class="card-details">
            <h2>{{ p.name }}</h2>
            <div class="price-tag">{{ p.price }}</div>
          </div>
          <div class="action-group">
            {% if p.live %}
              <a href="{{ p.upi_link }}" class="btn btn-upi">Pay via UPI</a>
              <button class="btn btn-qr" onclick="openQr('{{ p.qr }}', '{{ p.name }}', '{{ p.price }}')">Scan QR</button>
            {% else %}
              <span class="btn btn-disabled">Coming Soon</span>
            {% endif %}
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>

  <!-- QR Modal Pop-up -->
  <div id="qrModal" class="modal-backdrop" onclick="closeModalOnBackdrop(event)">
    <div class="modal-box">
      <button class="close-btn" onclick="closeQr()">&times;</button>
      <h3 id="modalProductName">Payment</h3>
      <p id="modalProductPrice">Scan to pay with any UPI app</p>
      <img id="modalQrImg" src="" alt="Payment QR Code">
    </div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  {% raw %}
  <script>
  (function () {
    var bg = document.getElementById('intro-bg');
    var canvas = document.getElementById('cyl');

    function abandon() {
      if (bg) bg.style.display = 'none';
      if (canvas) canvas.style.display = 'none';
    }
    if (typeof THREE === 'undefined') { abandon(); return; }

    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    } catch (e) { abandon(); return; }

    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    // Exact Dimensions: Diameter 6.0mm (Radius = 3mm), Length = 84mm
    var R = 3, L = 84;

    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(30, 1, 1, 1000);
    
    scene.add(new THREE.AmbientLight(0xffffff, 1.15));
    var key = new THREE.DirectionalLight(0xff3355, 1.2);
    key.position.set(-40, 60, 80);
    scene.add(key);

    var fill = new THREE.DirectionalLight(0xffffff, 0.5);
    fill.position.set(40, -30, -50);
    scene.add(fill);

    var side = new THREE.MeshStandardMaterial({ roughness: 0.35, metalness: 0.1, transparent: true });
    var cap = new THREE.MeshStandardMaterial({ color: 0x140407, roughness: 0.6, transparent: true });
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

      var a = (aspect < 1 ? 62 : 18) * Math.PI / 180;
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
    var BG_SCALE = 0.72, BG_OPACITY = 0.42;
    var started = false, faded = false, finished = false;
    var t0 = 0, last = 0, lastDraw = 0, spin = 0, lastY = window.scrollY || 0;

    function setLook(scale, opacity) {
      pose.scale.set(scale, scale, scale);
      side.opacity = opacity;
      cap.opacity = opacity;
    }

    function finish() {
      finished = true;
      if (bg) bg.style.display = 'none';
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
      if (started) return;
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
      grad.addColorStop(0, '#8a0a14');
      grad.addColorStop(1, '#1a0507');
      g.fillStyle = grad;
      g.fillRect(0, 0, 512, 512);
      useTexture(new THREE.CanvasTexture(c));
    }

    // Loads static/panel_artwork.jpg directly onto the cylinder
    new THREE.TextureLoader().load('/static/panel_artwork.jpg', useTexture, undefined, fallbackTexture);
  })();

  function openQr(qrUrl, name, price) {
    document.getElementById('modalQrImg').src = qrUrl;
    document.getElementById('modalProductName').innerText = name;
    document.getElementById('modalProductPrice').innerText = 'Pay ' + price + ' with any UPI app';
    document.getElementById('qrModal').classList.add('active');
  }

  function closeQr() {
    document.getElementById('qrModal').classList.remove('active');
  }

  function closeModalOnBackdrop(e) {
    if (e.target.id === 'qrModal') closeQr();
  }
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
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)
    
