"""
This program is a calendar.
"""

from datetime import date
import tkinter as tk
from tkinter import ttk
import re
from typing import Optional
import sys


class Calendar():
    def __init__(self) -> None:
        self.MIN_YEAR = 1970
        self.MAX_YEAR = 2050
        self.device = "pc"  # laptop or pc
        if self.device == "laptop":
            self.DAY_WIDTH = 10
            self.DAY_HEIGHT = 2
        elif self.device == "pc":
            self.DAY_WIDTH = 14
            self.DAY_HEIGHT = 4
        else:
            raise Exception("Invalid device:", self.device)
        self.year_numbers = list(range(self.MIN_YEAR, self.MAX_YEAR + 1))
        self.month_names = ["January", "February", "March", "April", "May", "June",
                            "July", "August", "September", "October", "November", "December"]
        self.days_in_a_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.general_font = ("Consolas", 20)

        self.years: list[Year] = []

        self.already_displayed_months: set[Month] = set()

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

        # I need to move this up here, because the day labels are in this frame
        self.month_display_frame = tk.Frame(self.root)

        for i in self.year_numbers:
            if len(self.years) != 0:
                self.years.append(Year(i, self.years[-1].months[-1].last_used_day_name, self.month_names, self))
            else:
                self.years.append(Year(i, "Thursday", self.month_names, self))

        today = str(date.today())

        # These will be used as indexes
        self.current_year = self.year_numbers.index(int(today[0:4]))
        self.current_month = int(today[5:7]) - 1

        self.root.resizable(False, False)
        self.root.title("Calendar")
        self.navigation_frame = tk.Frame(self.root)

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

        for count, day_name in enumerate(self.days_in_a_week):
            day_name_label = tk.Label(self.month_display_frame, font=self.general_font, text=day_name)
            day_name_label.grid(row=0, column=count)

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
        # Remove the currently visible days (except the days of the week at the top)
        for i, (child_name, child) in enumerate(self.month_display_frame.children.items()):
            if i >= 7 and child_name != "label":
                child.grid_remove()

        # Grid every day in the current month
        # If the month is already displayed, then just grid() the days
        month = self.years[self.current_year].months[self.current_month]
        if month not in self.already_displayed_months:
            for day in month.days:
                row = day.week_index + 1  # +1 because the first row is for the days of the week
                column = day.day_index
                day.label = tk.Label(self.month_display_frame, font=self.general_font,
                                     text=day.day_num, border=2, relief="groove", width=self.DAY_WIDTH, height=self.DAY_HEIGHT, anchor="n")

                day.label.grid(row=row, column=column)

                day.label.bind("<Button-1>", lambda event, day=day: day.view_events_window())
                self.already_displayed_months.add(month)
        else:
            for day in month.days:
                day.label.grid()
                for event in day.events:
                    event.event_name_short_label.grid()

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

        self.years[year].months[month].days[day].open_add_event_window()


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
        self.window_open: int = 0  # 0 means no window is open, otherwise it's the day number of the open window

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

    def __hash__(self):
        return hash((self.name, self.year))

    def __eq__(self, other: "Month"):
        return (self.name, self.year) == (other.name, other.year)


class Day():
    def __init__(self, day_num: int, day_name: str, week_index: int, day_index, month: Month) -> None:
        self.day_num = day_num
        self.day_name = day_name
        self.week_index = week_index
        self.day_index = day_index
        self.month = month
        self.only_name = True  # ! If true the program only checks if the name is inputted for the event creation
        self.EVENT_Y_TOP_OFFSET = 28
        self.general_font = self.month.year.calendar.general_font
        self.max_event_name_length = 30
        self.label: tk.Label = tk.Label(self.month.year.calendar.month_display_frame)

        device = self.month.year.calendar.device
        if device == "laptop":
            self.max_event_display = 2
            self.max_event_width = 17
            self.between_events_distance = 18

        elif device == "pc":
            self.max_event_display = 4
            self.max_event_width = 20
            self.between_events_distance = 22
        else:
            print("This should never be printed, because this exception was raised at the beggining of the file")
            raise Exception("Invalid device:", device)

        # Every event will have a different event ID, that is unique on the given day, but not in a bigger scope
        self.event_id_tracker = 0
        self.events: list[Event] = []  # This is going to be used as a queue

    def view_events_window(self):
        if not self.init_event_window():
            return

        self.event_window.title("View events")
        # Since viewing events and adding events are the same window, we need to destroy the children
        self.destroy_children(self.event_window, "destroy")

        for count, event in enumerate(self.events):
            event_frame = tk.Frame(self.event_window)

            event_name = event.event_name
            event_duration = event.from_time + " - " + event.to_time
            event_id = event.event_id

            name_label = tk.Label(event_frame, font=self.general_font, text=event_name)
            duration_label = tk.Label(event_frame, font=self.general_font, text=event_duration)

            name_label.grid(row=0, column=0, sticky="w")
            duration_label.grid(row=1, column=0, sticky="w")

            event_frame.grid(row=count, column=0, sticky="w")
            name_label.bind("<Button-1>", lambda e, event=event: self.view_event_del_window(event))
            duration_label.bind("<Button-1>", lambda e, event=event: self.view_event_del_window(event))

        self.add_button = tk.Button(self.event_window, font=self.general_font,
                                    text="Add", command=lambda: self.open_add_event_window())

        if len(self.events) == 0:
            rowspan = 1
            no_events_label = tk.Label(self.event_window, font=self.general_font, text="No events on this day")
            no_events_label.grid(row=0, column=0)
        else:
            rowspan = len(self.events)

        self.add_button.grid(row=0, column=1, rowspan=rowspan)
        self.center_window(self.event_window)
        self.event_window.mainloop()

    def open_add_event_window(self, event_id: int = -1):
        if not self.init_event_window(event_id):
            return

        title = "Add event" if event_id == -1 else "Modify event"
        self.event_window.title(title)

        # If the event_name_label doesn't exist then none of these exists, so we create them
        self.event_name_label = tk.Label(self.event_window, font=self.general_font, text="Event name:")
        self.event_name_entry = tk.Entry(self.event_window, font=self.general_font)
        self.from_time_label = tk.Label(self.event_window, font=self.general_font, text="Event starts at:")
        self.from_time_entry = tk.Entry(self.event_window, font=self.general_font)
        self.to_time_label = tk.Label(self.event_window, font=self.general_font, text="Event ends at:")
        self.to_time_entry = tk.Entry(self.event_window, font=self.general_font)
        self.event_description_label = tk.Label(
            self.event_window, font=self.general_font, text="Event description:")
        self.event_description_entry = tk.Entry(self.event_window, font=self.general_font)
        self.error_label = tk.Label(self.event_window, font=self.general_font, text="")

        self.event_create_button = tk.Button(self.event_window, font=self.general_font, text="Create event",
                                             command=lambda: self.create_event_and_sort())
        self.event_cancel_button = tk.Button(self.event_window, font=self.general_font, text="Cancel",
                                             command=lambda: self.close_event_window())

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

            if event_origin.modify_event_window is not None:
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

            self.event_create_button.config(
                text="Modify event", command=lambda event_id=event_id: self.modify_event(event_id))

        self.center_window(self.event_window)

        self.event_window.mainloop()

    def create_event_and_sort(self):
        self.create_event()
        self.sort_events()

    def create_event(self, event_id: int = -1, ignore_validation: bool = False, order: int = -1):
        if not ignore_validation:
            if not self.validate_input():
                return

        # Get the data from the user, or resort to getting it from the event if it exists
        if not ignore_validation:
            event_name, from_time, to_time, event_description = self.get_event_data_by_user()
        else:
            temp_event = self.get_event_by_id(event_id)
            if temp_event:
                event_name = temp_event.event_name
                from_time = temp_event.from_time
                to_time = temp_event.to_time
                event_description = temp_event.event_description
            else:
                raise Exception("Event is not found with id", event_id)

        # If the event is already present, delete it
        if self.get_event_by_id(self.event_id_tracker):
            self.delete_event(self.event_id_tracker)
        elif self.get_event_by_id(event_id):
            self.delete_event(event_id)

        # Initialize the event class
        id_of_new_event = event_id if event_id != -1 else self.event_id_tracker

        event = Event(event_name, from_time, to_time, event_description, id_of_new_event, self)

        # Just to make sure each event is in the list only once
        if event not in self.events and id_of_new_event not in [event.event_id for event in self.events]:
            self.events.append(event)
        elif self.event_id_tracker in [event.event_id for event in self.events]:
            print("Existing event:", self.event_id_tracker, self.get_event_by_id(
                self.event_id_tracker), "\nNew event", event)

        if len(self.events) <= self.max_event_display:
            if order == -1:
                self.calculate_event_padding(event)
            else:
                self.calculate_event_padding(event, order)

            event.event_name_short_label.bind(
                "<Button-1>", lambda e, current_event=event: current_event.view_event())

        self.close_event_window()

        if id_of_new_event == self.event_id_tracker:
            self.event_id_tracker += 1
        print("\nCreated event with name", event_name,
              f"\nid_of_new_event: {id_of_new_event}\nevent_id: {event_id}\nignore_validation: {ignore_validation}\norder: {order}\n")

    def modify_event(self, event_id: int):
        event = self.get_event_by_id(event_id)
        if event:
            event_name, from_time, to_time, event_description = self.get_event_data_by_user()
            event["event_name"] = event_name
            event["from_time"] = from_time
            event["to_time"] = to_time
            event["event_description"] = event_description
            if self.validate_input():
                self.sort_events()
                self.close_event_window()
        else:
            raise Exception("Event is not found with id", event_id, "Or something else went wrong idk")

    def get_event_data_by_user(self) -> tuple[str, str, str, str]:
        event_name = self.event_name_entry.get()
        from_time = self.from_time_entry.get()
        to_time = self.to_time_entry.get()
        event_description = self.event_description_entry.get()
        return (event_name, from_time, to_time, event_description)

    def delete_event(self, event_id: int):
        """
        Find the event and delete it while also unmapping every event on the given day
        and map the two first events in the queue
        """

        # Delete the modify event window if it exists
        event = self.get_event_by_id(event_id)
        if event:
            if "modify_event_window" in vars(event):
                if event.modify_event_window is not None:
                    if event.modify_event_window.children != {}:
                        event.modify_event_window.destroy()
                    event.modify_event_window = None

        # I'm not using self.get_event_by_id() because I need to iterate through the events anyway
        found = False
        for count, event in enumerate(self.events):
            event.event_name_short_label.grid_forget()
            if event.event_id == event_id:
                self.events.pop(count)
                found = True
                print("Event deleted successfully! Remaining events:", [
                      (event.event_id, event.event_name) for event in self.events])

        # If there are no events left, then we don't need to sort them
        if len(self.events) == 0:
            print("No events left so not sorting")
            return

        if not found:
            raise Exception("Event is not found with id", event_id)

        self.sort_events()

    def sort_events(self):
        """
        Sorts the events by their starting time
        """
        # If there are no events left, then we don't need to sort them,
        # BUT event if there's only one event we need to sort them, since
        # the remaining event might be on the second place and we would need to "push it up"
        if len(self.events) == 0:
            return

        # Create a dictionary with the event_id as the key and the combined hour and minute as the value
        initial_dict: dict[str, int] = {}
        event_without_start_time: list[Event] = []
        for event in self.events:
            if not event.from_time:
                event_without_start_time.append(event)
                continue
            hour = int(event.from_time[0:event.from_time.find(":")])
            minute = int(event.from_time[event.from_time.find(":") + 1:])
            # Combine the hour and minute into a single value
            time = hour * 60 + minute
            initial_dict[str(event.event_id)] = time

        # Now sort_dict will sort by the combined hour and minute
        dict_sorted_by_time: dict[str, int] = self.sort_dict(initial_dict)

        # Now gird_forget each event
        for event in self.events:
            event.event_name_short_label.grid_forget()

        # Append the events into self.events in order
        new_events: list[Event] = []

        # And create every event in the order of the sorted dictionary
        for event_id in dict_sorted_by_time.keys():
            event = self.get_event_by_id(int(event_id))
            if event:  # This check is probably useless, but I'm keeping cuz the vscode keeps complaining
                new_events.append(event)

        # lastly append the events that don't have a starting time
        for event_index in range(len(event_without_start_time)):
            # I need to get it starting from the end so the order doesn't change
            new_events.append(event_without_start_time[-(event_index + 1)])

        for order, event in enumerate(new_events):
            # True is passed so it doesn't validate the input, order to pass the order for calculate_event_padding()
            self.create_event(event.event_id, True, order)

    def sort_dict(self, input_dict: dict[str, int]) -> dict:
        """
        Sorts a dictionary by it's keys and returns it
        """
        return dict(sorted(input_dict.items(), key=lambda item: item[1]))

    def view_event_del_window(self, event: "Event"):
        """
        calls the event's view_event function after destroying the event_window
        """
        if self.event_window:
            self.close_event_window()
            event.view_event()

    def init_event_window(self, event_id: int = -1):
        """
        Initializes the event window (if it wasn't already)
        Destroys its previous children
        Lets the month know that the window is open
        Binds the close_event_window function to the event_window's destroy event
        Returns True if the window was initialized, False if it couldn't initialize
        """
        if self.month.window_open == self.day_num or self.month.window_open == 0:  # Allow to open a new window only if there's no other window open
            self.close_event_window()
            if "event_window" not in vars(self) or self.event_window.children == {}:
                self.event_window = tk.Tk()
                self.event_window.resizable(False, False)
            # Since viewing events and adding events are the same window, we need to destroy the children
            self.destroy_children(self.event_window, "destroy")
            self.month.window_open = self.day_num
            self.event_window.bind("<Destroy>", lambda e: self.close_event_window(True))
            return True
        else:
            return False

    def close_event_window(self, from_destroy_event: bool = False):
        """
        We need a sepearate function for this, because we also need to let the month know that the window is closed\n
        Also I check if the window actually exists, so I don't try to close the window if it's already closed\n
        The parameter is used to check if the window was closed by the destroy event, 
        because if it was, then I don't need to manually destroy it
        """
        if not from_destroy_event and "event_window" in vars(self) and self.event_window.children != {}:
            self.event_window.destroy()
        self.month.window_open = 0

    def destroy_children(self, parent: tk.Tk | tk.Frame, mode: str = "destroy"):
        """
        If mode is "destroy" then it means that it destroy()s the children,
        but if it's remove, then it just grid_remove()s them, which means that they're still functional,
        you just have to call grid() on them again with the any parameters
        """
        for child in parent.winfo_children():
            if mode == "destroy":
                child.destroy()
            elif mode == "remove":
                child.grid_remove()
            else:
                raise Exception("Invalid mode:", mode)

    def calculate_event_padding(self, event: "Event", order_override: int = -1):
        """
        Calculates the top padding for the event name label and also maps it
        order override is used when we want to specify the order of the event
        """
        event_num = (len(self.events) - 1) if order_override == -1 else order_override
        if event.event_name_short_label.winfo_ismapped():
            event.event_name_short_label.grid_forget()
        pady = (self.EVENT_Y_TOP_OFFSET + event_num * self.between_events_distance, 0)
        event.event_name_short_label.grid(
            row=self.week_index + 1, column=self.day_index, sticky="wn", pady=pady, padx=(1, 0))

    def center_window(self, window: tk.Tk) -> None:
        window.update_idletasks()  # This updates the window's widgets so it's size is properly readable
        x = int(abs(window.winfo_screenwidth() / 2 - window.winfo_reqwidth() / 2))
        y = int(abs(window.winfo_screenheight() / 2 - window.winfo_reqheight() / 2))
        window.geometry(f"+{x}+{y}")

    def check_time_validity(self, time: str) -> tuple[int, int] | None:
        """
        returns none if the time is invalid, otherwise returns a tuple of the hour and minute
        """
        hour = int(time[0:time.find(":")])
        minute = int(time[time.find(":") + 1:])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return (hour, minute)

    def validate_input(self) -> bool:
        """
        This function checks if the user inputted correct data and returns if the inputs are valid.
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

            # I'm declaring this here, so it doesn't calculate this unless it's needed, same with to_time
            regex_expression_no_leading_0 = r"^[0-9]{2}:[0-9]{2}$"
            regex_expression_with_leading_0 = r"^[0-9]{1}:[0-9]{2}$"

            if from_time == "" or not (re.match(regex_expression_with_leading_0, from_time) or re.match(regex_expression_no_leading_0, from_time)):
                self.error_label["text"] = "Please enter a valid starting time!"
                return False

            if to_time == "" or not (re.match(regex_expression_with_leading_0, to_time) or re.match(regex_expression_no_leading_0, to_time)):
                self.error_label["text"] = "Please enter a valid ending time!"
                return False

            if not self.check_time_validity(from_time) or not self.check_time_validity(to_time):
                self.error_label["text"] = "Please enter a valid starting/ending time!"
                return False

            if len(event_name) > self.max_event_name_length:
                self.error_label["text"] = "The event name is too long! The maximum length is " + \
                    str(self.max_event_name_length)
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


class Event():
    def __init__(self, event_name: str, from_time: str, to_time: str, event_description: str, event_id: int, day: Day) -> None:
        self.from_time = from_time
        self.to_time = to_time
        self.event_name = event_name
        self.event_description = event_description
        self.event_id = event_id
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

        self.event_name_short_label = tk.Label(self.frame, font=("Consolas", self.font_size))
        self.set_name()

    def view_event(self):
        self.modify_event_window: Optional[tk.Tk] = tk.Tk()
        self.modify_event_window.resizable(False, False)
        self.modify_event_window.title("View event")

        event_data: list[str] = [self.short_name, self.from_time, self.to_time, self.event_description]
        pretexts = ["Event name: ", "From time: ", "To time: ", "Event description: "]

        pretext_frame = tk.Frame(self.modify_event_window)
        data_frame = tk.Frame(self.modify_event_window)
        pretext_frame.grid(row=0, column=0)
        data_frame.grid(row=0, column=1)

        for count, (label_pretext, label_text) in enumerate(zip(pretexts, event_data)):
            pretext_label = tk.Label(pretext_frame, font=self.general_font, text=label_pretext)
            data_label = tk.Label(data_frame, font=self.general_font, text=label_text)

            pretext_label.grid(row=count, column=0, sticky="e")
            data_label.grid(row=count, column=0, sticky="w")

        modify_button = tk.Button(data_frame, font=self.general_font, text="Modify",
                                  command=lambda event_id=self.event_id: self.day.open_add_event_window(event_id))
        delete_button = tk.Button(data_frame, font=self.general_font, text="Delete",
                                  command=lambda event_id=self.event_id: self.day.delete_event(event_id))

        modify_button.grid(row=0, column=2, rowspan=2)
        delete_button.grid(row=2, column=2, rowspan=2)

        self.day.center_window(self.modify_event_window)
        self.modify_event_window.mainloop()

    def set_name(self):
        self.short_name = self.event_name
        if len(self.short_name) > self.max_event_width:
            self.short_name = self.short_name[:self.max_event_width] + "..."
        self.event_name_short_label["text"] = self.short_name

    def __setitem__(self, key: str, value: str):
        if key == "event_name":
            self.event_name = value
            self.set_name()
        elif key == "from_time":
            self.from_time = value
        elif key == "to_time":
            self.to_time = value
        elif key == "event_description":
            self.event_description = value
        else:
            raise Exception("Invalid key:", key)


if __name__ == "__main__":
    app = Calendar()

    app.root.mainloop()
