import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import allLocales from "@fullcalendar/core/locales-all";

const CalendarPage = () => {
  const events = [
    {
      title: "Etkinlik 1",
      start: "2024-08-29",
      end: "2024-08-29",
    },
    {
      title: "Etkinlik 2",
      start: "2024-08-30",
      end: "2024-08-31",
    },
  ];

  return (
    <div style={{ padding: "20px" }}>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={events}
        editable={true}
        selectable={true}
        eventClick={(event) => {
          console.log(event);
        }}
        headerToolbar={{
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay",
        }}
        locale="tr"
        locales={allLocales}
        height="auto"
      />
    </div>
  );
};

export default CalendarPage;
