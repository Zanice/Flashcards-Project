# native imports

# project imports

# external imports
import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()
Session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())

def init_db(username, password, database):
	connection_url = sqlalchemy.engine.url.make_url('postgresql://localhost/')
	connection_url.username = username
	connection_url.password = password
	connection_url.database = database
	engine = sqlalchemy.create_engine(connection_url)
	Session.remove()
	Session.configure(bind=engine)
	Base.metadata.create_all(engine)

class Flashcard(Base):
	__tablename__ = 'flashcards'
	question = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=False)
	answer = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=False)
	category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
	one_to_one = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)

