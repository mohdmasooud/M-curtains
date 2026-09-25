/**
 * M Curtains Core Frontend JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Live Instant Search in Navbar
  const searchInput = document.getElementById('navbarSearchInput');
  const searchDropdown = document.getElementById('navbarSearchResults');

  if (searchInput && searchDropdown) {
    let debounceTimer;

    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      const query = e.target.value.trim();

      if (query.length < 2) {
        searchDropdown.style.display = 'none';
        searchDropdown.innerHTML = '';
        return;
      }

      debounceTimer = setTimeout(() => {
        fetch(`/products/search-api/?q=${encodeURIComponent(query)}`)
          .then((res) => res.json())
          .then((data) => {
            if (data.results && data.results.length > 0) {
              let html = '';
              data.results.forEach((item) => {
                html += `
                  <a href="/products/${item.slug}/" class="search-item-row">
                    <img src="${item.image}" alt="${item.name}">
                    <div class="flex-grow-1">
                      <div class="fw-semibold text-truncate" style="max-width: 260px;">${item.name}</div>
                      <div class="small text-muted">${item.category} • <span class="fw-bold text-dark">₹${item.price}</span></div>
                    </div>
                    <i class="fas fa-chevron-right text-muted small"></i>
                  </a>
                `;
              });
              searchDropdown.innerHTML = html;
              searchDropdown.style.display = 'block';
            } else {
              searchDropdown.innerHTML = '<div class="p-3 text-center text-muted small">No curtains found matching "' + query + '"</div>';
              searchDropdown.style.display = 'block';
            }
          })
          .catch((err) => {
            console.error('Search error:', err);
          });
      }, 250);
    });

    // Close dropdown on outside click
    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.style.display = 'none';
      }
    });
  }

  // 2. Product Detail Image Gallery Switcher
  const mainProductImage = document.getElementById('mainProductImage');
  const thumbnailImages = document.querySelectorAll('.gallery-thumb-btn');

  if (mainProductImage && thumbnailImages.length > 0) {
    thumbnailImages.forEach((thumb) => {
      thumb.addEventListener('click', function () {
        const fullUrl = this.getAttribute('data-full-img');
        if (fullUrl) {
          mainProductImage.src = fullUrl;
          thumbnailImages.forEach((t) => t.classList.remove('active', 'border-warning'));
          this.classList.add('active', 'border-warning');
        }
      });
    });
  }

  // 3. Auto-dismiss Alert Messages after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 6000);
  });
});
