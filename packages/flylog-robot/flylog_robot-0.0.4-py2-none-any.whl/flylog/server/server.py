#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来作为接受log传递的agent
通过udp通道。

不使用 gevent，因为测试了 gevent 对 smtplib 似乎没法异步，还是会阻塞
"""

from __future__ import unicode_literals

import logging.config
import json
from collections import defaultdict

from .six import socketserver, _thread
from .utils import import_string
from .log import logger


class Server(object):
    backend_dict = None

    def __init__(self, config=None):
        self.config = config
        if hasattr(config, 'LOGGING'):
            logging.config.dictConfig(config.LOGGING)

        self.backend_dict = dict()
        for name, backend_conf in self.config.BACKENDS.items():
            _class = import_string(backend_conf['class'])
            backend = _class(**backend_conf['init_data'])

            self.backend_dict[name] = backend

    @staticmethod
    def is_exist_filter_keyword(source, keyword_filter_list):
        for keyword in keyword_filter_list:
            if keyword in source:
                return True
        return False

    def handle_message(self, message, address):
        recv_dict = json.loads(message)

        source = recv_dict.get('source')
        title = '[%s]Attention!' % source
        content = recv_dict.get('content')

        logger.info('%s\n%s', title, content)

        role_list = recv_dict.get('role_list') or ('default',)

        # backend_name -> params
        merged_backends = defaultdict(dict)

        for role in role_list:
            handler_list = self.config.ROLES.get(role)
            if handler_list is None:
                continue

            for handler in handler_list:
                backend_name = handler['backend']
                params = handler['params']
                if self.is_exist_filter_keyword(source, handler['keyword_filter_list']):
                    continue

                merged_backends[backend_name] = self._merge_backend_params(
                    merged_backends[backend_name],
                    params
                )

        for backend_name, params in merged_backends.items():
            _thread.start_new_thread(self._process_backend_emit, (backend_name, params, title, content))

    def _merge_backend_params(self, params1, params2):
        """
        因为有可能不同role之间对应同样的发送人，为了避免重复，所以需要合并
        """

        merged_keys = set(params1.keys()) | set(params2.keys())
        merged_params = dict()

        for key in merged_keys:
            value1 = params1.get(key) or list()
            value2 = params2.get(key) or list()

            merged_params[key] = list(set(value1) | set(value2))

        return merged_params

    def _process_backend_emit(self, backend_name, params, title, content):
        """
        为了支持单独线程，所以独立出来
        """
        backend = self.backend_dict[backend_name]

        try:
            if not backend.emit(title, content, **params):
                logger.error('emit error. backend: %s, params: %s, title: %s, content: %s',
                             backend_name, params, title, content)
        except:
            logger.error('exc occur. backend: %s, params: %s, title: %s, content: %s',
                         backend_name, params, title, content, exc_info=True)

    def run(self, host, port):
        class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
            def handle(sub_self):
                message = sub_self.request[0]
                try:
                    self.handle_message(message, sub_self.client_address)
                except:
                    logger.error('exc occur. message: %r, address: %s', message, sub_self.client_address, exc_info=True)

        class MyUDPServer(socketserver.ThreadingUDPServer):
            daemon_threads = True
            allow_reuse_address = True

        logger.info('running on %s:%s', host, port)

        server = MyUDPServer((host, port), ThreadedUDPRequestHandler)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)
