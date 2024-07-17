import React, { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import './App.css';

const locales = {
  'en-US': require('date-fns/locale/en-US'),
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const HomePage = (props) => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    if (props.assignments && props.assignments.length > 0) {
      const eventsData = formatAssignments(props.assignments);
      setEvents(eventsData);
    }
  }, [props.assignments]);

  const formatAssignments = (assignmentsData) => {
    const formattedEvents = assignmentsData.map((assignment) => {
      const [assignmentName, dueDate] = assignment;

      const [dueTimeString, dueDateString] = dueDate.split(', ');
      const [, time] = dueTimeString.split(' ');

      const dateParts = dueDateString.split('/');
      const month = parseInt(dateParts[0], 10) - 1;
      const day = parseInt(dateParts[1], 10);
      const year = new Date().getFullYear();

      const formattedDueDate = new Date(year, month, day, parseInt(time), 0, 0, 0);

      return {
        title: assignmentName,
        start: formattedDueDate,
        end: formattedDueDate,
      };
    });

    return formattedEvents;
  };

  return (
    <div>
      <main>
        <p>Course Work</p>
        <div>
          {/* Calendar component */}
          <Calendar
            localizer={localizer}
            events={events}
            startAccessor="start"
            endAccessor="end"
            style={{ height: 500 }}
          />
        </div>
      </main>
    </div>
  );
};

export default HomePage;
