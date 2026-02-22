
from flask import Blueprint, request, jsonify
from typing import Dict
from utils.validators import validate_transaction_data, validate_alert_resolution
from utils.logger import log_api_request, log_error
from datetime import datetime
import time



api = Blueprint('api', __name__)


transaction_service = None
alert_manager = None


def init_routes(txn_service, alert_mgr):

    global transaction_service, alert_manager
    transaction_service = txn_service
    alert_manager = alert_mgr


@api.route('/health', methods=['GET'])
def health_check():

    start_time = time.time()
    
    response = {
        'status': 'healthy',
        'service': 'Transaction Monitoring API',
        'timestamp': datetime.now().isoformat()
    }
    
    duration = time.time() - start_time
    log_api_request('GET', '/health', 200, duration)
    
    return jsonify(response), 200


@api.route('/api/transactions', methods=['POST'])
def create_transaction():

    start_time = time.time()
    
    try:

        data = request.get_json()
        
        if not data:
            log_api_request('POST', '/api/transactions', 400)
            return jsonify({'error': 'No JSON data provided'}), 400
        

        is_valid, error_message = validate_transaction_data(data)
        if not is_valid:
            log_api_request('POST', '/api/transactions', 400)
            return jsonify({'error': error_message}), 400
        

        result = transaction_service.process_transaction(data)
        

        duration = time.time() - start_time
        status_code = 201
        log_api_request('POST', '/api/transactions', status_code, duration)
        
        return jsonify(result), status_code
    
    except Exception as e:
        log_error("Error processing transaction", e)
        log_api_request('POST', '/api/transactions', 500)
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/api/transactions', methods=['GET'])
def get_transactions():

    start_time = time.time()
    
    try:
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        

        transactions = transaction_service.get_transactions(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        

        duration = time.time() - start_time
        log_api_request('GET', '/api/transactions', 200, duration)
        
        return jsonify({
            'count': len(transactions),
            'transactions': transactions
        }), 200
    
    except Exception as e:
        log_error("Error retrieving transactions", e)
        log_api_request('GET', '/api/transactions', 500)
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/api/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id: str):

    start_time = time.time()
    
    try:
        transaction = transaction_service.get_transaction(transaction_id)
        
        if not transaction:
            log_api_request('GET', f'/api/transactions/{transaction_id}', 404)
            return jsonify({'error': 'Transaction not found'}), 404
        
        duration = time.time() - start_time
        log_api_request('GET', f'/api/transactions/{transaction_id}', 200, duration)
        
        return jsonify(transaction), 200
    
    except Exception as e:
        log_error(f"Error retrieving transaction {transaction_id}", e)
        log_api_request('GET', f'/api/transactions/{transaction_id}', 500)
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/api/alerts', methods=['GET'])
def get_alerts():

    start_time = time.time()
    
    try:

        status = request.args.get('status')
        severity = request.args.get('severity')
        

        alerts = alert_manager.get_alerts(status=status, severity=severity)
        

        alert_dicts = [alert.to_dict() for alert in alerts]
        

        duration = time.time() - start_time
        log_api_request('GET', '/api/alerts', 200, duration)
        
        return jsonify({
            'count': len(alert_dicts),
            'alerts': alert_dicts
        }), 200
    
    except Exception as e:
        log_error("Error retrieving alerts", e)
        log_api_request('GET', '/api/alerts', 500)
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/api/alerts/<alert_id>', methods=['GET'])
def get_alert(alert_id: str):

    start_time = time.time()
    
    try:
        alert = alert_manager.get_alert_by_id(alert_id)
        
        if not alert:
            log_api_request('GET', f'/api/alerts/{alert_id}', 404)
            return jsonify({'error': 'Alert not found'}), 404
        
        duration = time.time() - start_time
        log_api_request('GET', f'/api/alerts/{alert_id}', 200, duration)
        
        return jsonify(alert.to_dict()), 200
    
    except Exception as e:
        log_error(f"Error retrieving alert {alert_id}", e)
        log_api_request('GET', f'/api/alerts/{alert_id}', 500)
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/api/alerts/<alert_id>/resolve', methods=['PUT'])
def resolve_alert(alert_id: str):

    start_time = time.time()
    
    try:

        data = request.get_json()
        
        if not data:
            log_api_request('PUT', f'/api/alerts/{alert_id}/resolve', 400)
            return jsonify({'error': 'No JSON data provided'}), 400
        

        is_valid, error_message = validate_alert_resolution(data)
        if not is_valid:
            log_api_request('PUT', f'/api/alerts/{alert_id}/resolve', 400)
            return jsonify({'error': error_message}), 400
        

        alert = alert_manager.resolve_alert(
            alert_id=alert_id,
            resolution=data['resolution'],
            reviewed_by=data['reviewed_by'],
            notes=data.get('notes')
        )
        
        if not alert:
            log_api_request('PUT', f'/api/alerts/{alert_id}/resolve', 404)
            return jsonify({'error': 'Alert not found'}), 404
        
        duration = time.time() - start_time
        log_api_request('PUT', f'/api/alerts/{alert_id}/resolve', 200, duration)
        
        return jsonify(alert.to_dict()), 200
    
    except Exception as e:
        log_error(f"Error resolving alert {alert_id}", e)
        log_api_request('PUT', f'/api/alerts/{alert_id}/resolve', 500)
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/api/reports/daily', methods=['GET'])
def daily_report():

    start_time = time.time()
    
    try:

        date_str = request.args.get('date', datetime.now().date().isoformat())
        

        start_datetime = f"{date_str}T00:00:00"
        end_datetime = f"{date_str}T23:59:59"
        
        transactions = transaction_service.get_transactions(
            start_date=start_datetime,
            end_date=end_datetime
        )
        

        all_alerts = alert_manager.db.execute_query(
            "SELECT * FROM alerts WHERE timestamp >= ? AND timestamp <= ?",
            (start_datetime, end_datetime)
        )
        

        total_volume = sum(txn['amount'] for txn in transactions)
        

        alerts_by_severity = {}
        for alert in all_alerts:
            severity = alert['severity']
            alerts_by_severity[severity] = alerts_by_severity.get(severity, 0) + 1
        

        alerts_by_rule = {}
        for alert in all_alerts:
            rule = alert['rule_name']
            alerts_by_rule[rule] = alerts_by_rule.get(rule, 0) + 1
        
        report = {
            'date': date_str,
            'total_transactions': len(transactions),
            'total_volume': total_volume,
            'alerts_triggered': len(all_alerts),
            'alerts_by_severity': alerts_by_severity,
            'alerts_by_rule': alerts_by_rule
        }
        
        duration = time.time() - start_time
        log_api_request('GET', '/api/reports/daily', 200, duration)
        
        return jsonify(report), 200
    
    except Exception as e:
        log_error("Error generating daily report", e)
        log_api_request('GET', '/api/reports/daily', 500)
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/api/users/<user_id>/stats', methods=['GET'])
def get_user_stats(user_id: str):

    start_time = time.time()
    
    try:
        stats = transaction_service.get_user_statistics(user_id)
        
        duration = time.time() - start_time
        log_api_request('GET', f'/api/users/{user_id}/stats', 200, duration)
        
        return jsonify(stats), 200
    
    except Exception as e:
        log_error(f"Error getting stats for user {user_id}", e)
        log_api_request('GET', f'/api/users/{user_id}/stats', 500)
        return jsonify({'error': 'Internal server error'}), 500


