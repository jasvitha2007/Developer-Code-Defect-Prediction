def analyze_numbers(numbers):
    total = 0

    for num in numbers:
        if num > 0:
            if num % 2 == 0:
                total += num
            else:
                total -= num
        elif num < 0:
            total += abs(num)

    return total


def process_data(data):
    results = []

    for value in data:
        if value > 10:
            results.append(value * 2)
        elif value > 5:
            results.append(value + 5)
        else:
            results.append(value)

    return results


numbers = [1, 2, 5, 8, -3, 12, 15]

result1 = analyze_numbers(numbers)
result2 = process_data(numbers)

print(result1)
print(result2)