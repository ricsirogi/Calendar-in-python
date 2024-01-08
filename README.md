# Calendar in python

I'm trying to create a functioning calendar in python that will work for windows 10

## How to use:

- Use the arrows on the left and right to navigate between the months
- Click on the year or month to change them more quickly, and when you wrote in you desired year or month, press enter to verify it

## To-do:

- [x] Make the calendar functional, with quickly modifiable year and month, and buttons to go through every month one by one
- [x] Make each day clickable, and when a day is clicked, it creates new window where you can add the details of the event
- [x] The events should be displayed, so I want to do what google calendar does on phone, and have a little space below the days and the first few words of the event can be displayed there
- [x] and these events will also be clickable, and when clicked a new window pops up, where you can view the event
- [x] There's a button in the event view window, to edit the event
- [x] Fix the events, because if you modify events when there are two or more events then the first event will take the the place of the last/second (idk) event and the first place will just be left out with (i guess) an emtpy string
- [x] Instead of the 'add event' window popping up when a day is clicked, an 'events view' window pops up where you can see all the events, there's an 'add' button to add an event, or you can click any of the events to view them and then modify them
- [x] The events are sorted by their start time
- [ ] The sorting sometimes just straight up doesn't remove the old labels and so when sorting there are two times more widgets and it's a mess so I want to fix that
- [ ] Make it so the user can't open more than one window at any time
- [ ] Fix the bug where when I step between months the events are no longer visible if I go back (so I create an event on august, go to september, back go august, the event I created there is gone, but if I click on its day, it's still there)
- [ ] Maybe find a better way to change the month and year
- [ ] Store events in a json file
- [ ] Optimizations, like instead of generating each month's days every time, store them, and access them when needed
- [ ] Make more specific exceptions
