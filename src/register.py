# from src.messenger.contexts.person import PersonBase
# from src.messenger.contexts.message import MessageBase
# from src.messenger.contexts.dialog import DialogBase
# from src.auth.contexts.user import UserBase
# from src.agent.contexts.messages import MessageCreate, MessageResponseBase
# from src.project.contexts.project import ProjectBase
# from src.agent.contexts.agent import AgentBase
# from src.agent.contexts.prompt import PromptBase
# from src.agent.contexts.seance import SeanceBase
# from src.agent.contexts.label import LabelBase
# from src.agent.contexts.action import ActionBase
# from src.agent.contexts.parameters import ParameterBase, ParameterPredefinedBase
# from src.agent.contexts.proposal import ProposalBase
# from src.agent.contexts.callback import CallbackBase, CallbackPredefinedBase


from sqlmodel import SQLModel, Session, Field, Relationship, Field
from typing import List, Optional
from datetime import datetime


# class Person(PersonBase, table=True):
#     __tablename__ = "persons"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)

#     messages_as_sender: Optional[List["Message"]
#                                  ] = Relationship(back_populates="sender")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class AgentPredefinedParameters(SQLModel, table=True):
#     __tablename__ = "agentpredefinedparameters"
#     __table_args__ = {'extend_existing': True}
#     agent_id: Optional[int] = Field(
#         default=None, foreign_key="agents.id", primary_key=True)
#     predefined_parameter_id: Optional[int] = Field(
#         default=None, foreign_key="parameterspredefined.id", primary_key=True)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class LabelPredefined(SQLModel, table=True):
#     __tablename__ = "labelspredefined"
#     __table_args__ = {'extend_existing': True}
#     label_id: Optional[int] = Field(
#         default=None, foreign_key="labels.id", primary_key=True
#     )
#     project_id: Optional[int] = Field(
#         default=None, foreign_key="projects.id", primary_key=True
#     )
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class LabelToSeance(SQLModel, table=True):
#     __tablename__ = "labelstoseances"
#     __table_args__ = {'extend_existing': True}
#     label_id: Optional[int] = Field(
#         default=None, foreign_key="labels.id", primary_key=True
#     )
#     seance_id: Optional[int] = Field(
#         default=None, foreign_key="seances.id", primary_key=True
#     )
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class Dialog(DialogBase, table=True):
#     __tablename__ = "dialogs"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     seances: Optional[List["Seance"]] = Relationship(
#         back_populates="dialog")
#     messages: Optional[List["Message"]] = Relationship(back_populates="dialog")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class Message(MessageBase, table=True):
#     __tablename__ = "messages"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)

#     sender_id: Optional[int] = Field(default=None, foreign_key="persons.id")
#     sender: Optional["Person"] = Relationship(
#         back_populates="messages_as_sender")

#     dialog_id: Optional[int] = Field(default=None, foreign_key="dialogs.id")

#     dialog: Optional["Dialog"] = Relationship(back_populates="messages")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

#     actions: Optional[List["Action"]] = Relationship(
#         back_populates="message")

#     proposals: Optional[List["Proposal"]] = Relationship(
#         back_populates="message")


# class User(UserBase, table=True):
#     __tablename__ = "users"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
#     projects: Optional[List["Project"]] = Relationship(
#         back_populates="owner")


# class MessageResponse(MessageResponseBase, table=True):
#     __tablename__ = "messagesresponses"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class IncomingAgentsLabels(SQLModel, table=True):
#     __tablename__ = "incomingagentslabels"
#     __table_args__ = {'extend_existing': True}
#     label_id: Optional[int] = Field(
#         default=None, foreign_key="labels.id", primary_key=True
#     )
#     agent_id: Optional[int] = Field(
#         default=None, foreign_key="agents.id", primary_key=True
#     )
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class OutgoingAgentsLabels(SQLModel, table=True):
#     __tablename__ = "outgoingagentslabels"
#     __table_args__ = {'extend_existing': True}
#     label_id: Optional[int] = Field(
#         default=None, foreign_key="labels.id", primary_key=True
#     )
#     agent_id: Optional[int] = Field(
#         default=None, foreign_key="agents.id", primary_key=True
#     )
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class Seance(SeanceBase, table=True):
#     __tablename__ = "seances"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)

#     dialog_id: Optional[int] = Field(default=None, foreign_key="dialogs.id")
#     dialog: Optional["Dialog"] = Relationship(
#         back_populates="seances")
#     active_labels: Optional[List["Label"]] = Relationship(
#         back_populates="active_seances", link_model=LabelToSeance)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
#     parameters: Optional[List["Parameter"]] = Relationship(
#         back_populates="seance")

#     callbacks: Optional[List["Callback"]] = Relationship(
#         back_populates="seance")


# class Label(LabelBase, table=True):
#     __tablename__ = "labels"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     settable_incoming_agents: List["Agent"] = Relationship(
#         back_populates="incoming_labels", link_model=IncomingAgentsLabels)
#     settable_outgoing_agents: List["Agent"] = Relationship(
#         back_populates="outgoing_labels", link_model=OutgoingAgentsLabels)

#     active_seances: Optional[List["Seance"]] = Relationship(
#         back_populates="active_labels", link_model=LabelToSeance
#     )
#     projects: List["Project"] = Relationship(
#         back_populates="labels_predefined", link_model=LabelPredefined)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class Agent(AgentBase, table=True):
#     __tablename__ = "agents"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)

#     project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
#     project: Optional["Project"] = Relationship(
#         back_populates="agents")

#     actions: Optional[List["Action"]] = Relationship(
#         back_populates="agent")

#     prompts: Optional[List["Prompt"]] = Relationship(
#         back_populates="agent")

#     incoming_labels: List["Label"] = Relationship(
#         back_populates="settable_incoming_agents", link_model=IncomingAgentsLabels)
#     outgoing_labels: List["Label"] = Relationship(
#         back_populates="settable_outgoing_agents", link_model=OutgoingAgentsLabels)

#     parameters_predefined: Optional[List["ParameterPredefined"]] = Relationship(
#         back_populates="agents", link_model=AgentPredefinedParameters)

#     proposals: Optional[List["Proposal"]] = Relationship(
#         back_populates="agent")

#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class Prompt(PromptBase, table=True):
#     __tablename__ = "prompts"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     agent_id: Optional[int] = Field(default=None, foreign_key="agents.id")
#     agent: Optional["Agent"] = Relationship(
#         back_populates="prompts")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class Project(ProjectBase, table=True):
#     __tablename__ = "projects"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     owner_id: Optional[int] = Field(default=None, foreign_key="users.id")
#     owner: Optional["User"] = Relationship(
#         back_populates="projects")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

#     agents: Optional[List["Agent"]] = Relationship(
#         back_populates="project")

#     # DOING
#     labels_predefined: List["Label"] = Relationship(
#         back_populates="projects", link_model=LabelPredefined)

#     parameters_predefined: Optional[List["ParameterPredefined"]] = Relationship(
#         back_populates="project")

#     callbacks_predefined: Optional[List["CallbackPredefined"]] = Relationship(
#         back_populates="project")


# class Parameter(ParameterBase, table=True):
#     __tablename__ = "parameters"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     seance_id: Optional[int] = Field(default=None, foreign_key="seances.id")
#     seance: Optional["Seance"] = Relationship(
#         back_populates="parameters")

#     predefined_parameter_id: Optional[int] = Field(
#         default=None, foreign_key="parameterspredefined.id")
#     predefined_parameter: Optional["ParameterPredefined"] = Relationship(
#         back_populates="parameters")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class Proposal(ProposalBase, table=True):
#     __tablename__ = "proposals"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     message_id: Optional[int] = Field(default=None, foreign_key="messages.id")
#     # BASE: Agent
#     agent_id: Optional[int] = Field(default=None, foreign_key="agents.id")
#     agent: Optional["Agent"] = Relationship(
#         back_populates="proposals")

#     message: Optional["Message"] = Relationship(
#         back_populates="proposals")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class Action(ActionBase, table=True):
#     __tablename__ = "actions"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)

#     message_id: Optional[int] = Field(default=None, foreign_key="messages.id")
#     message: Optional["Message"] = Relationship(
#         back_populates="actions")

#     agent_id: Optional[int] = Field(default=None, foreign_key="agents.id")
#     agent: Optional["Agent"] = Relationship(
#         back_populates="actions")

#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class CallbackToParameters(SQLModel, table=True):
#     __tablename__ = "callbacktoparameters"
#     __table_args__ = {'extend_existing': True}

#     predefined_callback_id: Optional[int] = Field(
#         default=None, foreign_key="callbackspredefined.id", primary_key=True
#     )
#     predefined_parameter_id: Optional[int] = Field(
#         default=None, foreign_key="parameterspredefined.id", primary_key=True
#     )


# class CallbackPredefined(CallbackPredefinedBase, table=True):
#     __tablename__ = "callbackspredefined"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)

#     project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
#     project: Optional["Project"] = Relationship(
#         back_populates="callbacks_predefined")

#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
#     callbacks: Optional[List["Callback"]] = Relationship(
#         back_populates="predefined_callback")

#     predefined_parameters: Optional[List["ParameterPredefined"]] = Relationship(
#         back_populates="predefined_callbacks", link_model=CallbackToParameters)


# class ParameterPredefined(ParameterPredefinedBase, table=True):
#     __tablename__ = "parameterspredefined"
#     __table_args__ = {'extend_existing': True}
#     id: Optional[int] = Field(default=None, primary_key=True)
#     project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
#     project: Optional["Project"] = Relationship(
#         back_populates="parameters_predefined")
#     parameters: Optional[List["Parameter"]] = Relationship(
#         back_populates="predefined_parameter")

#     agents: Optional[List["Agent"]] = Relationship(
#         back_populates="parameters_predefined", link_model=AgentPredefinedParameters)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

#     predefined_callbacks: Optional[List["CallbackPredefined"]] = Relationship(
#         back_populates="predefined_parameters", link_model=CallbackToParameters)


# class CallbackSeanceRegister(SQLModel, table=True):
#     __tablename__ = "callbacktoseanceregisters"
#     __table_args__ = {'extend_existing': True}

#     predefined_callback_id: Optional[int] = Field(default=None, foreign_key="callbackspredefined.id", primary_key=True)
#     seance_id: Optional[int] = Field(default=None, foreign_key="seances.id", primary_key=True)
    
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
#     is_complete: Optional[bool] = Field(default=False)


# class Callback(CallbackBase, table=True):
#     __tablename__ = "callbacks"
#     __table_args__ = {'extend_existing': True}

#     id: Optional[int] = Field(default=None, primary_key=True)

#     seance_id: Optional[int] = Field(default=None, foreign_key="seances.id")
#     seance: Optional["Seance"] = Relationship(
#         back_populates="callbacks")

#     predefined_callback_id: Optional[int] = Field(
#         default=None, foreign_key="callbackspredefined.id")
#     predefined_callback: Optional["CallbackPredefined"] = Relationship(
#         back_populates="callbacks")
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

# class Trace(SQLModel, table=True):
#     __tablename__ = "traces"
#     __table_args__ = {'extend_existing': True}

#     id: Optional[int] = Field(default=None, primary_key=True)
#     content: Optional[str] = Field(default=None)
