def encode(input_string):
    lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    output_string = ""

    i = 0

    while True:
        chr1 = ord(input_string[i]) if i < len(input_string) else 0
        chr2 = ord(input_string[i + 1]) if i < len(input_string) - 1 else 0
        chr3 = ord(input_string[i + 2]) if i < len(input_string) - 2 else 0

        enc1 = chr1 >> 2
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
        if chr2 == 0:
            enc3 = enc4 = 64
        elif chr3 == 0:
            enc3 = ((chr2 & 15) << 2)
            enc4 = 64
        else:
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
            enc4 = chr3 & 63

        output_string = f'{output_string}{lookup[enc1]}{lookup[enc2]}{lookup[enc3]}{lookup[enc4]}'

        i = i + 3
        if i >= len(input_string):
            break

    return output_string
