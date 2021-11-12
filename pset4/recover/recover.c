#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc < 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // initial all
    typedef uint8_t BYTE;
    int count = 0;
    int size = 512;
    BYTE *buffer = malloc(size);
    char *filename = malloc(3);
    FILE *img;

    // Loop file
    while (fread(buffer, sizeof(BYTE), size, file))
    {
        // Get new photo header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close recent image file
            if (count > 0)
            {
                fclose(img);
            }
            // write new image file
            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "w");
            fwrite(buffer, 1, size, img);
            count++;
        }
        else if (count > 0)
        {
            // write data
            fwrite(buffer, 1, size, img);
        }
    }
    // close all
    fclose(img);
    fclose(file);
    free(buffer);
    free(filename);
    return 0;
}