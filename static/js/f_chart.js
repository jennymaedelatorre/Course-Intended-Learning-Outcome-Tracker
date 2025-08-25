const ctx = document.getElementById('ciloProgressChart').getContext('2d');

  const ciloProgressChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['CILO 1', 'CILO 2', 'CILO 3', 'CILO 4'],
      datasets: [{
        label: 'Progress (%)',
        data: [80, 60, 45, 70], // Example data
        backgroundColor: [
          '#198754', '#0d6efd', '#ffc107', '#dc3545'
        ],
        borderRadius: 6,
        barThickness: 40
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            stepSize: 20
          },
          title: {
            display: true,
            text: 'Completion (%)'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: (context) => context.raw + '%'
          }
        }
      }
    }
  });
