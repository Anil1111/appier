#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
#
# This file is part of Hive Appier Framework.
#
# Hive Appier Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Appier Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Appier Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import threading

import appier

class AsyncNeoApp(appier.App):

    def __init__(self, *args, **kwargs):
        appier.App.__init__(
            self,
            name = "async_neo",
            *args, **kwargs
        )

    @appier.route("/async", "GET")
    @appier.route("/async/hello", "GET")
    async def hello(self):
        partial = self.field("partial", True, cast = bool)
        handler = self.handler_partial if partial else self.handler
        await appier.header_a()
        await appier.await_yield("before\n")
        await handler()
        await appier.await_yield("after\n")

    @appier.route("/async/http", "GET")
    async def http(self):
        url = self.field("url", "https://www.flickr.com/")
        delay = self.field("delay", 0.0, cast = float)
        self.request.content_type = "text/html"
        await appier.header_a()
        await appier.sleep(delay)
        await appier.await_wrap(appier.get_a(url))

    async def handler(self):
        thread = threading.current_thread()
        print("executing in %s" % thread)
        message = "hello world\n"
        timeout = await appier.sleep(3.0)
        message += "timeout: %.2f\n" % timeout
        result = await self.calculator(2, 2)
        message += "result: %d\n" % result
        await appier.await_yield("hello world\n")

    async def handler_partial(self):
        await appier.await_yield("hello world\n")
        timeout = await appier.sleep(3.0)
        await appier.await_yield("timeout: %.2f\n" % timeout)
        result = await self.calculator(2, 2)
        await appier.await_yield("result: %d\n" % result)

    async def calculator(self, *args, **kwargs):
        print("computing...")
        await appier.sleep(3.0)
        print("finished computing...")
        return sum(args)

app = AsyncNeoApp()
app.serve()
