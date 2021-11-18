from cs50 import get_string
import re


def main():
    # Prompt
    text = get_string("Text: ")

    # number of letters. words and sentences
    letters = len(re.findall('[a-zA-Z]', text))
    words = len(text.split())
    sentences = len(re.findall(r'[.!?]', text))

    print(f"{letters} letters")
    print(f"{words} words")
    print(f"{sentences} sentences")

    # Get Coleman-Liau index
    index = cal_readability(letters, words, sentences)

    # Print
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def cal_readability(letters, words, sentences):
    per_100_words = words / 100.0

    # L is the average number of letters per 100 words in the text
    L = letters / per_100_words

    # S is the average number of sentences per 100 words in the text
    S = sentences / per_100_words

    # Coleman-Liau index Formula
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)


if __name__ == "__main__":
    main()
