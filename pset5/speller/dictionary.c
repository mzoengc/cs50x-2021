// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 5381;

// Hash table
node *table[N];

// Number of word;
int count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int code = hash(word);
    node *cursor = table[code];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO http://www.cse.yorku.ca/~oz/hash.html djb2
    unsigned long hash = 5381;
    int c;

    while ((c = tolower(*word++)))
    {
        /* hash * 33 + c */
        hash = ((hash << 5) + hash) + c;
    }

    return hash & N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    char word[LENGTH + 1];
    FILE *file = fopen(dictionary, "r");
    if (file != NULL)
    {
        while (fscanf(file, "%s", word) != EOF)
        {
            unsigned int code = hash(word);
            node *n = malloc(sizeof(node));
            strcpy(n->word, word);
            n->next = table[code];
            table[code] = n;
            count++;
        }
        fclose(file);
        return true;
    }

    return false;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *cursor;
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return cursor == NULL;
}
