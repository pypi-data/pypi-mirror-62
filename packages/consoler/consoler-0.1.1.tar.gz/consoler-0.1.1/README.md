## Consoler

A terminal printer that's totally tailored to how I like terminal printouts. If this happens to also be how you like terminal printouts, this package may well be for you too.

### Installing

`poetry add consoler` or `pip install consoler`

### Usage

    from consoler import console
    console.log("This is a log level print out")
    console.info("This is an info level print out")
    console.warn("This is a warning level print out")

    try:
        1 / 0
    except Exception as e:
        console.error("Oh no!", e)

