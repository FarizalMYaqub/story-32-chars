"""Tell a Whole Story in 32 Characters — entry program.

The entry is one Wi-Fi network name: a breakup told in seven
words. She left, she took the dog, and she took the Wi-Fi too —
listed as a prize possession beside the dog. The name itself is
the stolen network, so the joke is self-referential: the reader
is staring at the very Wi-Fi she took. Character, situation and
event all fit in 23 characters, and nothing is wasted.

This program writes that name to /output/entry.txt and does
nothing else. The name is a literal in this file, so the judge
reads the same bytes on every run: no network, no randomness,
no files read.
"""

import os
import sys

NAME = "SheTookTheDogAndTheWiFi"

LIMIT = 32

OUTPUT = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def validate(text):
    """Check the name against the gate the sealed scorer applies:
    UTF-8 text, 1 to 32 characters, not only white space, exactly
    one line. Returns the character count or exits explaining why
    the name fails."""
    if text != text.strip():
        sys.exit("name has leading or trailing whitespace")
    if not text:
        sys.exit("name is blank")
    if "\n" in text or "\r" in text:
        sys.exit("name must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        sys.exit("name contains a control character")
    count = len(text)
    if count > LIMIT:
        sys.exit("name is %d chars, limit is %d" % (count, LIMIT))
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        sys.exit("name is not valid UTF-8")
    return count


def publish(text, path):
    """Write the name to path through a staging file beside it and
    an atomic rename, then read it back and insist it matches the
    name exactly, byte for byte."""
    count = validate(text)
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    staging = path + ".staging"
    with open(staging, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.replace(staging, path)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        landed = handle.read()
    if landed != text:
        sys.exit("entry on disk is not the name")
    if len(landed.encode("utf-8")) != len(text.encode("utf-8")):
        sys.exit("entry on disk is not the name, byte for byte")
    return count


def main():
    count = publish(NAME, OUTPUT)
    print("Name published: %d chars, 1 line -> %s" % (count, OUTPUT))


if __name__ == "__main__":
    main()
