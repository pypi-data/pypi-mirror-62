
import process_cuwb_data
import geom_render
from minimal_honeycomb import MinimalHoneycombClient
import pandas as pd
import numpy as np
import datetime
import os
import logging

logger = logging.getLogger(__name__)

def fetch_geoms_2d(
    environment_name,
    start_time,
    end_time,
    frames_per_second=10.0,
    progress_bar=False,
    notebook=False
):
    ## Fetch CUWB position data
    df_position = process_cuwb_data.fetch_cuwb_position_data(
        environment_name=environment_name,
        start_time=start_time,
        end_time=end_time,
        environment_assignment_info=False,
        entity_assignment_info=True
    )
    ## Create 3D geom collection from data
    geom_collection_3d = create_geom_collection_3d(
        df_position,
        progress_bar=progress_bar,
        notebook=notebook
    )
    ## Resample 3D geom collection
    geom_collection_3d_resampled = resample_geom(
        geom_collection_3d,
        start_time=start_time,
        end_time=end_time,
        frames_per_second=frames_per_second,
        progress_bar=progress_bar,
        notebook=notebook
    )
    ## Fetch camera info
    camera_info_dict = fetch_camera_info(
        environment_name=environment_name,
        start_time=start_time,
        end_time=end_time
    )
    ## Project onto camera views
    geom_collection_2d_dict = project_onto_camera_views(
        geom_collection_3d_resampled,
        camera_info_dict
    )
    return geom_collection_2d_dict

def create_geom_collection_3d(
    df,
    colors = {
        'Person': '#ff0000',
        'Tray': '#00ff00'
    },
    progress_bar=False,
    notebook=False
):
    # Create dictionary of 3D geom collections, one for each object in data
    logger.info('Creating dictionary of 3D geom collections, for each sensor in data: {}'.format(
        df['device_serial_number'].unique().tolist()
    ))
    geom_collection_3d_dict = dict()
    for (device_id, device_serial_number, entity_type, person_id, person_short_name, material_id, material_name), group_df in df.fillna('NA').groupby([
        'device_id',
        'device_serial_number',
        'entity_type',
        'person_id',
        'person_short_name',
        'material_id',
        'material_name'
    ]):
        entity_name = material_name
        if entity_type == 'Person':
            entity_name = person_short_name
        entity_id = material_id
        if entity_type == 'Person':
            entity_id = person_id
        logger.info('Creating 3D geom collection for {} ({}) [{} to {}]'.format(
            entity_name,
            device_serial_number,
            group_df.index.min().isoformat(),
            group_df.index.max().isoformat()
        ))
        time_index = group_df.index.to_pydatetime()
        position_values = group_df.loc[:, ['x_meters', 'y_meters', 'z_meters']].values
        coordinates = np.expand_dims(position_values, axis=1)
        geom_list = [
            geom_render.Point3D(
                coordinate_indices=[0],
                color=colors[entity_type],
                object_type=entity_type,
                object_id=entity_id,
                object_name=entity_name
            ),
            geom_render.Text3D(
                text=entity_name,
                coordinate_indices=[0],
                color=colors[entity_type],
                object_type=entity_type,
                object_id=entity_id,
                object_name=entity_name
            )
        ]
        geom_collection_3d_dict[device_id] = geom_render.GeomCollection3D(
            time_index=time_index,
            coordinates=coordinates,
            geom_list=geom_list
        )
    # Create combined 3D geom collection
    logger.info('Combining 3D geom collections into single 3D geom collection')
    combined_geom_collection_3d = geom_render.GeomCollection3D.from_geom_list(
        list(geom_collection_3d_dict.values()),
        progress_bar=progress_bar,
        notebook=notebook
    )
    return combined_geom_collection_3d

def resample_geom(
    geom,
    start_time,
    end_time,
    frames_per_second = 10.0,
    progress_bar=False,
    notebook=False
):
    logger.info('Resampling geom to match start time {}, end time {}, and {} frames per second'.format(
        start_time.isoformat(),
        end_time.isoformat(),
        frames_per_second
    ))
    time_between_frames = datetime.timedelta(microseconds = int(round(10**6/frames_per_second)))
    num_frames = int(round((end_time - start_time)/time_between_frames))
    geom_resampled = geom.resample(
        new_start_time=start_time,
        new_frames_per_second=frames_per_second,
        new_num_frames=num_frames,
        progress_bar=progress_bar,
        notebook=notebook
    )
    return geom_resampled

def project_onto_camera_views(
    geom_3d,
    camera_info_dict
):
    logger.info('Creating 2D geoms from 3D geom, one for each camera: {}'.format(
        [camera_info['device_name'] for camera_info in camera_info_dict.values()]
    ))
    geom_2d_dict = dict()
    for device_id, camera_info in camera_info_dict.items():
        logger.info('Creating 2D geom for camera {}'.format(
            camera_info['device_name']
        ))
        geom_2d_dict[device_id] = dict()
        geom_2d_dict[device_id]['device_name'] = camera_info['device_name']
        geom_2d_dict[device_id]['geom'] = geom_3d.project(
            rotation_vector=camera_info['rotation_vector'],
            translation_vector=camera_info['translation_vector'],
            camera_matrix=camera_info['camera_matrix'],
            distortion_coefficients=camera_info['distortion_coefficients'],
            frame_width=camera_info['image_width'],
            frame_height=camera_info['image_height']
        )
    return geom_2d_dict

def write_json(
    geom_dict,
    output_directory='.',
    prefix='geom_2d',
    indent=None
):
    logger.info('Writing geom data to local JSON file for: {}'.format(
        [geom_info['device_name'] for geom_info in geom_dict.values()]
    ))
    for device_id, geom_info in geom_dict.items():
        logger.info('Writing geom data to local JSON file for {}'.format(
            geom_info['device_name']
        ))
        path = os.path.join(
            output_directory,
            '_'.join([prefix, geom_info['device_name']]) + '.json'
        )
        with open(path, 'w') as fp:
            fp.write(geom_info['geom'].to_json(indent=indent))

def fetch_camera_info(
    environment_name,
    start_time,
    end_time,
    camera_device_types=['PI3WITHCAMERA', 'PIZEROWITHCAMERA']
):
    logger.info('Fetching camera info between start time {} and end time {} for environment {}'.format(
        start_time.isoformat(),
        end_time.isoformat(),
        environment_name
    ))
    device_ids = fetch_camera_device_ids(
        environment_name=environment_name,
        start_time=start_time,
        end_time=end_time,
        camera_device_types=camera_device_types
    )
    logger.info('Fetching camera info between start time {} and end time {} for the following device_ids: {}'.format(
        start_time.isoformat(),
        end_time.isoformat(),
        device_ids
    ))
    client=MinimalHoneycombClient()
    result = client.request(
        request_type='query',
        request_name='searchDevices',
        arguments={
            'query': {
                'type': 'QueryExpression!',
                'value': {
                    'field': 'device_id',
                    'operator': 'IN',
                    'values': device_ids
                }
            }
        },
        return_object = [
            {'data': [
                'device_id',
                'name',
                {'intrinsic_calibrations':[
                    'start',
                    'end',
                    'camera_matrix',
                    'distortion_coefficients',
                    'image_width',
                    'image_height'
                ]},
                {'extrinsic_calibrations':[
                    'start',
                    'end',
                    'translation_vector',
                    'rotation_vector'
                ]}
            ]}
        ]
    )
    devices = result.get('data')
    camera_info_dict = dict()
    for device in devices:
        intrinsic_calibration = extract_assignment(
            assignments=device['intrinsic_calibrations'],
            start_time=start_time,
            end_time=end_time
        )
        if intrinsic_calibration is None:
            continue
        extrinsic_calibration = extract_assignment(
            assignments=device['extrinsic_calibrations'],
            start_time=start_time,
            end_time=end_time
        )
        if extrinsic_calibration is None:
            continue
        camera_info_dict[device['device_id']] = {
            'device_name': device['name'],
            'camera_matrix': intrinsic_calibration['camera_matrix'],
            'distortion_coefficients': intrinsic_calibration['distortion_coefficients'],
            'image_width': intrinsic_calibration['image_width'],
            'image_height': intrinsic_calibration['image_height'],
            'translation_vector': extrinsic_calibration['translation_vector'],
            'rotation_vector': extrinsic_calibration['rotation_vector'],
        }
    return camera_info_dict

def fetch_camera_device_ids(
    environment_name,
    start_time,
    end_time,
    camera_device_types=['PI3WITHCAMERA', 'PIZEROWITHCAMERA']
):
    client=MinimalHoneycombClient()
    result = client.request(
        request_type='query',
        request_name='findEnvironments',
        arguments={
            'name': {
                'type': 'String',
                'value': environment_name
            }
        },
        return_object = [
            {'data': [
                {'assignments': [
                    'start',
                    'end',
                    'assigned_type',
                    {'assigned': [
                        '__typename',
                        {'... on Device': [
                            'device_id',
                            'device_type'
                        ]}
                    ]}
                ]}
            ]}
        ]
    )
    environments = result.get('data')
    if len(environments) == 0:
        raise ValueError('No environments match environment name {}'.format(environment_name))
    if len(environments) > 1:
        raise ValueError('More than one environments matched name {}'.format(environment_name))
    assignments = environments[0].get('assignments')
    camera_device_ids = list()
    for assignment in assignments:
        if assignment.get('start') is not None and (pd.to_datetime(assignment.get('start')).to_pydatetime() > end_time):
            continue
        if assignment.get('end') is not None and (pd.to_datetime(assignment.get('end')).to_pydatetime() < start_time):
            continue
        if assignment.get('assigned').get('__typename') != 'Device':
            continue
        if assignment.get('assigned').get('device_type') not in camera_device_types:
            continue
        camera_device_ids.append(assignment.get('assigned').get('device_id'))
    return camera_device_ids

def extract_assignment(
    assignments,
    start_time,
    end_time
):
    matched_assignments = list()
    for assignment in assignments:
        if assignment.get('start') is not None and (pd.to_datetime(assignment.get('start')).to_pydatetime() > end_time):
            continue
        if assignment.get('end') is not None and (pd.to_datetime(assignment.get('end')).to_pydatetime() < start_time):
            continue
        matched_assignments.append(assignment)
    if len(matched_assignments) == 0:
        return None
    if len(matched_assignments) > 1:
        raise ValueError('Multiple assignments matched start time {} and end time {}'.format(
            start_time.isoformat(),
            end_time.isoformat()
        ))
    return matched_assignments[0]
