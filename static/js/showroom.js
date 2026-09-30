/**
 * M Curtains - Haute Showroom & Atelier Interactive Experience
 */
document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  // --- 1. City Tabs Filter & Smooth Scroll ---
  const cityButtons = document.querySelectorAll('.city-nav-btn');
  const showroomCards = document.querySelectorAll('.showroom-flagship-card');

  cityButtons.forEach(button => {
    button.addEventListener('click', function () {
      const targetCity = this.getAttribute('data-city');

      cityButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');

      if (targetCity === 'all') {
        showroomCards.forEach(card => {
          card.style.display = 'block';
          card.style.animation = 'fadeInCard 0.4s ease forwards';
        });
      } else {
        showroomCards.forEach(card => {
          if (card.getAttribute('data-city-id') === targetCity) {
            card.style.display = 'block';
            card.style.animation = 'fadeInCard 0.4s ease forwards';
            // Smoothly scroll to the selected card
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
          } else {
            card.style.display = 'none';
          }
        });
      }
    });
  });

  // --- 2. "Book Appointment Here" Quick Action from Card ---
  const bookHereButtons = document.querySelectorAll('.btn-book-showroom');
  const showroomSelect = document.getElementById('bookingShowroomSelect');
  const bookingSuiteSection = document.getElementById('bookingSuiteSection');

  bookHereButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const showroomName = this.getAttribute('data-showroom-name');
      if (showroomSelect && showroomName) {
        for (let i = 0; i < showroomSelect.options.length; i++) {
          if (showroomSelect.options[i].text.includes(showroomName) || showroomSelect.options[i].value.includes(showroomName.toLowerCase())) {
            showroomSelect.selectedIndex = i;
            break;
          }
        }
      }
      if (bookingSuiteSection) {
        bookingSuiteSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Flash subtle highlight on the form
        bookingSuiteSection.classList.add('booking-card-highlight');
        setTimeout(() => {
          bookingSuiteSection.classList.remove('booking-card-highlight');
        }, 1500);
      }
    });
  });

  // --- 3. Booking Mode Switcher (In-Person, Virtual, Swatches) ---
  const modeTabs = document.querySelectorAll('.booking-mode-tab');
  const bookingTypeInput = document.getElementById('bookingTypeInput');
  const inPersonFields = document.querySelectorAll('.field-in-person');
  const virtualFields = document.querySelectorAll('.field-virtual');
  const swatchFields = document.querySelectorAll('.field-swatches');
  const bookingSubmitBtn = document.getElementById('bookingSubmitBtn');
  const bookingHeaderTitle = document.getElementById('bookingHeaderTitle');
  const bookingHeaderDesc = document.getElementById('bookingHeaderDesc');

  modeTabs.forEach(tab => {
    tab.addEventListener('click', function () {
      modeTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');

      const mode = this.getAttribute('data-mode');
      if (bookingTypeInput) bookingTypeInput.value = mode;

      if (mode === 'in_person') {
        inPersonFields.forEach(el => el.classList.remove('d-none'));
        virtualFields.forEach(el => el.classList.add('d-none'));
        swatchFields.forEach(el => el.classList.add('d-none'));
        if (bookingSubmitBtn) bookingSubmitBtn.innerHTML = '<i class="fas fa-calendar-check me-2"></i> Confirm Private Atelier Reservation';
        if (bookingHeaderTitle) bookingHeaderTitle.textContent = 'Reserve a Private Showroom Suite';
        if (bookingHeaderDesc) bookingHeaderDesc.textContent = 'Enjoy 1-on-1 consultation with our senior drapery architects, tactile fabric draping, and complimentary sommelier hospitality.';
      } else if (mode === 'virtual') {
        inPersonFields.forEach(el => el.classList.add('d-none'));
        virtualFields.forEach(el => el.classList.remove('d-none'));
        swatchFields.forEach(el => el.classList.add('d-none'));
        if (bookingSubmitBtn) bookingSubmitBtn.innerHTML = '<i class="fas fa-video me-2"></i> Schedule 1-on-1 Virtual Walkthrough';
        if (bookingHeaderTitle) bookingHeaderTitle.textContent = 'Schedule Virtual 1-on-1 Video Walkthrough';
        if (bookingHeaderDesc) bookingHeaderDesc.textContent = 'Join a live 20-minute video session from anywhere. Our master draper will showcase fabrics live under studio light and review your window photos.';
      } else if (mode === 'swatches') {
        inPersonFields.forEach(el => el.classList.add('d-none'));
        virtualFields.forEach(el => el.classList.add('d-none'));
        swatchFields.forEach(el => el.classList.remove('d-none'));
        if (bookingSubmitBtn) bookingSubmitBtn.innerHTML = '<i class="fas fa-box-open me-2"></i> Dispatch My Curated Swatch Box';
        if (bookingHeaderTitle) bookingHeaderTitle.textContent = 'Order Curated Atelier Swatch Box';
        if (bookingHeaderDesc) bookingHeaderDesc.textContent = 'Select up to 5 luxury drapery textile swatches. Assembled by our master weavers and delivered to your doorstep in 48 hours.';
      }
    });
  });

  // --- 4. Interactive FAQ Accordion ---
  const faqItems = document.querySelectorAll('.showroom-faq-item');
  faqItems.forEach(item => {
    const header = item.querySelector('.showroom-faq-header');
    if (header) {
      header.addEventListener('click', function () {
        const isActive = item.classList.contains('active');
        faqItems.forEach(otherItem => otherItem.classList.remove('active'));
        if (!isActive) {
          item.classList.add('active');
        }
      });
    }
  });

  // --- 5. Virtual 360 Panorama Tour Controls ---
  const panoramaImg = document.getElementById('panoramaImg');
  const panLeftBtn = document.getElementById('panLeftBtn');
  const panRightBtn = document.getElementById('panRightBtn');
  const panResetBtn = document.getElementById('panResetBtn');
  const lightFilterBtns = document.querySelectorAll('.panorama-light-btn');
  const panoramaOverlay = document.getElementById('panoramaOverlay');

  let currentPan = 0;
  if (panLeftBtn && panoramaImg) {
    panLeftBtn.addEventListener('click', () => {
      currentPan = Math.min(currentPan + 120, 240);
      panoramaImg.style.transform = `translateX(${currentPan}px) scale(1.1)`;
    });
  }
  if (panRightBtn && panoramaImg) {
    panRightBtn.addEventListener('click', () => {
      currentPan = Math.max(currentPan - 120, -240);
      panoramaImg.style.transform = `translateX(${currentPan}px) scale(1.1)`;
    });
  }
  if (panResetBtn && panoramaImg) {
    panResetBtn.addEventListener('click', () => {
      currentPan = 0;
      panoramaImg.style.transform = `translateX(0) scale(1)`;
    });
  }

  lightFilterBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      lightFilterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const light = this.getAttribute('data-light');
      if (panoramaOverlay) {
        if (light === 'day') {
          panoramaOverlay.style.background = 'rgba(255, 255, 255, 0.05)';
        } else if (light === 'sunset') {
          panoramaOverlay.style.background = 'rgba(235, 140, 52, 0.2)';
        } else if (light === 'night') {
          panoramaOverlay.style.background = 'rgba(10, 18, 40, 0.45)';
        }
      }
    });
  });

  // Hotspot Click Interactivity
  const hotspots = document.querySelectorAll('.panorama-hotspot');
  hotspots.forEach(hotspot => {
    hotspot.addEventListener('click', function () {
      const title = this.getAttribute('data-hotspot-title');
      const desc = this.getAttribute('data-hotspot-desc');
      const infoBox = document.getElementById('hotspotInfoBox');
      const infoTitle = document.getElementById('hotspotInfoTitle');
      const infoDesc = document.getElementById('hotspotInfoDesc');
      if (infoBox && infoTitle && infoDesc) {
        infoTitle.textContent = title;
        infoDesc.textContent = desc;
        infoBox.classList.remove('d-none');
      }
    });
  });

  const closeHotspotBtn = document.getElementById('closeHotspotBtn');
  if (closeHotspotBtn) {
    closeHotspotBtn.addEventListener('click', () => {
      const infoBox = document.getElementById('hotspotInfoBox');
      if (infoBox) infoBox.classList.add('d-none');
    });
  }

  // --- 6. Set Min Date for Appointment to Today ---
  const dateInput = document.getElementById('appointmentDateInput');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
  }
});
