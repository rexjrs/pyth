from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from auth import auth, identity
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)
jwt = JWT(app, auth, identity)
items = []
db = pymysql.connect(
    host='172.104.41.128',
    user='thomasch_admin',
    password='Zooper125',
    db='thomasch_pyth'
)

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return { 'item': item }, 200 if item else 500

    def post(self, name):
        data = request.get_json(force=True)
        if next(filter(lambda x: x['name'] == data['name'], items), None) is not None:
            return { 'message': 'An item with the name "{}" already exists.'.format(data['name']) }, 400
        item = { 'name': data['name'], 'price': data['price'] }
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return { 'message': 'Item deleted' }

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type=float,
            required=True,
            help='This field cannot be left blank'
        )
        data = parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = { 'name': name, 'price': data['price'] }
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return { 'items': items }

class Test(Resource):
    def post(self, name):
        try:
            with db.cursor() as cursor:
                sql = "INSERT INTO users (username, password) VALUES ('test', 'asdasd')"
                cursor.execute(sql)
                db.commit()
        finally:
            return { 'name': name }
            

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Test, '/test/<string:name>')
app.debug = True
app.run(port=3000)