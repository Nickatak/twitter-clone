"""Authentication models."""

from flask import abort

from app import bcrypt, db


class User(db.Model):
    """
    Custom User model.

    Attributes:
        name (string): Display name of a user with a 50 char max.
        username (string): User handle (EG: @user123) with a 15 char limit.
        id (int): User identification number.
        phone (string): User phone number with a 30 char maxiumum.
        email (string): Email of a user with a 100 char limit.
        password (string): User password with 256 char limit.

    Methods:
        authenticate(cls, username, password)
            Helper function to authorize a user given a username/password combination.

        create(cls, name, username, email, password)
            Instance method to create a new instance of a User.
        
        get_by_username_or_404(cls, username)
            Helper method to retrieve a User by their username.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # This is the "display name."
    name = db.Column(db.String(50))
    # This is the "handle" (EG: @blah).  Twitter has a 15 character limit on
    # handles, but admins can be longer, so I'll set this to 15 for now, and
    # we'll find something else for admins.
    username = db.Column(db.String(15), unique=True, index=True)

    # India's phone numbers can be 13 digits long.
    # TODO: Replace this with PhoneNumberField.
    # phone = db.Column(db.String(30), unique=True)
    # Going to set an arbitrary length here, I think that this is pretty
    # reasonable for humans and should deny extremely long auto-generated
    # emails.  Of course, additional validation still needs to be applied.
    email = db.Column(db.String(100), unique=True)

    # ALthough things like SHA512 use 128 chars, and Bcrypt uses somewhere
    # about 64 (max) chars depending upon implementation, I figured we'd be
    # safer by just having a larger storage container for future hash
    # implementations.
    password = db.Column(db.String(256))

    @classmethod
    def authenticate(cls, username, password):
        """Helper function to authorize a user given a username/password combination.
            :username: Attempted username.
            :password: Attempted password.

        returns:
            User instance if the combination was valid.
            NoneType if the combination was not valid.
        """

        attempted_user = cls.query.filter(cls.username == username).first()

        if attempted_user is not None and bcrypt.check_password_hash(
                attempted_user.password, password):
            return attempted_user

        return None

    @classmethod
    def create(cls, name, username, email, password):
        """Instance method to create a new instance of a User.
            This method adds a new user to the database.

            :name: Display name.
            :username: Twitter handle (ex. @user123).
            :email: User email.
            :password: User password.

            returns:
                New instance of a User.
        """
        new_user = cls(name=name,
                       username=username,
                       email=email
                       )
        new_user.password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @classmethod
    def get_by_username_or_404(cls, username):
        """Helper method to retrieve a User by their username.
            WARNING: This method aborts and returns a 404 if the username isn't found.

            :username: The username you want to fetch a User instance by.

        returns:
            User instance if the username exists in the DB.
            None (aborts view-method with a 404 response) if username doesn't exist.
        """

        user = cls.query.filter(cls.username == username).first()

        if user is None:
            abort(404, description='Resource not found.')

        return user
