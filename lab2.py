import curses

text = """Hello world!
This is a tiny text editor.
Edit me!"""

cursor = 0

def findLastNL(c):

    while c > 0 and (c >= len(text) or text[c] != "\n"):
        c -= 1
    
    return c

def findNextNL(c):

    while c < len(text) and text[c] != "\n":
        c += 1
    
    return c

def draw(screen):
    screen.clear()

    # ==========================================================
    # INITIALIZE THE DISPLAY
    #
    # Display the document with the cursor at the current
    # cursor position.
    #
    # Example
    #
    # text    = "Hello"
    # cursor  = 0
    #
    # display = "|Hello"
    #
    # ---------------- TODO ----------------

    if cursor < 0:
        raise ValueError("The provided number must be nonnegative.")
    display = text[:cursor] + "|" + text[cursor:]
    

    # ----------------------------------------

    for row, line in enumerate(display.split("\n")):
        screen.addstr(row, 0, line)

    screen.addstr(
        len(display.split("\n")) + 1,
        0,
        "← → Move   Type Insert   Backspace Delete   Enter New Line   Esc Quit"
    )

    screen.refresh()


def main(screen):
    global text, cursor

    while True:
        draw(screen)

        key = screen.getch()

        if key == 27:
            break

        # ==========================================================
        # LEFT ARROW
        #
        # Move the cursor one position to the left.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # After
        # text    = "Hello"
        # cursor  = 2
        # display = "He|llo"
        #
        # ---------------- ANSWER ----------------

        elif key == curses.KEY_LEFT:

            if cursor > 0:
                cursor -= 1

            

        # ----------------------------------------

        # ==========================================================
        # RIGHT ARROW
        #
        # Move the cursor one position to the right.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # After
        # text    = "Hello"
        # cursor  = 4
        # display = "Hell|o"
        #
        # ---------------- ANSWER ----------------

        elif key == curses.KEY_RIGHT:

            if cursor < len(text):
                cursor += 1


        # ----------------------------------------

        # ==========================================================
        # BACKSPACE
        #
        # Delete the character immediately before the cursor.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # After
        # text    = "Helo"
        # cursor  = 2
        # display = "He|lo"
        #
        # ---------------- ANSWER ----------------

        elif key in (8, 127, curses.KEY_BACKSPACE):

            if cursor > 0:
                text = text[:cursor-1] + text[cursor:]
                cursor -= 1

        # ----------------------------------------

        # ==========================================================
        # ENTER
        #
        # Insert a newline at the cursor.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # After
        # text    = "Hel\nlo"
        # cursor  = 4
        # display = "Hel\n|lo"
        #
        # ---------------- ANSWER ----------------

        elif key == 10:

            text = text[:cursor] + "\n" + text[cursor:]
            cursor += 1


        # ----------------------------------------

        # ==========================================================
        # INSERT CHARACTER
        #
        # Insert the typed character at the cursor.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # Typing X
        #
        # After
        # text    = "HelXlo"
        # cursor  = 4
        # display = "HelX|lo"
        #
        # ---------------- ANSWER ----------------

        elif 32 <= key <= 126:

            text = text[:cursor] + chr(key) + text[cursor:]
            cursor += 1


        # ----------------------------------------

        #BONUS: Can you figure out how to select one line up/down by yourself?

        elif key == curses.KEY_UP:
        

            # words = text.split("\n")
            # lineCounts = [len(word) for word in words]
            # currentLine = 0
            # charCount = 0
            # for count in lineCounts:
            #     charCount += count
            #     if charCount >= cursor:
            #         break
            #     currentLine += 1

            # if currentLine == 0:
            #     cursor = 0
            # else:
            #     prevCharCount = charCount - lineCounts[currentLine]
            #     overhang = cursor - prevCharCount - lineCounts[currentLine-1]
            #     if overhang < 0:
            #         cursor -= overhang
            #     cursor = cursor - lineCounts[currentLine-1] - 1
            if cursor >= len(text) or text[cursor] == '\n':
                    if text[cursor-1] == text[cursor-2] == '\n':
                        cursor -= 1
                        continue
            lastNL = findLastNL(cursor)
            if lastNL <= 0:
                cursor = 0
            else:
                
                charsToRight = cursor - lastNL - 1
                lastLast = findLastNL(lastNL - 1)
                lastLineLen = lastNL - lastLast
                if charsToRight > lastLineLen:
                    charsToRight = lastLineLen-1
                
                cursor = lastLast + charsToRight + 1
                if (lastLast == 0 and charsToRight > lastLineLen):
                    cursor -= 1
                
            

        elif key == curses.KEY_DOWN:

            # words = text.split("\n")
            # lineCounts = [len(word) for word in words]
            # currentLine = 0
            # charCount = 0
            # for count in lineCounts:
            #     currentLine += 1
            #     charCount += count
            #     if charCount >= cursor:
            #         break

            # if currentLine == len(lineCounts):
            #     cursor = len(text)
            # else:
            #     cursor = cursor + lineCounts[currentLine-1]+1
            #     if cursor > len(text):
            #         cursor = len(text)-1
            if cursor >= len(text) or text[cursor] == '\n':
                    cursor -= 1
                    if text[cursor] == '\n':
                        cursor += 2
                        continue
            lastNL = findLastNL(cursor)
            nextNL = findNextNL(cursor)
            if nextNL == len(text)-1:
                cursor = len(text)-1
            else:
                
                charsToRight = cursor - lastNL - 1
                if lastNL == 0:
                    charsToRight += 1
                nextNext = findNextNL(nextNL+1)
                nextLineLen = nextNext - nextNL
                if charsToRight > nextLineLen:
                    charsToRight = nextLineLen-1
                
                cursor = nextNL + charsToRight + 1


curses.wrapper(main)
