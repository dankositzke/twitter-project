from flask import Flask, render_template, request
from twitoff.predict import predict_user
from twitoff.models import db, User
import os
from twitoff.twitter import add_or_update_user


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET", "POST"])
    def hello_world():

        # name = request.form.get("name")
        # tweet = request.form.get("tweet")

        # if request.method == "POST" and name:
        #     user_and_tweet = UserAndTweet(name=name, tweet=tweet)  # need to update
        #     db.session.add(user_and_tweet)
        #     db.session.commit()

        # users_and_tweets = UserAndTweet.query.all()

        return render_template("base.html", title="Home", users=User.query.all())

    @app.route("/about")
    def about_page():
        return "About Page"

    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def user(name=None, message=""):

        # we either take name that was passed in or we pull it
        # from our request.values which would be accessed through the
        # user submission
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} Succesfully added!".format(name)

            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)

            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route("/compare", methods=["POST"])
    def compare():
        user0, user1 = sorted([request.values["user0"], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            # prediction returns a 0 or 1
            prediction = predict_user(user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1,
            )

        return render_template("prediction.html", title="Prediction", message=message)

    return app
