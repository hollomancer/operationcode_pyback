import pprint

from flask import Flask, request, make_response, redirect, url_for, render_template, json
from ocbot.pipeline.routing import RoutingHandler

from config.configs import configs
from ocbot.web.route_decorators import validate_response, url_verification
import logging
from ..log_manager import setup_logging

VERIFICATION_TOKEN = configs['VERIFICATION_TOKEN']

logger = logging.getLogger(__name__)
app = Flask(__name__)

# ensures tests don't call setup_logging() function
if logger.parent.level:
    setup_logging()
    logger.level = logging.DEBUG


@app.route("/zap_airtable_endpoint", methods=['POST'])
def zap_endpoint():
    data = request.get_json()
    logger.info(f'Zapier event received: {data}')
    RoutingHandler(data, route_id="new_airtable_request")
    return make_response('', 200)


@validate_response('token', VERIFICATION_TOKEN)
@app.route("/user_interaction", methods=['POST'])
def interaction_route():
    """
    Receives request from slack interactive messages.
    These are the messages that contain key: 'token_id'
    """
    data = json.loads(request.form['payload'])
    logger.info(f"Interaction received: {data}")
    # print('Interaction payload:', data)
    route_id = data['callback_id']
    RoutingHandler(data, route_id=route_id)
    return make_response('', 200)


@app.route('/event_endpoint', methods=['POST'])
@url_verification
@validate_response('token', VERIFICATION_TOKEN)
def events_route():
    """
    Any event based response will get routed here.
    Decorates first make sure it's a verified route and this isn't a challenge event
    Lastly forwards event data to route director
    """
    response_data = request.get_json()
    logger.debug(f'Event received: {json.dumps(response_data)}')
    route_id = response_data['event']['type']
    RoutingHandler(response_data, route_id=route_id)
    return make_response('', 200)


@app.route('/options_load', methods=['POST'])
def options_route():
    """
    Can provide dynamically created options for interactive messages.
    Currently unused.
    """
    return redirect(url_for('HTTP404'))


@app.route('/HTTP404')
def HTTP404():
    return render_template(url_for('HTTP404'))


def start_server():
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    start_server()
