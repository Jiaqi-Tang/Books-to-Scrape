def price_to_decimal(price):
    price = price.replace('£', '').strip()
    price = price.replace('$', '').strip()

    price_decimal = float(price)
    return price_decimal


def availability_breakdown(availability):
    in_stock = 'In stock' in availability

    if in_stock:
        start = availability.find('(') + 1
        end = availability.find('available')
        num_available = int(availability[start:end].strip())
    else:
        num_available = 0  # Set to 0 if not in stock

    return in_stock, num_available


def word_to_int(word):
    int_dict = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
    }
    word = word.lower()
    return int_dict.get(word, None)