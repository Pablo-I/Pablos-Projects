// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Counts number of words in dictionary in load() and returns this value in the size()
unsigned int wordCount = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 676;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int hashkey;

    //Get hashcode using hash() function
    hashkey = hash(word);

    //Go to the element with the corresponding hascode in the hash table and loop through the linked list at that hascode
    for (node *cursor = table[hashkey]; cursor != NULL; cursor = cursor -> next)
    {
        if (strcasecmp(cursor -> word, word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int char1;
    unsigned int char2;
    unsigned int counter1 = 0;
    unsigned int counter2 = 1;
    unsigned int hashcode;

    // Remove case sensitivity
    char1 = tolower(word[0]);
    char2 = tolower(word[1]);

    //Find code for first letter
    for (int i = 0; i < 26; i++)
    {
        if (char1 == 'a' + i)
        {
            break;
        }
        else
        {
            counter1++;
        }
    }

    // Find code for second letter
    for (int k = 0; k < 26; k++)
    {
        if (char2 == 'a' + k)
        {
            break;
        }
        else
        {
            counter2++;
        }
    }

    // Combine the keys from the firts and second letetr to create overall hashcode
    if (counter1 == 0)
    {
        hashcode = counter2 - 1;
    }
    else
    {
        hashcode = (25 + ((counter1 - 1) * 26)) + counter2;
    }

    return hashcode;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    char bufferWord[LENGTH + 1];
    unsigned int hashCode;

    // Initialize table as NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Open dictionary file for reading
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Could not open dictionary.\n");
        return false;
    }

    // Read the dictionary file and record the words into the hash table
    while (fscanf(dict, "%s", bufferWord) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        strcpy(n -> word, bufferWord);
        hashCode = hash(n -> word);

        n -> next = table[hashCode];
        table[hashCode] = n;

        wordCount++;
    }

    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *temp;
    node *cursor;

    // Free the entire linked list at each element in the has table array
    for (int i = 0; i < 676; i++)
    {
        cursor = table[i];
        while (cursor != NULL)
        {
            temp = cursor;
            cursor = cursor -> next;
            free(temp);
        }
    }

    return true;
}