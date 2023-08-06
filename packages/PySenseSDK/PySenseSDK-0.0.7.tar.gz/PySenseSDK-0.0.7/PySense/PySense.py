import json
import requests
import yaml

from . import PySenseDashboard
from . import PySenseFolder
from . import PySenseUser
from . import PySenseUtils


def authenticate_by_file(config_file):
    """
    Creates a new PySense client with the credentials in the given config file.

    :param config_file: Yaml file with entries for host, username, and password
    :return: A new PySense client for the given credentials
    """
    with open(config_file, 'r') as yml_file:
        cfg = yaml.safe_load(yml_file)
        return PySense(cfg['host'], cfg['username'], cfg['password'])


class PySense:

    def __init__(self, host, username, password):
        data = {'username': username, 'password': password}
        host = PySenseUtils.format_host(host)
        resp = requests.post('{}/api/v1/authentication/login'.format(host), data=data)
        PySenseUtils.parse_response(resp)
        access_code = "Bearer " + resp.json()['access_token']
        self._token = {'authorization': access_code}
        self._host = host

    def custom_rest(self, action_type, url, *, data=None, json_payload=None):
        if action_type.lower() == 'get':
            return requests.get('{}/{}'.format(self._host, url), headers=self._token, data=data, json=json_payload)
        elif action_type.lower() == 'post':
            return requests.post('{}/{}'.format(self._host, url), headers=self._token, data=data, json=json_payload)
        elif action_type.lower() == 'patch':
            return requests.patch('{}/{}'.format(self._host, url), headers=self._token, data=data, json=json_payload)
        elif action_type.lower() == 'delete':
            return requests.delete('{}/{}'.format(self._host, url), headers=self._token, data=data, json=json_payload)
        else:
            raise Exception('No rest action {}'.format(action_type))

    def get_authentication(self):
        """
        Returns authentication parameters
        @return: A dictionary with an entry for host and token
        """
        return {'host': self._host, 'token': self._token}

    ############################################
    # Dashboards                               #
    ############################################

    def get_dashboards(self, *, parent_folder_name=None, name=None, data_source_title=None,
                       data_source_address=None, fields=None, sort=None, expand=None):
        """
         Get all dashboards

         :param parent_folder_name: Parent folder name to filter by
         :param name: Name to filter by
         :param data_source_title: Data source name to filter by
         :param data_source_address: Data source address to filter by
         :param fields: Whitelist of fields to return for each document.
            Can also exclude by prefixing field names with -
         :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
         :param expand: List of fields that should be expanded
         :return: All found dashboards
         """
        ret_arr = []
        folder_id = None
        if parent_folder_name:
            folders = self.get_folders(name=parent_folder_name)
            if len(folders) == 1:
                folder_id = folders[0].get_folder_oid()
            else:
                raise Exception("{} folders found with name {}".format(len(folders), parent_folder_name))

        param_string = PySenseUtils.build_query_string({
            'parentFolder': folder_id,
            'name': name,
            'datasourceTitle': data_source_title,
            'datasourceAddress': data_source_address,
            'fields': fields,
            'sort': sort,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/dashboards?{}'.format(self._host, param_string),
                            headers=self._token)

        PySenseUtils.parse_response(resp)
        json_arr = json.loads(resp.content)
        for dash in json_arr:
            ret_arr.append(PySenseDashboard.Dashboard(self._host, self._token, dash))
        return ret_arr

    def get_dashboards_id(self, dashboard_id, *, fields=None, expand=None):
        """
        Returns a specific dashboard object by ID.

        :param dashboard_id: The ID of the dashboard to get
        :param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        :param expand: List of fields that should be expanded (substitures their IDs with actual objects). May be nested
            using the resource.subResource format
        :return: Dashboard with id given
        """
        param_string = PySenseUtils.build_query_string({
            'fields': fields,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/dashboards/{}?{}'.format(self._host, dashboard_id, param_string),
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        return PySenseDashboard.Dashboard(self._host, self._token, resp.json())

    def post_dashboards(self, dashboard_obj):
        """
        Import given dashboard

        :param dashboard_obj: A PySense dashboard object
        :return: The dashboard given by the response object
        """
        resp = requests.post('{}/api/v1/dashboards/'.format(self._host), headers=self._token,
                             json=dashboard_obj.get_dashboard_json())
        PySenseUtils.parse_response(resp)
        return PySenseDashboard.Dashboard(self._host, self._token, json.loads(resp.content))

    def delete_dashboards(self, dashboard_id):
        """
        Delete dashboard with id

        :param dashboard_id: The ID of the dashboard to delete
        :return: The response object
        """
        resp = requests.delete('{}/api/v1/dashboards/{}'.format(self._host, dashboard_id),
                               headers=self._token)
        return PySenseUtils.parse_response(resp)

    ############################################
    # Folders                                  #
    ############################################

    def get_folders(self, *, name=None, structure=None, ids=None, fields=None,
                    sort=None, skip=None, limit=None, expand=None):
        """
        Provides access to a specified user’s folders in their stored format

        @param name: Name to filter by
        @param structure: Structure type of the folders
        @param ids: Array of folder IDs to get, separated by a comma (,) and without spaces
        @param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        @param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
        @param skip: Number of results to skip from the start of the data set. skip is to be used with the limit
            parameter for paging
        @param limit: How many results should be returned. limit is to be used with the skip parameter for paging
        @param expand: List of fields that should be expanded (substitures their IDs with actual objects). May be
            nested using the resource.subResource format
        @return: An array of folders matching the search criteria
        """
        ret_arr = []
        param_string = PySenseUtils.build_query_string({
            'name': name,
            'structure': structure,
            'ids': ids,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/folders?{}'.format(self._host, param_string),
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        # Sisense Rest API always returns the root folder, so we filter it out when looking by name
        if name:
            for folder in resp.json():
                if folder['name'] == name:
                    ret_arr.append(PySenseFolder.Folder(self._host, self._token, folder))
        else:
            for folder in resp.json():
                ret_arr.append(PySenseFolder.Folder(self._host, self._token, folder))
        return ret_arr

    def get_folders_id(self, folder_id):
        """
        Get a specific folder by folder id

        @param folder_id: The folder id of the folder
        @return: A PySense folder object of the folder
        """
        resp = requests.get('{}/api/v1/folders/{}'.format(self._host, folder_id), headers=self._token)
        PySenseUtils.parse_response(resp)
        return PySenseFolder.Folder(self._host, self._token, resp.json())

    ############################################
    # Groups                                   #
    ############################################

    def get_group_ids(self, groups):
        """
        Get the ids for groups
        @param groups: An array of group names
        @return: An array of ids for the groups
        """
        resp = requests.get('{}/api/v1/groups'.format(self._host),
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        json_rep = json.loads(resp.content.decode('utf8'))
        ret = []
        for group in groups:
            found = False
            for item in json_rep:
                if group == item['name']:
                    ret.append(item['_id'])
                    found = True
            if not found:
                return 'Cannot find id for group {}'.format(group)
        return ret

    ############################################
    # Users                                    #
    ############################################

    def post_user(self, email, username, role, *, first_name=None, last_name=None,
                  groups=None, preferences=None, ui_settings=None):
        """
        Receives a new user object and creates that user in SiSense, returning the created object.
        If a user with the same username or email exists, it will return an error.

        @param email: email address for user
        @param username: username
        @param role: role name
        @param first_name: user first name
        @param last_name: user last name
        @param groups: The groups to add the user to
        @param preferences: User preferences
        @param ui_settings: User ui settings
        @return: Newly created user object
        """
        user_obj = PySenseUtils.build_json_object({
            'email': email,
            'username': username,
            'firstName': first_name,
            'lastName': last_name,
            'roleId': PySenseUtils.get_role_id(self._host, self._token, role),
            'groups': self.get_group_ids(groups),
            'preferences': preferences,
            'uiSettings': ui_settings
        })
        resp = requests.post('{}/api/v1/users'.format(self._host), headers=self._token,
                             json=user_obj)
        PySenseUtils.parse_response(resp)
        return PySenseUser.User(self._host, self._token, json.loads(resp.content))

    def get_users(self, *, user_name=None, email=None, first_name=None, last_name=None, role_name=None, group=None, active=None,
                  origin=None, ids=None, fields=None, sort=None, skip=None, limit=None, expand=None):
        """
        Returns a list of users with their details.
        Results can be filtered by parameters such as username and email.
        The expandable fields for the user object are groups, adgroups and role.

        @param user_name: Username to filter by
        @param email: Email to filter by
        @param first_name: First name to filter by
        @param last_name: Last name to filter by
        @param role_name: Role filter by
        @param group: Group to filter by
        @param active: User state to filter by (true for active users, false for inactive users)
        @param origin: User origin to filter by (ad for active directory or sisense)
        @param ids: Array of user ids to get separated by comma and without spaces
        @param fields: Whitelist of fields to return for each document.
            Fields can also define which fields to exclude by prefixing field names with -
        @param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
        @param skip: Number of results to skip from the start of the data set.
            Skip is to be used with the limit parameter for paging
        @param limit: How many results should be returned. limit is to be used with the skip parameter for paging
        @param expand: List of fields that should be expanded (substitutes their IDs with actual objects).
            May be nested using the resource.subResource format

        @return: An array of users objects
        """
        param_string = PySenseUtils.build_query_string({
            'userName': user_name,
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'role': PySenseUtils.get_role_id(self._host, self._token, role_name),
            'group': group,
            'active': active,
            'origin': origin,
            'ids': ids,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/users?{}'.format(self._host, param_string), headers=self._token)
        ret_arr = []
        PySenseUtils.parse_response(resp)
        for user in json.loads(resp.content):
            ret_arr.append((PySenseUser.User(self._host, self._token, user)))
        return ret_arr

    def delete_user(self, user):
        """
        Deletes the specified user
        @param user: User obj to delete
        @return: Response
        """
        resp = requests.delete('{}/api/v1/users/{}'.format(self._host, user.get_user_id()), headers=self._token)
        return PySenseUtils.parse_response(resp)

    ############################################
    # Alerts                                   #
    ############################################
    # This isn't at all done
    def post_alert(self, alert_obj):
        resp = requests.post('{}/api/v1/alerts'.format(self._host),
                             headers=self._token, json=json.loads(alert_obj))
        PySenseUtils.parse_response(resp)




