/**
 * M Curtains - Haute Bespoke Sizing & Custom Pricing Calculator Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  // =========================================================================
  // 1. PRODUCT DETAIL LIVE CUSTOMIZER (Single Product Page Support)
  // =========================================================================
  const priceDisplay = document.getElementById('liveCalculatedPrice');
  const widthInput = document.getElementById('customWidthInput');
  const dropInput = document.getElementById('customDropInput');
  const pleatRadios = document.querySelectorAll('input[name="pleat_id"]');
  const liningRadios = document.querySelectorAll('input[name="lining_id"]');
  const productIdInput = document.getElementById('customizerProductId');

  function updateLiveProductPrice() {
    if (!productIdInput || !priceDisplay) return;

    const productId = productIdInput.value;
    const width = widthInput ? widthInput.value : 140;
    const drop = dropInput ? dropInput.value : 225;
    
    let pleatId = '';
    const checkedPleat = document.querySelector('input[name="pleat_id"]:checked');
    if (checkedPleat) pleatId = checkedPleat.value;

    let liningId = '';
    const checkedLining = document.querySelector('input[name="lining_id"]:checked');
    if (checkedLining) liningId = checkedLining.value;

    fetch(`/products/calculate-price/${productId}/?width=${width}&drop=${drop}&pleat_id=${pleatId}&lining_id=${liningId}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          priceDisplay.textContent = data.formatted_price;
          priceDisplay.classList.add('text-success');
          setTimeout(() => priceDisplay.classList.remove('text-success'), 300);
        }
      })
      .catch((err) => console.error('Price calculation error:', err));
  }

  if (widthInput && dropInput) {
    widthInput.addEventListener('input', updateLiveProductPrice);
    dropInput.addEventListener('input', updateLiveProductPrice);
  }
  pleatRadios.forEach((radio) => radio.addEventListener('change', updateLiveProductPrice));
  liningRadios.forEach((radio) => radio.addEventListener('change', updateLiveProductPrice));


  // =========================================================================
  // 2. STANDALONE ATELIER MEASUREMENT & SIZING CALCULATOR STUDIO
  // =========================================================================
  const studioRoot = document.getElementById('calculatorStudioRoot');
  if (!studioRoot) return;

  // Initial Selected Elements
  const productSelector = document.getElementById('calcProductSelector');
  const initialOption = productSelector ? productSelector.options[productSelector.selectedIndex] : null;

  // Selected Pleat & Lining Defaults
  const initialPleatCard = document.querySelector('.calc-pleat-opt.selected') || document.querySelector('.calc-pleat-opt');
  const initialLiningCard = document.querySelector('.calc-lining-opt.selected') || document.querySelector('.calc-lining-opt');

  // State
  const state = {
    unit: 'cm', // 'cm', 'in', 'ft'
    widthCm: 220,
    dropCm: 245,
    panelSplit: 'pair', // 'pair', 'single_left', 'single_right'
    hardware: 'track', // 'track', 'pole_rings', 'grommet'
    hangingStyle: 'floating', // 'floating', 'kiss', 'break', 'puddle', 'sill', 'below_sill'
    fullness: initialPleatCard ? parseFloat(initialPleatCard.dataset.fullness) || 2.0 : 2.0,
    pleatId: initialPleatCard ? initialPleatCard.dataset.id || '1' : '1',
    pleatName: initialPleatCard ? initialPleatCard.dataset.name || 'Pinch Pleat' : 'Pinch Pleat',
    pleatCost: initialPleatCard ? parseFloat(initialPleatCard.dataset.cost) || 0 : 0,
    liningId: initialLiningCard ? initialLiningCard.dataset.id || '1' : '1',
    liningName: initialLiningCard ? initialLiningCard.dataset.name || 'Standard Unlined' : 'Standard Unlined',
    liningCost: initialLiningCard ? parseFloat(initialLiningCard.dataset.cost) || 0 : 0,
    productId: initialOption ? initialOption.dataset.id || '1' : '1',
    productName: initialOption ? initialOption.dataset.name || 'Bespoke Curtains' : 'Bespoke Curtains',
    productSlug: initialOption ? initialOption.dataset.slug || '' : '',
    productBasePrice: initialOption ? parseFloat(initialOption.dataset.price) || 2499 : 2499,
    curtainColor: initialOption ? initialOption.dataset.color || '#C5A880' : '#C5A880',
    curtainColorName: initialOption ? initialOption.dataset.colorName || 'Champagne Gold' : 'Champagne Gold',
    curtainDrawnOpen: 0.15, // 0 = closed, 1 = open
    quantity: 1
  };

  // Hanging style drop adjustments in CM
  const hangingAdjustments = {
    floating: -1.5,
    kiss: 0,
    break: 2.0,
    puddle: 8.0,
    sill: -1.0,
    below_sill: 15.0
  };

  // Unit conversion helpers
  function cmToCurrentUnit(cmVal) {
    if (state.unit === 'in') return (cmVal / 2.54).toFixed(1);
    if (state.unit === 'ft') return (cmVal / 30.48).toFixed(2);
    return Math.round(cmVal);
  }

  function currentUnitToCm(val) {
    const num = parseFloat(val) || 0;
    if (state.unit === 'in') return num * 2.54;
    if (state.unit === 'ft') return num * 30.48;
    return num;
  }

  function formatMeasurement(cmVal) {
    if (state.unit === 'in') return `${(cmVal / 2.54).toFixed(1)} in`;
    if (state.unit === 'ft') {
      const totalInches = cmVal / 2.54;
      const feet = Math.floor(totalInches / 12);
      const inches = Math.round(totalInches % 12);
      return `${feet}' ${inches}" (${(cmVal / 30.48).toFixed(2)} ft)`;
    }
    return `${Math.round(cmVal)} cm`;
  }

  // Interactive Inputs
  const trackWidthNum = document.getElementById('calcTrackWidthNum');
  const trackWidthRange = document.getElementById('calcTrackWidthRange');
  const windowDropNum = document.getElementById('calcWindowDropNum');
  const windowDropRange = document.getElementById('calcWindowDropRange');
  const unitLabelElements = document.querySelectorAll('.dynamic-unit-label');
  const drawCurtainSlider = document.getElementById('calcDrawCurtainSlider');
  const qtyInput = document.getElementById('calcQuantityInput');
  const qtyMinusBtn = document.getElementById('qtyMinusBtn');
  const qtyPlusBtn = document.getElementById('qtyPlusBtn');

  // Hidden Form Inputs for Add-to-Cart
  const formWidthCm = document.getElementById('formWidthCm');
  const formDropCm = document.getElementById('formDropCm');
  const formPleatId = document.getElementById('formPleatId');
  const formLiningId = document.getElementById('formLiningId');
  const bespokeCartForm = document.getElementById('bespokeAddToCartForm');
  const linkOpenCustomizer = document.getElementById('linkOpenCustomizer');
  const conciergeModalNotes = document.getElementById('conciergeModalNotes');

  // Outputs
  const outPanels = document.getElementById('outPanelsCount');
  const outFinishedDrop = document.getElementById('outFinishedDrop');
  const outCutLength = document.getElementById('outCutLength');
  const outFabricMeters = document.getElementById('outFabricMeters');
  const outTotalFlatWidth = document.getElementById('outTotalFlatWidth');
  const outStackBack = document.getElementById('outStackBack');
  const outHardware = document.getElementById('outHardwareRec');
  const outPrice = document.getElementById('outEstimatedPrice');
  const outPriceBreakdown = document.getElementById('outPriceBreakdown');
  const svgCanvas = document.getElementById('curtainSvgStage');

  // Product Banner Elements
  const selectedProductImg = document.getElementById('selectedProductImg');
  const selectedProductTitle = document.getElementById('selectedProductTitle');
  const selectedProductCategory = document.getElementById('selectedProductCategory');
  const selectedProductColorDot = document.getElementById('selectedProductColorDot');
  const selectedProductColorName = document.getElementById('selectedProductColorName');
  const selectedProductBasePrice = document.getElementById('selectedProductBasePrice');
  const selectedProductLink = document.getElementById('selectedProductLink');

  // Sync Input Elements with State
  function syncInputsFromState() {
    if (trackWidthNum) trackWidthNum.value = cmToCurrentUnit(state.widthCm);
    if (trackWidthRange) trackWidthRange.value = state.widthCm;
    if (windowDropNum) windowDropNum.value = cmToCurrentUnit(state.dropCm);
    if (windowDropRange) windowDropRange.value = state.dropCm;

    unitLabelElements.forEach(el => {
      el.textContent = state.unit;
    });

    if (qtyInput) qtyInput.value = state.quantity;
  }

  // Calculate Specifications & Update Form
  function calculateSpecs() {
    const width = state.widthCm;
    const drop = state.dropCm;
    const fullness = state.fullness;
    const hangOffset = hangingAdjustments[state.hangingStyle] || 0;

    // Hardware adjustment
    let hardwareOffset = 0;
    if (state.hardware === 'pole_rings') hardwareOffset = -2.5; // distance from top of pole to eyelet
    if (state.hardware === 'grommet') hardwareOffset = +2.5; // grommet header rises above pole

    const finishedDropCm = Math.max(30, drop + hangOffset + hardwareOffset);
    const cutLengthCm = finishedDropCm + 12 + 10; // 12cm double bottom hem + 10cm buckram header

    // Fabric width
    const totalFlatWidthCm = width * fullness;
    const standardRollWidth = 140; // cm

    let rawPanels = totalFlatWidthCm / standardRollWidth;
    let panelsCount = Math.max(1, Math.ceil(rawPanels));
    
    if (state.panelSplit === 'pair') {
      if (panelsCount % 2 !== 0) panelsCount += 1;
      if (panelsCount < 2) panelsCount = 2;
    }

    // Fabric meterage
    const fabricMeters = Math.ceil((panelsCount * cutLengthCm) / 100 * 10) / 10;
    const fabricYards = (fabricMeters * 1.09361).toFixed(1);

    // Stack-back required
    const stackBackCm = Math.round(width * (fullness > 2.0 ? 0.26 : 0.20) + 12);

    // Hardware specifications
    let bracketsCount = 2;
    if (width > 300) bracketsCount = 4;
    else if (width > 180) bracketsCount = 3;
    const ringsCount = Math.ceil(width / 10);

    // Update Output Elements in Dashboard
    if (outPanels) {
      if (state.panelSplit === 'pair') {
        outPanels.textContent = `${panelsCount} Panels (${panelsCount / 2} Pair${panelsCount / 2 > 1 ? 's' : ''})`;
      } else {
        outPanels.textContent = `${panelsCount} Panel${panelsCount > 1 ? 's' : ''} (Single)`;
      }
    }

    if (outFinishedDrop) outFinishedDrop.textContent = formatMeasurement(finishedDropCm);
    if (outCutLength) outCutLength.textContent = `${formatMeasurement(cutLengthCm)} (incl. 22cm hems)`;
    if (outFabricMeters) outFabricMeters.textContent = `~${fabricMeters} m (${fabricYards} yds)`;
    if (outTotalFlatWidth) outTotalFlatWidth.textContent = `${formatMeasurement(totalFlatWidthCm)} (${fullness}x Fullness)`;
    if (outStackBack) outStackBack.textContent = `~${formatMeasurement(stackBackCm)} clearance`;
    if (outHardware) outHardware.textContent = `${bracketsCount} Brackets • ${ringsCount} Rings`;

    // Update Hidden Form Fields for Add-to-Cart
    if (formWidthCm) formWidthCm.value = Math.round(width);
    if (formDropCm) formDropCm.value = Math.round(finishedDropCm);
    if (formPleatId) formPleatId.value = state.pleatId;
    if (formLiningId) formLiningId.value = state.liningId;
    if (bespokeCartForm) bespokeCartForm.action = `/cart/add/${state.productId}/`;

    if (linkOpenCustomizer && state.productSlug) {
      linkOpenCustomizer.href = `/products/${state.productSlug}/?width=${Math.round(width)}&drop=${Math.round(finishedDropCm)}&pleat_id=${state.pleatId}&lining_id=${state.liningId}`;
    }

    if (conciergeModalNotes) {
      conciergeModalNotes.value = `Curtain: ${state.productName}\nTrack Width: ${formatMeasurement(width)}\nDrop: ${formatMeasurement(finishedDropCm)}\nHanging Style: ${state.hangingStyle}\nPleat: ${state.pleatName}\nLining: ${state.liningName}\nPanels: ${panelsCount}`;
    }

    // Dynamic Price Calculation via API or Fallback
    fetchCustomPrice(width, finishedDropCm, state.pleatId, state.liningId, state.quantity, panelsCount, fabricMeters);

    // Render Dynamic SVG Visualizer
    renderSvgVisualizer({
      widthCm: width,
      dropCm: drop,
      finishedDropCm: finishedDropCm,
      hangingStyle: state.hangingStyle,
      fullness: fullness,
      panelSplit: state.panelSplit,
      curtainColor: state.curtainColor,
      drawnRatio: state.curtainDrawnOpen,
      stackBackCm: stackBackCm
    });
  }

  // Fetch or calculate price dynamically
  let priceFetchTimeout = null;
  function fetchCustomPrice(width, drop, pleatId, liningId, quantity, panelsCount, fabricMeters) {
    if (!state.productId) return;

    // Instant local estimate for zero latency
    const baseStdArea = 140 * 225;
    const customArea = width * drop;
    const areaRatio = customArea / baseStdArea;
    const baseCalc = state.productBasePrice * (0.5 + 0.5 * areaRatio);
    const unitTotal = baseCalc + state.pleatCost + state.liningCost;
    const estimatedTotal = Math.round(unitTotal * quantity);

    if (outPrice) outPrice.textContent = `₹${estimatedTotal.toLocaleString('en-IN')}`;
    if (outPriceBreakdown) {
      outPriceBreakdown.textContent = `${quantity}x ${state.productName} • ${state.pleatName} • ${state.liningName}`;
    }

    // Debounced API confirmation to sync with backend model
    clearTimeout(priceFetchTimeout);
    priceFetchTimeout = setTimeout(() => {
      fetch(`/products/calculate-price/${state.productId}/?width=${Math.round(width)}&drop=${Math.round(drop)}&pleat_id=${pleatId}&lining_id=${liningId}`)
        .then(res => res.json())
        .then(data => {
          if (data.success && data.calculated_price) {
            const apiTotal = Math.round(data.calculated_price * quantity);
            if (outPrice) outPrice.textContent = `₹${apiTotal.toLocaleString('en-IN')}`;
          }
        })
        .catch(err => {
          // Local calculation continues gracefully if API is unreachable
          console.debug('Using local price calculation fallback');
        });
    }, 200);
  }

  // =========================================================================
  // 3. DYNAMIC REAL-TIME SVG WINDOW & DRAPERY SIMULATOR
  // =========================================================================
  function renderSvgVisualizer(data) {
    if (!svgCanvas) return;

    const svgWidth = 560;
    const svgHeight = 320;
    const floorY = 270;
    const rodY = 48;
    const maxWindowWidth = 380;
    const windowLeft = (svgWidth - maxWindowWidth) / 2;
    const windowRight = windowLeft + maxWindowWidth;

    // Hanging style offset in pixels on stage
    let floorGap = 12; // floating gap
    if (data.hangingStyle === 'kiss') floorGap = 0;
    else if (data.hangingStyle === 'break') floorGap = -5;
    else if (data.hangingStyle === 'puddle') floorGap = -14;
    else if (data.hangingStyle === 'sill') floorGap = 65;
    else if (data.hangingStyle === 'below_sill') floorGap = 40;

    const curtainBottomY = floorY - floorGap;
    const curtainHeight = curtainBottomY - rodY;

    // Fullness pleat count (higher fullness = denser wave pleats)
    const waveFreq = Math.round(data.fullness * 5);
    const colorHex = data.curtainColor;

    const drawn = data.drawnRatio; // 0 = closed, 1 = fully open
    const rodLeft = windowLeft - 24;
    const rodRight = windowRight + 24;

    let draperySvg = '';

    if (data.panelSplit === 'pair') {
      const halfWidth = maxWindowWidth / 2;
      const leftPanelEnd = windowLeft + halfWidth * (1 - drawn * 0.7);
      const rightPanelStart = windowRight - halfWidth * (1 - drawn * 0.7);

      draperySvg += renderDrapePanel(windowLeft, rodY, leftPanelEnd - windowLeft, curtainHeight, waveFreq, colorHex, 'left', data.hangingStyle);
      draperySvg += renderDrapePanel(rightPanelStart, rodY, windowRight - rightPanelStart, curtainHeight, waveFreq, colorHex, 'right', data.hangingStyle);
    } else if (data.panelSplit === 'single_left') {
      const panelEnd = windowRight - (maxWindowWidth * drawn * 0.75);
      draperySvg += renderDrapePanel(windowLeft, rodY, panelEnd - windowLeft, curtainHeight, waveFreq * 1.6, colorHex, 'left', data.hangingStyle);
    } else {
      const panelStart = windowLeft + (maxWindowWidth * drawn * 0.75);
      draperySvg += renderDrapePanel(panelStart, rodY, windowRight - panelStart, curtainHeight, waveFreq * 1.6, colorHex, 'right', data.hangingStyle);
    }

    const svgContent = `
      <defs>
        <!-- Gold Rod Metallic Gradient -->
        <linearGradient id="goldRodGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#fff0c7" />
          <stop offset="40%" stop-color="#dfba43" />
          <stop offset="100%" stop-color="#8a6723" />
        </linearGradient>

        <!-- Window Glass Reflection -->
        <linearGradient id="glassSky" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#2a3f5f" />
          <stop offset="100%" stop-color="#141f33" />
        </linearGradient>
      </defs>

      <!-- Stage Background -->
      <rect x="0" y="0" width="${svgWidth}" height="${svgHeight}" fill="transparent" />

      <!-- Window Glass & Frame -->
      <rect x="${windowLeft}" y="65" width="${maxWindowWidth}" height="195" fill="url(#glassSky)" rx="6" stroke="#475569" stroke-width="4" />
      <line x1="${windowLeft + maxWindowWidth / 2}" y1="65" x2="${windowLeft + maxWindowWidth / 2}" y2="260" stroke="#475569" stroke-width="3" />
      <line x1="${windowLeft}" y1="150" x2="${windowRight}" y2="150" stroke="#475569" stroke-width="2" />

      <!-- Window Sill -->
      <rect x="${windowLeft - 10}" y="258" width="${maxWindowWidth + 20}" height="7" fill="#cbd5e1" rx="2" />

      <!-- Floor Line -->
      <line x1="20" y1="${floorY}" x2="${svgWidth - 20}" y2="${floorY}" stroke="#64748b" stroke-width="2" stroke-dasharray="4 4" opacity="0.6" />
      <text x="30" y="${floorY - 6}" fill="#94a3b8" font-size="10" font-family="Outfit, sans-serif" font-weight="600">FLOOR LEVEL</text>

      <!-- Drapery Panels -->
      ${draperySvg}

      <!-- Curtain Rod & Finials -->
      <!-- Left Finial -->
      <path d="M ${rodLeft - 14} ${rodY - 6} C ${rodLeft - 22} ${rodY - 6}, ${rodLeft - 22} ${rodY + 6}, ${rodLeft - 14} ${rodY + 6} Z" fill="url(#goldRodGrad)" />
      <!-- Right Finial -->
      <path d="M ${rodRight + 14} ${rodY - 6} C ${rodRight + 22} ${rodY - 6}, ${rodRight + 22} ${rodY + 6}, ${rodRight + 14} ${rodY + 6} Z" fill="url(#goldRodGrad)" />
      <!-- Rod Bar -->
      <rect x="${rodLeft - 14}" y="${rodY - 3.5}" width="${rodRight - rodLeft + 28}" height="7" fill="url(#goldRodGrad)" rx="2" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.4))" />
      <!-- Brackets -->
      <rect x="${rodLeft + 15}" y="${rodY - 8}" width="6" height="14" fill="url(#goldRodGrad)" rx="1" />
      <rect x="${svgWidth / 2 - 3}" y="${rodY - 8}" width="6" height="14" fill="url(#goldRodGrad)" rx="1" />
      <rect x="${rodRight - 21}" y="${rodY - 8}" width="6" height="14" fill="url(#goldRodGrad)" rx="1" />

      <!-- Width Dimension Line (Top) -->
      <g opacity="0.95">
        <line x1="${windowLeft}" y1="26" x2="${windowRight}" y2="26" stroke="#d4af37" stroke-width="1.5" />
        <line x1="${windowLeft}" y1="20" x2="${windowLeft}" y2="32" stroke="#d4af37" stroke-width="1.5" />
        <line x1="${windowRight}" y1="20" x2="${windowRight}" y2="32" stroke="#d4af37" stroke-width="1.5" />
        <rect x="${svgWidth / 2 - 45}" y="16" width="90" height="20" fill="#080d1a" rx="10" stroke="#d4af37" stroke-width="1" />
        <text x="${svgWidth / 2}" y="30" fill="#d4af37" font-size="11" font-weight="700" font-family="Plus Jakarta Sans, sans-serif" text-anchor="middle">↔ ${formatMeasurement(data.widthCm)}</text>
      </g>

      <!-- Height Dimension Line (Right Side) -->
      <g opacity="0.95">
        <line x1="${rodRight + 20}" y1="${rodY}" x2="${rodRight + 20}" y2="${curtainBottomY}" stroke="#d4af37" stroke-width="1.5" />
        <line x1="${rodRight + 14}" y1="${rodY}" x2="${rodRight + 26}" y2="${rodY}" stroke="#d4af37" stroke-width="1.5" />
        <line x1="${rodRight + 14}" y1="${curtainBottomY}" x2="${rodRight + 26}" y2="${curtainBottomY}" stroke="#d4af37" stroke-width="1.5" />
        <rect x="${rodRight + 10}" y="${(rodY + curtainBottomY) / 2 - 11}" width="78" height="22" fill="#080d1a" rx="8" stroke="#d4af37" stroke-width="1" />
        <text x="${rodRight + 49}" y="${(rodY + curtainBottomY) / 2 + 4}" fill="#d4af37" font-size="10.5" font-weight="700" font-family="Plus Jakarta Sans, sans-serif" text-anchor="middle">↕ ${formatMeasurement(data.finishedDropCm)}</text>
      </g>
    `;

    svgCanvas.innerHTML = svgContent;
  }

  // Generate SVG Drapery Path with Wave Pleats
  function renderDrapePanel(startX, topY, width, height, waveCount, color, alignSide, hangingStyle) {
    if (width <= 5) return '';

    const pleatWidth = width / Math.max(1, waveCount);
    let paths = '';
    const bottomY = topY + height;

    for (let i = 0; i < waveCount; i++) {
      const px = startX + (i * pleatWidth);
      const isOdd = i % 2 === 0;
      const foldDepth = isOdd ? 'rgba(0,0,0,0.24)' : 'rgba(255,255,255,0.12)';
      
      let bottomCurve = '';
      if (hangingStyle === 'puddle') {
        const puddleExtend = (i % 2 === 0 ? 12 : 6);
        bottomCurve = `C ${px + pleatWidth / 2} ${bottomY + puddleExtend}, ${px + pleatWidth} ${bottomY + puddleExtend - 4}, ${px + pleatWidth} ${bottomY}`;
      } else {
        bottomCurve = `L ${px + pleatWidth} ${bottomY}`;
      }

      paths += `
        <path d="M ${px} ${topY} L ${px + pleatWidth} ${topY} ${bottomCurve} L ${px} ${bottomY} Z" 
              fill="${color}" 
              stroke="rgba(0,0,0,0.18)" 
              stroke-width="0.5" />
        <rect x="${px}" y="${topY}" width="${pleatWidth}" height="${height + (hangingStyle === 'puddle' ? 12 : 0)}" fill="${foldDepth}" pointer-events="none" />
      `;
    }

    // Header pleat band
    paths += `
      <rect x="${startX}" y="${topY}" width="${width}" height="14" fill="rgba(0,0,0,0.3)" />
      <line x1="${startX}" y1="${topY + 14}" x2="${startX + width}" y2="${topY + 14}" stroke="rgba(255,255,255,0.25)" stroke-width="1" />
    `;

    return `<g filter="drop-shadow(2px 6px 12px rgba(0,0,0,0.35))">${paths}</g>`;
  }


  // =========================================================================
  // 4. EVENT BINDINGS & USER INTERACTION
  // =========================================================================

  // A. Product Selection
  if (productSelector) {
    productSelector.addEventListener('change', () => {
      const opt = productSelector.options[productSelector.selectedIndex];
      if (!opt) return;

      state.productId = opt.dataset.id;
      state.productName = opt.dataset.name;
      state.productSlug = opt.dataset.slug;
      state.productBasePrice = parseFloat(opt.dataset.price) || 2499;
      state.curtainColor = opt.dataset.color || '#C5A880';
      state.curtainColorName = opt.dataset.colorName || 'Champagne Gold';

      // Update Product Banner
      if (selectedProductImg) selectedProductImg.src = opt.dataset.image;
      if (selectedProductTitle) selectedProductTitle.textContent = state.productName;
      if (selectedProductCategory) selectedProductCategory.textContent = opt.dataset.category || 'Luxury Drapes';
      if (selectedProductColorDot) selectedProductColorDot.style.backgroundColor = state.curtainColor;
      if (selectedProductColorName) selectedProductColorName.textContent = state.curtainColorName;
      if (selectedProductBasePrice) selectedProductBasePrice.textContent = state.productBasePrice.toLocaleString('en-IN');
      if (selectedProductLink && state.productSlug) selectedProductLink.href = `/products/${state.productSlug}/`;

      // Update Swatch Active State if matches
      document.querySelectorAll('.calc-color-swatch').forEach(s => {
        s.classList.toggle('active', s.dataset.color.toLowerCase() === state.curtainColor.toLowerCase());
      });

      calculateSpecs();
      showToast(`Selected: ${state.productName}`);
    });
  }

  // B. "Size This" buttons from Catalog Grid
  document.querySelectorAll('.select-this-product-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const prodId = btn.dataset.id;
      if (productSelector) {
        productSelector.value = prodId;
        productSelector.dispatchEvent(new Event('change'));
      }
      studioRoot.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // C. Quantity Controls
  if (qtyMinusBtn && qtyInput) {
    qtyMinusBtn.addEventListener('click', () => {
      let q = parseInt(qtyInput.value) || 1;
      if (q > 1) {
        q -= 1;
        state.quantity = q;
        qtyInput.value = q;
        calculateSpecs();
      }
    });
  }

  if (qtyPlusBtn && qtyInput) {
    qtyPlusBtn.addEventListener('click', () => {
      let q = parseInt(qtyInput.value) || 1;
      if (q < 20) {
        q += 1;
        state.quantity = q;
        qtyInput.value = q;
        calculateSpecs();
      }
    });
  }

  // D. Unit Toggle (cm, in, ft)
  const unitButtons = document.querySelectorAll('.calc-unit-btn');
  unitButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      unitButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.unit = btn.dataset.unit;
      syncInputsFromState();
      calculateSpecs();
      showToast(`Switched units to ${btn.dataset.unit.toUpperCase()}`);
    });
  });

  // E. Preset Chips
  const presetChips = document.querySelectorAll('.calc-preset-chip');
  presetChips.forEach(chip => {
    chip.addEventListener('click', () => {
      presetChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      state.widthCm = parseFloat(chip.dataset.width) || 220;
      state.dropCm = parseFloat(chip.dataset.drop) || 245;
      if (chip.dataset.split) state.panelSplit = chip.dataset.split;
      if (chip.dataset.style) state.hangingStyle = chip.dataset.style;

      // Update Hanging Style visual card selection
      if (chip.dataset.style) {
        document.querySelectorAll('.calc-hanging-opt').forEach(opt => {
          opt.classList.toggle('selected', opt.dataset.style === chip.dataset.style);
        });
      }

      // Update Split visual card selection
      if (chip.dataset.split) {
        document.querySelectorAll('.calc-split-opt').forEach(opt => {
          opt.classList.toggle('selected', opt.dataset.split === chip.dataset.split);
        });
      }

      syncInputsFromState();
      calculateSpecs();
      showToast(`Preset: ${chip.textContent.trim()}`);
    });
  });

  // F. Width & Drop Range / Number Sync
  if (trackWidthRange) {
    trackWidthRange.addEventListener('input', (e) => {
      state.widthCm = parseFloat(e.target.value);
      if (trackWidthNum) trackWidthNum.value = cmToCurrentUnit(state.widthCm);
      calculateSpecs();
    });
  }

  if (trackWidthNum) {
    trackWidthNum.addEventListener('input', (e) => {
      state.widthCm = Math.max(40, Math.min(800, currentUnitToCm(e.target.value)));
      if (trackWidthRange) trackWidthRange.value = state.widthCm;
      calculateSpecs();
    });
  }

  if (windowDropRange) {
    windowDropRange.addEventListener('input', (e) => {
      state.dropCm = parseFloat(e.target.value);
      if (windowDropNum) windowDropNum.value = cmToCurrentUnit(state.dropCm);
      calculateSpecs();
    });
  }

  if (windowDropNum) {
    windowDropNum.addEventListener('input', (e) => {
      state.dropCm = Math.max(40, Math.min(600, currentUnitToCm(e.target.value)));
      if (windowDropRange) windowDropRange.value = state.dropCm;
      calculateSpecs();
    });
  }

  // Quick Step Buttons (+/- 10)
  document.querySelectorAll('.calc-step-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.target;
      const step = parseFloat(btn.dataset.step) || 0;

      if (target === 'width') {
        state.widthCm = Math.max(50, Math.min(600, state.widthCm + step));
      } else if (target === 'drop') {
        state.dropCm = Math.max(50, Math.min(450, state.dropCm + step));
      }

      syncInputsFromState();
      calculateSpecs();
    });
  });

  // G. Hanging Style Selection
  const hangingOptions = document.querySelectorAll('.calc-hanging-opt');
  hangingOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      hangingOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.hangingStyle = opt.dataset.style;
      calculateSpecs();
    });
  });

  // H. Fullness & Pleat Selection
  const pleatOptions = document.querySelectorAll('.calc-pleat-opt');
  pleatOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      pleatOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.pleatId = opt.dataset.id;
      state.fullness = parseFloat(opt.dataset.fullness) || 2.0;
      state.pleatName = opt.dataset.name || 'Pinch Pleat';
      state.pleatCost = parseFloat(opt.dataset.cost) || 0;
      calculateSpecs();
    });
  });

  // I. Lining Selection
  const liningOptions = document.querySelectorAll('.calc-lining-opt');
  liningOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      liningOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.liningId = opt.dataset.id;
      state.liningName = opt.dataset.name || 'Standard Unlined';
      state.liningCost = parseFloat(opt.dataset.cost) || 0;
      calculateSpecs();
    });
  });

  // J. Panel Split Selection
  const splitOptions = document.querySelectorAll('.calc-split-opt');
  splitOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      splitOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.panelSplit = opt.dataset.split;
      calculateSpecs();
    });
  });

  // K. Hardware Mounting Selection
  const hardwareOptions = document.querySelectorAll('.calc-hardware-opt');
  hardwareOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      hardwareOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.hardware = opt.dataset.hardware;
      calculateSpecs();
    });
  });

  // L. Color Swatches on Visualizer
  const colorSwatches = document.querySelectorAll('.calc-color-swatch');
  colorSwatches.forEach(swatch => {
    swatch.addEventListener('click', () => {
      colorSwatches.forEach(s => s.classList.remove('active'));
      swatch.classList.add('active');
      state.curtainColor = swatch.dataset.color;
      state.curtainColorName = swatch.dataset.name || 'Champagne Gold';
      calculateSpecs();
    });
  });

  // M. Interactive Draw / Open Curtains Slider
  if (drawCurtainSlider) {
    drawCurtainSlider.addEventListener('input', (e) => {
      state.curtainDrawnOpen = parseFloat(e.target.value) / 100;
      calculateSpecs();
    });
  }

  // N. Copy Specs to Clipboard
  const copyBtn = document.getElementById('calcCopySpecsBtn');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const summaryText = `
=== M CURTAINS BESPOKE SPECIFICATIONS ===
- Drapery Collection: ${state.productName}
- Color: ${state.curtainColorName}
- Window / Track Width: ${formatMeasurement(state.widthCm)}
- Desired Drop Height: ${formatMeasurement(state.dropCm)}
- Finished Cut Length: ${outCutLength ? outCutLength.textContent : ''}
- Hanging Style: ${state.hangingStyle.toUpperCase()}
- Header & Pleat: ${state.pleatName} (${state.fullness}x Fullness)
- Lining: ${state.liningName}
- Configuration: ${outPanels ? outPanels.textContent : ''}
- Fabric Requirement: ${outFabricMeters ? outFabricMeters.textContent : ''}
- Stack-Back Clearance: ${outStackBack ? outStackBack.textContent : ''}
- Hardware Requirement: ${outHardware ? outHardware.textContent : ''}
- Quantity: ${state.quantity} window set(s)
- Calculated Total: ${outPrice ? outPrice.textContent : ''}
==========================================
Generated via M Curtains Haute Sizing Atelier
      `.trim();

      navigator.clipboard.writeText(summaryText).then(() => {
        copyBtn.classList.add('copied');
        copyBtn.innerHTML = '<i class="fas fa-check me-1"></i> Copied!';
        showToast('Curtain specifications copied to clipboard!');
        setTimeout(() => {
          copyBtn.classList.remove('copied');
          copyBtn.innerHTML = '<i class="fas fa-copy me-1"></i> Copy Sizing Specs';
        }, 3000);
      });
    });
  }

  // O. Print Sizing Sheet
  const printBtn = document.getElementById('calcPrintSpecsBtn');
  if (printBtn) {
    printBtn.addEventListener('click', () => {
      window.print();
    });
  }

  // P. Interactive Guide Tabs
  const guideTabs = document.querySelectorAll('.calc-guide-tab');
  const guidePanes = document.querySelectorAll('.calc-guide-pane');
  guideTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.dataset.target;
      guideTabs.forEach(t => t.classList.remove('active'));
      guidePanes.forEach(p => p.classList.add('d-none'));

      tab.classList.add('active');
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.remove('d-none');
    });
  });

  // Helper: Toast Notification
  function showToast(message) {
    let toast = document.getElementById('calcToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'calcToast';
      toast.className = 'calc-toast-feedback';
      document.body.appendChild(toast);
    }
    toast.innerHTML = `<i class="fas fa-check-circle text-warning fs-5"></i> <span>${message}</span>`;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2800);
  }

  // Initial calculation run on page load
  syncInputsFromState();
  calculateSpecs();
});
