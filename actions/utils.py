import dateutil.parser
import datetime

def get_time_from_tracked_entities(entities):
    start_time = None
    end_time = None
    for entity in entities:
        if entity['entity'] == 'time' and entity['extractor'] == 'DucklingHTTPExtractor' and 'from' in entity['value']:
            start_time = entity['value']['from']
            end_time = entity['value']['to']
            break
        elif entity['entity'] == 'time' and entity['extractor'] == 'DucklingHTTPExtractor':
            start_time = entity['value']
            start_time_datetime = dateutil.parser.parse(start_time)
            end_time_datetime = start_time_datetime + datetime.timedelta(days=1)
            end_time = end_time_datetime.isoformat()
            break
    if start_time: start_time = start_time.replace('+02:00', 'Z')
    if end_time: end_time = end_time.replace('+02:00', 'Z')
    return start_time, end_time

def get_number_from_tracked_entities(entities):
    number = None
    for entity in entities:
        if (entity['entity'] == 'number' or entity['entity'] == 'ordinal') and entity['extractor'] == 'DucklingHTTPExtractor':
            number = entity['value']
            break
    return number

def calc_reporting_time():
    reporting_time = datetime.datetime.now(datetime.timezone.utc)
    reporting_time = reporting_time - datetime.timedelta(minutes=2)
    reporting_time = reporting_time.isoformat()[0:-9] + 'Z'
    return reporting_time

def dict_to_markdown(data):
    output = ''
    for key in data:
        if isinstance(data[key], list):
            output += '**{}** \n'.format(key)
            for idx, val in enumerate(data[key]):
                output += '{}. {} \n'.format(idx, val)
        elif isinstance(data[key], dict):
            output += '**{}** \n'.format(key)
            for k, v in dict(data[key]).items():
                output += '- {}: {} \n'.format(k, v)
        else:
            output += '**{}**: {} \n'.format(key, data[key])
    return output

def format_datetime(dt_str):
    dt = dateutil.parser.parse(dt_str)
    return 'the {:%dth of %b %Y at %H:%M}'.format(dt)
