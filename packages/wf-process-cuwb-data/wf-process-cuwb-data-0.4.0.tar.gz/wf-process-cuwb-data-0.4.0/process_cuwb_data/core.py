from database_connection_honeycomb import DatabaseConnectionHoneycomb
from minimal_honeycomb import MinimalHoneycombClient
import pandas as pd
from pandas.io.json import json_normalize
import datetime
import logging
import os

logger = logging.getLogger(__name__)

# CUWB Data Protocol: Byte size for accelerometer values
ACCELEROMETER_BYTE_SIZE = 4

# CUWB Data Protocol: Maximum integer for each byte size
CUWB_DATA_MAX_INT = {
    1: 127,
    2: 32767,
    4: 2147483647
}

def fetch_cuwb_position_data(
    environment_name,
    start_time,
    end_time,
    read_chunk_size=2,
    device_type='UWBTAG',
    environment_assignment_info=False,
    entity_assignment_info=False
):
    df = fetch_cuwb_data(
        environment_name,
        start_time,
        end_time,
        read_chunk_size,
        device_type,
        environment_assignment_info,
        entity_assignment_info
    )
    df = extract_position_data(df)
    return df

def fetch_cuwb_accelerometer_data(
    environment_name,
    start_time,
    end_time,
    read_chunk_size=2,
    device_type='UWBTAG',
    environment_assignment_info=False,
    entity_assignment_info=False
):
    df = fetch_cuwb_data(
        environment_name,
        start_time,
        end_time,
        read_chunk_size,
        device_type,
        environment_assignment_info,
        entity_assignment_info
    )
    df = extract_accelerometer_data(df)
    return df

def fetch_cuwb_status_data(
    environment_name,
    start_time,
    end_time,
    read_chunk_size=2,
    device_type='UWBTAG',
    environment_assignment_info=False,
    entity_assignment_info=False
):
    df = fetch_cuwb_data(
        environment_name,
        start_time,
        end_time,
        read_chunk_size,
        device_type,
        environment_assignment_info,
        entity_assignment_info
    )
    df = extract_status_data(df)
    return df

def extract_position_data(
    df
):
    df = df.loc[df['type'] == 'position'].copy()
    df['x_meters'] = df['x']/1000.0
    df['y_meters'] = df['y']/1000.0
    df['z_meters'] = df['z']/1000.0
    df.drop(
        columns=[
            'type',
            'battery_percentage',
            'temperature',
            'scale',
            'x',
            'y',
            'z'
        ],
        inplace=True
    )
    return df

def extract_accelerometer_data(
    df
):
    df = df.loc[df['type'] == 'accelerometer'].copy()
    df['x_gs'] = df['x']*df['scale']/CUWB_DATA_MAX_INT[ACCELEROMETER_BYTE_SIZE]
    df['y_gs'] = df['y']*df['scale']/CUWB_DATA_MAX_INT[ACCELEROMETER_BYTE_SIZE]
    df['z_gs'] = df['z']*df['scale']/CUWB_DATA_MAX_INT[ACCELEROMETER_BYTE_SIZE]
    df.drop(
        columns=[
            'type',
            'battery_percentage',
            'temperature',
            'x',
            'y',
            'z',
            'scale',
            'anchor_count',
            'quality',
            'smoothing',

        ],
        inplace=True
    )
    return df

def extract_status_data(
    df
):
    df = df.loc[df['type'] == 'status'].copy()
    df.drop(
        columns=[
            'type',
            'x',
            'y',
            'z',
            'scale',
            'anchor_count',
            'quality',
            'smoothing',

        ],
        inplace=True
    )
    return df

def fetch_cuwb_data(
    environment_name,
    start_time,
    end_time,
    read_chunk_size=2,
    device_type='UWBTAG',
    environment_assignment_info=False,
    entity_assignment_info=False
):
    object_type_honeycomb = 'DEVICE'
    object_id_field_name_honeycomb ='device_type'
    object_ids=[device_type]
    dbc = DatabaseConnectionHoneycomb(
        environment_name_honeycomb = environment_name,
        time_series_database = True,
        object_database = True,
        object_type_honeycomb = object_type_honeycomb,
        object_id_field_name_honeycomb = object_id_field_name_honeycomb,
        read_chunk_size=read_chunk_size
    )
    data = dbc.fetch_data_object_time_series(
        start_time = start_time,
        end_time = end_time,
        object_ids = object_ids
    )
    df = pd.DataFrame(data)
    df.drop(
        columns = [
            'timestamp',
            'environment_name',
            'object_id',
            'memory',
            'flags',
            'minutes_remaining',
            'processor_usage',
            'network_time',
            'object_id_secondary'
        ],
        inplace=True
    )
    df.rename(
        columns = {
            'timestamp_secondary': 'timestamp',
            'serial_number': 'device_serial_number'
        },
        inplace=True
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df.dropna(subset=['timestamp'], inplace=True)
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    device_data = fetch_cuwb_tag_device_data(device_type=device_type)
    df = df.join(device_data.reset_index().set_index('device_serial_number'), on='device_serial_number')
    df = df.reindex(columns=[
        'type',
        'device_id',
        'device_part_number',
        'device_serial_number',
        'device_name',
        'device_tag_id',
        'device_mac_address',
        'battery_percentage',
        'temperature',
        'x',
        'y',
        'z',
        'scale',
        'anchor_count',
        'quality',
        'smoothing'
    ])
    if environment_assignment_info:
        df = add_environment_assignment_info(df)
    if entity_assignment_info:
        df = add_entity_assignment_info(df)
    return df

def fetch_cuwb_tag_device_data(
    device_type='UWBTAG'
):
    logger.info('Fetching CUWB tag device data')
    client = MinimalHoneycombClient()
    result = client.request(
        request_type="query",
        request_name='findDevices',
        arguments={
            'device_type': {
                'type': 'DeviceType',
                'value': device_type
            }
        },
        return_object = [
            {'data': [
                'device_id',
                'part_number',
                'serial_number',
                'name',
                'tag_id',
                'mac_address'
            ]}
        ]
    )
    logger.info('Found CUWB device data for {} devices'.format(len(result.get('data'))))
    df = pd.DataFrame(result.get('data'))
    df.rename(
        columns={
            'part_number': 'device_part_number',
            'serial_number': 'device_serial_number',
            'name': 'device_name',
            'tag_id': 'device_tag_id',
            'mac_address': 'device_mac_address'
        },
        inplace=True
    )
    df.set_index('device_id', inplace=True)
    return df

def add_environment_assignment_info(df):
    # Fetch environment assignment IDs (devices to environment)
    environment_assignments = fetch_cuwb_tag_assignments(
        assignment_field_name='assignments',
        assignment_id_field_name='assignment_id'
    )
    # Add environment assignment IDs to dataframe
    df = add_assignment_ids(
        df=df,
        assignments_dict=environment_assignments,
        lookup_field_name='device_id',
        assignment_field_name='assignment_id'
    )
    return df

def add_entity_assignment_info(df):
    # Fetch entity assignment IDs (trays and people to devices)
    entity_assignments = fetch_cuwb_tag_assignments(
        assignment_field_name='entity_assignments',
        assignment_id_field_name='entity_assignment_id'
    )
    # Add entity assignments IDs to dataframe
    df = add_assignment_ids(
        df=df,
        assignments_dict=entity_assignments,
        lookup_field_name='device_id',
        assignment_field_name='entity_assignment_id'
    )
    # Fetch entity info (tray and person info)
    entity_info = fetch_entity_info()
    # Add entity info to dataframe
    df = df.join(entity_info, on = 'entity_assignment_id')
    # Fetch material assignment IDs (trays to materials)
    material_assignments = fetch_material_assignments()
    # Add material assignment IDs to dataframe
    df = add_assignment_ids(
        df=df,
        assignments_dict=material_assignments,
        lookup_field_name='tray_id',
        assignment_field_name='material_assignment_id'
    )
    # Fetch material names
    material_names = fetch_material_names()
    # Add material names to dataframe
    df = df.join(material_names, on = 'material_assignment_id')
    return df

def fetch_cuwb_tag_assignments(
    device_type='UWBTAG',
    assignment_field_name='assignments',
    assignment_id_field_name='assignment_id'
):
    logger.info('Fetching CUWB tag assignment IDs for {}'.format(assignment_field_name))
    client = MinimalHoneycombClient()
    result = client.request(
        request_type="query",
        request_name='findDevices',
        arguments={
            'device_type': {
                'type': 'DeviceType',
                'value': device_type
            }
        },
        return_object = [
            {'data': [
                'device_id',
                {assignment_field_name: [
                    assignment_id_field_name,
                    'start',
                    'end',
                ]}
            ]}
        ]
    )
    logger.info('Found {} {}'.format(
        len(result.get('data')),
        assignment_field_name
    ))
    if len(result.get('data')) == 0:
        raise ValueError('No devices of type {} found'.format(device_type))
    assignments_dict = {device['device_id']: device[assignment_field_name] for device in result.get('data')}
    for device_id in assignments_dict.keys():
        num_assignments = len(assignments_dict[device_id])
        # Convert timestamp strings to Pandas datetime objects
        for assignment_index in range(num_assignments):
            assignments_dict[device_id][assignment_index]['start'] = pd.to_datetime(
                assignments_dict[device_id][assignment_index]['start'],
                utc=True
            )
            assignments_dict[device_id][assignment_index]['end'] = pd.to_datetime(
                assignments_dict[device_id][assignment_index]['end'],
                utc=True
            )
        # Sort assignment list by start time
        assignments_dict[device_id] = sorted(
            assignments_dict[device_id],
            key = lambda assignment: assignment['start']
        )
        # Check integrity of assignment list
        if num_assignments > 1:
            for assignment_index in range(1, num_assignments):
                if pd.isna(assignments_dict[device_id][assignment_index - 1]['end']):
                    raise ValueError('Assignment {} starts at {} but previous assignment for this device {} starts at {} and has no end time'.format(
                        assignments_dict[device_id][assignment_index][assignment_id_field_name],
                        assignments_dict[device_id][assignment_index]['start'],
                        assignments_dict[device_id][assignment_index - 1][assignment_id_field_name],
                        assignments_dict[device_id][assignment_index - 1]['start']
                    ))
                if assignments_dict[device_id][assignment_index]['start'] < assignments_dict[device_id][assignment_index - 1]['end']:
                    raise ValueError('Assignment {} starts at {} but previous assignment for this device {} starts at {} and ends at {}'.format(
                        assignments_dict[device_id][assignment_index][assignment_id_field_name],
                        assignments_dict[device_id][assignment_index]['start'],
                        assignments_dict[device_id][assignment_index - 1][assignment_id_field_name],
                        assignments_dict[device_id][assignment_index - 1]['start'],
                        assignments_dict[device_id][assignment_index - 1]['end']
                    ))
    return assignments_dict

def add_assignment_ids(
    df,
    assignments_dict,
    lookup_field_name='device_id',
    assignment_field_name='assignment_id'
):
    df = df.copy()
    df[assignment_field_name] = None
    for lookup_value, assignments in assignments_dict.items():
        if len(assignments) > 0:
            lookup_boolean = (df[lookup_field_name] == lookup_value)
            for assignment in assignments:
                if pd.isnull(assignment['start']):
                    start_boolean = True
                else:
                    start_boolean = (df.index > assignment['start'])
                if pd.isnull(assignment['end']):
                    end_boolean = True
                else:
                    end_boolean = (df.index < assignment['end'])
                df.loc[
                    lookup_boolean & start_boolean & end_boolean,
                    assignment_field_name
                ] = assignment[assignment_field_name]
    return df

def fetch_tray_ids():
    logger.info('Fetching entity assignment info to extract tray IDs')
    client = MinimalHoneycombClient()
    result = client.request(
        request_type="query",
        request_name='entityAssignments',
        arguments=None,
        return_object = [
            {'data': [
                'entity_assignment_id',
                {'entity': [
                    {'... on Tray': [
                        'tray_id'
                    ]}
                ]}
            ]}
        ]
    )
    df = json_normalize(result.get('data'))
    df.rename(
        columns={
            'entity.tray_id': 'tray_id',
        },
        inplace=True
    )
    logger.info('Found {} entity assignments for trays'.format(df['tray_id'].notna().sum()))
    df.set_index('entity_assignment_id', inplace=True)
    return df

def fetch_material_assignments(
):
    logger.info('Fetching material assignment IDs')
    client = MinimalHoneycombClient()
    result = client.request(
        request_type="query",
        request_name='materialAssignments',
        arguments=None,
        return_object = [
            {'data': [
                'material_assignment_id',
                {'tray': [
                    'tray_id'
                ]},
                'start',
                'end'
            ]}
        ]
    )
    if len(result.get('data')) == 0:
        raise ValueError('No material assignments found')
    logger.info('Found {} material assignments'.format(len(result.get('data'))))
    assignments_dict = dict()
    for material_assignment in result.get('data'):
        tray_id = material_assignment['tray']['tray_id']
        assignment = {
            'material_assignment_id': material_assignment['material_assignment_id'],
            'start': material_assignment['start'],
            'end': material_assignment['end']
        }
        if tray_id in assignments_dict.keys():
            assignments_dict[tray_id].append(assignment)
        else:
            assignments_dict[tray_id] = [assignment]
    for tray_id in assignments_dict.keys():
        num_assignments = len(assignments_dict[tray_id])
        # Convert timestamp strings to Pandas datetime objects
        for assignment_index in range(num_assignments):
            assignments_dict[tray_id][assignment_index]['start'] = pd.to_datetime(
                assignments_dict[tray_id][assignment_index]['start'],
                utc=True
            )
            assignments_dict[tray_id][assignment_index]['end'] = pd.to_datetime(
                assignments_dict[tray_id][assignment_index]['end'],
                utc=True
            )
        # Sort assignment list by start time
        assignments_dict[tray_id] = sorted(
            assignments_dict[tray_id],
            key = lambda assignment: assignment['start']
        )
        # Check integrity of assignment list
        if num_assignments > 1:
            for assignment_index in range(1, num_assignments):
                if pd.isna(assignments_dict[tray_id][assignment_index - 1]['end']):
                    raise ValueError('Assignment {} starts at {} but previous assignment for this device {} starts at {} and has no end time'.format(
                        assignments_dict[tray_id][assignment_index]['material_assignment_id'],
                        assignments_dict[tray_id][assignment_index]['start'],
                        assignments_dict[tray_id][assignment_index - 1]['material_assignment_id'],
                        assignments_dict[tray_id][assignment_index - 1]['start']
                    ))
                if assignments_dict[tray_id][assignment_index]['start'] < assignments_dict[tray_id][assignment_index - 1]['end']:
                    raise ValueError('Assignment {} starts at {} but previous assignment for this device {} starts at {} and ends at {}'.format(
                        assignments_dict[tray_id][assignment_index]['material_assignment_id'],
                        assignments_dict[tray_id][assignment_index]['start'],
                        assignments_dict[tray_id][assignment_index - 1]['material_assignment_id'],
                        assignments_dict[tray_id][assignment_index - 1]['start'],
                        assignments_dict[tray_id][assignment_index - 1]['end']
                    ))
    return assignments_dict

def fetch_entity_info():
    logger.info('Fetching entity assignment info to extract tray and person names')
    client = MinimalHoneycombClient()
    result = client.request(
        request_type="query",
        request_name='entityAssignments',
        arguments=None,
        return_object = [
            {'data': [
                'entity_assignment_id',
                {'entity': [
                    'entity_type: __typename',
                    {'... on Tray': [
                        'tray_id',
                        'tray_name: name'
                    ]},
                    {'... on Person': [
                        'person_id',
                        'person_name: name',
                        'person_short_name: short_name'
                    ]}
                ]}
            ]}
        ]
    )
    df = json_normalize(result.get('data'))
    df.rename(
        columns={
            'entity.entity_type': 'entity_type',
            'entity.tray_id': 'tray_id',
            'entity.tray_name': 'tray_name',
            'entity.person_id': 'person_id',
            'entity.person_name': 'person_name',
            'entity.person_short_name': 'person_short_name',
        },
        inplace=True
    )
    df.set_index('entity_assignment_id', inplace=True)
    logger.info('Found {} entity assignments for trays and {} entity assignments for people'.format(
        df['tray_id'].notna().sum(),
        df['person_id'].notna().sum()
    ))
    return df

def fetch_material_names(
):
    logger.info('Fetching material assignment info to extract material names')
    client = MinimalHoneycombClient()
    result = client.request(
        request_type="query",
        request_name='materialAssignments',
        arguments=None,
        return_object = [
            {'data': [
                'material_assignment_id',
                {'material': [
                    'material_id',
                    'material_name: name'
                ]}
            ]}
        ]
    )
    df = json_normalize(result.get('data'))
    df.rename(
        columns={
            'material.material_id': 'material_id',
            'material.material_name': 'material_name'
        },
        inplace=True
    )
    df.set_index('material_assignment_id', inplace=True)
    logger.info('Found {} material assignments'.format(
        df['material_id'].notna().sum()
    ))
    return df

def write_cuwb_data_pkl(
    df,
    filename_prefix,
    environment_name,
    start_time,
    end_time,
    environment_assignment_info=False,
    entity_assignment_info=False,
    directory='.'
):
    path = cuwb_data_path(
        filename_prefix,
        environment_name,
        start_time,
        end_time,
        environment_assignment_info,
        entity_assignment_info,
        directory
    )
    logger.info('Writing CUWB data to {}'.format(path))
    df.to_pickle(path)

def read_cuwb_data_pkl(
    filename_prefix,
    environment_name,
    start_time,
    end_time,
    environment_assignment_info=False,
    entity_assignment_info=False,
    directory='.'
):
    path = cuwb_data_path(
    filename_prefix,
        environment_name,
        start_time,
        end_time,
        environment_assignment_info,
        entity_assignment_info,
        directory
    )
    logger.info('Reading CUWB data from {}'.format(path))
    df = pd.read_pickle(path)
    return df

def cuwb_data_path(
    filename_prefix,
    environment_name,
    start_time,
    end_time,
    environment_assignment_info=False,
    entity_assignment_info=False,
    directory='.'
):
    start_time_string = "None"
    if start_time is not None:
        start_time_string = datetime_filename_format(start_time)
    end_time_string = "None"
    if end_time is not None:
        end_time_string = datetime_filename_format(end_time)
    filename = '-'.join([
        filename_prefix,
        environment_name,
        start_time_string,
        end_time_string
    ])
    if environment_assignment_info:
        filename = filename + '(env_assignments)'
    if entity_assignment_info:
        filename = filename + '(entity_assignments)'
    filename = filename + '.pkl'
    path = os.path.join(
        directory,
        filename
    )
    return path

def datetime_filename_format(timestamp):
    return timestamp.astimezone(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
