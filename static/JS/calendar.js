"use strict";


document.addEventListener('DOMContentLoaded', function() {
    let containerEl = document.getElementById('external-events');
    let calendarEl = document.getElementById('calendar');

     new FullCalendar.Draggable(containerEl, {
        itemSelector: '.fc-event',
        eventData: function(eventEl) {
            return {
                title: eventEl.innertext
            };
        }
    });


    let calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,dayGridWeek,dayGridDay"
        },
    initialView: 'dayGridMonth',
    editable: true,
    droppable: true,
    selectable: true,
    events: [
        {
            title:
            start:
        }
    ]
      
    });

    calendar.render();
  });

