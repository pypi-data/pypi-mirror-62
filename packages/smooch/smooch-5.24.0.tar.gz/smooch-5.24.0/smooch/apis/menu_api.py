# coding: utf-8

"""
    Smooch

    The Smooch API is a unified interface for powering messaging in your customer experiences across every channel. Our API speeds access to new markets, reduces time to ship, eliminates complexity, and helps you build the best experiences for your customers. For more information, visit our [official documentation](https://docs.smooch.io).

    OpenAPI spec version: 5.24
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class MenuApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def delete_menu(self, app_id, **kwargs):
        """
        Remove the specified app’s menu.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_menu(app_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str app_id: Identifies the app. (required)
        :return: MenuResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_menu_with_http_info(app_id, **kwargs)
        else:
            (data) = self.delete_menu_with_http_info(app_id, **kwargs)
            return data

    def delete_menu_with_http_info(self, app_id, **kwargs):
        """
        Remove the specified app’s menu.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_menu_with_http_info(app_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str app_id: Identifies the app. (required)
        :return: MenuResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['app_id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_menu" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'app_id' is set
        if ('app_id' not in params) or (params['app_id'] is None):
            raise ValueError("Missing the required parameter `app_id` when calling `delete_menu`")


        collection_formats = {}

        path_params = {}
        if 'app_id' in params:
            path_params['appId'] = params['app_id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basicAuth', 'jwt']

        return self.api_client.call_api('/v1.1/apps/{appId}/menu', 'DELETE',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='MenuResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_menu(self, app_id, **kwargs):
        """
        Get the specified app’s menu.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_menu(app_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str app_id: Identifies the app. (required)
        :return: MenuResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_menu_with_http_info(app_id, **kwargs)
        else:
            (data) = self.get_menu_with_http_info(app_id, **kwargs)
            return data

    def get_menu_with_http_info(self, app_id, **kwargs):
        """
        Get the specified app’s menu.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_menu_with_http_info(app_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str app_id: Identifies the app. (required)
        :return: MenuResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['app_id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_menu" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'app_id' is set
        if ('app_id' not in params) or (params['app_id'] is None):
            raise ValueError("Missing the required parameter `app_id` when calling `get_menu`")


        collection_formats = {}

        path_params = {}
        if 'app_id' in params:
            path_params['appId'] = params['app_id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basicAuth', 'jwt']

        return self.api_client.call_api('/v1.1/apps/{appId}/menu', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='MenuResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update_menu(self, app_id, menu_update_body, **kwargs):
        """
        Configure the specified app’s menu.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_menu(app_id, menu_update_body, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str app_id: Identifies the app. (required)
        :param Menu menu_update_body: Body for a updateMenu request. (required)
        :return: MenuResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_menu_with_http_info(app_id, menu_update_body, **kwargs)
        else:
            (data) = self.update_menu_with_http_info(app_id, menu_update_body, **kwargs)
            return data

    def update_menu_with_http_info(self, app_id, menu_update_body, **kwargs):
        """
        Configure the specified app’s menu.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_menu_with_http_info(app_id, menu_update_body, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str app_id: Identifies the app. (required)
        :param Menu menu_update_body: Body for a updateMenu request. (required)
        :return: MenuResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['app_id', 'menu_update_body']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_menu" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'app_id' is set
        if ('app_id' not in params) or (params['app_id'] is None):
            raise ValueError("Missing the required parameter `app_id` when calling `update_menu`")
        # verify the required parameter 'menu_update_body' is set
        if ('menu_update_body' not in params) or (params['menu_update_body'] is None):
            raise ValueError("Missing the required parameter `menu_update_body` when calling `update_menu`")


        collection_formats = {}

        path_params = {}
        if 'app_id' in params:
            path_params['appId'] = params['app_id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'menu_update_body' in params:
            body_params = params['menu_update_body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basicAuth', 'jwt']

        return self.api_client.call_api('/v1.1/apps/{appId}/menu', 'PUT',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='MenuResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
