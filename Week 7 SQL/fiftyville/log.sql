-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Take peak at database
.schema
-- crime_scene_reports, interviews, atm_transactions, bank_accounts, airports, flights, passengers, phone_calls, people, bakery_security_logs

-- Take peak at crime_scene_reports table
SELECT * FROM crime_scene_reports;

-- Narrow down data in crime_scene_reports based on know data that occured on Humphrey Street
SELECT description FROM crime_scene_reports WHERE street = "Humphrey Street";
-- | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

-- Check out interviews
SELECT name, month, day, transcript FROM interviews WHERE month = 7 and year = 2021 and day = 28;
-- | Ruth    | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
-- | Eugene  | 7     | 28  | I don't know the thief's name, but it was someone I recognized.
-- Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- | Raymond | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket. |

-- Follow up on Ruth's lead. Look for people associated with license plates within 10 minutes after theft occured.
SELECT name, phone_number, passport_number, people.license_plate FROM people
      INNER JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
      WHERE month = 7 AND year = 2021 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;
-- | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
-- | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       |
-- | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
-- | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |

-- Following Eugene's lead. Looking up person associated with bank account number based on Eugene seeing thief using atm.
SELECT name, phone_number, passport_number, license_plate FROM people
      INNER JOIN bank_accounts ON person_id = people.id
      INNER JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
      WHERE atm_location = "Leggett Street" AND month = 7 AND year = 2021 AND day = 28;
-- | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | Kaelyn  | (098) 555-1164 | 8304650265      | I449449       |
-- | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       |
-- | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
-- | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
-- | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |

-- Based on previous data, Bruce, Diana, Iman, and Luca are main suspects

-- Following Raymond's lead. Looking at phone calls made.
-- Caller
SELECT name, phone_number, passport_number, license_plate FROM people
      INNER JOIN phone_calls ON caller = phone_number WHERE month = 7 AND year = 2021 AND day = 28 AND duration BETWEEN 1 AND 60;
-- | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
-- | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
-- | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | Kathryn | (609) 555-5876 | 6121106406      | 4ZY7I8T       |
-- | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
-- | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
-- | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | Carina  | (031) 555-6622 | 9628244268      | Q12B3Z3       |
-- | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
-- | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |

-- Bruce and Diana are primary suspects

-- Receiver
SELECT name, phone_number, passport_number, license_plate FROM people
      INNER JOIN phone_calls ON receiver = phone_number WHERE month = 7 AND year = 2021 AND day = 28 AND duration BETWEEN 1 AND 60;
-- | Jack       | (996) 555-8899 | 9029462229      | 52R0Y8U       |
-- | Larry      | (892) 555-8872 | 2312901747      | O268ZZ0       |
-- | Robin      | (375) 555-8161 |                 | 4V16VO0       |
-- | Luca       | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | Melissa    | (717) 555-1342 | 7834357192      |               |
-- | James      | (676) 555-6554 | 2438825627      | Q13SVG6       |
-- | Philip     | (725) 555-3243 | 3391710505      | GW362R6       |
-- | Jacqueline | (910) 555-3251 |                 | 43V0R5D       |
-- | Doris      | (066) 555-9701 | 7214083635      | M51FA04       |
-- | Anna       | (704) 555-2131 |                 |               |

-- Robin and Philip are suspected of being an accomplish

-- Continuing Raymond's lead, use passport number to find person. Search flights in Fiftyville airport. Earliest flight is our thief!
SELECT name, phone_number, people.passport_number, license_plate FROM people
      INNER JOIN passengers ON passengers.passport_number = people.passport_number
      INNER JOIN flights ON flight_id = flights.id
      INNER JOIN airports ON airports.id = origin_airport_id WHERE city = "Fiftyville"
      AND month = 7 AND year = 2021 AND day = 29 ORDER BY hour ASC, minute ASC;
-- | Doris     | (066) 555-9701 | 7214083635      | M51FA04       |
-- | Sofia     | (130) 555-0289 | 1695452385      | G412CB7       |
-- | Bruce     | (367) 555-5533 | 5773159633      | 94KL13X       |

-- Out of our two remaining suspects, Bruce has the earliest flight. That would make Robin the accomplish.

-- Find out destination city
SELECT city FROM airports INNER JOIN flights ON destination_airport_id = airports.id INNER JOIN passengers ON flight_id = flights.id WHERE passport_number = 5773159633;
-- | New York City |

-- Bruce's flight is headed to NYC

-- Answer: Bruce is the thief, Robin is the accomplish, city of escape is NYC