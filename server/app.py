#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        #create a list of game representations, which is then returned in the API response.
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    #Handle the Get request
    if request.method == 'GET':
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)

        response = make_response(
            reviews,
            200
        )

        return response

    #Handling a POST request
    elif request.method == 'POST':
        new_review = Review(
            #get the data from the form for each field
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )

        #add the new review to the database
        db.session.add(new_review)
        db.session.commit()

        #create a dictionary representation of the new review, which is then returned in the API response.
        review_dict = new_review.to_dict()

        response = make_response(
            review_dict,
            201
        )

        return response


#View that retrieves a single review by it's id
@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    # Retrieve the review object from the database based on the provided ID
    review = Review.query.filter(Review.id == id).first()

    # Check if the review object exists in the database
    if review == None:
        # If the review object does not exist, return a 404 error response
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        # Handle GET request
        if request.method == 'GET':
            # Convert the review object to a dictionary
            review_dict = review.to_dict()

            # Return the review dictionary as a response
            response = make_response(
                review_dict,
                200
            )

            return response

        # Handle PATCH request
        elif request.method == 'PATCH':
            # Loop through the request form attributes and update the corresponding attributes on the review object
            for attr in request.form:
                # Use setattr to update the attributes
                setattr(review, attr, request.form.get(attr))
                #eg setattr(review, "title", "New Review Title")
                #setattr(review, "rating", 5)
                #setattr(review, "comment", "This is a great game!")

            # Add the updated review object to the database session
            db.session.add(review)
            # Commit the changes to the database
            db.session.commit()

            # Convert the updated review object to a dictionary
            review_dict = review.to_dict()

            # Return the updated review dictionary as a response
            response = make_response(
                review_dict,
                200
            )

            return response

        # Handle DELETE request
        elif request.method == 'DELETE':
            # Delete the review object from the database
            db.session.delete(review)
            # Commit the changes to the database
            db.session.commit()

            # Create a response body to indicate that the review was deleted successfully
            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }

            # Return the response body as a response
            response = make_response(
                response_body,
                200
            )

            return response


@app.route('/users')
def users():
    # Retrieve all user objects from the database
    users = []
    for user in User.query.all():
        # Convert each user object to a dictionary
        user_dict = user.to_dict()
        # Append the user dictionary to the list of users
        users.append(user_dict)

    # Return the list of users as a response
    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
