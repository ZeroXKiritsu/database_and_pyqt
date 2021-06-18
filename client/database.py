from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import os
import sys

sys.path.append('../')
from shared.variables import *
import datetime

class ClientStorage:
    class Users:
        def __init__(self, user):
            self.id = None
            self.user = user

    class History:
        def __init__(self, from_user, to_user, message):
            self.id = None
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        def __init__(self, contact):
            self.id = None
            self.name = contact

    
    def __init__(self, name):
        path = os.path.dirname(os.path.realpath(__file__))
        file_name = f'client_{name}.db3'
        self.engine = create_engine(f'sqlite:///{os.path.join(path, file_name)}', echo=False, pool_recycle=7200, connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        users = Table('users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user', String)
                     )

        history = Table('history', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('from_user', String),
                      Column('to_user', String),
                      Column('message', Text),
                      Column('date', DateTime)
                      )
        
        contacts = Table('contacts', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String, unique=True)
                     )

        self.metadata.create_all(self.engine)

        mapper(self.Users, users)
        mapper(self.History, history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()
    
    def add_contact(self, contact):
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            row = self.Contacts(contact)
            self.session.add(row)
            self.session.commit()
    
    def delete_contact(self, contact):
       self.session.query(self.Contacts).filter_by(name=contact).delete()
    
    def add_users(self, users_list):
        self.session.query(self.Users).delete()
        for user in users_list:
            row = self.Users(user)
            self.session.add(row)
        self.session.commit()
    
    def save_message(self, from_user, to_user, message):
        row = self.History(from_user, to_user, message)
        self.session.add(row)
        self.session.commit()
    
    def get_contacts(self):
         return [contact[0] for contact in self.session.query(self.Contacts.name).all()]
        
    def get_users(self):
          return [user[0] for user in self.session.query(self.Users.user).all()]
    
    def check_user(self, user):
        if self.session.query(self.Users).filter_by(user=user).count():
            return True
        else:
            return False
    
    def check_contact(self, contact):
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False
    
    def get_history(self, from_who=None, to_who=None):
         query = self.session.query(self.History)
         if from_who:
              query = query.filter_by(from_user=from_who)
         elif to_who:
             query = query.filter_by(to_user=to_who)
         return [(row.from_user, row.to_user,
                 row.message, row.date)
                for row in query.all()]


if __name__ == '__main__':
    test_db = ClientStorage('test1')
    print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))        