CREATE DATABASE BookMyShow;

USE BookMyShow;

CREATE TABLE User
(
  UserName VARCHAR(20) NOT NULL,
  UserId INT NOT NULL,
  Date_Of_Birth INT NOT NULL,
  PRIMARY KEY (UserId)
);

CREATE TABLE Event_organiser
(
  OrgName VARCHAR(20) NOT NULL,
  OrgId INT NOT NULL,
  PRIMARY KEY (OrgId)
);

CREATE TABLE Tags
(
  TagId INT NOT NULL,
  Details INT NOT NULL,
  PRIMARY KEY (TagId)
);

CREATE TABLE Venue
(
  VenueId INT NOT NULL,
  VenueName INT NOT NULL,
  Address INT NOT NULL,
  PRIMARY KEY (VenueId)
);

CREATE TABLE Event
(
  EventName VARCHAR(50) NOT NULL,
  EventId INT NOT NULL,
  EventDate DATETIME NOT NULL,
  Age_of_Entry INT DEFAULT 0,
  SeatPrice float NOT NULL,
  SeatsAvailable INT NOT NULL,
  Details TEXT,
  OrgId INT NOT NULL,
  VenueId INT NOT NULL,
  PRIMARY KEY (EventId),
  FOREIGN KEY (OrgId) REFERENCES Event_organiser(OrgId) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (VenueId) REFERENCES Venue(VenueId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Booking
(
  BookingId INT NOT NULL,
  TransactionID VARCHAR(12) NOT NULL,
  Seats INT NOT NULL,
  UserId INT,
  EventId INT,
  PRIMARY KEY (BookingId),
  FOREIGN KEY (UserId) REFERENCES User(UserId),
  FOREIGN KEY (EventId) REFERENCES Event(EventId),
  UNIQUE (TransactionID)
);


CREATE TABLE hasTag
(
  EventId INT NOT NULL,
  TagId INT NOT NULL,
  PRIMARY KEY (EventId, TagId),
  FOREIGN KEY (EventId) REFERENCES Event(EventId),
  FOREIGN KEY (TagId) REFERENCES Tags(TagId)
);

CREATE TABLE Reviews
(
  Rating INT NOT NULL,
  Body TEXT,
  UserId INT NOT NULL,
  EventId INT NOT NULL,
  PRIMARY KEY (UserId, EventId),
  FOREIGN KEY (UserId) REFERENCES User(UserId),
  FOREIGN KEY (EventId) REFERENCES Event(EventId)
);

ALTER TABLE Tags
ADD TagName VARCHAR(20) UNIQUE; 