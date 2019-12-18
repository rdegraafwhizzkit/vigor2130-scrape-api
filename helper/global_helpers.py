import pandas as pd
import time


def get_joined_data(vigor_2130, velop=None):
    """Get a summary of the state of clients connected to the Vigor modem.

    Args:
        vigor_2130 (Vigor2130): A Vigor2130 object
        velop: QQQ

    Returns:
        iterable: An array with the client state

    """
    # Load the dhcp table into a pandas dataframe
    df_dhcp_table = pd.DataFrame(vigor_2130.get_dhcp_leases())

    # Load the mac to ip bind table into a pandas dataframe
    df_mac_ip = pd.DataFrame([x for x in vigor_2130.get_mac_ip_bind()])

    # Load the detailed data flow into a pandas dataframe
    df_dataflow = pd.DataFrame(vigor_2130.get_detailed_dataflow())

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


def dict_path_value(d, path, default=None):
    """Get a value in a dict using a dot separated path to the key.

    Args:
        d (dict): The dict to search in
        path (str): The dot separated path to traverse
        default (object): The default value to return if the path could not be traversed

    Returns:
        any : The value for the requested key, if present

    """
    steps = path.split('.')
    for i, step in enumerate(steps):
        d = d.get(step, default) if i == len(steps) - 1 else d.get(step, {})
    return d
