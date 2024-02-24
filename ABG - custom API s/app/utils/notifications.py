from app import mongo
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import DESCENDING


def send_notification(notification_data):
    if notification_data:
        add_notification = mongo.db.notification.insert_one(notification_data)
        return True
    else:
        return False


def create_notification_data(metadata, current_user):
    if metadata:
        screen_info = {}
        details = {}
        if metadata['status'] == 'NEW':
            screen_info['screen_type'] = ''
            title = 'Ticket Created !!!'
            message = 'New ticket got created !!!'
            send_to = ''
        elif metadata['status'] == 'CONFIRMED':
            screen_info['screen_type'] = ''
            title = 'Ticket Confirmed'
            message = 'The ticket got confirmed !!!'
            send_to = ''
        elif metadata['status'] == 'CANCELLED':
            screen_info['screen_type'] = ''
            title = 'Ticket Cancelled'
            message = 'The ticket got cancelled !!!'
            send_to = ''
        elif metadata['status'] == 'PAID':
            screen_info['screen_type'] = ''
            title = 'Payment is Done'
            message = 'The payment is Done !!!'
            send_to = ''
        elif metadata['status'] == 'UNPAID':
            screen_info['screen_type'] = ''
            title = 'Payment is not Done'
            message = 'The payment is not done !!!'
            send_to = ''
        elif metadata['status'] == 'PARTIALLY_PAID':
            screen_info['screen_type'] = ''
            title = 'Payment is Partially Done'
            message = 'The payment is partially done !!!'
            send_to = ''
        elif metadata['status'] == 'VEHICLE_ASSIGNED':
            screen_info['screen_type'] = ''
            title = 'Vehicle Assigned'
            message = 'The required vehicle is assigned !!!'
            send_to = ''
        elif metadata['status'] == 'AUDITOR_ASSIGNED':
            screen_info['screen_type'] = ''
            title = 'Auditor Assigned'
            message = 'The auditor got assigned !!!'
            send_to = ''
        elif metadata['status'] == 'RESCHEDULE_AUDIT':
            screen_info['screen_type'] = ''
            title = 'Rescheduling Request By Auditor '
            message = 'The auditor has requested for rescheduling the auditing !!!'
            send_to = ''
        elif metadata['status'] == 'REJECT':
            screen_info['screen_type'] = ''
            title = 'Auditing Got Rejected'
            message = 'The auditing got rejected by the supplier.Now a new schedule is required!!!'
            send_to = ''
        elif metadata['status'] == 'ACCEPT':
            screen_info['screen_type'] = ''
            title = 'Auditing Got Accepted'
            message = 'The auditing got accepted by the supplier!!!'
            send_to = ''
        elif metadata['status'] == 'AUDIT_STARTED':
            screen_info['screen_type'] = ''
            title = 'Audit has Started'
            message = 'The auditing got started!!!'
            send_to = ''
        elif metadata['status'] == 'PACKED':
            screen_info['screen_type'] = ''
            title = 'Packing is completed'
            message = 'The packing is completed!!!'
            send_to = ''
        elif metadata['status'] == 'AUDIT_COMPLETED':
            screen_info['screen_type'] = ''
            title = 'Audit has Completed'
            message = 'The auditing has completed!!!'
            send_to = ''
        elif metadata['status'] == 'FPE_ASSIGNED':
            screen_info['screen_type'] = ''
            title = 'FPE Got Assigned'
            message = 'The FPE got assigned by the operation manager!!!'
            send_to = ''
        elif metadata['status'] == 'RESCHEDULE_FPE':
            screen_info['screen_type'] = ''
            title = 'Rescheduling Request By FPE '
            message = 'The FPE has requested for rescheduling !!!'
            send_to = ''
        elif metadata['status'] == 'PICKUP_LOCATION_VERIFIED':
            screen_info['screen_type'] = ''
            title = 'Pickup Location is Verified'
            message = 'The pickup location is verified !!!'
            send_to = ''
        elif metadata['status'] == 'PICKUP':
            screen_info['screen_type'] = ''
            title = 'Pickup has Started'
            message = 'The pickup has started !!!'
            send_to = ''
        elif metadata['status'] == 'PICKUP_COMPLETED':
            screen_info['screen_type'] = ''
            title = 'Pickup has Completed'
            message = 'The pickup has completed !!!'
            send_to = ''
        elif metadata['status'] == 'UNLOADED':
            screen_info['screen_type'] = ''
            title = 'Unload is Done'
            message = 'The unloading is done !!!'
            send_to = ''
        elif metadata['status'] == 'COMPLETED':
            screen_info['screen_type'] = ''
            title = 'Request is Completed'
            message = 'The request is completed !!!'
            send_to = ''
        elif metadata['status'] == 'RECEIVED':
            screen_info['screen_type'] = ''
            title = 'Products Received'
            message = 'The products got received !!!'
            send_to = ''
        else:
            return 400, 'Invalid notification status', {}
        screen_info['ticket_id'] = metadata['ticket_id']
        details['meta_data'] = screen_info
        print("###########",ObjectId(current_user))
        notification_data = {'user_id': ObjectId(current_user), 'type': '', 'title': title,
                             'description': message,
                             'read_status': False,
                             'datetime': str(datetime.now()),
                             'meta_data': details['meta_data'], 'send_to': send_to}
        return notification_data
    else:
        return None


def get_notification_list(current_user):
    notification_list = mongo.db.notification.find({'user_id': ObjectId(current_user['data']['_id'])}).sort('datetime', DESCENDING)
    if notification_list:
        result = []
        for notify in notification_list:
            result.append(notify)
        return 200, 'Notification list', result, {}
    else:
        return 400, 'No notification found', {}


def mark_all_read(current_user, notification_id):
    # If notification_id is provided, update only those notifications
    if notification_id:
        existing_notify = mongo.db.notification.find({'_id':ObjectId(notification_id)})
        if existing_notify:
            mongo.db.notification.update_one(
                {'_id': ObjectId(notification_id)},
                {'$set': {'read_status': True}}
            )
            return 200, 'Marked selected notifications as read', {}
        else:
            return 400, 'No notification found', {}

    # If notification_id is not provided, update all notifications for the user
    all_notify = mongo.db.notification.find({'user_id': ObjectId(current_user['data']['_id'])})
    if mark_all_read:
        for notify in all_notify:
            mongo.db.notification.update_one(
                {'_id': notify['_id']},
                {'$set': {'read_status': True}}
            )
        return 200, 'Marked all notifications as read', {}
    else:
        return 400, 'No notification found', {}



