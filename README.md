# Background

Most calendar applications provide some kind of "meet with" feature where the user
can input a list of coworkers with whom they want to meet, and the calendar will
output a list of times where all the coworkers are available.

For example, say that we want to schedule a meeting with Jane, John, and Mary on Monday.

- Jane is busy from 9am - 10am, 12pm - 1pm, and 4pm - 5pm.
- John is busy from 9:30am - 11:00am and 3pm - 4pm
- Mary is busy from 3:30pm - 5pm.

Based on that information, our calendar app should tell us that everyone is available:
- 11:00am - 12:00pm
- 1pm - 3pm

We can then schedule a meeting during any of those available times.


# Instructions

Given the data in `events.json` and `users.json`, you can find the available meeting times for a given set of users using the following syntax:

```
python3 availability.py Maggie,Joe,Jordan
```

which would output something like this:

```
2021-07-05 13:30 - 16:00
2021-07-05 17:00 - 19:00
2021-07-05 20:00 - 21:00

2021-07-06 14:30 - 15:00
2021-07-06 16:00 - 18:00
2021-07-06 19:00 - 19:30
2021-07-06 20:00 - 20:30

2021-07-07 14:00 - 15:00
2021-07-07 16:00 - 16:15
```


Working hours are between 13:00 and 21:00 UTC


## Data files

### `users.json`

A list of users that our system is aware of. You can assume all the names are unique (in the real world, maybe
they would be input as email addresses).

`id`: An integer unique to the user

`name`: The display name of the user - your program should accept these names as input.

### `events.json`

A dataset of all events on the calendars of all our users.

`id`: An integer unique to the event

`user_id`: A foreign key reference to a user

`start_time`: The time the event begins

`end_time`: The time the event ends


# Notes

- Feel free to use whatever language you feel most comfortable working with

** I used python because it seemed to provide the simplest and most portable solution for a problem like this

- Please provide instructions for execution of your program

** Provided above

- Please include a description of your approach to the problem, as well as any documentation about
  key parts of your code.

** My code used ther following approach
1. Collect usernames as user input, allowing for some variation in input style
2. Return ids given usernames
3. Return schedules given ids
4. Convert the schedule array into an int array by calculating the minutes since start date of each time entry.
5. Sort the schedule array from the earliest start time to the latest start time
6. Calculate free times from array by checking the difference between the start date of each event and the end date of the prevoious event
7. Remove any free times that might fall outside of the specified time range (this doesn't seem to exist in the provided data but would likely exist in the real world)
8. Convert free times array into readable format and print output

- You'll notice that all our events start and end on 15 minute blocks. However, this is not a strict
  requirement. Events may start or end on any minute (for example, you may have an event from 13:26 - 13:54).

** This program should produce accurate results down to the minute
