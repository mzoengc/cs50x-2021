#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

bool is_sentence_char(char);
int count_letters(string);
int count_words(string);
int count_sentences(string);
int cal_readability(int letters, int words, int sentences);

int main(void)
{
    // Get input texts
    string text = get_string("Text: ");

    // Get number of letters
    int letters = count_letters(text);
    printf("%i letter%s\n", letters, letters > 1 ? "(s)" : "");

    // Get number of words
    int words = count_words(text);
    printf("%i word%s\n", words, words > 1 ? "(s)" : "");

    // Get number of sentences
    int sentences = count_sentences(text);
    printf("%i sentence%s\n", sentences, sentences > 1 ? "(s)" : "");

    // Get Coleman-Liau index
    int index = cal_readability(letters, words, sentences);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    // number of letters in the text.
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];
        // uppercase or lowercase alphabetic characters
        if (isalpha(c))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    // number of words in the text.
    int words = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];
        char c2 = text[i + 1];
        // characters separated by a space to be a word
        if (isspace(c) || (!isspace(c2) && is_sentence_char(c)))
        {
            words++;
        }
    }
    return words;
}

int count_sentences(string text)
{
    // number of sentences in the text.
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];
        if (is_sentence_char(c))
        {
            sentences++;
        }
    }
    return sentences;
}

int cal_readability(int letters, int words, int sentences)
{
    float per_100_words = words / 100.0f;

    // L is the average number of letters per 100 words in the text
    float L = letters / per_100_words;

    // S is the average number of sentences per 100 words in the text
    float S = sentences / per_100_words;

    // Coleman-Liau index Formula
    float index = 0.0588 * L - 0.296 * S - 15.8;
    return round(index);
}

bool is_sentence_char(char c)
{
    // characters that ends with a . or a ! or a ? to be a sentence
    return c == '.' || c == '?' || c == '!';
}