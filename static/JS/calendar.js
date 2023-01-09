"use strict";

// import { Calendar } from '@fullcalendar/core';
// import interactionPlugin, { Draggable } from '@fullcalendar/interaction';

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

    // fetch('/events.json')
    // .then((response) => response.json())
    // .then((responseJson) => {
    //     const eventdata = responseJson.symptoms});

    // initialize the calendar
    // -----------------------------------------------------------------
    
    var calendar = new Calendar(calendarEl, {
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,dayGridWeek,dayGridDay'
      },
      editable: true,
      droppable: true, // this allows things to be dropped onto the calendar
      // events: eventdata
    });
  
    calendar.render();
  });


