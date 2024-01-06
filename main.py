"""
This program is a calendar.
"""

from datetime import date
import tkinter as tk
from tkinter import ttk
import re


class Calendar():
    def __init__(self) -> None:
        self.MIN_YEAR = 1970
        self.MAX_YEAR = 2050
        self.device = "laptop"  # laptop or pc
        if self.device == "laptop":
            self.DAY_WIDTH = 10
            self.DAY_HEIGHT = 2
        elif self.device == "pc":
            self.DAY_WIDTH = 14
            self.DAY_HEIGHT = 5
        else:
            raise Exception("Invalid device:", self.device)
        self.year_numbers = list(range(self.MIN_YEAR, self.MAX_YEAR + 1))
        self.month_names = ["January", "February", "March", "April", "May", "June",
                            "July", "August", "September", "October", "November", "December"]
        self.days_in_a_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.general_font = ("Consolas", 20)

        self.years: list[Year] = []

        for i in self.year_numbers:
            if len(self.years) != 0:
                self.years.append(Year(i, self.years[-1].months[-1].last_used_day_name, self.month_names, self))
            else:
                self.years.append(Year(i, "Thursday", self.month_names, self))

        today = str(date.today())

        # These will be used as indexes
        self.current_year = self.year_numbers.index(int(today[0:4]))
        self.current_month = int(today[5:7]) - 1

        self.root = tk.Tk()
        self.root.title("Calendar")
        self.navigation_frame = tk.Frame(self.root)
        self.month_display_frame = tk.Frame(self.root)

        intro_text = " " * 20
        self.intro_text_label = tk.Label(self.navigation_frame, font=self.general_font, text=intro_text)
        self.month_name_label = tk.Label(self.navigation_frame, font=self.general_font,
                                         text=self.month_names[self.current_month])
        self.year_name_label = tk.Label(self.navigation_frame, font=self.general_font,
                                        text=self.year_numbers[self.current_year])
        self.navigate_left_button = tk.Button(
            self.navigation_frame, font=self.general_font, text="<", command=lambda: self.navigate_press("l"))
        self.navigate_right_button = tk.Button(
            self.navigation_frame, font=self.general_font, text=">", command=lambda: self.navigate_press("r"))

        self.year_stringvar = tk.StringVar()
        self.month_stringvar = tk.StringVar()
        self.change_year_combobox = ttk.Combobox(self.navigation_frame, textvariable=self.year_stringvar)
        self.change_month_combobox = ttk.Combobox(self.navigation_frame, textvariable=self.month_stringvar)
        self.change_year_combobox["values"] = [str(year) for year in self.year_numbers]
        self.change_month_combobox["values"] = list(self.month_names)

        self.days_in_a_week_labels = []
        for count, day_name in enumerate(self.days_in_a_week):
            day_label = tk.Label(self.month_display_frame, font=self.general_font, text=day_name)
            self.days_in_a_week_labels.append(day_label)
            day_label.grid(row=0, column=count)

        self.intro_text_label.grid(row=0, column=1)
        self.year_name_label.grid(row=1, column=1)
        self.month_name_label.grid(row=2, column=1)
        self.navigate_left_button.grid(row=2, column=0, sticky="W")
        self.navigate_right_button.grid(row=2, column=2, sticky="E")

        self.navigation_frame.grid(row=0, column=0)
        self.month_display_frame.grid(row=1, column=0)

        self.year_name_label.bind("<Button-1>", lambda event, arg="y": self.change_date(event, arg))
        self.month_name_label.bind("<Button-1>", lambda event, arg="m": self.change_date(event, arg))
        self.change_year_combobox.bind("<Return>", lambda event, arg="by": self.change_date(event, arg))
        self.change_month_combobox.bind("<Return>", lambda event, arg="bm": self.change_date(event, arg))
        
        self.display_month()
        self.years[0].months[0].days[0].center_window(self.root)

    def navigate_press(self, direction: str):
        if direction == "l":
            if self.current_month == 0 and self.current_year == 0:
                return  # Return if we're at the edge of the calendar
            self.current_month -= 1
        elif direction == "r":
            if self.current_month == 11 and self.current_year == len(self.year_numbers)-1:
                return  # Return if we're at the edge of the calendar
            self.current_month += 1
        else:
            raise Exception("Invalid direction:", direction)

        if self.current_month < 0:
            self.current_month = 11
            self.current_year -= 1
            self.update_label("y")
        elif self.current_month > 11:
            self.current_month = 0
            self.current_year += 1
            self.update_label("y")

        self.update_label("m")

        self.display_month()

    def update_label(self, label: str):
        if label == "y":
            self.year_name_label["text"] = self.year_numbers[self.current_year]
        elif label == "m":
            self.month_name_label["text"] = self.month_names[self.current_month]
        else:
            raise Exception("Invalid label to change:", label)

    def change_date(self, event, date_type: str):
        """
        Possible date_types:
        y, m: Allow the user to change the year or month
        by, bm: Change the year or month comboboxes back to a label
        """
        if date_type == "y":
            self.get_row_column_of_widget(self.year_name_label, self.change_year_combobox)
            self.change_year_combobox.set(str(self.year_numbers[self.current_year]))
        elif date_type == "m":
            self.get_row_column_of_widget(self.month_name_label, self.change_month_combobox)
            self.change_month_combobox.set(str(self.month_names[self.current_month]))
        elif date_type == "by":
            self.current_year = self.year_numbers.index(int(self.change_year_combobox.get()))
            self.get_row_column_of_widget(self.change_year_combobox, self.year_name_label)
            self.display_month()
            self.update_label("y")
        elif date_type == "bm":
            self.current_month = self.month_names.index(self.change_month_combobox.get())
            self.get_row_column_of_widget(self.change_month_combobox, self.month_name_label)
            self.display_month()
            self.update_label("m")
        else:
            raise Exception("Invalid date_type:", date_type)

    def get_row_column_of_widget(self, widget_to_forget: tk.Widget, widget_to_grid: tk.Widget | None = None) -> tuple[int, int]:
        """
        Originally made for the change_date function, 
        so if you add a second widget, it will grid_forget() it
        and grid() the first widget, but if you don't give a second widget
        it just returns the row and column of the widget.
        """
        if not widget_to_grid:
            return (widget_to_forget.grid_info()["row"], widget_to_forget.grid_info()["column"])
        row, column = self.get_row_column_of_widget(widget_to_forget)

        widget_to_forget.grid_forget()

        widget_to_grid.grid(row=row, column=column)
        return (-1, -1)

    def display_month(self):
        for i, (child_name, child) in enumerate(self.month_display_frame.children.items()):
            if i >= 7 and child_name != "label":
                child.grid_forget()
        for day in self.years[self.current_year].months[self.current_month].days:
            row = day.week_index + 1  # +1 because the first row is for the days of the week
            column = day.day_index
            day_label = tk.Label(self.month_display_frame, font=self.general_font,
                                 text=day.day_num, border=2, relief="groove", width=self.DAY_WIDTH, height=self.DAY_HEIGHT, anchor="n")

            day_label.grid(row=row, column=column)

            day_label.bind("<Button-1>", lambda event, day=day: day.add_event())

        # If we got to either edge of the calendar, disable the button in that direction
        # and enable the button, if we're not at the edge anymore
        if self.current_month == 0 and self.current_year == 0:
            self.navigate_left_button["state"] = "disabled"
        elif self.current_month == 11 and self.current_year == len(self.year_numbers) - 1:
            self.navigate_right_button["state"] = "disabled"
        else:
            self.navigate_left_button["state"] = "normal"
            self.navigate_right_button["state"] = "normal"

    def add_event(self):
        """
        Obsolete, since the calendar is not in the console anymore,
        but could still use this during testing
        """

        from_time = input("From what time will the event take place?\nFormat: HHMM\n")
        to_time = input("Until what time will the event take place?\nFormat: HHMM\n")
        event_name = input("What will be the name of the event?\n")
        event_description = input("Description\n")

        event_date = input("When does the event take place?\nFormat: YYYYMMDD\n")
        year = int(event_date[0:4])
        year = self.year_numbers.index(year)
        month = int(event_date[4:6]) - 1
        day = int(event_date[6:8]) - 1

        self.years[year].months[month].days[day].add_event()


class Year():
    def __init__(self, year_num: int, starting_day: str, month_names: list[str], calendar: Calendar) -> None:
        self.leap_year = self.is_leap_year(year_num)

        self.year_num = year_num
        self.starting_day = starting_day
        self.calendar = calendar
        self.month_names = month_names

        self.months: list[Month] = []

        self.month_lengths = [31, 28 if not self.leap_year else 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        for name, length in zip(self.month_names, self.month_lengths):
            if len(self.months) != 0:
                self.months.append(Month(name, length, self.months[-1].last_used_day_name, self))
            else:
                self.months.append(Month(name, length, self.starting_day, self))

    def is_leap_year(self, year_num: int) -> bool:
        return (year_num % 100 != 0 and year_num % 4 == 0) or (year_num % 100 == 0 and year_num % 400 == 0)


class Month():
    def __init__(self, name: str, length: int, day_name: str, year: Year) -> None:
        self.name = name
        self.length = length
        self.last_used_day_name = day_name
        self.year = year

        self.days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.days: list[Day] = []

        day_name_index = self.days_of_the_week.index(self.last_used_day_name)
        week_index = 0

        for i in range(1, length + 1):
            self.days.append(Day(i, self.last_used_day_name, week_index, day_name_index, self))
            if day_name_index != 6:
                day_name_index = self.days_of_the_week.index(self.last_used_day_name) + 1
            else:
                day_name_index = 0
                week_index += 1
            self.last_used_day_name = self.days_of_the_week[day_name_index]


class Day():
    def __init__(self, day_num: int, day_name: str, week_index: int, day_index, month: Month) -> None:
        self.day_num = day_num
        self.day_name = day_name
        self.week_index = week_index
        self.day_index = day_index
        self.month = month
        self.only_name = True
        self.EVENT_Y_TOP_OFFSET = 28
        self.general_font = self.month.year.calendar.general_font

        device = self.month.year.calendar.device
        if device == "laptop":
            self.max_event_display = 2
            self.max_event_width = 17
            self.between_events_distance = 18
        elif device == "pc":
            self.max_event_display = 6
            self.max_event_width = 20
            self.between_events_distance = 20
        else:
            print("This should never be printed, because this exception was raised at the beggining of the file")
            raise Exception("Invalid device:", device)

        # Every event will have a different event ID, that is unique on the given day, but not in a bigger scope
        self.event_id_tracker = 0
        self.events: list[Event] = []  # This is going to be used as a queue

    def add_event(self, event_id: int = -1):
        self.event_window = tk.Tk()
        title = "Add event" if event_id == -1 else "Modify event"
        self.event_window.title(title)

        self.event_name_label = tk.Label(self.event_window, font=self.general_font, text="Event name:")
        self.event_name_entry = tk.Entry(self.event_window, font=self.general_font)
        self.from_time_label = tk.Label(self.event_window, font=self.general_font, text="Event starts at:")
        self.from_time_entry = tk.Entry(self.event_window, font=self.general_font)
        self.to_time_label = tk.Label(self.event_window, font=self.general_font, text="Event ends at:")
        self.to_time_entry = tk.Entry(self.event_window, font=self.general_font)
        self.event_description_label = tk.Label(self.event_window, font=self.general_font, text="Event description:")
        self.event_description_entry = tk.Entry(self.event_window, font=self.general_font)
        self.error_label = tk.Label(self.event_window, font=self.general_font, text="")

        self.event_create_button = tk.Button(self.event_window, font=self.general_font, text="Create event",
                                             command=lambda: self.create_event())
        self.event_cancel_button = tk.Button(self.event_window, font=self.general_font, text="Cancel",
                                             command=lambda: self.event_window.destroy())

        self.event_name_label.grid(row=0, column=0)
        self.event_name_entry.grid(row=0, column=1)
        self.from_time_label.grid(row=1, column=0)
        self.from_time_entry.grid(row=1, column=1)
        self.to_time_label.grid(row=2, column=0)
        self.to_time_entry.grid(row=2, column=1)
        self.event_description_label.grid(row=3, column=0)
        self.event_description_entry.grid(row=3, column=1)
        self.event_create_button.grid(row=0, column=2, rowspan=2)
        self.event_cancel_button.grid(row=2, column=2, rowspan=2)
        self.error_label.grid(row=5, column=0, columnspan=3)

        if event_id != -1:
            event_origin = self.get_event_by_id(event_id)
            if not event_origin:
                raise Exception("Event is not found with id", event_id)

            event_origin.modify_event_window.destroy()
            event_origin.modify_event_window = None

            self.event_name = event_origin.event_name
            self.from_time = event_origin.from_time
            self.to_time = event_origin.to_time
            self.event_description = event_origin.event_description

            self.event_name_entry.insert(0, self.event_name)
            self.from_time_entry.insert(0, self.from_time)
            self.to_time_entry.insert(0, self.to_time)
            self.event_description_entry.insert(0, self.event_description)

            self.event_create_button.config(text="Modify event", command=lambda: self.create_event(event_id))

        self.center_window(self.event_window)

        self.event_window.mainloop()

    def create_event(self, event_id: int = -1):
        if not self.validate_input():
            return

        if event_id != -1:
            self.delete_event(event_id)

        event_name = self.event_name_entry.get()
        from_time = self.from_time_entry.get()
        to_time = self.to_time_entry.get()
        event_description = self.event_description_entry.get()

        if self.get_event_by_id(self.event_id_tracker):
            self.delete_event(self.event_id_tracker)

        self.events.insert(0, Event(from_time, to_time, event_name, event_description, self.event_id_tracker, self))
        if len(self.events) <= self.max_event_display:
            self.calculate_event_padding(self.events[0])

            self.events[0].event_name_short_label.bind("<Button-1>", lambda event:self.events[0].modify_event())

        self.event_window.destroy()

        self.event_id_tracker += 1

    def delete_event(self, event_id: int):
        """
        Find the event and delete it while also unmapping every event on the given day
        and map the two first events in the queue
        """

        # Delete the modify event window if it exists
        event = self.get_event_by_id(event_id)
        if event:
            if event.modify_event_window is not None:
                if event.modify_event_window.winfo_exists():
                    event.modify_event_window.destroy()
                event.modify_event_window = None

        found = False
        for count, event in enumerate(self.events):
            if event.event_name_short_label.winfo_ismapped():
                event.event_name_short_label.grid_forget()
            if event.event_id == event_id:
                self.events.pop(count)
                found = True
                print("Event deleted successfully!", self.events)
        if self.events:
            for i in range(self.max_event_display):
                if i < len(self.events):
                    self.calculate_event_padding(self.events[-(i + 1)], i)
        if not found:
            raise Exception("Event is not found with id", event_id)

    def calculate_event_padding(self, event: "Event", order_override: int = -1):
        """
        Calculates the top padding for the event name label and also maps it
        """
        event_num = (len(self.events) - 1) if order_override == -1 else order_override

        pady = (self.EVENT_Y_TOP_OFFSET + event_num * self.between_events_distance, 0)
        event.event_name_short_label.grid(
            row=self.week_index + 1, column=self.day_index, sticky="wn", pady=pady, padx=(1, 0))

    def center_window(self, window: tk.Tk) -> None:
        window.update_idletasks() # This updates the window's widgets so it's size is properly readable
        x = int(abs(window.winfo_screenwidth() / 2 - window.winfo_reqwidth() / 2))
        y = int(abs(window.winfo_screenheight() / 2 - window.winfo_reqheight() / 2))
        window.geometry(f"+{x}+{y}")

    def check_time_validity(self, time: str) -> tuple[int, int] | None:
        """
        returns none if the time is invalid, otherwise returns a tuple of the hour and minute
        """
        hour = int(time[0:2])
        minute = int(time[3:5])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return (hour, minute)

    def validate_input(self) -> bool:
        """
        This function mainly checks if the user inputted correct data.
        """
        event_name = self.event_name_entry.get()
        from_time = self.from_time_entry.get()
        to_time = self.to_time_entry.get()
        event_description = self.event_description_entry.get()

        if event_name == "":
            self.error_label["text"] = "Please enter an event name!"
            return False
        if not self.only_name:  # For debugging and testing it will ignore errors except name
            if event_description == "":
                self.error_label["text"] = "Please enter an event description!"
                return False
            if from_time == "" or not re.match(r"[0-9][0-9]:[0-9][0-9]", from_time):
                self.error_label["text"] = "Please enter a valid starting time!"
                return False
            if to_time == "" or not re.match(r"[0-9][0-9]:[0-9][0-9]", to_time):
                self.error_label["text"] = "Please enter a valid ending time!"
                return False
            if not self.check_time_validity(from_time) or not self.check_time_validity(to_time):
                self.error_label["text"] = "Please enter a valid starting/ending time!"
                return False

            from_time_h, from_time_m = self.check_time_validity(from_time)  # type:ignore
            to_time_h, to_time_m = self.check_time_validity(to_time)  # type:ignore
            if to_time_h < from_time_h or (to_time_h == from_time_h and to_time_m < from_time_m):
                self.error_label["text"] = "The event cannot end before it starts!"
                return False

        self.error_label.config(text="")

        return True

    def get_event_by_id(self, id: int) -> "Event | None":
        for event in self.events:
            if event.event_id == id:
                return event
        return


class Event():
    def __init__(self, from_time: str, to_time: str, event_name: str, event_description: str, event_id: int, day: Day) -> None:
        self.from_time = from_time
        self.to_time = to_time
        self.event_name = event_name
        self.event_description = event_description
        self.event_id = event_id
        self.event_data: list[str] = [event_name, from_time, to_time, event_description]
        short_name = event_name
        self.day = day
        self.frame = day.month.year.calendar.month_display_frame
        self.max_event_width = day.max_event_width
        self.pady: tuple[int, int] = (-1, -1)
        self.general_font = day.month.year.calendar.general_font
        self.device = day.month.year.calendar.device

        if self.device == "laptop":
            self.font_size = 10
        elif self.device == "pc":
            self.font_size = 13
        else:
            raise Exception("Invalid device:", self.device)

        if len(short_name) > self.max_event_width:
            short_name = short_name[:self.max_event_width] + "..."
        self.event_name_short_label = tk.Label(self.frame, text=short_name,
                                               font=("Consolas", self.font_size), bg="SystemButtonFace")
        print("Event created successfully!", from_time, to_time, event_name, event_description, event_id)

    def modify_event(self):
        self.modify_event_window = tk.Tk()
        self.modify_event_window.title("Modify event")
        label_pretexts = ["Event name: ", "From time: ", "To time: ", "Event description: "]
        for count, (label_pretext, label_text) in enumerate(zip(label_pretexts, self.event_data)):
            label = tk.Label(self.modify_event_window, font=self.general_font, text=label_pretext + label_text)
            label.grid(row=count, column=0, sticky="w")
        modify_button = tk.Button(self.modify_event_window, font=self.general_font, text="Modify",
                                  command=lambda: self.day.add_event(self.event_id))
        delete_button = tk.Button(self.modify_event_window, font=self.general_font, text="Delete",
                                  command=lambda: self.day.delete_event(self.event_id))

        modify_button.grid(row=0, column=1, rowspan=2)
        delete_button.grid(row=2, column=1, rowspan=2)

        self.day.center_window(self.modify_event_window)
        self.modify_event_window.mainloop()


if __name__ == "__main__":
    app = Calendar()


    app.root.mainloop()
