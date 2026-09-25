/**
 * LuxeDrape Measurement & Custom Pricing Calculator
 */

document.addEventListener('DOMContentLoaded', () => {
  // Product Detail Live Customizer
  const customizerForm = document.getElementById('curtainCustomizerForm');
  const priceDisplay = document.getElementById('liveCalculatedPrice');
  const widthInput = document.getElementById('customWidthInput');
  const dropInput = document.getElementById('customDropInput');
  const pleatRadios = document.querySelectorAll('input[name="pleat_id"]');
  const liningRadios = document.querySelectorAll('input[name="lining_id"]');
  const productIdInput = document.getElementById('customizerProductId');

  function updateLivePrice() {
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
          // Trigger slight pulse animation
          priceDisplay.classList.add('text-success');
          setTimeout(() => priceDisplay.classList.remove('text-success'), 300);
        }
      })
      .catch((err) => console.error('Price calculation error:', err));
  }

  if (widthInput && dropInput) {
    widthInput.addEventListener('input', updateLivePrice);
    dropInput.addEventListener('input', updateLivePrice);
  }

  pleatRadios.forEach((radio) => radio.addEventListener('change', updateLivePrice));
  liningRadios.forEach((radio) => radio.addEventListener('change', updateLivePrice));

  // --- Standalone Guide Calculator ---
  const guideForm = document.getElementById('standaloneGuideForm');
  if (guideForm) {
    guideForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const trackWidth = parseFloat(document.getElementById('guideTrackWidth').value) || 200;
      const windowDrop = parseFloat(document.getElementById('guideWindowDrop').value) || 240;
      const fullnessRatio = parseFloat(document.getElementById('guideFullness').value) || 2.0;
      const pannelWidth = 140; // standard panel width cm

      // Total fabric width required
      const totalFabricWidth = trackWidth * fullnessRatio;
      const recommendedPanels = Math.ceil(totalFabricWidth / pannelWidth);
      const fabricYardage = Math.ceil((recommendedPanels * (windowDrop + 30)) / 100); // 30cm for hems

      const resultBox = document.getElementById('guideResultBox');
      if (resultBox) {
        document.getElementById('resultPanelsCount').textContent = `${recommendedPanels} Panels (${Math.ceil(recommendedPanels / 2)} Pairs)`;
        document.getElementById('resultTotalWidth').textContent = `${totalFabricWidth.toFixed(0)} cm (${fullnessRatio}x Fullness)`;
        document.getElementById('resultRecommendedDrop').textContent = `${(windowDrop + 1.5).toFixed(0)} cm (Puddle / Floating)`;
        document.getElementById('resultYardage').textContent = `~${fabricYardage} Linear Metres`;
        resultBox.style.display = 'block';
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  }
});
