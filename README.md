# Overview

This charm provides an example of deploying a simple http server, powered by [cherrypy](https://cherrypy.org/) via a charm.

# Usage

Step by step instructions on using the charm:

```
$ juju deploy cs:~aisrael/cherrypy-helloworld
```

You can then browse to http://ip-address:port to view the service.

## Known Limitations and Issues

This is an example charm, not intended for production use.

# Configuration

It's useful to expose configurable options using `config.yaml`. In this case, we have the option to change the port that cherrypy will listen to.

For example, if we wanted to listen on port 8080, instead of the default port 80, we could inform the charm of this:
```
juju config cherrypy-helloworld http-port=8080
```

# Contact Information

For any issues or questions, please see [Github](https://github.com/AdamIsrael/layer-cherrypy-helloworld).
