# from flask import Flask, jsonify
# from apispec import APISpec
# from apispec.ext.marshmallow import MarshmallowPlugin, Schema
# from marshmallow import fields
#
# app = Flask(__name__)
#
#
# ##Demo APi
# @app.route('/')
# def hello_world():
#     return ('hello')
#
#
# ##Spec of API
# spec = APISpec(
#     title='Flask-api-swagger-doc',
#     version='1.0.1',
#     openapi_version='3.0.2',
#     plugins=[MarshmallowPlugin()]
# )
#
#
# @app.route('/api/swagger.json')
# def create_swagger_spec():
#     return jsonify(spec.to_dict())
#
#
# class taskResponseSchema(Schema):
#     id = fields.Int()
#     title = fields.Str()
#     status = fields.Boolean()
#
#
# class listTaskSchema(Schema):
#     taskList = fields.List(fields.Nested(taskResponseSchema))
#
#
# @app.route('/task')
# def task():
#     """get list of tasks
#         ---
#         get:
#             description: get list of tasks
#             response:
#                 200:
#                     description: Return a task list
#                     content:
#                         application/json:
#                             schema: listTaskSchema
#
#     :return:
#     """
#     dummy_Data = [{
#         'id' : 1,
#         'title' : 'Finish the swagger task',
#         'status' : 'True'
#     }]
#     return listTaskSchema().dump({'taskList': dummy_Data})
#
#
# with app.test_request_context():
#     spec.path(view=task)
#


from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='swagger/templates')


@app.route('/')
def hello_world():
    return 'Hello, World'


spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


class TodoResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Boolean()


class TodoListResponseSchema(Schema):
    todo_list = fields.List(fields.Nested(TodoResponseSchema))


@app.route('/todo')
def todo():
    """Get List of Todo
    ---
    get:
        description: Get List of Todos
        responses:
            200:
                description: Return a todo list
                content:
                    application/json:
                        schema: TodoListResponseSchema
    """

    dummy_data = [{
        'id': 1,
        'title': 'Finish this task',
        'status': False
    }, {
        'id': 2,
        'title': 'Finish that task',
        'status': True
    }]

    return TodoListResponseSchema().dump({'todo_list': dummy_data})


with app.test_request_context():
    spec.path(view=todo)


@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', secure_filename(path))


if __name__ == '__main__':
    app.run(debug=True)