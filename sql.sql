CREATE DATABASE BookMyShow;

USE BookMyShow;

CREATE TABLE User
(
  UserName VARCHAR(20) NOT NULL,
  UserId INT NOT NULL AUTO_INCREMENT,
  Date_Of_Birth DATE NOT NULL,
  PRIMARY KEY (UserId)
);

CREATE TABLE Event_organiser
(
  OrgName VARCHAR(20) NOT NULL,
  OrgId INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (OrgId)
);

CREATE TABLE Tags
(
  TagId INT NOT NULL AUTO_INCREMENT,
  Details TEXT NOT NULL,
  TagName VARCHAR(20) UNIQUE NOT NULL,
  PRIMARY KEY (TagId)
  
);

CREATE TABLE Venue
(
  VenueId INT NOT NULL AUTO_INCREMENT,
  VenueName varchar(20) NOT NULL,
  Address TEXT NOT NULL,
  PRIMARY KEY (VenueId)
);

CREATE TABLE Event
(
  EventName VARCHAR(50) NOT NULL,
  EventId INT NOT NULL AUTO_INCREMENT,
  EventDate DATETIME NOT NULL,
  Age_of_Entry INT DEFAULT 0,
  SeatPrice float NOT NULL,
  SeatsAvailable INT NOT NULL,
  Details TEXT,
  OrgId INT NOT NULL,
  VenueId INT NOT NULL,
  isActive BOOLEAN default 1,
  PRIMARY KEY (EventId),
  FOREIGN KEY (OrgId) REFERENCES Event_organiser(OrgId) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (VenueId) REFERENCES Venue(VenueId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Booking
(
  BookingId INT NOT NULL AUTO_INCREMENT,
  TransactionID VARCHAR(12) NOT NULL,
  Seats INT NOT NULL,
  UserId INT,
  EventId INT,
  PRIMARY KEY (BookingId),
  FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (EventId) REFERENCES Event(EventId) ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE (TransactionID)
);


CREATE TABLE hasTag
(
  EventId INT NOT NULL,
  TagId INT NOT NULL,
  PRIMARY KEY (EventId, TagId),
  FOREIGN KEY (EventId) REFERENCES Event(EventId) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (TagId) REFERENCES Tags(TagId)
);

CREATE TABLE Reviews
(
  Rating INT NOT NULL,
  Body TEXT,
  UserId INT NOT NULL,
  EventId INT NOT NULL,
  PRIMARY KEY (UserId, EventId),
  FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (EventId) REFERENCES Event(EventId) ON DELETE CASCADE ON UPDATE CASCADE
);

DELIMITER $$
CREATE TRIGGER CheckIfSeatsAreAvailable
	BEFORE INSERT ON booking FOR EACH ROW
    BEGIN
		DECLARE availabel_seats INT;
        SELECT SeatsAvailable INTO available_seats FROM event WHERE EventId = NEW.EventId;
		IF available_seats < NEW.seats THEN 
			SIGNAL SQLSTATE '45000'
				SET MESSAGE_TEXT = "requested number of seats unavailable";
		END IF;
	END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CheckAge
	BEFORE INSERT ON booking FOR EACH ROW
    BEGIN
		DECLARE AgeLimit INT;
        DECLARE UserAge INT;
        SELECT age_of_entry INTO ageLimit  FROM event WHERE EventId = NEW.EventId;
        SELECT timestampdiff(year, date_of_birth, curdate()) INTO UserAge FROM user WHERE userid = NEW.userId;
        
		IF UserAge < AgeLimit THEN 
			SIGNAL SQLSTATE '45000'
				SET MESSAGE_TEXT = "User Underage";
		END IF;
	END;
$$
DELIMITER ;
	

DELIMITER $$
CREATE TRIGGER DecrementSeats
AFTER INSERT ON booking FOR EACH ROW
BEGIN

	DECLARE currentSeats INT;
	SELECT SeatsAvailable INTO currentSeats FROM event WHERE EventId = NEW.EventId;
	SET currentSeats = currentSeats - NEW.seats;
	UPDATE event SET SeatsAvailable = currentSeats WHERE EventId = NEW.EventId;
END;
$$
DELIMITER ;

DELIMITER $$	
CREATE TRIGGER TriggerCheckVenueClash
BEFORE INSERT ON Event FOR EACH ROW
BEGIN
	IF (CheckVenueClash(NEW.EventDate, NEW.venueId) = 0) THEN 
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = "Venue Clash";
	END IF;
END;
$$
DELIMITER ;

DELIMITER $$	
CREATE TRIGGER TriggerCheckVenueClashOnUpdate
BEFORE UPDATE ON Event FOR EACH ROW
BEGIN
	IF (CheckVenueClash(NEW.EventDate, NEW.venueId) = 0) THEN 
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = "Venue Clash";
	END IF;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE FUNCTION CheckVenueClash(myeventDate DATETIME, myvenueId INT) RETURNS INT 
DETERMINISTIC
BEGIN
	IF EXISTS(SELECT eventId FROM event WHERE DATE(eventdate)=DATE(myeventDate) AND venueId = myvenueId) THEN
		RETURN 0;
	ELSE
		RETURN 1;
	END IF;
END;
$$
DELIMITER ;







DELIMITER $$
CREATE PROCEDURE DeactivateEvents ()
BEGIN
	UPDATE Event 
    SET isActive = 0
    WHERE EventDate < CURDATE();
    
    DELETE FROM booking 
	WHERE bookingId in 
		(SELECT * FROM (SELECT bookingId FROM
        Booking NATURAL JOIN (SELECT eventId FROM event WHERE eventDate < CURDATE()) AS e) as B);
END;
$$
DELIMITER ;


CREATE EVENT EventCleanup 
	ON SCHEDULE EVERY 1 DAY STARTS TIMESTAMP(curdate())
    DO
		CALL DeactivateEvents();




CREATE TABLE SimilarityMatrix (
	EventId INT NOT NULL,
    ComparedEventId INT NOT NULL,
    Similarity FLOAT NOT NULL,
    PRIMARY KEY(EventId, ComparedEventId)
);


DELIMITER $$
CREATE PROCEDURE RecommendEvent(IN MyUserId INT)
BEGIN
	DECLARE likedEvent INT;
    DECLARE fetchedEvent INT;
    DECLARE finished INT DEFAULT  0;
    DECLARE similarity FLOAT;
    DECLARE commonTags INT;
    DECLARE totalTags INT;
    DECLARE eventCur CURSOR FOR SELECT DISTINCT eventId FROM event; 
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished=1;
    SELECT eventId INTO likedEvent FROM reviews WHERE UserId = MyUserId ORDER BY Rating LIMIT 1;
    IF likedEvent IS NULL THEN
		SELECT likedEvent, eventId, Avr FROM event as E NATURAL JOIN (SELECT Avg(Rating) as Avr, eventId FROM reviews GROUP BY eventId) as R ORDER BY -Avr ASC;
	ELSE
		OPEN eventCur;
		label: LOOP
				FETCH eventCur INTO fetchedEvent;
                IF finished THEN
					LEAVE label;
				END IF;
				IF fetchedEvent = likedEvent THEN
					ITERATE label;
				END IF;
				SELECT COUNT(*) INTO totalTags FROM ((SELECT TagId FROM hastag WHERE eventId = likedEvent) UNION (SELECT TagId FROM hastag WHERE eventId = fetchedEvent)) as F;
				SELECT COUNT(*) INTO commonTags FROM hastag WHERE eventid = likedEvent AND tagId IN (SELECT tagId FROM hasTag WHERE eventId = fetchedEvent);
				SET similarity = CAST(commonTags AS DECIMAL)/CAST(totalTags AS DECIMAL);
				INSERT INTO SimilarityMatrix VALUES (likedEvent, fetchedEvent, similarity);
                
		END LOOP label;
		SELECT * FROM similarityMatrix WHERE eventId = likedEvent order by similarity desc;
        DELETE FROM similarityMatrix WHERE eventId = likedEvent;
        CLOSE eventCur;
	END IF;
    COMMIT;
END;
$$
DELIMITER ;
    
DELIMITER $$    
CREATE FUNCTION getRevenueFromEvent(MyeventId INT) RETURNS FLOAT
DETERMINISTIC
BEGIN
	 RETURN (SELECT SUM(b.seats*e.seatPrice) FROM (SELECT Seats, EventId FROM Booking WHERE EventId = MyeventId) as b NATURAL JOIN (SELECT EventId, SeatPrice FROM Event WHERE eventId = MyeventId) as e GROUP BY e.eventId);
END$$
DELIMITER ;


  







