import os
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

BASE_URL = "https://panel-online-services.onrender.com"

PRODUCTS = [
    {
        "id": 1,
        "name": "Panel",
        "price": "₹20",
        "image": f"{BASE_URL}/static/panel_artwork.jpg",
        "live": True,
        "upi_link": "upi://pay?pa=7276052050@fam&pn=PANEL%20OFFICIAL&am=20.00&cu=INR&tn=Panel%20Payment",
        "qr": "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=upi%3A%2F%2Fpay%3Fpa%3D7276052050%40fam%26pn%3DPANEL%2520OFFICIAL%26am%3D20.00%26cu%3DINR%26tn%3DPanel%2520Payment",
    },
    {
        "id": 2,
        "name": "Panel Pro",
        "price": "₹25",
        "image": f"{BASE_URL}/static/panel_artwork.jpg",
        "live": True,
        "upi_link": "upi://pay?pa=7276052050@fam&pn=PANEL%20OFFICIAL&am=25.00&cu=INR&tn=Panel%20Pro%20Payment",
        "qr": "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=upi%3A%2F%2Fpay%3Fpa%3D7276052050%40fam%26pn%3DPANEL%2520OFFICIAL%26am%3D25.00%26cu%3DINR%26tn%3DPanel%2520Pro%2520Payment",
    },
    {
        "id": 3,
        "name": "Panel Premium",
        "price": "₹30",
        "image": f"{BASE_URL}/static/panel_artwork.jpg",
        "live": True,
        "upi_link": "upi://pay?pa=7276052050@fam&pn=PANEL%20OFFICIAL&am=30.00&cu=INR&tn=Panel%20Premium%20Payment",
        "qr": "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=upi%3A%2F%2Fpay%3Fpa%3D7276052050%40fam%26pn%3DPANEL%2520OFFICIAL%26am%3D30.00%26cu%3DINR%26tn%3DPanel%2520Premium%2520Payment",
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

    .container {
      position: relative;
      z-index: 10;
      max-width: 680px;
      margin: 0 auto;
      padding: 40px 16px 40px;
    }

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

    .footer {
      text-align: center;
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }

    .footer-text {
      font-size: 0.9rem;
      font-weight: 600;
      letter-spacing: 0.6px;
      color: var(--text-sub);
    }

    .footer-text span {
      color: #ff4766;
      font-weight: 700;
    }

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
      padding: 28px 22px;
      border-radius: 20px;
      text-align: center;
      max-width: 360px;
      width: 100%;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.85);
      position: relative;
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

    .input-group {
      text-align: left;
      margin-bottom: 14px;
    }
    .input-group label {
      display: block;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-sub);
      margin-bottom: 5px;
    }
    .input-group input, .input-group textarea {
      width: 100%;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 8px;
      padding: 10px 12px;
      color: #ffffff;
      font-family: inherit;
      font-size: 0.88rem;
      outline: none;
    }
    .input-group input:focus, .input-group textarea:focus {
      border-color: #ff1e3c;
      box-shadow: 0 0 10px rgba(255, 30, 60, 0.3);
    }
    .input-group textarea {
      resize: vertical;
      min-height: 65px;
    }

    .modal-box img {
      width: 210px;
      height: 210px;
      border-radius: 12px;
      background: #ffffff;
      padding: 8px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
      margin: 12px auto;
      display: block;
    }
  </style>
</head>
<body>

  <!-- Audio Element (Intro Sound) -->
  <audio id="introAudio" src="/static/intro_sound.mp3" preload="auto"></audio>

  <div id="intro-bg" aria-hidden="true"></div>
  <canvas id="cyl" aria-hidden="true"></canvas>

  <div class="container">
    <header class="brand-header">
      <h1 class="brand-title">PANEL OFFICIAL</h1>
      <div class="verified-badge">● 20-30 MINS DELIVERY ACTIVE</div>
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
            <button class="btn btn-upi" onclick="openOrder('{{ p.name }}', '{{ p.price }}', '{{ p.upi_link }}', '{{ p.qr }}')">Pay via UPI</button>
            <button class="btn btn-qr" onclick="openOrder('{{ p.name }}', '{{ p.price }}', '{{ p.upi_link }}', '{{ p.qr }}')">Scan QR</button>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>

    <footer class="footer">
      <p class="footer-text">A Brand By - <span>Vijay , Sachin and Shekhar</span></p>
    </footer>
  </div>

  <!-- Order & Payment Modal -->
  <div id="orderModal" class="modal-backdrop" onclick="closeModalOnBackdrop(event)">
    <div class="modal-box">
      <button class="close-btn" onclick="closeModal()">&times;</button>
      
      <div id="step-details">
        <h3 id="formTitle" style="color:#fff; font-size:1.2rem; margin-bottom:4px;">Delivery Details</h3>
        <p style="color:var(--text-sub); font-size:0.8rem; margin-bottom:16px;">Enter details for 20-30 mins delivery</p>
        
        <form id="orderForm" onsubmit="submitDetails(event)">
          <div class="input-group">
            <label>Full Name</label>
            <input type="text" id="custName" required placeholder="Your name">
          </div>
          <div class="input-group">
            <label>Phone Number (for delivery)</label>
            <input type="tel" id="custPhone" required placeholder="e.g. 9876543210">
          </div>
          <div class="input-group">
            <label>Delivery Address / Location</label>
            <textarea id="custAddress" required placeholder="House / Flat / Area / Landmark"></textarea>
          </div>
          <button type="submit" class="btn btn-upi" style="width:100%; margin-top:8px;">Proceed to Pay</button>
        </form>
      </div>

      <div id="step-pay" style="display:none;">
        <h3 id="payTitle" style="color:#fff; font-size:1.15rem; margin-bottom:4px;"></h3>
        <p style="color:var(--text-sub); font-size:0.82rem; margin-bottom:10px;">Scan QR or click below to complete payment</p>
        <img id="payQrImg" src="" alt="Payment QR Code">
        <a id="payUpiBtn" href="" class="btn btn-upi" style="width:100%; margin-top:8px;">Open UPI App to Pay</a>
      </div>
    </div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  {% raw %}
  <script>
  // Play sound after 3 seconds with user interaction fallback for mobile browsers
  var audioPlayed = false;
  function triggerAudio() {
    if (audioPlayed) return;
    var audio = document.getElementById('introAudio');
    if (audio) {
      audio.play().then(function() {
        audioPlayed = true;
      }).catch(function() {
        // If autoplay policy blocks it, play on the first touch/click
        var unlock = function() {
          if (!audioPlayed) {
            audio.play();
            audioPlayed = true;
          }
          window.removeEventListener('click', unlock);
          window.removeEventListener('touchstart', unlock);
        };
        window.addEventListener('click', unlock);
        window.addEventListener('touchstart', unlock);
      });
    }
  }

  // Trigger precisely after 3 seconds
  setTimeout(triggerAudio, 3000);

  var currentOrder = { name: '', price: '', upi: '', qr: '' };

  function openOrder(prodName, prodPrice, upiLink, qrLink) {
    currentOrder = { name: prodName, price: prodPrice, upi: upiLink, qr: qrLink };
    document.getElementById('formTitle').innerText = prodName + ' (' + prodPrice + ')';
    document.getElementById('step-details').style.display = 'block';
    document.getElementById('step-pay').style.display = 'none';
    document.getElementById('orderModal').classList.add('active');
  }

  function closeModal() {
    document.getElementById('orderModal').classList.remove('active');
  }

  function closeModalOnBackdrop(e) {
    if (e.target.id === 'orderModal') closeModal();
  }

  function submitDetails(e) {
    e.preventDefault();
    var name = document.getElementById('custName').value.trim();
    var phone = document.getElementById('custPhone').value.trim();
    var address = document.getElementById('custAddress').value.trim();

    fetch('/save_order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        product: currentOrder.name,
        price: currentOrder.price,
        customer_name: name,
        phone: phone,
        address: address
      })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      if (data.status === 'ok') {
        document.getElementById('step-details').style.display = 'none';
        document.getElementById('step-pay').style.display = 'block';
        document.getElementById('payTitle').innerText = currentOrder.name + ' - ' + currentOrder.price;
        document.getElementById('payQrImg').src = currentOrder.qr;
        document.getElementById('payUpiBtn').href = currentOrder.upi;
      }
    })
    .catch(function(err) {
      alert('Unable to process order. Please try again.');
    });
  }

  // 3D Cylinder Simulation
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

    new THREE.TextureLoader().load('/static/panel_artwork.jpg', useTexture);
  })();
  </script>
  {% endraw %}
</body>
</html>
"""

ORDERS_FILE = "orders.txt"

@app.route("/")
def home():
    return render_template_string(PAGE, products=PRODUCTS)

@app.route("/save_order", methods=["POST"])
def save_order():
    data = request.get_json() or {}
    cust_name = data.get("customer_name", "").strip()
    phone = data.get("phone", "").strip()
    address = data.get("address", "").strip()
    product = data.get("product", "").strip()
    price = data.get("price", "").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_entry = (
        f"----------------------------------------\n"
        f"Time: 
