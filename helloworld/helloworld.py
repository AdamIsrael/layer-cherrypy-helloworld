#!/usr/bin/env python3
import cherrypy
import os


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"


if __name__ == "__main__":
    hellocfg = os.path.join(os.path.dirname(__file__), 'helloworld.conf')

    cherrypy.quickstart(HelloWorld(), config=hellocfg)
