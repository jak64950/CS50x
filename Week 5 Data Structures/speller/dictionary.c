// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
const unsigned int N = 150000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Set index to value of word in hash table
    int index = hash(word);
    // Point cursor to first node in linked list
    node *cursor = table[index];
    // Compare inputted word to cursor until reach end of linked list and return true if match found
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor -> word) == 0)
        {
            return true;
        }
        // Set cursor to next node in linked list
        cursor = cursor -> next;
    }
    return false;
}

// Hashes word to a number
#define PI 3.1415926535897932384626433832795028
unsigned int hash(const char *word)
{
    // This hash function takes the sum of the ASCII characters in the word and multiplies by the value of pi
    long index = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        index += PI * toupper(word[i]);
    }
    return index % N;
}

// Loads dictionary into memory, returning true if successful, else false
int count = 0;
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    // Return false if file fails to open
    if (file == NULL)
    {
        return false;
    }
    // Create a buffer array to input data from file
    char buffer[LENGTH + 1];
    // Input word from file into buffer, transfer to node, transfer to linked list in hash table
    while (fscanf(file, "%s", buffer) != EOF)
    {
        // Allocate space for new node
        node *n = malloc(sizeof(node));
        // Return false if not enough memory
        if (n == NULL)
        {
            return false;
        }
        // Copy buffer to node
        strcpy(n -> word, buffer);
        n -> next = NULL;
        // Run word through hash function to get hash table index
        int i = hash(n -> word);
        // Fill in hash table with nodes expanding linked lists if necessary
        if (table[i] == NULL)
        {
            table[i] = n;
        }
        else
        {
            n -> next = table[i];
            table[i] = n;
        }
        // Count words
        count++;
    }
    // Close open file
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return numnber of words counted from load() function
    if (count != 0)
    {
        return count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Define nodes
    node *tmp, *cursor;
    // Loop through linked lists unloading memory
    for (int i = 0; i < N; i++)
    {
        // Point cursor to first word in linked list
        cursor = table[i];
        // Free memory until reach end of linked list
        while (cursor != NULL)
        {
            // Create another pointer at the linked list to prevent losing track of linked list elements
            tmp = cursor;
            // Move to next word in linked list
            cursor = cursor -> next;
            // Free memory
            free(tmp);
        }
    }
    if (cursor == NULL)
    {
        return true;
    }
    return false;
}
