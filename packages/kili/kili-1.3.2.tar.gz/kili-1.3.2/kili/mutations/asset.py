from json import dumps
from typing import List

from ..helpers import (content_escape, encode_image, format_result, is_url,
                       json_escape)
from ..queries.project import get_project


def delete_assets_by_external_id(client, project_id: str, external_id: str):
    result = client.execute('''
    mutation {
      deleteAssetsByExternalId(projectID: "%s", externalID: "%s") {
        id
      }
    }
    ''' % (project_id, external_id))
    return format_result('deleteAssetsByExternalId', result)


def append_many_to_dataset(client, project_id: str, content_array: List[str], external_id_array: List[str],
                           is_honeypot_array: List[bool] = None, status_array: List[str] = None, json_metadata_array: List[dict] = None):
    is_honeypot_array = [
        False] * len(content_array) if not is_honeypot_array else is_honeypot_array
    status_array = ['TODO'] * \
        len(content_array) if not status_array else status_array
    json_metadata_array = [
        {}] * len(content_array) if not json_metadata_array else json_metadata_array
    input_type = get_project(client, project_id)['inputType']
    if input_type == 'IMAGE':
        content_array = [content if is_url(content) else encode_image(
            content) for content in content_array]
    result = client.execute('''
        mutation {
          appendManyToDataset(
            projectID: "%s",
            contentArray: %s,
            externalIDArray: %s,
            isHoneypotArray: %s,
            statusArray: %s,
            jsonMetadataArray: %s) {
            id
          }
        }
    ''' % (project_id, dumps(content_array), dumps(external_id_array),
           dumps(is_honeypot_array).lower(),
           dumps(status_array).replace('"', ''), dumps([dumps(elem) for elem in json_metadata_array])))
    return format_result('appendManyToDataset', result)


def update_asset(client, asset_id: str, project_id: str, content: str, external_id: str,
                 is_honeypot: bool, consensus_mark: float, honeypot_mark: float, status: str, json_metadata: dict):
    result = client.execute('''
    mutation {
      updateAsset(
        assetID: "%s",
        projectID: "%s",
        content: "%s",
        externalID: "%s",
        isHoneypot: %s,
        consensusMark: %d,
        honeypotMark: %d,
        status: %s,
        jsonMetadata: "%s") {
        id
      }
    }
    ''' % (asset_id, project_id, content, external_id,
           str(is_honeypot).lower(), consensus_mark, honeypot_mark, status, json_escape(json_metadata)))
    return format_result('updateAsset', result)


def update_properties_in_asset(client, asset_id: str, external_id: str = None,
                               priority: int = None, json_metadata: dict = None, consensus_mark: float = None,
                               honeypot_mark: float = None, to_be_labeled_by: List[str] = None):
    formatted_external_id = 'null' if external_id is None else f'"{external_id}"'
    formatted_priority = 'null' if priority is None else f'{priority}'
    formatted_json_metadata = 'null'
    if json_metadata is None:
        formatted_json_metadata = 'null'
    elif isinstance(json_metadata, str):
        formatted_json_metadata = f'"{json_metadata}"'
    elif isinstance(json_metadata, dict) or isinstance(json_metadata, list):
        formatted_json_metadata = f'"{json_escape(json_metadata)}"'
    else:
        raise Exception('json_metadata',
                        'Should be either a dict, a list or a string url')
    formatted_consensus_mark = 'null' if consensus_mark is None else f'{consensus_mark}'
    formatted_honeypot_mark = 'null' if honeypot_mark is None else f'{honeypot_mark}'
    formatted_to_be_labeled_by = 'null' if to_be_labeled_by is None else f'{dumps(to_be_labeled_by)}'

    result = client.execute('''
        mutation {
          updatePropertiesInAsset(
            where: {id: "%s"},
            data: {
              externalId: %s
              priority: %s
              jsonMetadata: %s
              consensusMark: %s
              honeypotMark: %s
              toBeLabeledBy: %s
            }
          ) {
            id
          }
        }
        ''' % (asset_id, formatted_external_id, formatted_priority,
               formatted_json_metadata, formatted_consensus_mark,
               formatted_honeypot_mark, formatted_to_be_labeled_by))
    return format_result('updatePropertiesInAsset', result)


def delete_from_dataset(client, asset_id: str):
    result = client.execute('''
    mutation {
      deleteFromDataset(assetID: "%s") {
        id
      }
    }
    ''' % (asset_id))
    return format_result('deleteFromDataset', result)


def delete_many_from_dataset(client, asset_ids: List[str]):
    result = client.execute('''
    mutation {
      deleteManyFromDataset(assetIDs: %s) {
        id
      }
    }
    ''' % (dumps(asset_ids)))
    return format_result('deleteManyFromDataset', result)
