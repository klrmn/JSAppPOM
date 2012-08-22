#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import logging
import os
import socket
import threading
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


def pytest_funcarg__mozwebqa(request):
    mozwebqa = request.getfuncargvalue('mozwebqa')
    mozwebqa.selenium.get('%s/tests/webpage_for_test.html' % mozwebqa.base_url)
    return mozwebqa

def pytest_sessionstart(session):
    webserver = SimpleWebServer()
    webserver.start()
    WebServer.webserver = webserver

def pytest_sessionfinish(session, exitstatus):
    WebServer.webserver.stop()

def pytest_internalerror(excrepr):
    if hasattr(WebServer, 'webserver'):
        WebServer.webserver.stop()

def pytest_keyboard_interrupt(excinfo):
    if hasattr(WebServer, 'webserver'):
        WebServer.webserver.stop()


class WebServer:
    pass



LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 8000


class HtmlOnlyHandler(BaseHTTPRequestHandler):
    """Http handler."""

    def do_GET(self):
        """GET method handler."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(open('tests/webpage_for_test.html', 'r').read())

    def log_message(self, format, *args):
        """Override default to avoid trashing stderr"""
        pass


class SimpleWebServer(object):
    """A very basic web server."""

    def __init__(self, port=DEFAULT_PORT):
        self.stop_serving = False
        port = port
        while True:
            try:
                self.server = HTTPServer(
                    ('', port), HtmlOnlyHandler)
                self.port = port
                break
            except socket.error:
                LOGGER.debug("port %d is in use, trying to use next one"
                              % port)
                port += 1

        self.thread = threading.Thread(target=self._run_web_server)

    def _run_web_server(self):
        """Runs the server loop."""
        LOGGER.debug("web server started")
        while not self.stop_serving:
            self.server.handle_request()
        self.server.server_close()

    def start(self):
        """Starts the server."""
        self.thread.start()

    def stop(self):
        """Stops the server."""
        self.stop_serving = True
        try:
            # This is to force stop the server loop
            urllib.URLopener().open("http://localhost:%d" % self.port)
        except Exception:
            pass
        LOGGER.info("Shutting down the webserver")
        self.thread.join()
