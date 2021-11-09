#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

bool valid_key(string key);
void encrypt_message(string key, string message);

int main(int argc, string argv[])
{
    // Check arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Check is a valid key
    string key = argv[1];
    bool valid = valid_key(key);
    if (!valid)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Do Encrypt Message
    string message = get_string("plaintext:  ");
    encrypt_message(key, message);
    return 0;
}

bool valid_key(string key)
{
    int length = strlen(key);
    int a = (int) 'A';
    int z = (int) 'Z';

    // containing each letter exactly once
    int total_ascii = ((float)(a + z) / 2) * (z - a + 1);
    int sum_key = 0;

    // containing 26 characters
    if (length != 26)
    {
        return false;
    }


    for (int i = 0, n = length; i < n; i++)
    {
        // any character is an alphabetic character
        char c = key[i];
        if (isalpha(c))
        {
            // uppercase characters and add to sum_key
            sum_key += (int) toupper(c);
        }
        else
        {
            return false;
        }

    }

    // check sum_key equal to total_ascii, mean all alphabetic character exactly once
    return sum_key == total_ascii;
}

void encrypt_message(string key, string message)
{
    printf("ciphertext: ");
    // Encrypting
    for (int i = 0, n = strlen(message); i < n; i++)
    {
        char c = message[i];
        if (isalpha(c))
        {
            int index_in_key = (int) toupper(c) - (int) 'A';
            char r = key[index_in_key];
            printf("%c", isupper(c) ? toupper(r) : tolower(r));
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");
}