from bolinette import db, marshalling, env

users_roles = db.Table('users_roles',
                       db.Column('u_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                       db.Column('r_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=env.init['USER_EMAIL_REQUIRED'],
                      nullable=(not env.init['USER_EMAIL_REQUIRED']))

    roles = db.relationship('Role', secondary=users_roles, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def has_role(self, role):
        return any(filter(lambda r: r.name == role, self.roles))

    @staticmethod
    def payloads():
        yield 'register', [
            marshalling.Field(marshalling.types.string, 'username', required=True),
            marshalling.Field(marshalling.types.email, 'email', required=True),
            marshalling.Field(marshalling.types.password, 'password', required=True)
        ]
        yield 'admin_register', [
            marshalling.Field(marshalling.types.string, 'username', required=True),
            marshalling.Field(marshalling.types.email, 'email', required=True),
            marshalling.Field(marshalling.types.boolean, 'send_mail', required=True)
        ]
        yield 'login', [
            marshalling.Field(marshalling.types.string, 'username', required=True),
            marshalling.Field(marshalling.types.password, 'password', required=True)
        ]

    @staticmethod
    def responses():
        yield [
            marshalling.Field(marshalling.types.string, 'username')
        ]
        yield 'private', [
            marshalling.Field(marshalling.types.string, 'username'),
            marshalling.Field(marshalling.types.email, 'email'),
            marshalling.List('roles', marshalling.Definition('role', 'role'))
        ]

    def __repr__(self):
        return f'<User {self.username}>'


marshalling.register(User, 'user')
