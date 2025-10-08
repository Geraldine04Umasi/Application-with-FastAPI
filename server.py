from wsgiref.simple_server import make_server
from jinja2 import Environment, FileSystemLoader   


#env diccionario con info de la peticion
#start_response funcion que inicia la respuesta
def application(env, start_response):
    headers = [('Content-Type', 'text/html')]
    start_response('200 OK', headers)

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    HTML = template.render(title="Mi Primer Servidor WSGI", name="Geraldine")
    return [bytes(HTML, 'utf-8')] 


server = make_server('localhost', 8000, application)
server.serve_forever()