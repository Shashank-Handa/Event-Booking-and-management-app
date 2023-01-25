import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="BookMyShow"
)
c= mydb.cursor()
d= mydb.cursor()

def get_all_events():
    c.execute("SELECT eventName, eventDate, Age_of_entry, Details, OrgName, VenueName, eventId, seatsAvailable FROM event AS e NATURAL JOIN event_organiser AS eo NATURAL JOIN VENUE as v")
    return c.fetchall()

def get_events_by_eventId(eventId: object) -> object:
    if(not eventId):
        return []
    stringIds = [str(x) for x in eventId]
    d.execute("SELECT eventName, eventDate, Age_of_entry, Details, OrgName, VenueName,eventId, seatsAvailable FROM (SELECT * FROM event WHERE eventid in ({})) AS e NATURAL JOIN event_organiser AS eo NATURAL JOIN VENUE as v".format((",".join(stringIds))))
    return d.fetchall()

def get_events_by_tag(tagName):
    c.execute("SELECT tagId FROM tags WHERE tagName = '{}'".format(tagName))
    tagId=c.fetchone()
    c.execute("SELECT EventId FROM Event NATURAL JOIN (SELECT * FROM hasTag WHERE tagId = '{}') as b WHERE isActive = 1".format(tagId[0]))
    eventIdList=[]
    for i in c.fetchall():
        eventIdList.append((i[0]))
    eventList = get_events_by_eventId(eventIdList)
    return eventList

def get_events_by_date(fromDate, toDate):
    c.execute("SELECT eventId FROM event WHERE EventDate BETWEEN '{0}' AND '{1}' AND isActive = 1".format(fromDate, toDate))
    eventIdList = [x[0] for x in c.fetchall()]
    eventList = get_events_by_eventId((eventIdList))
    return eventList

def book_event(TransactionId, Seats, UserId, EventId):
    if Seats==0:
        return 0
    c.execute("SELECT isActive FROM event WHERE EventId = {}".format(EventId))
    status = c.fetchone()[0]
    if(not status):
        print("event unavailable")
        return 0

    c.execute("INSERT INTO booking (TransactionId, Seats, UserId, EventId) VALUES ('{0}', {1}, {2}, {3})".format(TransactionId, Seats, UserId, EventId))
    mydb.commit()
    return 1


def get_bookings_by_org(OrgId):
    c.execute("SELECT eventId FROM event WHERE OrgId={}".format(OrgId))
    eventIdList = [x[0] for x in c.fetchall()]
    stringIds = [str(x) for x in eventIdList]
    c.execute("SELECT b.eventId, SUM(b.seats), getRevenueFromEvent(b.eventId) FROM (SELECT Seats, EventId FROM Booking WHERE EventId in ({0})) as b GROUP BY b.eventId".format(",".join(stringIds)))
    return c.fetchall()

def add_review(userId, eventId, Rating, Review):
    print("reviewed")
    c.execute("INSERT INTO `bookmyshow`.`reviews` (`Rating`, `Body`, `UserId`, `EventId`) VALUES ('{2}', '{3}', '{0}', '{1}');".format(userId, eventId, Rating, Review))
    c.execute("COMMIT")

def get_user_bookings(userId):
    c.execute("SELECT  b.bookingId, e.eventName, b.Seats FROM (SELECT bookingId, Seats, eventId FROM booking WHERE userId = {} ) as b NATURAL JOIN event AS e".format(userId))
    return c.fetchall()

def add_event(EventName, EventDate, SeatPrice, SeatsAvailable, Details, OrgId, VenueId,  AgeOfEntry = 0):
    c.execute("INSERT INTO event (eventName, EventDate, Age_Of_Entry, SeatPrice, SeatsAvailable, Details, OrgId, VenueId) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(EventName, EventDate, AgeOfEntry, SeatPrice, SeatsAvailable, Details, OrgId, VenueId))
    c.execute("COMMIT")



def renew_event(eventId, EventDate):
    c.execute("UPDATE event SET EventDate = '{0}' WHERE eventId = {1}".format(EventDate, eventId))
    c.execute("COMMIT")


def get_review(eventId):
    c.execute(("SELECT Rating, Body FROM Reviews WHERE eventId = {}".format(eventId)))
    return c.fetchall()

def get_events_by_rating():
    c.execute(
        "SELECT eventName, eventDate, Age_of_entry, Details, OrgName, VenueName FROM event AS e NATURAL JOIN event_organiser AS eo NATURAL JOIN VENUE as v LEFT JOIN (SELECT eventId, AVG(rating) as avg from Reviews GROUP BY eventId) as r on e.eventId = r.eventId order by -r.avg ASC")
    return c.fetchall()

def get_tags():
    c.execute("SELECT tagName, tagId FROM tags")
    return c.fetchall()

def get_venues():
    c.execute("SELECT VenueId, VenueName, address FROM Venue")
    return c.fetchall()

def get_inactive_events(OrgId):
    c.execute("SELECT eventId, eventName FROM event WHERE OrgId = {} AND isActive = 0".format(OrgId))
    return c.fetchall()

def add_tags(eventId, TagIds):
    for TagId in TagIds:
        c.execute("INSERT INTO hastag (eventId, tagId) values('{0}', '{1}')".format(eventId, TagId))
        c.execute("COMMIT")

def run_query(query):
    c.execute(str(query))
    return c.fetchall()

def get_events_by_Org(OrgId):
    c.execute(
        "SELECT EventId FROM Event WHERE OrgId = '{}'".format(OrgId))
    eventIdList = []
    for i in c.fetchall():
        eventIdList.append((i[0]))
    eventList = get_events_by_eventId(eventIdList)
    return eventList

def add_user(username, DOB):
    c.execute("INSERT INTO user(username, Date_Of_Birth) VALUES('{0}', '{1}')".format(username,DOB))
    c.execute("COMMIT")

def get_recommendation(userId):
    c.execute("CALL RecommendEvent('{}')".format(userId))
    result = c.fetchall()
    result.sort(key=lambda x:x[2])
    eventIdList = [x[1] for x in result][0:6]
    print(eventIdList)
    eventList = get_events_by_eventId((eventIdList))
    return eventList

def update_event(eventId, EventName, EventDate, SeatPrice, SeatsAvailable, Details, OrgId, VenueId, AgeOfEntry, Status):
    c.execute(
        "UPDATE event SET eventName='{0}', EventDate='{1}', Age_Of_Entry='{2}', SeatPrice='{3}', SeatsAvailable='{4}', Details= '{5}', OrgId='{6}', VenueId='{7}', isActive = '{8}' WHERE eventId = '{9}' ".format(
            EventName, EventDate, AgeOfEntry, SeatPrice, SeatsAvailable, Details, OrgId, VenueId, Status, eventId))
    c.execute("COMMIT")

def add_venue(Name, Address):
    c.execute("INSERT INTO venue (VenueName, address) VALUES ('{0}', '{1}')".format(Name, Address))
    c.execute("COMMIT")

def delete_event(eventId):
    c.execute("DELETE FROM event WHERE eventId = '{}'".format(eventId))
    c.execute("COMMIT")

def get_event_details(eventId):
    c.execute("SELECT eventName, eventDate, Age_of_entry, Details, OrgName, VenueName,eventId, seatsAvailable FROM (SELECT * FROM event WHERE eventid in ({})) AS e NATURAL JOIN event_organiser AS eo NATURAL JOIN VENUE as v")

