import sys

def replace_non_ascii(text: str) -> str:
    """Replaces all non-ASCII characters in the input text with an underscore (_)."""
    return ''.join(char if ord(char) < 128 else '_' for char in text)

def main() -> None:
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python replace_non_ascii.py \"input_text\"")
        return

    input_text = sys.argv[1]
    cleaned_text = replace_non_ascii(input_text)
    print(cleaned_text)

if __name__ == "__main__":
    main()