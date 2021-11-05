#include <cs50.h>
#include <stdio.h>

long get_credit(void);
void print_credit_type(int, int);

int main(void)
{
    // Get Card number
    long credit = get_credit();
    long number = credit;
    int start = 0;
    int length = 0;
    int first_sum = 0;
    int second_sum = 0;

    // Loop to get digit and sum up
    while (number != 0)
    {
        // start number
        if (number / 100 == 0 && start == 0)
        {
            start = number;
        }

        // Get Digit
        int digit = number % 10;

        // Calculate First Step
        if (length % 2 == 0)
        {
            first_sum += digit;
        }
        else
        {
            digit *= 2;
            // if digit is greater than 9, sum up
            if (digit > 9)
            {
                second_sum += digit % 10 + digit / 10;
            }
            else
            {
                second_sum += digit;
            }
        }

        // Get next digit
        number /= 10;
        length++;
    }

    // Second Step, sum up first_sum and second_sum
    int sum = first_sum + second_sum;
    int checksum = sum % 10;

    // Print result
    if (checksum == 0)
    {
        print_credit_type(start, length);
    }
    else
    {
        printf("INVALID\n");
    }
}

// Prompt user for credit or debit card numer
long get_credit(void)
{
    long n;
    do
    {
        n = get_long("Number: ");
    }
    while (n < 1);
    return n;
}

// Check Credit Card Type
void print_credit_type(int start, int length)
{
    // check is valid
    bool is_ae_start = start == 34 || start == 37;
    bool is_master_start = start > 50 && start < 56;
    bool is_visa_start = start / 10 == 4;
    bool is_ae_length = length == 15;
    bool is_master_length = length == 16;
    bool is_visa_length = length == 13 || length == 16;

    // Print
    if (is_ae_start && is_ae_length)
    {
        printf("AMEX\n");
    }
    else if (is_master_start && is_master_length)
    {
        printf("MASTERCARD\n");
    }
    else if (is_visa_start && is_visa_length)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}