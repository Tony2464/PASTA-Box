from flask import Blueprint, request, jsonify
from flask_http_response import success, error
from werkzeug.security import generate_password_hash, check_password_hash

# Local
import database.db_config as config
from database import db_manager


def initDb():
    dbManager = db_manager.DbManager(
        config.dbConfig["user"],
        config.dbConfig["password"],
        config.dbConfig["host"],
        config.dbConfig["port"],
        config.dbConfig["database"]
    )
    return dbManager


user = Blueprint("user", __name__)


# GET ALL

@user.route('/', methods=['GET'])
def apiGetDevices():
    dbManager = initDb()
    data = dbManager.queryGet("SELECT * FROM User", [])
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["email"] = row[1]
        d["firstname"] = row[3]
        d["surname"] = row[4]
        d["admin"] = row[5]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)

# GET ONE


@user.route('/', methods=['GET'])
@user.route('/<id>', methods=['GET'])
def apiGetDevice(id=None):
    dbManager = initDb()
    data = dbManager.queryGet("SELECT * FROM User WHERE id = ?", [id])
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["email"] = row[1]
        d["firstname"] = row[3]
        d["surname"] = row[4]
        d["admin"] = row[5]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)


@user.route('/login', methods=['POST'])
def login():
    if request.form['email'] and request.form['password']:
        email = request.form['email']
        password = request.form['password']
        dbManager = initDb()
        data = dbManager.queryGet(
            "SELECT * FROM User WHERE email = ?", [email])
        user = []
        for row in data:
            d = {}
            d["id"] = row[0]
            d["email"] = row[1]
            d["password"] = row[2]
            d["firstname"] = row[3]
            d["surname"] = row[4]
            d["admin"] = row[5]
            user.append(d)
        dbManager.close()
        # Check if user exists
        if user:
            # Check password
            if check_password_hash(user[0]["password"], password):
                return jsonify(user)
            else:
                return error.return_response(status=403, message="Wrong password")
        else:
            return error.return_response(status=404, message="User not found")
    else:
        return error.return_response(status=400, message="Need email and password")

    # session['logged_in'] = True
    # token = jwt.encode(
    #     {
    #         "user": request.form['email'],
    #         "expiration": str(datetime.datetime.utcnow() + datetime.timedelta(seconds=12000))
    #     },
    #     current_app.config['SECRET_KEY'],
    #     algorithm="HS256"
    # )
    # resp = make_response()
    # resp.set_cookie('token', token, httponly=True)
    # return resp
    # return "HI"


@user.route('/register', methods=['POST'])
def register():
    if request.json:
        dbManager = initDb()
        user = request.get_json()

        # Check if user exists
        data = dbManager.queryGet(
            "SELECT * FROM User WHERE email = ?", [user["email"]])
        userDb = []
        for row in data:
            d = {}
            d["id"] = row[0]
            userDb.append(d)
        if userDb:
            return error.return_response(status=409, message="User exists already")
        else:
            # Check to do with all json data
            hashed_password = generate_password_hash(
                user['password'], method='sha256')

            dbManager.queryInsert("INSERT INTO `User` (`email`, `password`, `firstname`, `surname`, `admin`) VALUES (?, ?, ?, ?, ?)",
                                  [
                                      user["email"],
                                      hashed_password,
                                      user["firstname"],
                                      user["surname"],
                                      user["admin"]
                                  ])
            dbManager.close()
            return success.return_response(status=201, message="User added successfully")
    else:
        return error.return_response(status=400, message="Need JSON data")
