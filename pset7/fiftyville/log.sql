-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = "Chamberlin Street";
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.

SELECT transcript
FROM interviews
WHERE month = 7 AND day = 28
AND transcript LIKE "%courthouse%";
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
-- I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

SELECT DISTINCT(activity) FROM courthouse_security_logs;
-- entrance
-- exit

SELECT DISTINCT(transaction_type) FROM atm_transactions;
-- deposit
-- withdraw

-- Find Match transcript 1 people
SELECT name
FROM people
WHERE license_plate IN (
    SELECT DISTINCT(license_plate)
    FROM courthouse_security_logs
    WHERE month = 7 AND day = 28 AND hour = 10
    AND minute > 15 AND minute <= 25 AND activity = "exit"
)
-- Find Match transcript 2 people
INTERSECT
SELECT name
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE account_number IN (
    SELECT account_number
    FROM atm_transactions
    WHERE month = 7 AND day = 28
    AND transaction_type = "withdraw" AND atm_location = "Fifer Street"
)
INTERSECT
-- Find Match transcript 3 people
SELECT name
FROM people
WHERE passport_number IN (
    SELECT passport_number
    FROM passengers
    WHERE flight_id IN (
        SELECT id
        FROM flights
        WHERE month = 7 AND day = 29
        AND origin_airport_id IN (
            SELECT id
            FROM airports
            WHERE city = "Fiftyville"
        )
        ORDER BY hour, minute LIMIT 1
    )
) AND phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE month = 7 AND day = 28 AND duration < 60
);
-- The THIEF is: Ernest

SELECT city
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE month = 7 AND day = 29
AND origin_airport_id IN (
    SELECT id
    FROM airports
    WHERE city = "Fiftyville"
)
ORDER BY hour, minute LIMIT 1;
-- The thief ESCAPED TO: London

SELECT name
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE caller IN (
        SELECT phone_number
        FROM people
        WHERE name = "Ernest"
    ) AND month = 7 AND day = 28 AND duration < 60
);
-- The ACCOMPLICE is: Berthold