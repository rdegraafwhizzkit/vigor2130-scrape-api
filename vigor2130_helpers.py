def encode(input_string):
    lookup_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    output_string = ""

    i = 0

    while True:
        chr1 = ord(input_string[i]) if i < len(input_string) else None
        i = i + 1

        chr2 = ord(input_string[i]) if i < len(input_string) else None
        i = i + 1

        chr3 = ord(input_string[i]) if i < len(input_string) else None
        i = i + 1

        enc1 = chr1 >> 2 if chr1 is not None else 0
        enc2 = (((chr1 if chr1 is not None else 0) & 3) << 4) | (chr2 >> 4 if chr2 is not None else 0)
        if chr2 is None:
            enc3 = enc4 = 64
        elif chr3 is None:
            enc3 = ((chr2 & 15) << 2)
            enc4 = 64
        else:
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
            enc4 = chr3 & 63

        output_string = output_string + lookup_table[enc1] + lookup_table[enc2] + lookup_table[enc3] + lookup_table[
            enc4]

        if i >= len(input_string):
            break

    return output_string
