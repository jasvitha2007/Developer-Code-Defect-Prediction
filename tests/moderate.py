def calculate(numbers):
    total = 0

    for number in numbers:
        if number > 0:
            total += number
        else:
            total -= number

    return total


values = [10, -5, 20, -3]
print(calculate(values))