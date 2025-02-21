from datetime import datetime
from sqlalchemy import Column, Integer, String, LargeBinary, Text, Boolean, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

# ER Diagram Mapping:
# User: Stores client and employee information including encrypted personal data and balance
# Transaction: Records all financial operations with amount, timestamp and risk assessment
# Transaction_type: Defines different categories of financial operations (e.g. deposit, withdrawal)
# Transaction_status: Tracks the current state of transactions (e.g. pending, completed, rejected)
# Role: Manages access control and permissions for different user types
# Message: Stores encrypted communications between users related to transactions


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'))
    encrypted_name = Column(LargeBinary)
    encrypted_email = Column(LargeBinary)
    encrypted_phone = Column(LargeBinary)
    encrypted_address = Column(LargeBinary)
    encrypted_balance = Column(LargeBinary)
    password_hash = Column(LargeBinary)
    salt = Column(LargeBinary(16))
    is_active = Column(Boolean, default=True)

    # Relationships
    role = relationship("Role", back_populates="users")
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")
    created_tickets = relationship("Ticket", foreign_keys="Ticket.client_id", back_populates="client")
    sent_messages = relationship("TicketMessage", back_populates="sender")

class Transaction(Base):
    __tablename__ = 'transaction'
    
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    receiver_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    comment = Column(Text)
    encrypted_amount = Column(Text)
    risk_level = Column(Integer)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")
    tickets = relationship("Ticket", back_populates="related_transaction")

class Role(Base):
    __tablename__ = 'role'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))

    # Relationships
    users = relationship("User", back_populates="role")

class UserKey(Base):
    __tablename__ = 'user_key'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    encrypted_key = Column(LargeBinary)
    create_time = Column(DateTime, default=func.now())

    # Relationships
    associated_user = relationship("User", foreign_keys=[user_id])

class Ticket(Base):
    __tablename__ = 'ticket'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    assignee_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    encrypted_content = Column(Text)
    risk_level = Column(Integer)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
    related_transaction_id = Column(Integer, ForeignKey('transaction.id', ondelete='CASCADE'))

    # Relationships
    client = relationship("User", foreign_keys=[client_id], back_populates="created_tickets")
    assignee = relationship("User", foreign_keys=[assignee_id])
    related_transaction = relationship("Transaction", back_populates="tickets")
    messages = relationship("TicketMessage", back_populates="ticket")

class TicketMessage(Base):
    __tablename__ = 'ticket_message'
    
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('ticket.id', ondelete='CASCADE'))
    sender_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    encrypted_content = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())

    # Relationships
    ticket = relationship("Ticket", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")

