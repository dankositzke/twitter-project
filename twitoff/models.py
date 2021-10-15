from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create a 'User' table
class User(db.Model):
    """Creates a User Table with SQlAlchemy"""

    # id column
    id = db.Column(db.BigInteger, primary_key=True)
    # name column
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)


# Create a 'Tweet' table
class Tweet(db.Model):
    """Keeps track of Tweets for each user"""

    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Unicode(300))  # allows for text and links
    vect = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)
