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

void merge_sort_pairs(int left, int right);
void merge_pairs(int left, int middle, int right);
bool pair_cycles(int winner, int loser);

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
    // TODO
    for (int i = 0, n = candidate_count; i < n; i++)
    {
        if (strcmp(candidates[i], name) == 0)
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
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            int prefer = ranks[i];
            int over = ranks[j];
            if (prefer == over)
            {
                preferences[prefer][over] = 0;
            }
            else
            {
                preferences[prefer][over]++;
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            int compare1 = preferences[i][j];
            int compare2 = preferences[j][i];
            if (compare1 > compare2)

            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else if (compare1 < compare2)
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    merge_sort_pairs(0, pair_count - 1);
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0, n = pair_count; i < n; i++)
    {
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;
        if (!pair_cycles(winner, loser))
        {
            locked[winner][loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    int i = 0;
    int j = 0;
    while (i < candidate_count)
    {
        bool isLocked = locked[j][i];
        if (j == candidate_count && !isLocked)
        {
            printf("%s\n", candidates[i]);
            break;
        }
        else if (!isLocked)
        {
            j++;
        }
        else
        {
            i++;
            j = 0;
        }
    }
    return;
}

// Do Merge Sort
void merge_sort_pairs(int left, int right)
{
    if (pair_count < 2)
    {
        return;
    }

    if (left < right)
    {
        // Do sorting
        int middle = left + (right - left) / 2;
        merge_sort_pairs(left, middle);
        merge_sort_pairs(middle + 1, right);
        merge_pairs(left, middle, right);
    }
    return;
}

// Sort the pairs
void merge_pairs(int left, int middle, int right)
{
    int i, j, k;
    int n1 = middle - left + 1;
    int n2 = right - middle;
    // Create temp arrays
    pair pairs_temp_L[n1], pairs_temp_R[n2];

    // Copy data to temp array
    for (i = 0; i < n1; i++)
    {
        pairs_temp_L[i].winner = pairs[left + i].winner;
        pairs_temp_L[i].loser = pairs[left + i].loser;
    }
    for (j = 0; j < n2; j++)
    {
        pairs_temp_R[j].winner = pairs[middle + 1 + j].winner;
        pairs_temp_R[j].loser = pairs[middle + 1 + j].loser;
    }

    i = 0; // Initial index of L array
    j = 0; // Initial index of R array
    k = left; // Initial index of merged array
    while (i < n1 && j < n2)
    {
        int winner_L = pairs_temp_L[i].winner;
        int loser_L = pairs_temp_L[i].loser;
        int winner_R = pairs_temp_R[j].winner;
        int loser_R = pairs_temp_R[j].loser;

        int strength_L = preferences[winner_L][loser_L] - preferences[loser_L][winner_L];
        int strength_R = preferences[winner_R][loser_R] - preferences[loser_R][winner_R];
        // Merge the temp arrays
        if (strength_L >= strength_R)
        {
            pairs[k].winner = winner_L;
            pairs[k].loser = loser_L;
            i++;
        }
        else
        {
            pairs[k].winner = winner_R;
            pairs[k].loser = loser_R;
            j++;
        }
        k++;
    }
    // Copy the remaining elements of L array
    while (i < n1)
    {
        pairs[k].winner = pairs_temp_L[i].winner;
        pairs[k].loser = pairs_temp_L[i].loser;
        i++;
        k++;
    }
    // Copy the remaining elements of R array
    while (j < n2)
    {
        pairs[k].winner = pairs_temp_R[j].winner;
        pairs[k].loser = pairs_temp_R[j].loser;
        j++;
        k++;
    }
    return;
}

bool pair_cycles(int winner, int loser)
{
    if (locked[loser][winner])
    {
        return true;
    }
    if (winner == loser)
    {
        return true;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loser][i])
        {
            if (pair_cycles(winner, i))
            {
                return true;
            }
        }
    }

    return false;
}