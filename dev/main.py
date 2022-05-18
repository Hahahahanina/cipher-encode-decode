import argparse
import string


def parse():

    parser = argparse.ArgumentParser()

    parser.add_argument("mode")
    parser.add_argument("--cipher")
    parser.add_argument("--key")
    parser.add_argument("--input-file")
    parser.add_argument("--output-file")
    parser.add_argument("--model-file")
    parser.add_argument("--text-file")

    args = parser.parse_args()

    return args


def make_shift_dict(letters, shift):
    mod = len(letters)
    shift_letters = dict()
    for i in range(len(letters)):
        shift_letters[letters[i]] = letters[(i + shift + mod) % mod]

    return shift_letters


def make_reverse_shift_dict(letters, shift):
    mod = len(letters)
    reverse_shift_letters = dict()
    for i in range(len(letters)):
        reverse_shift_letters[letters[(i + shift + mod) % mod]] = letters[i]

    return reverse_shift_letters


def caesar_encode(text, shift):

    shift_lower = make_shift_dict(string.ascii_lowercase, shift)
    shift_upper = make_shift_dict(string.ascii_uppercase, shift)

    new_text = list(['' for i in range(len(text))])
    for i in range(len(text)):
        symbol = text[i]
        if symbol.isalpha():
            if symbol.islower():
                new_text[i] = shift_lower[symbol]
            else:
                new_text[i] = shift_upper[symbol]

        else:
            new_text[i] = symbol
    new_text = ''.join(new_text)
    return new_text


def make_vigenere_table(letters):
    vigenere_table = dict()
    for i in range(len(letters)):
        vigenere_table[letters[i]] = make_shift_dict(letters, i)

    return vigenere_table


def make_reverse_vigenere_table(letters):
    reverse_vigenere_table = dict()
    for i in range(len(letters)):
        reverse_vigenere_table[letters[i]] = make_reverse_shift_dict(letters, i)

    return reverse_vigenere_table


def vigenere_encode(text, code_word):
    code = (code_word * len(text))[:len(text)]

    lower_vigenere_table = make_vigenere_table(string.ascii_lowercase)
    upper_vigenere_table = make_vigenere_table(string.ascii_uppercase)

    new_text = list(['' for i in range(len(text))])

    for i in range(len(text)):
        symbol = text[i]
        code_symbol = code[i]
        if symbol.isalpha():
            if symbol.islower():
                new_text[i] = lower_vigenere_table[symbol][code_symbol]
            else:
                new_text[i] = upper_vigenere_table[symbol][code_symbol.upper()]
        else:
            new_text[i] = symbol

    new_text = ''.join(new_text)
    return new_text


def vigenere_decode(text, code_word):
    code = (code_word * len(text))[:len(text)]

    lower_reverse_vigenere_table = make_reverse_vigenere_table(string.ascii_lowercase)
    upper_reverse_vigenere_table = make_reverse_vigenere_table(string.ascii_uppercase)

    new_text = list(['' for i in range(len(text))])

    for i in range(len(text)):
        symbol = text[i]
        code_symbol = code[i]
        if symbol.isalpha():
            if symbol.islower():
                new_text[i] = lower_reverse_vigenere_table[code_symbol][symbol]
            else:
                new_text[i] = upper_reverse_vigenere_table[code_symbol.upper()][symbol]
        else:
            new_text[i] = symbol

    new_text = ''.join(new_text)
    return new_text


def xor(code, sym):
    code_s = bin(ord(code))[2:]
    sym_s = bin(ord(sym))[2:]
    if len(sym_s) > len(code_s):
        code_s = '0' * (len(sym_s) - len(code_s)) + code_s
    else:
        sym_s = '0' * (len(code_s) - len(sym_s)) + sym_s

    s = ''
    for i in range(len(sym_s)):
        s += str((int(sym_s[i]) + int(code_s[i])) % 2)
    s = '0b' + s
    return chr(int(s, 2))


def vernam_encode(text, code_word):
    code = (code_word * len(text))[:len(text)]

    new_text = list(['' for i in range(len(text))])
    for i in range(len(text)):
        new_text[i] = xor(code[i], text[i])

    new_text = ''.join(new_text)
    return new_text


def encode(args):
    if args.input_file:
        with open(args.input_file) as file:
            text = file.read()
    else:
        text = str(input())

    if args.cipher == "caesar":
        new_text = caesar_encode(text, int(args.key))
    elif args.cipher == "vigenere":
        new_text = vigenere_encode(text, str(args.key))
    elif args.cipher == "vernam":
        new_text = vernam_encode(text, str(args.key))

    if args.output_file:
        with open(args.output_file, 'w') as file:
            file.write(new_text)
    else:
        print(new_text)


def decode(args):
    if args.input_file:
        with open(args.input_file) as file:
            text = file.read()
    else:
        text = str(input())

    if args.cipher == "caesar":
        new_text = caesar_encode(text, -int(args.key))
    elif args.cipher == "vigenere":
        new_text = vigenere_decode(text, str(args.key))
    elif args.cipher == "vernam":
        new_text = vernam_encode(text, str(args.key))

    if args.output_file:
        with open(args.output_file, 'w') as file:
            file.write(new_text)
    else:
        print(new_text)


def make_frequency_dict(text):
    letters = string.ascii_lowercase
    frequency_dict = dict()

    for i in range(len(letters)):
        frequency_dict[letters[i]] = 0

    for i in range(len(text)):
        if text[i].isalpha():
            frequency_dict[text[i].lower()] += 1

    for i in range(len(letters)):
        frequency_dict[letters[i].lower()] /= len(text)

    return frequency_dict


def train(args):
    if args.text_file:
        with open(args.text_file) as file:
            text = file.read()
    else:
        text = str(input())

    frequency_dict = make_frequency_dict(text)

    with open(args.model_file, 'w') as file:
        for key in frequency_dict:
            print(frequency_dict[key], end=' ', file=file)


def calculate_approximation_index(values, model_values):
    index = 0
    for i in range(len(values)):
        index += abs(values[i] - model_values[i])

    return index


def read_model_values(file_name):
    with open(file_name) as file:
        values = list(map(float, file.readline().split()))

    return values


def make_list_from_dict(d):
    values = []
    for key in d:
        values.append(d[key])
    return values


def choose_shift(text, model_file):
    model_frequencies = read_model_values(model_file)

    inf = 1e10
    min_index = inf
    shift = -1
    for i in range(len(model_frequencies)):
        new_text = caesar_encode(text, i)
        current_frequency_dict = make_frequency_dict(new_text)
        current_frequency_list = make_list_from_dict(current_frequency_dict)
        current_index = calculate_approximation_index(current_frequency_list, model_frequencies)

        if current_index < min_index:
            min_index = current_index
            shift = i

    return shift


def hack(args):
    if args.input_file:
        with open(args.input_file) as file:
            text = file.read()
    else:
        text = str(input())

    shift = choose_shift(text, args.model_file)
    new_text = caesar_encode(text, shift)

    if args.output_file:
        with open(args.output_file, 'w') as file:
            file.write(new_text)
    else:
        print(new_text)


def main():

    args = parse()

    if args.mode == "encode":
        encode(args)
    elif args.mode == "decode":
        decode(args)
    elif args.mode == "train":
        train(args)
    elif args.mode == "hack":
        hack(args)


main()
