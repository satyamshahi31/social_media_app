from app import db

follower_followed = db.Table('follower_followed',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile_no = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    followed = db.relationship(
        'User', secondary=follower_followed,
        primaryjoin=(follower_followed.c.follower_id == id),
        secondaryjoin=(follower_followed.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
