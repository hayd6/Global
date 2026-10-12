/**
 * GLOBAL E-COMMERCE RESEARCH PORTAL — INTERACTIVE APP LOGIC
 * Supports 6-page navigation, dynamic SVG chart rendering,
 * and client-side Purchase Propensity Prediction Calculator.
 */

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  initPredictionDemo();
  renderPSOChart();
  renderROCChart();
});

// ==========================================
// 1. NAVIGATION & TAB SWITCHING
// ==========================================
function initNavigation() {
  const navBtns = document.querySelectorAll(".nav-btn");
  const pageViews = document.querySelectorAll(".page-view");

  navBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-page");

      // Update active nav button
      navBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      // Update active page view
      pageViews.forEach((page) => {
        page.classList.remove("active");
        if (page.id === `page-${targetId}`) {
          page.classList.add("active");
        }
      });

      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
}

// ==========================================
// 2. CLIENT-SIDE PURCHASE PROPENSITY CALCULATOR
// ==========================================
function initPredictionDemo() {
  const inputs = [
    "demo-cart",
    "demo-pages",
    "demo-duration",
    "demo-loyalty",
    "demo-spend",
    "demo-recency",
    "demo-tier",
    "demo-bounce"
  ];

  inputs.forEach((id) => {
    const el = document.getElementById(id);
    if (!el) return;

    el.addEventListener("input", () => {
      // Update display text for range inputs
      const displayEl = document.getElementById(`${id}-val`);
      if (displayEl) {
        if (id === "demo-spend") {
          displayEl.textContent = `$${Number(el.value).toLocaleString()}`;
        } else if (id === "demo-bounce") {
          displayEl.textContent = `${Math.round(el.value * 100)}%`;
        } else if (id === "demo-duration") {
          displayEl.textContent = `${el.value}s`;
        } else if (id === "demo-recency") {
          displayEl.textContent = `${el.value} ngày`;
        } else {
          displayEl.textContent = el.value;
        }
      }
      calculatePropensity();
    });
  });

  // Calculate once on load
  calculatePropensity();
}

function calculatePropensity() {
  // Grab inputs
  const cart = parseFloat(document.getElementById("demo-cart")?.value || 2);
  const pages = parseFloat(document.getElementById("demo-pages")?.value || 15);
  const duration = parseFloat(document.getElementById("demo-duration")?.value || 300);
  const loyalty = parseFloat(document.getElementById("demo-loyalty")?.value || 3.5);
  const spend = parseFloat(document.getElementById("demo-spend")?.value || 2500);
  const recency = parseFloat(document.getElementById("demo-recency")?.value || 14);
  const tier = document.getElementById("demo-tier")?.value || "Gold";
  const bounce = parseFloat(document.getElementById("demo-bounce")?.value || 0.25);

  // Empirical scoring weights derived from XGBoost Gain and PSO features
  let logOdds = -2.15; // Base log-odds (reflecting 20.3% prior conversion rate)

  // Behavioral signals
  logOdds += (cart - 1.5) * 0.42;                    // Cart additions are #1 predictor
  logOdds += Math.log(pages + 1) * 0.28;             // Pages viewed
  logOdds += Math.log(duration / 60 + 1) * 0.22;     // Duration in minutes
  logOdds += (loyalty - 2.5) * 0.35;                 // Loyalty score
  logOdds += Math.log(spend / 500 + 1) * 0.18;       // Monetary spend
  logOdds -= (recency / 30) * 0.25;                  // Recency decay
  logOdds -= (bounce - 0.20) * 0.85;                 // High bounce rate penalty

  // Tier multiplier
  if (tier === "Platinum") logOdds += 0.55;
  else if (tier === "Gold") logOdds += 0.30;
  else if (tier === "Silver") logOdds += 0.10;
  else if (tier === "Bronze") logOdds -= 0.15;

  // Sigmoid transfer to probability [0, 1]
  const probability = 1 / (1 + Math.exp(-logOdds));
  const pct = Math.max(0.01, Math.min(0.99, probability));
  const scoreDisplay = (pct * 100).toFixed(1);

  // Update DOM Score & Gauge
  const scoreEl = document.getElementById("demo-score-text");
  if (scoreEl) scoreEl.textContent = `${scoreDisplay}%`;

  const gaugeBar = document.getElementById("gauge-fill-path");
  if (gaugeBar) {
    // Semi-circle length is ~157px for radius 50
    const offset = 157 * (1 - pct);
    gaugeBar.style.strokeDashoffset = offset;
  }

  // Update Badge and Action
  const badgeEl = document.getElementById("demo-risk-badge");
  const actionEl = document.getElementById("demo-action-text");

  if (pct >= 0.50) {
    if (badgeEl) {
      badgeEl.className = "risk-badge risk-high";
      badgeEl.textContent = "Ý ĐỊNH MUA RẤT CAO ($\\hat{y} = 1$)";
    }
    if (actionEl) {
      actionEl.innerHTML = `<strong>Khuyến nghị tự động:</strong> Khách hàng có xu hướng chốt đơn cao (${scoreDisplay}%). Kích hoạt thông báo xác nhận ưu đãi tại trang thanh toán và ưu tiên dịch vụ giao hàng nhanh để tối ưu trải nghiệm.`;
    }
  } else if (pct >= 0.30) {
    if (badgeEl) {
      badgeEl.className = "risk-badge risk-med";
      badgeEl.textContent = "TIỀM NĂNG TRUNG BÌNH (Cần Kích Hoạt)";
    }
    if (actionEl) {
      actionEl.innerHTML = `<strong>Khuyến nghị tự động:</strong> Khách hàng đang trong giai đoạn so sánh/cân nhắc (${scoreDisplay}%). Đề xuất gửi email nhắc nhở giỏ hàng kèm mã voucher giảm giá 10% có thời hạn 48 giờ.`;
    }
  } else {
    if (badgeEl) {
      badgeEl.className = "risk-badge risk-low";
      badgeEl.textContent = "Ý ĐỊNH THẤP ($\\hat{y} = 0$)";
    }
    if (actionEl) {
      actionEl.innerHTML = `<strong>Khuyến nghị tự động:</strong> Xác suất mua hàng thấp (${scoreDisplay}%). Tránh lãng phí ngân sách tiếp thị trực tiếp; duy trì hiển thị sản phẩm đề xuất đại trà tại trang danh mục.`;
    }
  }
}

// ==========================================
// 3. DYNAMIC SVG CHARTS RENDERING
// ==========================================
function renderPSOChart() {
  const container = document.getElementById("pso-chart-container");
  if (!container) return;

  const iterations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  const bestFitness = [0.2512, 0.2689, 0.2845, 0.2991, 0.3084, 0.3150, 0.3212, 0.3245, 0.3245, 0.3245];
  const avgFitness = [0.2105, 0.2314, 0.2510, 0.2688, 0.2812, 0.2905, 0.2990, 0.3042, 0.3081, 0.3110];

  const w = 480;
  const h = 220;
  const pad = 40;

  // Scale functions
  const minF = 0.20;
  const maxF = 0.35;
  const getX = (i) => pad + ((i - 1) / (10 - 1)) * (w - 2 * pad);
  const getY = (val) => h - pad - ((val - minF) / (maxF - minF)) * (h - 2 * pad);

  // Generate paths
  let bestPath = `M ${getX(1)} ${getY(bestFitness[0])}`;
  let avgPath = `M ${getX(1)} ${getY(avgFitness[0])}`;

  for (let i = 1; i < 10; i++) {
    bestPath += ` L ${getX(i + 1)} ${getY(bestFitness[i])}`;
    avgPath += ` L ${getX(i + 1)} ${getY(avgFitness[i])}`;
  }

  container.innerHTML = `
    <svg viewBox="0 0 ${w} ${h}" style="width: 100%; height: auto;">
      <!-- Grid lines -->
      <line x1="${pad}" y1="${getY(0.25)}" x2="${w - pad}" y2="${getY(0.25)}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="4" />
      <line x1="${pad}" y1="${getY(0.30)}" x2="${w - pad}" y2="${getY(0.30)}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="4" />
      <line x1="${pad}" y1="${getY(0.35)}" x2="${w - pad}" y2="${getY(0.35)}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="4" />

      <!-- Axes -->
      <line x1="${pad}" y1="${h - pad}" x2="${w - pad}" y2="${h - pad}" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" />
      <line x1="${pad}" y1="${pad / 2}" x2="${pad}" y2="${h - pad}" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" />

      <!-- Labels -->
      <text x="${pad - 8}" y="${getY(0.25) + 4}" fill="#64748b" font-size="10" text-anchor="end">0.25</text>
      <text x="${pad - 8}" y="${getY(0.30) + 4}" fill="#64748b" font-size="10" text-anchor="end">0.30</text>
      <text x="${pad - 8}" y="${getY(0.35) + 4}" fill="#64748b" font-size="10" text-anchor="end">0.35</text>
      <text x="${w / 2}" y="${h - 8}" fill="#64748b" font-size="11" text-anchor="middle">Vòng lặp (Iterations 1-10)</text>

      <!-- Curves -->
      <path d="${avgPath}" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="3,3" />
      <path d="${bestPath}" fill="none" stroke="#6366f1" stroke-width="3" />

      <!-- Dots on best curve -->
      ${bestFitness.map((val, i) => `<circle cx="${getX(i + 1)}" cy="${getY(val)}" r="3.5" fill="#6366f1" />`).join("")}

      <!-- Legend -->
      <circle cx="${w - 180}" cy="18" r="4" fill="#6366f1" />
      <text x="${w - 170}" y="22" fill="#f8fafc" font-size="11">Best Fitness (0.3245)</text>
      <circle cx="${w - 180}" cy="34" r="4" fill="#f59e0b" />
      <text x="${w - 170}" y="38" fill="#94a3b8" font-size="11">Avg Fitness</text>
    </svg>
  `;
}

function renderROCChart() {
  const container = document.getElementById("roc-chart-container");
  if (!container) return;

  const w = 480;
  const h = 220;
  const pad = 40;

  // Approximate ROC curve points for E2 (0.6105), E4 (0.6006), E5 (0.5846)
  const getX = (fpr) => pad + fpr * (w - 2 * pad);
  const getY = (tpr) => h - pad - tpr * (h - 2 * pad);

  container.innerHTML = `
    <svg viewBox="0 0 ${w} ${h}" style="width: 100%; height: auto;">
      <!-- Diagonal random line -->
      <line x1="${pad}" y1="${h - pad}" x2="${w - pad}" y2="${pad / 2}" stroke="rgba(255,255,255,0.15)" stroke-dasharray="4" />

      <!-- Axes -->
      <line x1="${pad}" y1="${h - pad}" x2="${w - pad}" y2="${h - pad}" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" />
      <line x1="${pad}" y1="${pad / 2}" x2="${pad}" y2="${h - pad}" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" />

      <!-- Ticks -->
      <text x="${pad}" y="${h - pad + 15}" fill="#64748b" font-size="10" text-anchor="middle">0.0</text>
      <text x="${w / 2}" y="${h - pad + 15}" fill="#64748b" font-size="10" text-anchor="middle">0.5</text>
      <text x="${w - pad}" y="${h - pad + 15}" fill="#64748b" font-size="10" text-anchor="middle">1.0 (FPR)</text>
      <text x="${pad - 10}" y="${h - pad}" fill="#64748b" font-size="10" text-anchor="end">0.0</text>
      <text x="${pad - 10}" y="${getY(0.5) + 4}" fill="#64748b" font-size="10" text-anchor="end">0.5</text>
      <text x="${pad - 10}" y="${pad / 2 + 8}" fill="#64748b" font-size="10" text-anchor="end">1.0 (TPR)</text>

      <!-- Curve E2 (ANOVA AUC = 0.6105) -->
      <path d="M ${pad} ${h - pad} Q ${pad + 90} ${getY(0.55)}, ${w - pad} ${pad / 2}" fill="none" stroke="#10b981" stroke-width="2.5" />

      <!-- Curve E4 (XGBoost Full AUC = 0.6006) -->
      <path d="M ${pad} ${h - pad} Q ${pad + 105} ${getY(0.52)}, ${w - pad} ${pad / 2}" fill="none" stroke="#6366f1" stroke-width="2.5" />

      <!-- Curve E5 (XGBoost PSO AUC = 0.5846) -->
      <path d="M ${pad} ${h - pad} Q ${pad + 120} ${getY(0.48)}, ${w - pad} ${pad / 2}" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,2" />

      <!-- Legend -->
      <circle cx="${w - 170}" cy="20" r="3.5" fill="#10b981" />
      <text x="${w - 160}" y="23" fill="#f8fafc" font-size="10">E2 ANOVA (0.6105)</text>
      <circle cx="${w - 170}" cy="34" r="3.5" fill="#6366f1" />
      <text x="${w - 160}" y="37" fill="#f8fafc" font-size="10">E4 XGB Full (0.6006)</text>
      <circle cx="${w - 170}" cy="48" r="3.5" fill="#f59e0b" />
      <text x="${w - 160}" y="51" fill="#94a3b8" font-size="10">E5 XGB PSO (0.5846)</text>
    </svg>
  `;
}
