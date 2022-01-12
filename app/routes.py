from flask import request, Response

from app import bp
from app import data_preprocessor
from app.nalog_worker import NalogWorker
from utility_methods.response_objects import Inn, Suspension


@bp.route('/inn', methods=['POST'])
def fetch_inn():
    try:
        data = request.get_json()
    except Exception:
        return Response(response=Inn(None, 'Введены не все поля').to_json(), status=200)
    try:
        if data_preprocessor.inn_json_is_correct(data):
            nalog_worker = NalogWorker()
            return Response(response=nalog_worker.fetch_inn(
                data_preprocessor.prepare_inn_json(data)).to_json(), status=200)
        return Response(response=Inn(None, 'Введены не все поля').to_json(), status=200)
    except Exception as e:
        return Response(response=Inn(None, e.__str__()).to_json(), status=200)


@bp.route('/suspension', methods=['POST'])
def fetch_suspension():
    try:
        data = request.get_json()
    except Exception:
        return Response(response=Suspension(None, None, 'Введены не все поля').to_json(), status=200)
    try:
        if data_preprocessor.suspension_json_is_correct(data):
            nalog_worker = NalogWorker()
            return Response(response=nalog_worker.fetch_suspension(
                data_preprocessor.prepare_suspension_json(data)).to_json(), status=200)
        return Response(response=Suspension(None, None, 'Введены не все поля').to_json(), status=200)
    except Exception as e:
        return Response(response=Suspension(None, None, e.__str__()).to_json(), status=200)
