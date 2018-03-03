from flask import Flask, jsonify, request, abort
from werkzeug.exceptions import HTTPException

from db.entry import Entry
from db.event import DebitEvent, CreditEvent
from db.user import User
from db.account import Account, ACCOUNT_TYPES, DEBITED_TYPES
from db.session import get_session

session = get_session('sqlite:///sqlalchemy_example.db')


class NotFoundError(Exception):
    pass


app = Flask(__name__)


def get_user(username):
    user = session.query(User).filter(User.name == username).first()
    if user is None:
        abort(404)
    return user

def check_json(expected):
    if not request.json:
        abort(400)

    for e in expected:
        if e not in request.json:
            abort(400)

def create_event(e):
    account_uuid = e["account"]
    account = session.query(Account).filter(Account.uuid == account_uuid).first()
    if account is None:
        abort(400)

    events = {}
    if account.type in DEBITED_TYPES:
        events["increase"] = DebitEvent
        events["decrease"] = CreditEvent
    else:
        events["increase"] = CreditEvent
        events["decrease"] = DebitEvent

    value = e["value"]
    action = e["action"]

    event = events[action](value=value, account=account)
    return event

def handle_errors(func):
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            abort(502)
    return wrapped


@app.route('/<string:username>', methods=['GET'])
def user(username):
    #user = session.query(User).filter(User.name == username).first()
    user = get_user(username)
    return jsonify(user.to_dict())

@app.route('/users', methods=['GET'])
def users():
    users = [u.to_dict() for u in session.query(User)]
    d = {
        "users": users,
    }
    return (jsonify(d), 200)

@app.route('/users', methods=['POST'])
def create_user():
    #if not request.json or not 'username' in request.json:
    #    abort(400)
    #username = request.json['username']
    check_json(["username"])

    user = session.query(User).filter(User.name == username).first()
    if user is not None:
        abort(409)

    user = User(name=username)
    session.add(user)
    session.commit()
    return (jsonify(user.to_dict()), 201)

@app.route("/<string:username>/monthly", methods=['GET'])
def monthly_expenses(username):
    abort(501)

@app.route("/<string:username>/accounts", methods=['GET'])
def accounts(username):
    user = get_user(username)
    #user = session.query(User).filter(User.name == username).first()
    #if user is None:
    #    abort(404)
    accounts = [acc.to_dict(summarized=False) for acc in user.accounts]
    d = {
        "accounts": accounts,
    }
    return jsonify(d)

@app.route('/<string:username>/accounts', methods=['POST'])
def create_account(username):
    user = get_user(username)
    #user = session.query(User).filter(User.name == username).first()
    #if user is None:
    #    abort(404)

    #if (not request.json or not 'account_name' in request.json
    #    or not 'account_type' in request.json):
    #    abort(400)
    check_json(["account_name", "account_type"])
    account_name = request.json['account_name']
    account_type = request.json['account_type']

    if account_type not in ACCOUNT_TYPES:
        abort(400)

    account = Account(name=account_name, type=account_type, user=user)
    session.add(account)
    session.commit()
    return (jsonify(account.to_dict()), 201)

@app.route('/<string:username>/transactions', methods=['POST'])
@handle_errors
def create_transaction(username):
    user = get_user(username)
    check_json(["description", "date", "events"])

    events = []
    for e in request.json["events"]:
        accounting_event = create_event(e)
        session.add(accounting_event)
        events.append(accounting_event)

    entry = Entry(date=request.json["date"],
                  description=request.json["description"],
                  accounts=[e.account for e in events])
    session.add(entry)

    try:
        entry.add_events(events)
    except ValueError:
        abort(400)

    session.commit()
    return (jsonify(entry.to_dict()), 201)

@app.route("/<string:username>/total", methods=['GET'])
def total(username):
    abort(501)


if __name__ == "__main__":
    app.run("localhost", 8080)
