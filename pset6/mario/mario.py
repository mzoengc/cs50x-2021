from cs50 import get_int


def main():
    # Prompt for Height
    while True:
        height = get_int("Height: ")
        if (height > 0 and height < 9):
            break

    # Print
    for i in range(height):
        print(" " * (height - i - 1), end='')
        print("#" * (i + 1), end='')
        print("  ", end='')
        print("#" * (i + 1))


if __name__ == "__main__":
    main()
