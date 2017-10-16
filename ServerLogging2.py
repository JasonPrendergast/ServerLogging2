from bottle import Bottle, ServerAdapter, route, run, request
import logging, logging.handlers

# Make a global logging object.
x = logging.getLogger("logfun")
x.setLevel(logging.DEBUG)

# This handler writes everything to a file.
h1 = logging.FileHandler("myapp.txt")
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h1.setFormatter(f)
h1.setLevel(logging.DEBUG)
x.addHandler(h1)

# This handler emails me anything that is an error or worse.
#h2 = logging.handlers.SMTPHandler('localhost', 'j1mbob200@example.com', ['j1mbob200@yahoo.com'], 'ERROR log')
#h2.setLevel(logging.DEBUG)
#h2.setFormatter(f)
#x.addHandler(h2)


class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # self.server.server_close() <--- alternative but causes bad fd exception
        self.server.shutdown()
listen_addr='127.0.0.1'

listen_port=10001
app = Bottle()
server = MyWSGIRefServer(host=listen_addr, port=listen_port)
#####################################################################
#                       START APP HERE                              #
#####################################################################
tf_log = 'tf.log'
#http://127.0.0.1:10001/calculate?number1=7659&number2=7762&operation=addition
@app.route('/calculate')
def index():
#    http://blog.tplus1.com/blog/2007/09/28/the-python-logging-module-is-much-better-than-print-statements/
    logfun = logging.getLogger("logfun")

    #https://stackoverflow.com/questions/31405812/how-to-get-client-ip-address-using-python-bottle-framework
    client_ip = request.environ.get('REMOTE_ADDR')
    logfun.debug(client_ip)
    if request.GET.get('operation') == 'addition':
        Tempstring = str(int(request.GET.get('number1')) + int(request.GET.get('number2')))
        try:
            Count = int(open(tf_log,'r').read().split('\n')[-2])+1
        except Exception as ex:
            logfun.exception("Something awful happened!")
            logfun.debug("Finishing f!")
            Count=1
        #Count =+ Count+1
        with open(tf_log,'a') as f:
                f.write(str(Count)+'\n')
        print(Count)
        #Count++
        if Count == 10:
            server.stop()
        return Tempstring#str(int(request.GET.get('number1')) + int(request.GET.get('number2')))
    else:
        return 'Unsupported operation'



#####################################################################
#                       APP ENDS HERE                               #
#####################################################################
try:
    app.run(server=server)
except Exception.ex:
    print (ex)

