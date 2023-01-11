"use strict";

document.addEventListener('DOMContentLoaded', function() {
    let Calendar = FullCalendar.Calendar;
  
    let containerEl = document.getElementById('external-events');
    let calendarEl = document.getElementById('calendar');
  
    // initialize the external events
    // -----------------------------------------------------------------
  
    new FullCalendar.Interaction.Draggable(containerEl, {
      itemSelector: '.fc-event',
      eventData: function(eventEl) {
        return {
          title: eventEl.innerText
        };
      }
    });
// initialize the calendar
    // -----------------------------------------------------------------
    fetch('/symptoms.json')
    .then((response) => response.json())
    .then((responseJson) => {
        let eventdata = responseJson.symptoms

        let calendar = new Calendar(calendarEl, {
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek,dayGridDay'
          },
          editable: true,
          droppable: true, 
          events: eventdata
        });
        calendar.render();
        
      });
      });

    
    
  


