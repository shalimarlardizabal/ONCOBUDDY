// JS for profile charts
'user strict';

fetch('/logs.json')
  .then((response) => response.json())
  .then((responseJson) => {
    const paindata = responseJson.pain_data.map((totalPain) => ({
      x: totalPain.date,
      y: totalPain.pain_level,
    }));

    const sleepdata = responseJson.sleep_data.map((totalSleep) => ({
        x: totalSleep.date,
        y: totalSleep.sleep_level,
      }));
    
    const appetitedata = responseJson.appetite_data.map((totalAppetite) => ({
        x: totalAppetite.date,
        y: totalAppetite.appetite_level,
      }));
    
    const fatiguedata = responseJson.fatigue_data.map((totalFatigue) => ({
        x: totalFatigue.date,
        y: totalFatigue.fatigue_level,
      }));
    
    console.log(responseJson);

    new Chart(document.querySelector('#logchart'), {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'Pain Progression',
            data: paindata,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          },
          {
            label: 'Sleep Progression',
            data: sleepdata,
            borderColor: 'rgb(178, 102, 255)',
            tension: 0.1
          },
          {
            label: 'Appetite Progression',
            data: appetitedata,
            borderColor: 'rgb(255, 153, 51)',
            tension: 0.1
          },
          {
            label: 'Fatigue Progression',
            data: fatiguedata,
            borderColor: 'rgb(0, 102, 204)',
            tension: 0.1
          },
        ],
      },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              tooltipFormat: 'LLLL dd', // Luxon format string
              unit: 'week'
            },
          },
        },
      },
    });
  });
