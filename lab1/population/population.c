#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int start, end, current, years = 0;

    // TODO: Prompt for start size
    do
    {
        start = get_int("Start size: ");
        current = start;
    }
    while (start < 9);

    // TODO: Prompt for end size
    do
    {
        end = get_int("End size: ");
    }
    while (start > end);

    // TODO: Calculate number of years until we reach threshold
    while (current < end)
    {
        int born =  current / 3;
        int pass = current / 4;
        current += born - pass;
        years += 1;
    }


    // TODO: Print number of years
    printf("Years: %i\n", years);
}