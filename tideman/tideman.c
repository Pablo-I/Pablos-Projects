#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool check_cycle(int Winner, int Loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    //For the entire candidate list, loop checks if name is valid. If it is, then that name's rank is stored in ranks. Name is placed in the correspinding rank.
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    int higherRank;
    int lowerRank;

    //The following two for loops update the preferences array. The first loop corresponds to the row while the second one corresponds to the column.
    //Each row and column represents a candidate. If the rank of the candidate on specific row is greater than the rank of the candidate on a specific column, then one voter perfers the row candidate over the column candidate.
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            higherRank = ranks[i];
            lowerRank = ranks[j];

            preferences[higherRank][lowerRank] += 1;
        }
    }

    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    int paircount;
    int existingPair = 0;

    //The two for loops compare pairs of candidates based on the preferences array. First loop = row candidate, second loop = column candidate.
    paircount = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            //Check to see if row candidate is better than column candidate.
            if (preferences[i][j] > preferences[j][i])
            {
                //Check to see if the current pair has been previously recorded.
                for (int z = 0; z <= paircount; z++)
                {
                    if ((pairs[z].winner == i && pairs[z].loser == j) || (pairs[z].winner == j && pairs[z].loser == i))
                    {
                        existingPair = 1;
                    }
                }

                //If the pair being analyzed has not yet been recorded, record it.
                if (existingPair != 1)
                {
                    pairs[paircount].winner = i;
                    pairs[paircount].loser = j;
                    paircount++;
                    pair_count += 1;
                }
            }
            //Check if row candidate is worse than column candidate.
            else if (preferences[i][j] < preferences[j][i])
            {
                for (int z = 0; z <= paircount; z++)
                {
                    if ((pairs[z].winner == i && pairs[z].loser == j) || (pairs[z].winner == j && pairs[z].loser == i))
                    {
                        existingPair = 1;
                    }
                }

                if (existingPair != 1)
                {
                    pairs[paircount].winner = j;
                    pairs[paircount].loser = i;
                    paircount++;
                    pair_count += 1;
                }

            }

            existingPair = 0;
        }
    }

    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int paircount = pair_count - 1;
    int timesSwapped = -1;
    int diff1;
    int diff2;
    pair temp;

    //Loops until no items are swapped within the array (fully sorted)
    while (timesSwapped != 0)
    {
        //For the entire pairs array, the loop checks adjacent pairs. If the difference in the right-most pair is larger, then swap adjacent pairs.
        timesSwapped = 0;
        for (int i = 0; i < paircount; i++)
        {
            diff1 = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];
            diff2 = preferences[pairs[i + 1].winner][pairs[i + 1].loser] - preferences[pairs[i + 1].loser][pairs[i + 1].winner];

            if (diff2 > diff1)
            {
                temp = pairs[i];
                pairs[i] = pairs[i + 1];
                pairs[i + 1] = temp;
                timesSwapped++;
            }
        }

    }

    return;
}

//Check to see if a cycle is formed
bool check_cycle(int Winner, int Loser)
{
    int linkFound = 0;

    do
    {
        linkFound = 0;
        for (int i = 0; i < pair_count; i++)
        {
            if (pairs[i].loser == Winner)
            {
                Winner = pairs[i].winner;
                linkFound = 1;
            }

            if (Winner == Loser)
            {
                return true;
            }
        }

    }
    while (linkFound == 1);

    return false;
}


// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < pair_count; j++)
        {
            if (pairs[j].winner == i)
            {
                if (!check_cycle(pairs[j].winner, pairs[j].loser))
                {
                    locked[i][pairs[j].loser] = true;
                }
            }
        }
    }
    return;
}


// Print the winner of the election
void print_winner(void)
{
    bool col;

    for (int i = 0; i < candidate_count; i++)
    {
        //establish a fresh column check
        col = true;

        for (int j = 0; j < candidate_count; j++)
        {
            //if j candiate beats i, i is not our root and thus col is false
            if (locked[j][i] == true)
            {
                col = false;
            }
        }
        //when no nodes point to a node, that node is our root and winner
        if (col == true)
        {
            printf("%s\n", candidates[i]);
        }
    }
    return;
}
