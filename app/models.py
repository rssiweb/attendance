import jwt
from app import db, app, bcrypt
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(Base):
    __abstract__ = True

    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return dict(name=self.name)


class Faculty(User):
    __tablename__ = 'faculty'

    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean(), default=False)

    def __init__(self, name, email, password):
        super(Faculty, self).__init__(name)
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    def __repr__(self):
        return '<Faculty %r>' % self.name

    def serialize(self):
        return dict(id=self.id,
                    name=self.name,
                    email=self.email,
                    admin=self.admin,
                    )


    @staticmethod
    def encode_auth_token(email):
        """
        Generates the Auth Token
        :return: string
        """
        token_life = app.config.get('TOKEN_LIFESPAN_SEC')
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=token_life),
            'iat': datetime.utcnow(),
            'sub': email
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']


class Student(User):
    __tablename__ = 'student'

    dob = db.Column(db.Date(), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __init__(self, name, dob, student_id, category):
        super(Student, self).__init__(name)
        self.student_id = student_id
        self.category = category
        if not isinstance(dob, datetime):
            self.dob = datetime.strptime(dob, '%Y-%m-%d').date()
        else:
            self.dob = dob

    def __repr__(self):
        return '<Student %r>' % self.name

    def serialize(self):
        return dict(id=self.id,
                    name=self.name,
                    dob=self.dob,
                    category=self.category,
                    student_id=self.student_id,
                    )


class Attendance(Base):
    __tablename__ = 'attendance'

    date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    punchIn = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    punchOut = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    comments = db.Column(db.String(100), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = relationship('Student')

    def __init__(self, date, punchIn, punchOut, comments, student_id):
        if not isinstance(date, datetime):
            self.date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            self.date = date
        if not isinstance(punchIn, datetime):
            # 2018-02-19T18:50:40.067Z
            self.punchIn = datetime.strptime(punchIn, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.punchIn = punchIn
        if not isinstance(punchOut, datetime):
            self.punchOut = datetime.strptime(punchOut, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.punchOut = punchOut
        self.comments = comments
        self.student_id = student_id

    def serialize(self):
        return dict(id=self.id,
                    student=self.student.serialize(),
                    comments=self.comments,
                    punchIn=self.punchIn,
                    punchOut=self.punchOut)
