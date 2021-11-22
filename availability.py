import sys
import json
from datetime import datetime, timedelta

#hard-coded variables
startDate = '2021-07-05T13:00:00'
endDate = '2021-07-07T21:00:00'
# e.g. office closures, holidays
hardcodedExceptions = [('2021-07-05T21:00:00', '2021-07-06T13:00:00'),
                       ('2021-07-06T21:00:00', '2021-07-07T13:00:00')]

#sanitize user input and store in candidates array
candidates = []
for arg in sys.argv[1:]:
    for segment in arg.split(","):
        if segment.strip():
            candidates.append(segment.strip())

#load events and users object from json
allEvents = json.load(open("events.json"))
allUsers = json.load(open("users.json"))

#to get the id for one specified user


def getId(candidate):
    userId = next((user['id'] for user in allUsers if user['name'].lower(
    ) == candidate.lower()), False)
    if not userId:
        print("User '" + candidate +
              "' not found. Please check your spelling and try again.")
        sys.exit()
    return userId

#to get the events for one specified user


def getEvents(id):
    userEvents = [(event['start_time'], event['end_time'])
                  for event in allEvents if event['user_id'] == id]
    return userEvents

#to get the ids for all specified users


def getAllIds(candidateArray):
    allIds = []
    for candidate in candidateArray:
        allIds.append(getId(candidate))
    return allIds

#to get the events for all specified ids


def getAllEvents(idArray):
    allEvents = []
    for id in idArray:
        for eventTuple in getEvents(id):
            allEvents.append(eventTuple)
    return allEvents

#convert a date to an int (minutes since start time)


def convertDateToInt(date, startDate):
    startFrom = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
    countTo = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    dateAsInt = int((countTo - startFrom).total_seconds() / 60)
    return dateAsInt

#convert date array into int array (minutes since start time)


def convertDatesToInts(dateTupleArray, startDate):
    intDateTupleArray = []
    for dateTuple in dateTupleArray:
        start = convertDateToInt(dateTuple[0], startDate)
        end = convertDateToInt(dateTuple[1], startDate)
        intDateTupleArray.append((start, end))
    return intDateTupleArray

#calculate all free times


def getFreeTimesAsInts(intTupleArray, hardcodedExceptions, startDate, endDate):
    allEventsArray = []  # all busy times for all users
    freeTimesArray = []  # may include out-of-range values
    cleanFreeTimesArray = []  # all free times within range

    #convert all events to ints (minutes since start time)
    intTupleArray = convertDatesToInts(intTupleArray, startDate)
    hardcodedExceptions = convertDatesToInts(hardcodedExceptions, startDate)
    cutoff = convertDateToInt(endDate, startDate)

    #collect all events and hard-coded exceptions into one place
    for tuple in intTupleArray:
        allEventsArray.append(tuple)
    for tuple in hardcodedExceptions:
        allEventsArray.append(tuple)

    #sort array lowest to highest on start time
    allEventsArray.sort(key=lambda tup: tup[0])
    #test_allEventsArray = [(-1500,-1400),(-45,-40),(-30,-15),(10,400),(500,730),(3350,3355),(3370,3400),(3500,3700)]
    #if there is space between the booked events, log it
    previousEndDate = 0
    for tuple in allEventsArray:
        if (tuple[0]-previousEndDate) > 0:
            freeTimesArray.append((previousEndDate, tuple[0]))
        previousEndDate = tuple[1]

    #now trim free times before startDate and after endDate
    for tuple in freeTimesArray:
        #if it straddles the start time...
        if tuple[0] < 0 and tuple[1] > 0:
            cleanFreeTimesArray.append((0, tuple[1]))
        #if it is cleanly between start and end time...
        if tuple[0] > 0 and tuple[0] < cutoff and tuple[1] > 0 and tuple[1] < cutoff:
            cleanFreeTimesArray.append((tuple[0], tuple[1]))
        #if it straddles the cutoff time...
        if tuple[0] > 0 and tuple[0] < cutoff and tuple[1] > 0 and tuple[1] > cutoff:
            cleanFreeTimesArray.append((tuple[0], cutoff))

    return cleanFreeTimesArray

#convert back to readable date format


def outputIntsAsDates(intTupleArray, startDate):
    for tuple in intTupleArray:
        baseTime = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
        startTime = baseTime + timedelta(minutes=tuple[0])
        endTime = baseTime + timedelta(minutes=tuple[1])
        print(startTime.strftime("%Y-%M-%d %H:%M"),
              "-", endTime.strftime("%H:%M"))
    return


def main():

    if len(sys.argv) < 2:
        print("No users specified. Please provide at least one user.")
        sys.exit()

    allEventTimes = getAllEvents(getAllIds(candidates))
    allFreeTimesAsInts = getFreeTimesAsInts(
        allEventTimes, hardcodedExceptions, startDate, endDate)
    print("---------------------------")
    print("Users ", end=" ")
    for candidate in candidates:
        print(candidate, end=", ")
    print(" are available to meet at these times:")
    outputIntsAsDates(allFreeTimesAsInts, startDate)
    print("---------------------------")


main()