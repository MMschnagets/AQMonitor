drop table if exists AQDevices;
create table AQDevices
(
    ID          INT AUTO_INCREMENT
        primary key,
    AQDevice_ID INT
        unique,
    Latitude    FLOAT,
    Longitude   FLOAT,
    Status      VARCHAR(20)
);

drop table if exists AQIResults;
create table AQIResults
(
    ID          INT AUTO_INCREMENT
        primary key,
    AQDevice_ID INT
        references AQDevices (AQDevice_ID),
    PM25        FLOAT,
    PM10        FLOAT,
    O3          FLOAT,
    NO2         FLOAT,
    SO2         FLOAT,
    CO          FLOAT,
    DateTime    DATETIME default CURRENT_TIMESTAMP
);

drop table if exists RawData;
create table RawData
(
    ID          INT AUTO_INCREMENT
        primary key,
    AQDevice_ID INT
        references AQDevices (AQDevice_ID),
    PM25        FLOAT,
    PM10        FLOAT,
    O3          FLOAT,
    NO2         FLOAT,
    SO2         FLOAT,
    CO          FLOAT,
    DateTime    DATETIME default CURRENT_TIMESTAMP
);