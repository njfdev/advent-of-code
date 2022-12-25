def snafuToDecimal(snafu):
    # snafu is a base-5 system where to only symbols are 0, 1, 2, - (minus) and = (double minus)

    value = 0

    # enumerate the symbols in reverse order
    for i, symbol in enumerate(snafu[::-1]):
        # convert the symbol to a number
        if symbol == "0":
            number = 0
        elif symbol == "1":
            number = 1
        elif symbol == "2":
            number = 2
        elif symbol == "-":
            number = -1
        elif symbol == "=":
            number = -2
        else:
            raise ValueError(f"Unknown symbol {symbol}")

        # add the number to the value
        value += number * 5 ** i
    
    return value

def decimalToSnafu(decimal):
    # snafu is a base-5 system where to only symbols are 0, 1, 2, - (minus) and = (double minus)
    # just like converting from decimal to binary, we can do this by repeatedly dividing by 5
    # if the remainder is greater than 2, we assign 1 to the the place about the remainder and subtract 5 from the remainder
    decimal = int(decimal)
    snafu = ""

    while decimal != 0:
        remainder = decimal % 5
        decimal = decimal // 5

        if remainder > 2:
            remainder -= 5
            decimal += 1

        if remainder == 0:
            snafu = "0" + snafu
        elif remainder == 1:
            snafu = "1" + snafu
        elif remainder == 2:
            snafu = "2" + snafu
        elif remainder == -1:
            snafu = "-" + snafu
        elif remainder == -2:
            snafu = "=" + snafu
        else:
            raise ValueError(f"Unknown remainder {remainder}")
    
    return snafu

# read in snafu-numbers.txt as a list of strings
with open("snafu-numbers.txt") as f:
    snafus = f.read().splitlines()

# convert the snafu numbers to decimal and add them together
total = 0
for snafu in snafus:
    total += snafuToDecimal(snafu)

# convert the total to snafu
print(decimalToSnafu(total))