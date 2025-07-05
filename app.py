from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb+srv://mashookh_flask:hmSeCwTHsTOlG2D3@cluster0.pr1hyaa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['webhook_db']
events_collection = db['events']

@app.route('/')
def home():
    return 'Webhook Receiver Running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    event_type = request.headers.get('X-GitHub-Event', '').upper()
    event_doc = None

    if event_type == 'PUSH':
        event_doc = {
            'request_id': data.get('after'),
            'author': data.get('pusher', {}).get('name'),
            'action': 'PUSH',
            'from_branch': data.get('ref', '').split('/')[-1],
            'to_branch': data.get('ref', '').split('/')[-1],
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    elif event_type == 'PULL_REQUEST':
        pr = data.get('pull_request', {})
        action = data.get('action', '').upper()
        if action == 'OPENED':
            event_doc = {
                'request_id': str(pr.get('id')),
                'author': pr.get('user', {}).get('login'),
                'action': 'PULL_REQUEST',
                'from_branch': pr.get('head', {}).get('ref'),
                'to_branch': pr.get('base', {}).get('ref'),
                'timestamp': pr.get('created_at')
            }
        elif action == 'CLOSED' and pr.get('merged'):
            event_doc = {
                'request_id': str(pr.get('id')),
                'author': pr.get('user', {}).get('login'),
                'action': 'MERGE',
                'from_branch': pr.get('head', {}).get('ref'),
                'to_branch': pr.get('base', {}).get('ref'),
                'timestamp': pr.get('merged_at')
            }
    if event_doc:
        events_collection.insert_one(event_doc)
    return jsonify({'status': 'received'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(events_collection.find().sort('timestamp', -1).limit(20))
    formatted_events = []
    for event in events:
        action = event.get('action')
        author = event.get('author')
        to_branch = event.get('to_branch')
        from_branch = event.get('from_branch')
        timestamp = event.get('timestamp')
        if action == 'PUSH':
            msg = f'"{author}" pushed to "{to_branch}" on {timestamp}'
        elif action == 'PULL_REQUEST':
            msg = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
        elif action == 'MERGE':
            msg = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
        else:
            msg = f'Unknown event type'
        formatted_events.append(msg)
    return jsonify(formatted_events)

if __name__ == '__main__':
    app.run(debug=True) 