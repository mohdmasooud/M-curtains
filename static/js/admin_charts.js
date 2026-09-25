/**
 * M Curtains Admin Charts Initialization (Chart.js)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Order Status Distribution Chart (Doughnut)
  const statusCanvas = document.getElementById('orderStatusChart');
  if (statusCanvas) {
    const rawLabels = statusCanvas.getAttribute('data-labels') || '[]';
    const rawData = statusCanvas.getAttribute('data-values') || '[]';
    
    try {
      const labels = JSON.parse(rawLabels);
      const data = JSON.parse(rawData);

      new Chart(statusCanvas, {
        type: 'doughnut',
        data: {
          labels: labels.length > 0 ? labels : ['Delivered', 'Shipped', 'Tailoring', 'Pending'],
          datasets: [{
            data: data.length > 0 ? data : [12, 8, 5, 3],
            backgroundColor: [
              '#10b981', // Delivered
              '#3b82f6', // Shipped
              '#8b5cf6', // Tailoring
              '#f59e0b', // Pending
              '#ef4444', // Cancelled
            ],
            borderWidth: 2,
            borderColor: '#ffffff',
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                boxWidth: 12,
                padding: 15,
                font: { family: 'Plus Jakarta Sans', size: 12 }
              }
            }
          },
          cutout: '68%'
        }
      });
    } catch (e) {
      console.error('Error parsing status chart data', e);
    }
  }

  // Category Breakdown Chart (Bar)
  const categoryCanvas = document.getElementById('categoryBreakdownChart');
  if (categoryCanvas) {
    const rawCatLabels = categoryCanvas.getAttribute('data-labels') || '[]';
    const rawCatData = categoryCanvas.getAttribute('data-values') || '[]';

    try {
      const catLabels = JSON.parse(rawCatLabels);
      const catData = JSON.parse(rawCatData);

      new Chart(categoryCanvas, {
        type: 'bar',
        data: {
          labels: catLabels.length > 0 ? catLabels : ['Velvet', 'Linen', 'Blackout', 'Sheer', 'Jacquard', 'Motorized'],
          datasets: [{
            label: 'Products',
            data: catData.length > 0 ? catData : [3, 2, 2, 2, 2, 2],
            backgroundColor: '#c5a880',
            borderRadius: 6,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1 }
            },
            x: {
              grid: { display: false }
            }
          }
        }
      });
    } catch (e) {
      console.error('Error parsing category chart data', e);
    }
  }
});
