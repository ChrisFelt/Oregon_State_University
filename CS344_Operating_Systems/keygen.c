// Title: keygen
// Author: Christopher Felt
// Class: CS 344 OS1
// Description: Given an integer argument, generates a string of randomized
//              capital letters and/or spaces with a length equal to the integer. 
//              Includes all capital letters A-Z and space. The resulting string 
//              terminates with \n.


#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

// array of the 27 allowed characters for the keygen
static char const allowed_chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";


int main(int argc, const char *argv[]) {

    // error message if single integer not passed as argument
    if (argc != 2) {
        fprintf(stderr, "Usage: input one integer.\n");
        return 1;
    }
    // need to call srand in order to use rand - srand takes a seed value
    // we will use a changing seed for random number generation 
    // time function returns the time in seconds since the Unix epoch (1/1/1970)
    srand(time(NULL));

    // cast argument as an integer 
    // the user COULD pass a string or something weird, but we won't error check
    // NOTE: if a string is passed, num_chars will be 0
    int num_chars = atoi(argv[1]);

    // create buffer of size num_chars + 2 (for \n and \0 at end of string)
    char output[num_chars + 2];

    // zero out output. using sizeof() guarantees we do not exceed the buffer
    memset(output, '\0', sizeof(output));

    int i;

    // initialize random number int
    int rand_pick;

    // iterate through output and generate a random letter or space for each index
    for (i = 0; i < num_chars; ++i) {
        // rand() % 27 returns an integer [0, 26].
        rand_pick = rand() % 27;

        // for debugging purposes, make sure rand_pick falls in the number range
        if (rand_pick < 0 || rand_pick > 26) {
            fprintf(stderr, "Error: randomized number falls outside of [0, 26]!");
        }

        output[i] = allowed_chars[rand_pick];

    }

    // append a newline to output
    // null terminator already exists at end of string, so no need to add it
    output[i] = '\n';

    // hey ho let's go
    printf("%s", output);

    return 0;
}