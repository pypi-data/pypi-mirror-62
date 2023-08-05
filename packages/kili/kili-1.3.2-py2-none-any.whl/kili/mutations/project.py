import time
from json import dumps, loads
from typing import List

from tqdm import tqdm

from ..helpers import GraphQLError, format_result, json_escape
from ..queries.asset import get_assets
from ..queries.label import get_label
from ..queries.project import get_project
from .asset import update_properties_in_asset
from .lock import delete_locks


def create_project(client, title: str, description: str, use_honeypot: bool,
                   interface_json_settings: dict):
    result = client.execute('''
    mutation {
      createProject(
      title: "%s",
      description: "%s",
      useHoneyPot: %s,
      interfaceJsonSettings: "%s") {
        id
      }
    }
    ''' % (title, description, str(use_honeypot).lower(), json_escape(interface_json_settings)))
    return format_result('createProject', result)


def delete_project(client, project_id: str):
    result = client.execute('''
    mutation {
      deleteProject(projectID: "%s") {
        id
      }
    }
    ''' % (project_id))
    return format_result('deleteProject', result)


def append_to_roles(client, project_id: str, user_email: str, role: str):
    result = client.execute('''
    mutation {
      appendToRoles(
        projectID: "%s",
        userEmail: "%s",
        role: %s) {
          id
          title
          roles {
              user {
                id
                email
              }
              role
         }
      }
    }
    ''' % (project_id, user_email, role))
    return format_result('appendToRoles', result)


def update_properties_in_project(client, project_id: str,
                                 title: str = None,
                                 description: str = None,
                                 min_consensus_size: int = None,
                                 consensus_tot_coverage: int = None,
                                 number_of_assets: int = None,
                                 number_of_remaining_assets: int = None,
                                 number_of_assets_with_empty_labels: int = None,
                                 number_of_reviewed_assets: int = None,
                                 number_of_latest_labels: int = None,
                                 consensus_mark: float = None,
                                 honeypot_mark: float = None,
                                 instructions: str = None):
    formatted_title = 'null' if title is None else f'"{title}"'
    formatted_description = 'null' if description is None else f'"{description}"'
    formatted_min_consensus_size = 'null' if min_consensus_size is None else int(
        min_consensus_size)
    formatted_min_consensus_size = 'null' if min_consensus_size is None else int(
        min_consensus_size)
    formatted_consensus_tot_coverage = 'null' if consensus_tot_coverage is None else int(
        consensus_tot_coverage)
    formatted_number_of_assets = 'null' if number_of_assets is None else int(
        number_of_assets)
    formatted_number_of_remaining_assets = 'null' if number_of_remaining_assets is None else int(
        number_of_remaining_assets)
    formatted_number_of_assets_with_empty_labels = 'null' if number_of_assets_with_empty_labels is None else int(
        number_of_assets_with_empty_labels)
    formatted_number_of_reviewed_assets = 'null' if number_of_reviewed_assets is None else int(
        number_of_reviewed_assets)
    formatted_number_of_latest_labels = 'null' if number_of_latest_labels is None else int(
        number_of_latest_labels)
    formatted_consensus_mark = 'null' if consensus_mark is None else float(
        consensus_mark)
    formatted_honeypot_mark = 'null' if honeypot_mark is None else float(
        honeypot_mark)
    formatted_instructions = 'null' if instructions is None else f'{dumps(instructions)}'

    result = client.execute('''
        mutation {
          updatePropertiesInProject(
            where: {id: "%s"},
            data: {
              title: %s
              description: %s
              minConsensusSize: %s
              consensusTotCoverage: %s
              numberOfAssets: %s
              numberOfRemainingAssets: %s
              numberOfAssetsWithSkippedLabels: %s
              numberOfReviewedAssets: %s
              numberOfLatestLabels: %s
              consensusMark: %s
              honeypotMark: %s
              instructions: %s
            }
          ) {
            id
          }
        }
        ''' % (project_id, formatted_title, formatted_description,
               formatted_min_consensus_size, formatted_consensus_tot_coverage,
               formatted_number_of_assets, formatted_number_of_remaining_assets,
               formatted_number_of_assets_with_empty_labels, formatted_number_of_reviewed_assets,
               formatted_number_of_latest_labels, formatted_consensus_mark, formatted_honeypot_mark,
               formatted_instructions))
    return format_result('updatePropertiesInProject', result)


def update_interface_in_project(client, project_id: str, jsonSettings: str = None):
    result = client.execute('''
        mutation {
          updatePropertiesInProject(
            where: {id: "%s"},
            data: {
              jsonSettings: """%s""",
            }
          ) {
            id
          }
        }
        ''' % (project_id, jsonSettings))
    return format_result('updatePropertiesInProject', result)


def create_empty_project(client, user_id: str):
    result = client.execute('''
    mutation {
      createEmptyProject(userID: "%s") {
        id

      }
    }
    ''' % (user_id))
    return format_result('createEmptyProject', result)


def update_project(client, project_id: str,
                   title: str,
                   description: str,
                   interface_category: str,
                   input_type: str = 'TEXT',
                   consensus_tot_coverage: int = 0,
                   min_consensus_size: int = 1,
                   max_worker_count: int = 4,
                   min_agreement: int = 66,
                   use_honey_pot: bool = False,
                   instructions: str = None):
    formatted_instructions = 'null' if instructions is None else f'"{instructions}"'
    result = client.execute('''
    mutation {
      updateProject(projectID: "%s",
        title: "%s",
        description: "%s",
        interfaceCategory: %s,
        inputType: %s,
        consensusTotCoverage: %d,
        minConsensusSize: %d,
        maxWorkerCount: %d,
        minAgreement: %d,
        useHoneyPot: %s,
        instructions: %s) {
        id
      }
    }
    ''' % (
        project_id, title, description,
        interface_category, input_type,
        consensus_tot_coverage, min_consensus_size, max_worker_count, min_agreement,
        str(use_honey_pot).lower(), formatted_instructions))
    return format_result('updateProject', result)


def update_role(client, role_id: str, project_id: str, user_id: str, role: str):
    result = client.execute('''
    mutation {
      updateRole(roleID: "%s",
        projectID: "%s",
        userID: "%s",
        role: %s) {
          id
      }
    }
    ''' % (role_id, project_id, user_id, role))
    return format_result('updateRole', result)


def delete_from_roles(client, role_id: str):
    result = client.execute('''
    mutation {
      deleteFromRoles(roleID: "%s") {
        id
      }
    }
    ''' % (role_id))
    return format_result('deleteFromRoles', result)


def update_properties_in_project_user(client, project_user_id: str,
                                      total_duration: int = None,
                                      number_of_labeled_assets: int = None,
                                      consensus_mark: float = None,
                                      honeypot_mark: float = None):
    args = [total_duration,
            number_of_labeled_assets, consensus_mark, honeypot_mark]
    formatted_args = ['null' if arg is None else f'{arg}' for arg in args]

    result = client.execute('''
        mutation {
          updatePropertiesInProjectUser(
            where: {id: "%s"},
            data: {
              totalDuration: %s
              numberOfLabeledAssets: %s
              consensusMark: %s
              honeypotMark: %s
            }
          ) {
            id
          }
        }
        ''' % (project_user_id, *formatted_args))
    return format_result('updatePropertiesInProjectUser', result)


def force_project_kpis(client, project_id: str):
    _ = get_assets(client, project_id=project_id)
    _ = get_project(client, project_id=project_id)
