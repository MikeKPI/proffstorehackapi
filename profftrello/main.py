from flask import redirect, url_for, session, request, g, flash, jsonify

from flask_restful import Api, Resource
from app import app, trelloapp
from helpers import login_required


api = Api(app)

@app.route('/')
@app.route('/index')
@login_required
def index():
    resp = trelloapp.request("members/me")
    if resp.status == 200:
        print type(resp.data)
        return jsonify(me=resp.data)
    return jsonify(error="")

@trelloapp.tokengetter
def get_trello_token():
    print(session)
    if 'trello_oauth' in session:
        resp = session['trello_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@app.before_request
def before_request():
    g.user = None
    if 'trello_oauth' in session:
        g.user = session['trello_oauth']

@app.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return trelloapp.authorize(callback=callback_url or request.referrer or None)

@app.route('/logout')
def logout():
    session.pop('trello_oauth', None)
    return redirect(url_for('index'))

@app.route('/oauthorized')
def oauthorized():
    resp = trelloapp.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['trello_oauth'] = resp
    return redirect(url_for('index'))


# @app.route("/boards/<board_id>")
# @login_required
# def boards(board_id):
#     resp = trelloapp.request("boards/" + str(board_id))
#     print "RESPONSE: ", resp.status
#     if resp.status == 200:
#         board = resp.data
#         jsonify(boards=board)
#     else:
#         flash('Unable to load board from Trello.')
#     return jsonify(error="Board is private or does not exists.")


@app.route("/ping")
def ping():
    return jsonify(ping="pong")


def parse_my_boards(myinfo):
    return list(myinfo.get("idBoards", ""))


class Board(Resource):
    prefix = "boards/"

    @login_required
    def get(self, board_id):
        resp = trelloapp.request(self.prefix + board_id)
        if resp.status == 200:
            return {"board": resp.data}, 200
        return {"error": "Cant get board %s" % board_id}, 500


class BoardLists(Resource):
    prefix = "boards/"

    @login_required
    def get(self, board_id):
        resp = trelloapp.request(self.prefix + board_id + "/lists")
        if resp.status == 200:
            return {"lists": resp.data}, 200
        return {"error": "Cant get board %s" % board_id}, 500


class MyBoardsIds(Resource):
    prefix = "boards/"

    @login_required
    def get(self):
        my_info = trelloapp.request("members/me")
        if my_info.status == 200:
            boards = parse_my_boards(my_info.data)
            return {"boards": boards}, 200
        return {"error": "Cant get boards"}, 404


class Lists(Resource):
    prefix = "lists/"

    @login_required
    def get(self, list_id):
        resp = trelloapp.request(self.prefix + list_id)
        if resp.status == 200:
            return {"lists": resp.data}, 200
        return {"error", "Cant get board lists for %s board" % list_id}, 404




api.add_resource(MyBoardsIds, "/boards")
api.add_resource(BoardLists, "/boards/<string:board_id>/lists")
api.add_resource(Board, "/boards/<string:board_id>")
api.add_resource(Lists, "/lists/<list_id>")

if __name__ == '__main__':
    app.run(port=8080)
