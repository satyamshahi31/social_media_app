from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # type: ignore
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from services import auth, users, posts, comments, hashtags, follows

app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(posts.bp)
app.register_blueprint(comments.bp)
app.register_blueprint(hashtags.bp)
app.register_blueprint(follows.bp)

if __name__ == '__main__':
    app.run(debug=True)
