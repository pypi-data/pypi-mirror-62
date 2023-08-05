# coding: utf-8

"""
    Model Catalog

    This is the API of the  Software Description Ontology at [https://mintproject.github.io/Mint-ModelCatalog-Ontology/release/1.3.0/index-en.html](https://w3id.org/okn/o/sdm)  # noqa: E501

    OpenAPI spec version: v1.3.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from modelcatalog.api_client import ApiClient
from modelcatalog.exceptions import (
    ApiTypeError,
    ApiValueError
)


class HybridModelApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def hybridmodels_get(self, **kwargs):  # noqa: E501
        """List all HybridModel entities  # noqa: E501

        Gets a list of all HybridModel entities  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str username: Username to query
        :param str label: Filter by label
        :return: list[HybridModel]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.hybridmodels_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.hybridmodels_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def hybridmodels_get_with_http_info(self, **kwargs):  # noqa: E501
        """List all HybridModel entities  # noqa: E501

        Gets a list of all HybridModel entities  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str username: Username to query
        :param str label: Filter by label
        :return: list[HybridModel]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['username', 'label']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method hybridmodels_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'username' in local_var_params:
            query_params.append(('username', local_var_params['username']))  # noqa: E501
        if 'label' in local_var_params:
            query_params.append(('label', local_var_params['label']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/hybridmodels', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[HybridModel]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def hybridmodels_id_delete(self, id, user, **kwargs):  # noqa: E501
        """Delete a HybridModel  # noqa: E501

        Delete an existing HybridModel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_id_delete(id, user, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The ID of the resource (required)
        :param str user: Username (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.hybridmodels_id_delete_with_http_info(id, user, **kwargs)  # noqa: E501
        else:
            (data) = self.hybridmodels_id_delete_with_http_info(id, user, **kwargs)  # noqa: E501
            return data

    def hybridmodels_id_delete_with_http_info(self, id, user, **kwargs):  # noqa: E501
        """Delete a HybridModel  # noqa: E501

        Delete an existing HybridModel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_id_delete_with_http_info(id, user, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The ID of the resource (required)
        :param str user: Username (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id', 'user']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method hybridmodels_id_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in local_var_params or
                local_var_params['id'] is None):
            raise ApiValueError("Missing the required parameter `id` when calling `hybridmodels_id_delete`")  # noqa: E501
        # verify the required parameter 'user' is set
        if ('user' not in local_var_params or
                local_var_params['user'] is None):
            raise ApiValueError("Missing the required parameter `user` when calling `hybridmodels_id_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in local_var_params:
            path_params['id'] = local_var_params['id']  # noqa: E501
        if 'user' in local_var_params:
            path_params['user'] = local_var_params['user']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['BearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/hybridmodels/{id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def hybridmodels_id_get(self, id, **kwargs):  # noqa: E501
        """Get a HybridModel  # noqa: E501

        Gets the details of a single instance of a HybridModel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_id_get(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The ID of the resource (required)
        :param str username: Username to query
        :return: HybridModel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.hybridmodels_id_get_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.hybridmodels_id_get_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def hybridmodels_id_get_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get a HybridModel  # noqa: E501

        Gets the details of a single instance of a HybridModel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_id_get_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The ID of the resource (required)
        :param str username: Username to query
        :return: HybridModel
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id', 'username']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method hybridmodels_id_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in local_var_params or
                local_var_params['id'] is None):
            raise ApiValueError("Missing the required parameter `id` when calling `hybridmodels_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in local_var_params:
            path_params['id'] = local_var_params['id']  # noqa: E501

        query_params = []
        if 'username' in local_var_params:
            query_params.append(('username', local_var_params['username']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/hybridmodels/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='HybridModel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def hybridmodels_id_put(self, id, user, **kwargs):  # noqa: E501
        """Update a HybridModel  # noqa: E501

        Updates an existing HybridModel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_id_put(id, user, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The ID of the resource (required)
        :param str user: Username (required)
        :param HybridModel hybrid_model: An old HybridModelto be updated
        :return: HybridModel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.hybridmodels_id_put_with_http_info(id, user, **kwargs)  # noqa: E501
        else:
            (data) = self.hybridmodels_id_put_with_http_info(id, user, **kwargs)  # noqa: E501
            return data

    def hybridmodels_id_put_with_http_info(self, id, user, **kwargs):  # noqa: E501
        """Update a HybridModel  # noqa: E501

        Updates an existing HybridModel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_id_put_with_http_info(id, user, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The ID of the resource (required)
        :param str user: Username (required)
        :param HybridModel hybrid_model: An old HybridModelto be updated
        :return: HybridModel
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id', 'user', 'hybrid_model']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method hybridmodels_id_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in local_var_params or
                local_var_params['id'] is None):
            raise ApiValueError("Missing the required parameter `id` when calling `hybridmodels_id_put`")  # noqa: E501
        # verify the required parameter 'user' is set
        if ('user' not in local_var_params or
                local_var_params['user'] is None):
            raise ApiValueError("Missing the required parameter `user` when calling `hybridmodels_id_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in local_var_params:
            path_params['id'] = local_var_params['id']  # noqa: E501
        if 'user' in local_var_params:
            path_params['user'] = local_var_params['user']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'hybrid_model' in local_var_params:
            body_params = local_var_params['hybrid_model']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['BearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/hybridmodels/{id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='HybridModel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def hybridmodels_post(self, user, **kwargs):  # noqa: E501
        """Create a HybridModel  # noqa: E501

        Create a new instance of a HybridModel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_post(user, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str user: Username (required)
        :param HybridModel hybrid_model: A new HybridModelto be created
        :return: HybridModel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.hybridmodels_post_with_http_info(user, **kwargs)  # noqa: E501
        else:
            (data) = self.hybridmodels_post_with_http_info(user, **kwargs)  # noqa: E501
            return data

    def hybridmodels_post_with_http_info(self, user, **kwargs):  # noqa: E501
        """Create a HybridModel  # noqa: E501

        Create a new instance of a HybridModel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.hybridmodels_post_with_http_info(user, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str user: Username (required)
        :param HybridModel hybrid_model: A new HybridModelto be created
        :return: HybridModel
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['user', 'hybrid_model']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method hybridmodels_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'user' is set
        if ('user' not in local_var_params or
                local_var_params['user'] is None):
            raise ApiValueError("Missing the required parameter `user` when calling `hybridmodels_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'user' in local_var_params:
            path_params['user'] = local_var_params['user']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'hybrid_model' in local_var_params:
            body_params = local_var_params['hybrid_model']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['BearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/hybridmodels', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='HybridModel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
