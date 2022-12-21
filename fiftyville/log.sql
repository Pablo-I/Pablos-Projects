-- Keep a log of any SQL queries you execute as you solve the mystery.


-- Query to find the description of the crime that took place on July 28, 2021, on Humphrey Street
SELECT description FROM crime_scene_reports WHERE day = 28 AND month = 7 AND street = "Humphrey Street";

-- Query to scan through the Humphrey Bakery Security Logs at 10:15am
SELECT activity, minute, license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND hour = 10;

-- Query to determine who were the witnesses that saw the crime at Humphrey Bakery
SELECT name, transcript FROM interviews WHERE day = 28 AND month = 7 AND transcript LIKE "%bakery%";

-- Query to determine all license plates observed within 10min of the theft (Ruth's Lead)
SELECT activity, license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute >14 AND minute < 26;

-- Query to determine the names of people who made atm withdrawl transactions the day of the theft (Eugene's Lead)
SELECT name, person_id FROM bank_accounts JOIN people on people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND transaction_type = "withdraw" AND atm_location = "Leggett Street");

-- Query to determine the license plate numbers of the people that made withdrawls on the Leggett Street atm
SELECT name, license_plate FROM people WHERE id IN (SELECT person_id FROM bank_accounts JOIN people on people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND transaction_type = "withdraw" AND atm_location = "Leggett Street"));

-- Query to determine what people were at both the Bakery and Leggett Street the day of the crime
SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute > 14 AND minute < 26 INTERSECT SELECT license_plate FROM people WHERE id IN (SELECT person_id FROM bank_accounts JOIN people on people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")));

-- Query to determine who called the day of the crime (Raymond's Lead)
SELECT name, duration, caller, receiver FROM people JOIN phone_calls on phone_calls.caller = people.phone_number WHERE day = 28 AND month = 7 AND duration < 60;
SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute > 14 AND minute < 26 INTERSECT SELECT license_plate FROM people WHERE id IN (SELECT person_id FROM bank_accounts JOIN people on people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND transaction_type = "withdraw" AND atm_location = "Leggett Street"))) INTERSECT SELECT name FROM people JOIN phone_calls on phone_calls.caller = people.phone_number WHERE day = 28 AND month = 7;

-- Query to find out who flew on July 29th
SELECT passport_number FROM passengers JOIN flights on flights.id = passengers.flight_id WHERE day = 29 AND month = 7 INTERSECT SELECT passport_number FROM people WHERE name = "Bruce" OR name = "Diana" OR name = "Luca";
SELECT name, passport_number FROM people WHERE passport_number IN (SELECT passport_number FROM passengers JOIN flights on flights.id = passengers.flight_id WHERE day = 29 AND month = 7 INTERSECT SELECT passport_number FROM people WHERE name = "Bruce" OR name = "Diana" OR name = "Luca");
SELECT passport_number, hour, origin_airport_id, destination_airport_id FROM passengers JOIN flights on flights.id = passengers.flight_id WHERE passport_number IN (SELECT passport_number FROM people WHERE passport_number IN (SELECT passport_number FROM passengers JOIN flights on flights.id = passengers.flight_id WHERE day = 29 AND month = 7 INTERSECT SELECT passport_number FROM people WHERE name = "Bruce" OR name = "Diana"));

-- Query to find where Bruce flew
SELECT city FROM airports JOIN flights on flights.destination_airport_id = airports.id WHERE destination_airport_id = 4;

-- Query to find out who Bruce called
SELECT name, duration, caller, receiver FROM people JOIN phone_calls on phone_calls.caller = people.phone_number WHERE day = 28 AND month = 7 AND name = "Bruce";
SELECT name, phone_number FROM people WHERE phone_number IN (SELECT receiver FROM people JOIN phone_calls on phone_calls.caller = people.phone_number WHERE day = 28 AND month = 7 AND name = "Bruce");

-- CONCLUSION:
-- The thief is Bruce since he is the only person who was seen at the Bakery and at the Leggett ATM on the same day that he made a call early in the morning for about 30min. Additionally, he was the one that left the earliest the next day.
-- Destination: Bruce flew to New York City
-- The accomplice was Robin since Bruce called Robin for about 30min when he entered the bakery early in the morning and told them to book a flight for the next morning.