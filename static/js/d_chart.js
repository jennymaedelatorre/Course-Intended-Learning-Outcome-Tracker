const ctx2 = document.getElementById('englishProgressChart').getContext('2d');
  new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: ['Completed', 'Remaining'],
      datasets: [{
        data: [70, 30], // 75% complete, 25% left
        backgroundColor: ['#2196f3', '#e0e0e0']
      }]
    },
    options: {
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });