import sqlalchemy
import os
from sqlalchemy import create_engine, MetaData, select, update
from sqlalchemy.orm import sessionmaker


class SessionHolder:

    def __init__(self, address: str, engine=None):
        self.address = address
        self.engine = engine
        self._session = None  # Initialize session attribute

    def create_session(self):
        if not self.engine:  # Create engine only if it doesn't exist
            self.engine = create_engine(self.address)
        if not self._session:  # Create session only if it doesn't exist
            Session = sessionmaker(bind=self.engine)
            self._session = Session()
        return self._session

    def get_session(self):
        if self._session is None:
            self.create_session()
        return self._session


class UuidStorage:

    def __init__(self, adress: str, table=None, session=None):
        self.adress = adress
        self.table = table
        self.session = session

    def get_table(self, current_engine):
        if not self.table:
            metadata = MetaData()
            metadata.reflect(bind=current_engine)
            table_name = os.environ.get("TABLE_NAME")  # Get table name from environment variable
            self.table = sqlalchemy.Table(table_name, metadata, autoload_with=current_engine)

    def create_session(self, current_engine):
        if not self.session:
            Session = sessionmaker(bind=current_engine)
            self.session = Session()

    def connect(self):
        current_engine = create_engine(self.adress)
        self.get_table(current_engine)
        self.create_session(current_engine)

    def get_balance_by_uuid(self, uuid):
        query = select(self.table.c['balance']).where(self.table.c.uuid == uuid)
        result = self.session.execute(query).first()
        return result[0] if result else None

    def update_balance_by_uuid(self, uuid, new_balance):
        query = update(self.table).where(self.table.c.uuid == uuid).values(balance=new_balance)
        self.session.execute(query)
        self.session.commit()
