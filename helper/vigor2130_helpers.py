import pandas as pd
import time


class LoginException(Exception):
    """Exception that is thrown when wrong credentials have been provided

    """
    pass


class UnknownStatusException(Exception):
    """Exception that is thrown when an unknown status has been return from a requests call

    """
    pass


class NotLoggedInException(Exception):
    """Exception that is thrown when a requests call has been made without being authenticated

    """

    pass


def encode(unencoded):
    """Encoding function for the username and password.

    This is an implementation of the Base64 encoding with some minor
    quirks, like input '' returns 'AA==' while Base64 returns '' in that case. It is a Python implementation for the
    encode function found in index.htm on the modem

    Args:
        unencoded (str): unencoded string value

    Returns:
        str: The 'Base64' encoded string value

    """
    lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    encoded = ""

    i = 0

    while True:
        chr0 = ord(unencoded[i]) if i < len(unencoded) else 0
        chr1 = ord(unencoded[i + 1]) if i < len(unencoded) - 1 else 0
        chr2 = ord(unencoded[i + 2]) if i < len(unencoded) - 2 else 0

        enc1 = lookup[chr0 >> 2]
        enc2 = lookup[((chr0 & 3) << 4) | (chr1 >> 4)]
        if chr1 == 0:
            enc3 = enc4 = lookup[64]
        elif chr2 == 0:
            enc3 = lookup[((chr1 & 15) << 2)]
            enc4 = lookup[64]
        else:
            enc3 = lookup[((chr1 & 15) << 2) | (chr2 >> 6)]
            enc4 = lookup[chr2 & 63]

        encoded = f'{encoded}{enc1}{enc2}{enc3}{enc4}'

        i = i + 3
        if i >= len(unencoded):
            break

    return encoded


def get_info(vigor_2130, velop=None):
    """Get a summary of the state of clients connected to the Vigor modem.

    Args:
        vigor_2130 (Vigor2130): A Vigor2130 object
        velop: QQQ

    Returns:
        iterable: An array with the client state

    """
    # Load the dhcp table into a pandas dataframe
    df_dhcp_table = pd.DataFrame(vigor_2130.dhcp_table())

    # Load the mac to ip bind table into a pandas dataframe
    df_mac_ip = pd.DataFrame([x for x in vigor_2130.ip_bind_mac()])

    # Load the detailed data flow into a pandas dataframe
    df_dataflow = pd.DataFrame(vigor_2130.data_flow_monitor()['detailed'])

    # Load the velop info
    df_velop = pd.DataFrame(velop if velop is not None else [])

    # Outer join the dhcp table and mac to ip on mac address into a pandas dataframe
    df = pd.merge(df_dhcp_table, df_mac_ip, on="mac_address", how="outer")

    # Find a filled ip_address. Else if there is no lease we may run into merge trouble later
    df['ip_address'] = df.apply(
        lambda row: row.ip_address_x if pd.isna(row.ip_address_y) else row.ip_address_y,
        axis=1
    )

    # Outer join the dataflow
    df = pd.merge(df, df_dataflow, on='ip_address', how='outer')

    # Outer join the velop info
    df = pd.merge(df, df_velop, on='mac_address', how='outer')

    # Find the correct computer_name from the mac_ip table, if not found fill it from the dhcp table
    df['computer_name'] = df.apply(
        lambda row: row.computer_name_x if pd.isna(row.computer_name_y) else row.computer_name_y,
        axis=1
    )

    df['rx_rate_kbs'] = df.apply(
        lambda row: -1 if pd.isna(row.rx_rate_kbs) else row.rx_rate_kbs,
        axis=1
    )

    df['tx_rate_kbs'] = df.apply(
        lambda row: -1 if pd.isna(row.tx_rate_kbs) else row.tx_rate_kbs,
        axis=1
    )

    df['expire_minutes'] = df.apply(
        lambda row: -1 if pd.isna(row.expire_minutes) else row.expire_minutes,
        axis=1
    )

    # Drop unwanted columns
    df = df.drop(
        columns=['computer_name_x', 'computer_name_y', 'ip_address_x', 'ip_address_y']
    )

    # Fix missing data
    df['computer_name'] = df.apply(
        lambda row: 'unknown' if pd.isna(row.computer_name) else row.computer_name,
        axis=1
    )

    df['mac_address'] = df.apply(
        lambda row: 'unknown' if pd.isna(row.mac_address) else row.mac_address,
        axis=1
    )

    df['ip_address'] = df.apply(
        lambda row: 'unknown' if pd.isna(row.ip_address) else row.ip_address,
        axis=1
    )

    df['velop'] = df.apply(
        lambda row: 'unknown' if pd.isna(row.velop) else row.velop,
        axis=1
    )

    timestamp = int(time.time())
    df['timestamp'] = df.apply(
        lambda row: timestamp,
        axis=1
    )

    return [v for k, v in df.T.to_dict().items()]
