
#!/usr/bin/env python3

from flup.server.fcgi import WSGIServer
import main

if __name__ == '__main__':
    WSGIServer(application, bindAddress='/tmp/fcgi.sock').run()