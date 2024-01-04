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
        self.year_numbers = list(range(self.MIN_YEAR, self.MAX_YEAR + 1))
        self.month_names = ["January", "February", "March", "April", "May", "June",
                            "July", "August", "September", "October", "November", "December"]

        self.years: list[Year] = []

        for i in self.year_numbers:
            if len(self.years) != 0:
                self.years.append(Year(i, self.years[-1].months[-1].last_used_day_name, self.month_names))
            else:
                self.years.append(Year(i, "Thursday", self.month_names))

        today = str(date.today())

        # These will be used as indexes
        self.current_year = self.year_numbers.index(int(today[0:4]))
        self.current_month = int(today[5:7]) - 1

        self.general_font = ("Consolas", 20)

        self.root = tk.Tk()
        self.root.title("Calendar")
        self.navigation_frame = tk.Frame(self.root)
        self.month_display_frame = tk.Frame(self.root)

        intro_text = "Welcome to my calendar that I ricsirogi made. Enjoy!"
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

        # If we got to either edge of the calendar, disable the button in that direction
        # and enable the button, if we're not at the edge anymore
        #! still need to account for when I jumpt to the "edge date" with the comboboxes
        if self.current_month == 0 and self.current_year == 0:
            self.navigate_left_button["state"] = "disabled"
        elif self.current_month == 11 and self.current_year == len(self.year_numbers) - 1:
            self.navigate_right_button["state"] = "disabled"
        else:
            self.navigate_left_button["state"] = "normal"
            self.navigate_right_button["state"] = "normal"

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
        for child_name, child in self.month_display_frame.children.items():
            child.grid_forget()
        for day in self.years[self.current_year].months[self.current_month].days:
            row = day.week_index
            column = day.day_index
            day_label = tk.Label(self.month_display_frame, font=self.general_font,
                                 text=str(day.day_num) + "\n" + day.day_name)

            day_label.grid(row=row, column=column)

            day_label.bind("<Button-1>", lambda event: day.add_event())

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
    def __init__(self, year_num: int, starting_day: str, month_names: list[str]) -> None:
        self.leap_year = self.is_leap_year(year_num)
        self.year_num = year_num
        self.starting_day = starting_day
        self.months: list[Month] = []

        self.month_names = month_names
        self.month_lengths = [31, 28 if not self.leap_year else 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        for name, length in zip(self.month_names, self.month_lengths):
            if len(self.months) != 0:
                self.months.append(Month(name, length, self.months[-1].last_used_day_name))
            else:
                self.months.append(Month(name, length, self.starting_day))

    def is_leap_year(self, year_num: int) -> bool:
        return (year_num % 100 != 0 and year_num % 4 == 0) or (year_num % 100 == 0 and year_num % 400 == 0)


class Month():
    def __init__(self, name: str, length: int, day_name: str) -> None:
        self.name = name
        self.length = length
        self.last_used_day_name = day_name
        self.days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.days: list[Day] = []

        day_name_index = self.days_of_the_week.index(self.last_used_day_name)
        week_index = 0

        for i in range(1, length + 1):
            self.days.append(Day(i, self.last_used_day_name, week_index, day_name_index))
            if day_name_index != 6:
                day_name_index = self.days_of_the_week.index(self.last_used_day_name) + 1
            else:
                day_name_index = 0
                week_index += 1
            self.last_used_day_name = self.days_of_the_week[day_name_index]


class Day():
    def __init__(self, day_num: int, day_name: str, week_index: int, day_index) -> None:
        self.day_num = day_num
        self.day_name = day_name
        self.week_index = week_index
        self.day_index = day_index

        # Every event will have a different event ID, that is unique on the given day, but not in a bigger scope
        self.event_id_tracker = 0
        self.events: list[Event] = []

    def add_event(self):
        self.event_window = tk.Tk()
        self.event_window.title("Add event")

        self.event_name_label = tk.Label(self.event_window, text="Event name:")
        self.event_name_entry = tk.Entry(self.event_window)
        self.from_time_label = tk.Label(self.event_window, text="Event starts at:")
        self.from_time_entry = tk.Entry(self.event_window)
        self.to_time_label = tk.Label(self.event_window, text="Event ends at:")
        self.to_time_entry = tk.Entry(self.event_window)
        self.event_description_label = tk.Label(self.event_window, text="Event description:")
        self.event_description_entry = tk.Entry(self.event_window)
        self.error_label = tk.Label(self.event_window, text="")

        self.event_create_button = tk.Button(self.event_window, text="Create event",
                                             command=lambda: self.create_event())
        self.event_cancel_button = tk.Button(self.event_window, text="Cancel",
                                             command=lambda: self.event_window.destroy())

        self.event_name_label.grid(row=0, column=0)
        self.event_name_entry.grid(row=0, column=1)
        self.from_time_label.grid(row=1, column=0)
        self.from_time_entry.grid(row=1, column=1)
        self.to_time_label.grid(row=2, column=0)
        self.to_time_entry.grid(row=2, column=1)
        self.event_description_label.grid(row=3, column=0)
        self.event_description_entry.grid(row=3, column=1)
        self.event_create_button.grid(row=0, column=2, rowspan=4)
        self.event_cancel_button.grid(row=4, column=2)
        self.error_label.grid(row=5, column=0, columnspan=3)

        self.event_window.mainloop()

    def create_event(self):
        """
        This function mainly checks if the user inputted correct data.
        """
        event_name = self.event_name_entry.get()
        from_time = self.from_time_entry.get()
        to_time = self.to_time_entry.get()
        event_description = self.event_description_entry.get()

        if event_name == "":
            self.error_label["text"] = "Please enter an event name!"
            return
        if event_description == "":
            self.error_label["text"] = "Please enter an event description!"
            return
        if from_time == "" or not re.match(r"[0-9][0-9]:[0-9][0-9]", from_time):
            self.error_label["text"] = "Please enter a starting time!"
            return
        if to_time == "" or not re.match(r"[0-9][0-9]:[0-9][0-9]", to_time):
            self.error_label["text"] = "Please enter a ending time!"
            return
        if not self.check_time_validity(from_time) or not self.check_time_validity(to_time):
            self.error_label["text"] = "Please enter a valid starting/ending time!"
            return

        self.events.append(Event(from_time, to_time, event_name, event_description, self.event_id_tracker))

        self.event_id_tracker += 1

    def check_time_validity(self, time: str) -> tuple[int, int] | bool:
        hour = int(time[0:2])
        minute = int(time[3:5])
        if hour > 23 or minute > 59:
            return False
        return (hour, minute)

    def delete_event(self, event_id: int):
        for count, event in enumerate(self.events):
            if event.event_id == event_id:
                self.events.pop(count)
                print("Event deleted successfully!")
        raise Exception("Event is not found with id", event_id)


class Event():
    def __init__(self, from_time: str, to_time: str, event_name: str, event_description: str, event_id: int) -> None:
        self.from_time = from_time
        self.to_time = to_time
        self.event_name = event_name
        self.event_description = event_description
        self.event_id = event_id
        print("Event created successfully!", from_time, to_time, event_name, event_description, event_id)


if __name__ == "__main__":
    app = Calendar()

    app.display_month()

    app.root.mainloop()
