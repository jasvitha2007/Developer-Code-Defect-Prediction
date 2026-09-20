def calculate_total(a, b):
    if a > b:
        return a + b
    else:
        return a - b


def process_numbers(numbers):
    total = 0

    for number in numbers:
        if number > 0:
            total += number
        else:
            total -= number

    return total