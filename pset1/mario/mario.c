#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    // Prompt for Height
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Print All
    for (int i = 1; i <= height; i++)
    {
        // print gap same as one hash
        for (int j = height; j > i; j--)
        {
            printf(" ");
        }
        // print hashes
        for (int k = i; k > 0; k--)
        {
            printf("#");
        }
        // print gap same as two hash
        printf("  ");
        // print hashes
        for (int k = i; k > 0; k--)
        {
            printf("#");
        }
        // next line
        printf("\n");
    }
}