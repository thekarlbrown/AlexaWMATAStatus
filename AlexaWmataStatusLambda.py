import requests

api_key_file = open('api_key', 'r')
api_key = api_key_file.readlines()[0].rstrip()
station_prediction_url = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/'
wmata_get_parameters = { 'api_key': api_key }
train_color_conversions = { 'Red': 'RD', 'Blue': 'BL', 'Orange': 'OR', 'Silver': 'SV', 'Yellow': 'YL', 'Green': 'GR' }
train_station_conversions= {}
train_station_to_api_code = { 'Metro Center': 'A01', 'Farragut North': 'A02', 'Dupont Circle': 'A03', 'Woodley Park-Zoo/Adams Morgan': 'A04', 'Cleveland Park': 'A05',
 'Van Ness-UDC': 'A06', 'Tenleytown-AU': 'A07', 'Friendship Heights': 'A08', 'Bethesda': 'A09', 'Medical Center': 'A10', 'Grosvenor-Strathmore': 'A11', 'White Flint': 'A12',
  'Twinbrook': 'A13', 'Rockville': 'A14', 'Shady Grove': 'A15', 'Gallery Pl-Chinatown': 'B01', 'Judiciary Square': 'B02', 'Union Station': 'B03',
   'Rhode Island Ave-Brentwood': 'B04', 'Brookland-CUA': 'B05', 'Fort Totten': 'B06', 'Takoma': 'B07', 'Silver Spring': 'B08', 'Forest Glen': 'B09', 'Wheaton': 'B10',
    'Glenmont': 'B11', 'NoMa-Gallaudet U': 'B35', 'Metro Center': 'C01', 'McPherson Square': 'C02', 'Farragut West': 'C03', 'Foggy Bottom-GWU': 'C04', 'Rosslyn': 'C05',
     'Arlington Cemetery': 'C06', 'Pentagon': 'C07', 'Pentagon City': 'C08', 'Crystal City': 'C09', 'Ronald Reagan Washington National Airport': 'C10', 'Braddock Road': 'C12',
      'King St-Old Town': 'C13', 'Eisenhower Avenue': 'C14', 'Huntington': 'C15', 'Federal Triangle': 'D01', 'Smithsonian': 'D02', 'L\'Enfant Plaza': 'D03',
       'Federal Center SW': 'D04', 'Capitol South': 'D05', 'Eastern Market': 'D06', 'Potomac Ave': 'D07', 'Stadium-Armory': 'D08', 'Minnesota Ave': 'D09', 'Deanwood': 'D10',
        'Cheverly': 'D11', 'Landover': 'D12', 'New Carrollton': 'D13', 'Mt Vernon Sq 7th St-Convention Center': 'E01', 'Shaw-Howard U': 'E02',
         'U Street/African-Amer Civil War Memorial/Cardozo': 'E03', 'Columbia Heights': 'E04', 'Georgia Ave-Petworth': 'E05', 'Fort Totten': 'E06', 'West Hyattsville': 'E07',
          'Prince George\'s Plaza': 'E08', 'College Park-U of Md': 'E09', 'Greenbelt': 'E10', 'Gallery Pl-Chinatown': 'F01', 'Archives-Navy Memorial-Penn Quarter': 'F02',
           'L\'Enfant Plaza': 'F03', 'Waterfront': 'F04', 'Navy Yard-Ballpark': 'F05', 'Anacostia': 'F06', 'Congress Heights': 'F07', 'Southern Avenue': 'F08',
            'Naylor Road': 'F09', 'Suitland': 'F10', 'Branch Ave': 'F11', 'Benning Road': 'G01', 'Capitol Heights': 'G02', 'Addison Road-Seat Pleasant': 'G03', 'Morgan Boulevard': 'G04',
             'Largo Town Center': 'G05', 'Van Dorn Street': 'J02', 'Franconia-Springfield': 'J03', 'Court House': 'K01', 'Clarendon': 'K02', 'Virginia Square-GMU': 'K03', 'Ballston-MU': 'K04',
              'East Falls Church': 'K05', 'West Falls Church-VT/UVA': 'K06', 'Dunn Loring-Merrifield': 'K07', 'Vienna/Fairfax-GMU': 'K08', 'McLean': 'N01',
               'Tysons Corner': 'N02', 'Greensboro': 'N03', 'Spring Hill': 'N04', 'Wiehle-Reston East': 'N06' }

def return_full_alexa_wmata_response(startStation, endStation, trainColor):
    api_results_json = form_and_return_api_call(startStation)
    train_color_code = train_color_conversions[trainColor]
    if endStation in train_station_conversions:
        endStation = train_station_conversions[endStation]
    alexa_response = ''
    for car in api_results_json:
        if train_color_code == car['Line'] and endStation == car['DestinationName']:
            alexa_response += f"{trainColor} train toward {endStation} in {car['Min']} minutes. "
    if len(alexa_response) == 0:
        alexa_response = f"There are no {trainColor} trains at {startStation} Metro Station towards {endStation}. "
    return alexa_response

def form_and_return_api_call(startStation):
    if startStation in train_station_conversions:
        startStation = train_station_conversions[startStation]
    station_code_for_api = train_station_to_api_code[startStation]
    api_results_json = requests.get(station_prediction_url + station_code_for_api, wmata_get_parameters).json()
    return api_results_json['Trains']

def lambda_handler(event, context):

    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.e36d5c7c-db76-4d38-b7e3-fbc30b94c498"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print ('Starting new session.')

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetInfo":
        return get_app_info()
    elif intent_name == "GetTrainStatus":
        return get_train_status(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_app_info()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print ('Ending session.')
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "WMATA Status - Goodbye"
    speech_output = "Goodbye"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_app_info():
    session_attributes = {}
    card_title = "About WMATA Status"
    reprompt_text = ""
    should_end_session = False

    speech_output = "This is the Alexa Skill to provide you with the status of trains at Metro Stops in the WMATA Metro system. For example, ask Alexa for the Silver Line Trains at the McLean Metro Stop towards Wiehle-Reston East."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_train_status(intent):
            session_attributes = {}
            card_title = "WMATA Status Info"
            speech_output = "I'm not sure what train status you want to hear about. " \
                            "For example, ask Alexa for the Silver Line Trains at the McLean Metro Stop towards Wiehle-Reston East."
            reprompt_text = "I'm not sure what train status you want to hear about. " \
                            "For example, ask Alexa for the Silver Line Trains at the McLean Metro Stop towards Wiehle-Reston East."
            should_end_session = False

            if "TrainColor" in intent["slots"] and "StartingStation" in intent["slots"] and "EndingStation" in intent["slots"]:
                start_station = intent["slots"]["StartingStation"]["value"]
                end_station = intent["slots"]["EndingStation"]["value"]
                train_color = intent["slots"]["TrainColor"]["value"]

                speech_output = return_full_alexa_wmata_response(start_station, end_station, train_color)
                reprompt_text = ""

            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
