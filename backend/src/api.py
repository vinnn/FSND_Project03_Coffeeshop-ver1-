import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.order_by(Drink.id).all()
    except:
        abort(422)

    drink_array = [drink.short() for drink in drinks]

    print('this is drinks:' + str(drinks))
    return jsonify({
        'success': True,
        'drinks': drink_array
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.order_by(Drink.id).all()
    except:
        abort(422)
    
    #print('BEFORE DRINK_ARRAY')
    drink_array = [drink.long() for drink in drinks]
    #print('AFTER DRINK_ARRAY')
    print('this is drinks:' + str(drinks))
    return jsonify({
        'success': True,
        'drinks': drink_array
    })



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def post_drinks(payload):   # *args, **kwargs): 

    body = request.get_json()
    print('body22 : ' + str(body))

   # body2 = json.loads(json.dumps(request.get_data()))
   # print('body2 : ' + body2)

#    new_id = body.get('id', None)
    new_title = body.get("title", None)
    new_recipe = body.get("recipe", None)
    #new_recipe = """{}""".format(body['recipe'])

    print('new_title22 : ' + new_title)
    print('new_recipe22(before jsonloads) : ')
    print(new_recipe)


    try:
        new_drink = Drink(
            title=new_title, 
            recipe=json.dumps(new_recipe)
            )
        new_drink.insert()

        return jsonify({
            'success': True,
            'drinks': new_drink.long()
        }, 200)

    except:
        abort(422)
        

    #new_recipe2 = """{}""".format(body['recipe'])
#    new_recipe2 = json.loads(new_recipe)
 #   new_recipe2 = json.dumps(new_recipe)
  #  new_recipe2 = json.dumps(new_recipe)

  #  print('new_recipe22(after jsonloads) : ')
  #  print(new_recipe2)

    # json.loads

  #  new_drink = Drink(
  #      recipe=new_recipe2
  #      title=new_title,
  #      )

   # print('new_drink22 : ')
   # print(new_drink)
   # print('above')

    # check if unique name


    #try:

       # new_drink.insert() # method defined in models.py

       # drinks = Drink.query.order_by(Drink.id).all()
       # drink_array = [drink.long() for drink in drinks]

       # return jsonify({
       #     'success': True,
       #     'drinks':new_drink
       # })
    #except:
    #    abort(422)



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

'''
I have modified the test (see Mentor recommendation "https://knowledge.udacity.com/questions/618815")
Original:
pm.test("value contains drinks array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.drinks).to.be.an('array')
});

Modified:
pm.test("value contains drinks array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array')
});
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def patch_drink(payload, id):   # *args, **kwargs): 


    drink_to_patch = Drink.query.filter(Drink.id == id).one_or_none()
    if drink_to_patch is None: 
        abort(404)
     
    
    try:    
        body = request.get_json() 
        print('body22 : ' + str(body))

        new_title = body.get("title", None)
        new_recipe = body.get("recipe", None)
        new_recipe=json.dumps(new_recipe)

        print('new_title22 : ' + new_title)
        print('new_recipe22(before jsonloads) : ')
        print(new_recipe)

        if new_title != "null":
            drink_to_patch.title = new_title     #if new_title != ""
        if new_recipe != "null":
            drink_to_patch.recipe = new_recipe    #if new_recipe != ""
    except:
        abort(422, "bad request etc error description")

    try:
        drink_to_patch.update()
        return jsonify({
            'success': True,
            'drinks': drink_to_patch.long()
        }, 200)

    except:
        abort(422)






'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(payload, id):   # *args, **kwargs): 


    drink_to_delete = Drink.query.filter(Drink.id == id).one_or_none()
    if drink_to_delete is None: 
        abort(404)
     
    try:
        drink_to_delete.delete()

        return jsonify({
            'success': True,
            'delete': id
        }, 200)

    except:
        abort(422)




## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "not found"
                    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    '''
    Receive the raised authorization error and include it in the response.
    '''
    response = jsonify(ex.error)
    response.status_code = ex.status_code

    return response
    