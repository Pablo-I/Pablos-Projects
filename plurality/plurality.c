#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    //Loop that analyzes the entire candiate list. When candidate is found, the vote is added.
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes += 1;
            return true;
        }
    }

    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    string winner[MAX];
    int mostVotes = 0;

    //Loop that checks the candidate list to find the one(s) with the most votes
    int k = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes >= mostVotes)
        {
            //If the number of votes equals the mostVotes (tie), the the name is added to the winner array.
            if (candidates[i].votes == mostVotes)
            {
                winner[k] = candidates[i].name;
                k++;
            }
            //If the current number of votes exceeds the highest number previously recorded, the the winner array is reset with the new name added.
            else if (candidates[i].votes > mostVotes)
            {
                k = 0;
                mostVotes = candidates[i].votes;

                for (int z = 0; z < MAX; z++)
                {
                    winner[z] = " ";
                }

                winner[k] = candidates[i].name;
                k++;
            }
        }

    }

    //Print winner(s)
    int j = 0;
    while (strcmp(winner[j], " ") != 0)
    {
        printf("%s\n", winner[j]);
        j++;
    }

    return;
}