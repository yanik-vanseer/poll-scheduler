# Defined routes for other services to communicate with from outside the flask application

from flask import Blueprint, request, jsonify
from app.services.poll_service import addPoll, addVote

poll_bp = Blueprint('poll_bp', __name__)

@poll_bp.route('/create', methods=['POST'])
def createPoll():
    try:
        data = request.get_json()
        sender = data.get('sender')
        emails = data.get('emails')
        dates = data.get('dates')

        poll_id = addPoll(sender, emails, dates)

        return jsonify({'status': 'ok', 'poll_id': poll_id}), 201
    except ValueError as ve:
        return jsonify({'status': 'error', 'message': str(ve)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@poll_bp.route('/vote', methods=['POST'])
def voteOnPoll():
    try:
            data = request.get_json()
            poll_id = data.get('poll_id')
            voter_email = data.get('sender')
            selected_dates = data.get('selected_dates')
            
            vote_id = addVote(poll_id, voter_email, selected_dates)

            return jsonify({'status': 'ok', 'vote_id': vote_id}), 201
    except ValueError as ve:
        return jsonify({'status': 'error', 'message': str(ve)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500