/**
 * M Curtains Interactive Room Drapery Visualizer
 */

document.addEventListener('DOMContentLoaded', () => {
  const roomSceneImage = document.getElementById('visualizerRoomScene');
  const curtainOverlayLeft = document.getElementById('visualizerCurtainLeft');
  const curtainOverlayRight = document.getElementById('visualizerCurtainRight');
  const sceneSelectorBtns = document.querySelectorAll('.scene-selector-btn');
  const fabricSelectorBtns = document.querySelectorAll('.fabric-selector-btn');
  const timeOfDayToggle = document.getElementById('timeOfDayToggle');
  const roomLightingOverlay = document.getElementById('roomLightingOverlay');

  const selectedFabricName = document.getElementById('selectedFabricName');
  const selectedFabricPrice = document.getElementById('selectedFabricPrice');
  const selectedFabricLink = document.getElementById('selectedFabricLink');

  // Room backdrops
  const roomScenes = {
    living: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=80',
    bedroom: 'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1200&q=80',
    dining: 'https://images.unsplash.com/photo-1617806118233-18e1de247200?auto=format&fit=crop&w=1200&q=80',
  };

  // Change room scene
  sceneSelectorBtns.forEach((btn) => {
    btn.addEventListener('click', function () {
      sceneSelectorBtns.forEach((b) => b.classList.remove('active', 'btn-navy'));
      sceneSelectorBtns.forEach((b) => b.classList.add('btn-outline-secondary'));
      this.classList.remove('btn-outline-secondary');
      this.classList.add('active', 'btn-navy');

      const sceneKey = this.getAttribute('data-scene');
      if (roomSceneImage && roomScenes[sceneKey]) {
        roomSceneImage.src = roomScenes[sceneKey];
      }
    });
  });

  // Change fabric & drape color
  fabricSelectorBtns.forEach((btn) => {
    btn.addEventListener('click', function () {
      fabricSelectorBtns.forEach((b) => b.classList.remove('active', 'border-primary', 'shadow'));
      this.classList.add('active', 'border-primary', 'shadow');

      const colorHex = this.getAttribute('data-color');
      const opacity = this.getAttribute('data-opacity') || '0.9';
      const name = this.getAttribute('data-name');
      const price = this.getAttribute('data-price');
      const slug = this.getAttribute('data-slug');

      // Update overlay curtains
      if (curtainOverlayLeft && curtainOverlayRight) {
        curtainOverlayLeft.style.backgroundColor = colorHex;
        curtainOverlayLeft.style.opacity = opacity;
        curtainOverlayRight.style.backgroundColor = colorHex;
        curtainOverlayRight.style.opacity = opacity;
      }

      if (selectedFabricName) selectedFabricName.textContent = name;
      if (selectedFabricPrice) selectedFabricPrice.textContent = `₹${price}`;
      if (selectedFabricLink && slug) selectedFabricLink.href = `/products/${slug}/`;
    });
  });

  // Time of Day Lighting Toggle
  if (timeOfDayToggle && roomLightingOverlay) {
    timeOfDayToggle.addEventListener('change', function () {
      if (this.checked) {
        // Night mode
        roomLightingOverlay.style.background = 'rgba(10, 15, 30, 0.45)';
      } else {
        // Day mode
        roomLightingOverlay.style.background = 'transparent';
      }
    });
  }
});
