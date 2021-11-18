from cs50 import get_string
import re


def main():
    # Prompt
    while True:
        credit = get_string("Number: ")
        if (re.match(r'^[0-9]+$', credit)):
            break

    # Calculate checksum
    first_sum = 0
    second_sum = 0
    for i, c in enumerate(reversed(credit)):
        digit = int(c)
        if i % 2 == 0:
            first_sum += digit
        else:
            digit *= 2
            # if digit is greater than 9, sum up
            if digit > 9:
                second_sum += int(digit / 10) + digit % 10
            else:
                second_sum += digit
    checksum = (first_sum + second_sum) % 10

    # check checksum is 0
    if checksum == 0:
        # Check Credit Card Type
        if credit[:2] in ["34", "37"] and len(credit) == 15:
            print("AMEX")
        elif int(credit[:2]) in range(51, 56) and len(credit) == 16:
            print("MASTERCARD")
        elif credit[0] == "4" and len(credit) in [13, 16]:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


if __name__ == "__main__":
    main()
