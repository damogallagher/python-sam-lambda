import json
from shared_opsgenie import get_alert_api
from common_code import  error_response, success_response
from opsgenie_sdk.rest import ApiException

alert_api = get_alert_api()

# Fetch Opsgenie Alerts
# See https://docs.opsgenie.com/docs/python-sdk-alert#list-alerts and
# https://docs.opsgenie.com/docs/opsgenie-python-sdk-configurations


def lambda_handler(event, context):

    try:
        limit = 100
        offset = 0
        sort = 'updatedAt'
        order = 'asc'
        search_identifier_type = 'name'
        query = 'status=open'

        response_list = []
        alert_list_length = 0
        while True:
            alert_list = alert_api.list_alerts(
                limit=limit, offset=offset, sort=sort, order=order, search_identifier_type=search_identifier_type, query=query)

            if not alert_list or len(alert_list.data) == 0:
                break

            alert_list_length = len(alert_list.data)
            offset += limit

            print("Total records:", len(alert_list.data))
            for data in alert_list.data:
                data_dict = populate_alert_data(data)
                response_list.append(data_dict)

            if alert_list_length < limit:
               break

        return success_response(json.dumps(response_list, default=str))

    except ApiException as err:
        print("Exception when calling AlertApi->list_alerts: %s\n" % err)
        return error_response("Exception when calling AlertApi->list_alerts")


def populate_alert_data(data):
    data_dict = {}
    data_dict['id'] = data.id
    data_dict['acknowledged'] = data.acknowledged
    data_dict['alias'] = data.alias
    data_dict['count'] = data.count
    data_dict['created_at'] = data.created_at

    if data.integration is not None:
        integration_dict = {}
        integration_dict['id'] = data.integration.id
        integration_dict['name'] = data.integration.name
        integration_dict['type'] = data.integration.type
        data_dict['integration'] = integration_dict
    else:
        data_dict['integration'] = data.integration

    data_dict['is_seen'] = data.is_seen
    data_dict['last_occurred_at'] = data.last_occurred_at
    data_dict['message'] = data.message
    data_dict['owner'] = data.owner
    data_dict['priority'] = data.priority

    if data.report is not None:
        report_dict = {}
        report_dict['ack_time'] = data.report.ack_time
        report_dict['acknowledged_by'] = data.report.acknowledged_by
        report_dict['close_time'] = data.report.close_time
        report_dict['closed_by'] = data.report.closed_by
        data_dict['report'] = report_dict
    else:
        data_dict['report'] = data.report

    responders_list = []
    for responder in data.responders:
        responder_dict = {}
        responder_dict['id'] = responder.id
        responder_dict['type'] = responder.type
        responders_list.append(responder_dict)
    data_dict['responders'] = responders_list

    data_dict['snoozed'] = data.snoozed
    data_dict['snoozed_until'] = data.snoozed_until
    data_dict['source'] = data.source
    data_dict['status'] = data.status
    data_dict['tags'] = data.tags
    data_dict['tiny_id'] = data.tiny_id
    data_dict['updated_at'] = data.updated_at

    return data_dict
