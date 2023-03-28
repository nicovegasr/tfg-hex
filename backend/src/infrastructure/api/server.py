from flask import Flask

import config_modules
config_modules.add()

from infrastructure.api.controllers.algorithms import available_algorithms
from infrastructure.api.controllers.configuration import configuration_file
from infrastructure.api.controllers.performance import performance_algorithm
from infrastructure.api.controllers.description import  description
from infrastructure.api.controllers.process_files import process_files

from infrastructure.api.controllers.default import default

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return default()

app.add_url_rule('/available_algorithms', 'available_algorithms', available_algorithms, methods=['GET'])
app.add_url_rule('/configuration_file', 'configuration_file', configuration_file, methods=['GET'])
app.add_url_rule('/performance_algorithm', 'performance_algorithm', performance_algorithm, methods=['POST'])
app.add_url_rule('/description', 'description', description, methods=['GET'])
app.add_url_rule('/process_files', 'process_files', process_files, methods=['POST'])


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3000, debug=True)