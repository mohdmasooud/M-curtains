/**
 * M Curtains - Ultra-Fast & Smooth 3D Interactive Engine (60fps Optimized)
 */

document.addEventListener('DOMContentLoaded', () => {
  initScrollProgressBar();
  init3DHeroCanvas();
  init3DTiltCards();
  initScrollRevealObserver();
  initLiveCounters();
  init3DAtelierStudio();
  initVIPClubForm();
});

/* ==========================================================================
   1. HARDWARE-ACCELERATED TOP SCROLL PROGRESS BAR
   ========================================================================== */
function initScrollProgressBar() {
  const progressBar = document.getElementById('scrollProgressBar');
  if (!progressBar) return;

  let ticking = false;

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = `${Math.min(scrollPercent, 100)}%`;
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}

/* ==========================================================================
   2. HIGH-PERFORMANCE 3D GOLD STARDUST CANVAS (AUTO-PAUSES OFFSCREEN)
   ========================================================================== */
function init3DHeroCanvas() {
  const canvas = document.getElementById('hero3DCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];
  const particleCount = window.innerWidth < 768 ? 16 : 28;
  let isCanvasVisible = true;
  let animationFrameId = null;

  function resizeCanvas() {
    const parent = canvas.parentElement;
    if (!parent) return;
    width = canvas.width = parent.offsetWidth;
    height = canvas.height = parent.offsetHeight;
  }

  resizeCanvas();
  window.addEventListener('resize', resizeCanvas, { passive: true });

  // Auto-pause animation when user scrolls away from hero to preserve 100% CPU/GPU
  const canvasObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      isCanvasVisible = entry.isIntersecting;
      if (isCanvasVisible && !animationFrameId) {
        animate();
      } else if (!isCanvasVisible && animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
      }
    });
  }, { threshold: 0.05 });

  canvasObserver.observe(canvas);

  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.z = Math.random() * 0.7 + 0.3;
      this.radius = (Math.random() * 1.8 + 0.8) * this.z;
      this.vx = (Math.random() - 0.5) * 0.4 * this.z;
      this.vy = (Math.random() - 0.5) * 0.4 * this.z - 0.15 * this.z;
      this.alpha = Math.random() * 0.5 + 0.25;
      this.color = Math.random() > 0.4 ? '#dfba43' : '#f5eedc';
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0) this.x = width;
      if (this.x > width) this.x = 0;
      if (this.y < 0) this.y = height;
      if (this.y > height) this.y = 0;
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.globalAlpha = this.alpha * this.z;
      ctx.fill();
    }
  }

  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }

  function drawConnections() {
    const maxDist = 80;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < maxDist) {
          const alpha = (1 - dist / maxDist) * 0.15 * particles[i].z;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = '#c5a880';
          ctx.globalAlpha = alpha;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    if (!isCanvasVisible) {
      animationFrameId = null;
      return;
    }

    ctx.clearRect(0, 0, width, height);
    drawConnections();
    particles.forEach((p) => {
      p.update();
      p.draw();
    });

    animationFrameId = requestAnimationFrame(animate);
  }

  animate();
}

/* ==========================================================================
   3. OPTIMIZED 3D CARD PARALLAX TILT ENGINE
   ========================================================================== */
function init3DTiltCards() {
  if (window.innerWidth < 992) return; // Only enable on desktop for maximum mobile performance

  const tiltCards = document.querySelectorAll('.tilt-card-3d');

  tiltCards.forEach((card) => {
    let glare = card.querySelector('.tilt-glare-effect');
    if (!glare) {
      glare = document.createElement('div');
      glare.className = 'tilt-glare-effect';
      card.appendChild(glare);
    }

    const maxTilt = parseFloat(card.getAttribute('data-max-tilt') || '8');
    let rect = null;
    let rafId = null;

    card.addEventListener('mouseenter', () => {
      rect = card.getBoundingClientRect();
    });

    card.addEventListener('mousemove', (e) => {
      if (!rect) rect = card.getBoundingClientRect();

      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      if (rafId) cancelAnimationFrame(rafId);

      rafId = requestAnimationFrame(() => {
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -maxTilt;
        const rotateY = ((x - centerX) / centerX) * maxTilt;

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(1)}deg) rotateY(${rotateY.toFixed(1)}deg) translateZ(0)`;

        const glareX = (x / rect.width) * 100;
        const glareY = (y / rect.height) * 100;
        glare.style.opacity = '0.4';
        glare.style.background = `radial-gradient(circle at ${glareX}% ${glareY}%, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 60%)`;
      });
    });

    card.addEventListener('mouseleave', () => {
      rect = null;
      if (rafId) cancelAnimationFrame(rafId);
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0)';
      glare.style.opacity = '0';
    });
  });
}

/* ==========================================================================
   4. SCROLL REVEAL OBSERVER
   ========================================================================== */
function initScrollRevealObserver() {
  const revealElements = document.querySelectorAll('.reveal-on-scroll, .reveal-3d-left, .reveal-3d-right, .reveal-scale');

  if (!revealElements.length) return;

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal-active');
          obs.unobserve(entry.target); // Once revealed, stop tracking to save CPU
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -30px 0px',
    }
  );

  revealElements.forEach((el) => observer.observe(el));
}

/* ==========================================================================
   5. DYNAMIC STATISTIC COUNTERS
   ========================================================================== */
function initLiveCounters() {
  const counterElements = document.querySelectorAll('[data-count-to]');
  if (!counterElements.length) return;

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseFloat(el.getAttribute('data-count-to'));
          const prefix = el.getAttribute('data-prefix') || '';
          const suffix = el.getAttribute('data-suffix') || '';
          const isDecimal = target % 1 !== 0;
          const duration = 1400; // ms
          const startTime = performance.now();

          function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const currentVal = easeProgress * target;

            el.textContent = `${prefix}${isDecimal ? currentVal.toFixed(2) : Math.floor(currentVal).toLocaleString()}${suffix}`;

            if (progress < 1) {
              requestAnimationFrame(updateCounter);
            } else {
              el.textContent = `${prefix}${isDecimal ? target.toFixed(2) : target.toLocaleString()}${suffix}`;
            }
          }

          requestAnimationFrame(updateCounter);
          obs.unobserve(el);
        }
      });
    },
    { threshold: 0.2 }
  );

  counterElements.forEach((el) => observer.observe(el));
}

/* ==========================================================================
   6. INTERACTIVE 3D ATELIER DRAPERY STUDIO CONTROLLER
   ========================================================================== */
function init3DAtelierStudio() {
  const windowFrame = document.getElementById('studioWindowFrame');
  const leftPanel = document.getElementById('studioLeftPanel');
  const rightPanel = document.getElementById('studioRightPanel');
  const drawSlider = document.getElementById('studioDrawSlider');
  const drawValText = document.getElementById('studioDrawValText');
  const fabricButtons = document.querySelectorAll('[data-studio-fabric]');
  const lightButtons = document.querySelectorAll('[data-studio-light]');
  const fabricNameLabel = document.getElementById('studioFabricNameLabel');
  const fabricDescLabel = document.getElementById('studioFabricDescLabel');

  if (!windowFrame || !leftPanel || !rightPanel) return;

  const fabrics = {
    gold_velvet: {
      name: 'Champagne Gold Imperial Silk Velvet',
      desc: '420 GSM heavy drape with luminous incandescent highlights & acoustic dampening.',
      textureUrl: '/static/images/curtain_gold_velvet.jpg',
    },
    emerald_velvet: {
      name: 'Heritage Emerald Royal Velvet',
      desc: 'Deep jewel emerald silk pile providing stately winter insulation and light reduction.',
      textureUrl: '/static/images/curtain_emerald_velvet.jpg',
    },
    nordic_linen: {
      name: 'Normandy Pure Washed Flax Linen',
      desc: 'Organic washed flax offering relaxed natural slub textures and soft daylight diffusion.',
      textureUrl: '/static/images/curtain_nordic_linen.jpg',
    },
    navy_blackout: {
      name: 'Obsidian Midnight 100% Total Blackout',
      desc: 'Bonded 3-pass architectural blackout twill for total restorative darkness.',
      textureUrl: '/static/images/curtain_blackout_navy.jpg',
    },
  };

  // Fabric Switcher
  fabricButtons.forEach((btn) => {
    btn.addEventListener('click', function () {
      const key = this.getAttribute('data-studio-fabric');
      const fabric = fabrics[key];
      if (!fabric) return;

      fabricButtons.forEach((b) => b.classList.remove('active'));
      this.classList.add('active');

      leftPanel.style.backgroundImage = `url('${fabric.textureUrl}')`;
      rightPanel.style.backgroundImage = `url('${fabric.textureUrl}')`;

      if (fabricNameLabel) fabricNameLabel.textContent = fabric.name;
      if (fabricDescLabel) fabricDescLabel.textContent = fabric.desc;
    });
  });

  // Ambient Lighting Switcher
  lightButtons.forEach((btn) => {
    btn.addEventListener('click', function () {
      const lightMode = this.getAttribute('data-studio-light');
      lightButtons.forEach((b) => b.classList.remove('active'));
      this.classList.add('active');

      windowFrame.classList.remove('ambient-day', 'ambient-sunset', 'ambient-night');
      windowFrame.classList.add(`ambient-${lightMode}`);
    });
  });

  // Curtain Draw Slider
  if (drawSlider) {
    drawSlider.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      leftPanel.style.width = `${val}%`;
      rightPanel.style.width = `${val}%`;

      if (drawValText) {
        if (val <= 20) {
          drawValText.textContent = 'Fully Open (100% Daylight)';
        } else if (val >= 48) {
          drawValText.textContent = 'Fully Closed (Full Coverage)';
        } else {
          drawValText.textContent = `${Math.round((val / 48) * 100)}% Drawn`;
        }
      }
    });
  }
}

/* ==========================================================================
   7. VIP CONCIERGE CLUB NEWSLETTER FORM (SMOOTH TOAST FEEDBACK)
   ========================================================================== */
function initVIPClubForm() {
  const form = document.getElementById('vipConciergeForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const emailInput = form.querySelector('input[type="email"]');
    const email = emailInput ? emailInput.value.trim() : '';

    if (email) {
      // Create modern floating toast
      const toast = document.createElement('div');
      toast.className = 'position-fixed bottom-0 end-0 p-3';
      toast.style.zIndex = '99999';
      toast.innerHTML = `
        <div class="toast show align-items-center text-white bg-dark border border-warning shadow-lg rounded-4 p-2" role="alert">
          <div class="d-flex">
            <div class="toast-body d-flex align-items-center gap-2">
              <i class="fas fa-crown text-warning fs-4"></i>
              <div>
                <strong class="text-warning">Welcome to the VIP Atelier!</strong>
                <div class="small text-light opacity-90">Your 15% VIP promo code <code class="text-warning fw-bold">LUXEVIP15</code> is active.</div>
              </div>
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
          </div>
        </div>
      `;
      document.body.appendChild(toast);
      form.reset();

      setTimeout(() => {
        toast.remove();
      }, 7000);
    }
  });
}
