from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Boolean, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

def now(): return datetime.now(timezone.utc)
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True)
    full_name: Mapped[str]=mapped_column(String(120),default="Developer")
    password_hash: Mapped[str]=mapped_column(String(255))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    repositories: Mapped[list["Repository"]]=relationship(back_populates="user",cascade="all, delete-orphan")
class Repository(Base):
    __tablename__="repositories"
    __table_args__=(Index("ix_repo_user_full_name","user_id","full_name",unique=True),)
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    owner: Mapped[str]=mapped_column(String(100)); name: Mapped[str]=mapped_column(String(100))
    full_name: Mapped[str]=mapped_column(String(205)); html_url: Mapped[str]=mapped_column(String(500))
    description: Mapped[str]=mapped_column(Text,default=""); default_branch: Mapped[str]=mapped_column(String(120),default="main")
    private: Mapped[bool]=mapped_column(Boolean,default=False); stars: Mapped[int]=mapped_column(Integer,default=0)
    language: Mapped[str|None]=mapped_column(String(80),nullable=True); last_analyzed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    user: Mapped[User]=relationship(back_populates="repositories")
    analyses: Mapped[list["Analysis"]]=relationship(back_populates="repository",cascade="all, delete-orphan")
class Analysis(Base):
    __tablename__="analyses"
    id: Mapped[int]=mapped_column(primary_key=True); repository_id: Mapped[int]=mapped_column(ForeignKey("repositories.id",ondelete="CASCADE"),index=True)
    status: Mapped[str]=mapped_column(String(30),default="completed"); summary: Mapped[str]=mapped_column(Text,default="")
    file_count: Mapped[int]=mapped_column(Integer,default=0); languages_json: Mapped[str]=mapped_column(Text,default="{}")
    findings_count: Mapped[int]=mapped_column(Integer,default=0); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    repository: Mapped[Repository]=relationship(back_populates="analyses")
class Finding(Base):
    __tablename__="findings"
    id: Mapped[int]=mapped_column(primary_key=True); analysis_id: Mapped[int]=mapped_column(ForeignKey("analyses.id",ondelete="CASCADE"),index=True)
    path: Mapped[str]=mapped_column(String(500)); line: Mapped[int]=mapped_column(Integer); severity: Mapped[str]=mapped_column(String(20))
    category: Mapped[str]=mapped_column(String(80)); confidence: Mapped[float]=mapped_column(Float,default=.5)
    description: Mapped[str]=mapped_column(Text); evidence: Mapped[str]=mapped_column(Text); recommendation: Mapped[str]=mapped_column(Text)
    verification_status: Mapped[str]=mapped_column(String(40),default="unverified heuristic")
class ChatSession(Base):
    __tablename__="chat_sessions"
    id: Mapped[int]=mapped_column(primary_key=True); user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    repository_id: Mapped[int]=mapped_column(ForeignKey("repositories.id",ondelete="CASCADE"),index=True)
    title: Mapped[str]=mapped_column(String(200),default="Repository questions"); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class ChatMessage(Base):
    __tablename__="chat_messages"
    id: Mapped[int]=mapped_column(primary_key=True); session_id: Mapped[int]=mapped_column(ForeignKey("chat_sessions.id",ondelete="CASCADE"),index=True)
    role: Mapped[str]=mapped_column(String(20)); content: Mapped[str]=mapped_column(Text); citations_json: Mapped[str]=mapped_column(Text,default="[]")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Proposal(Base):
    __tablename__="pull_request_proposals"
    id: Mapped[int]=mapped_column(primary_key=True); user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    repository_id: Mapped[int]=mapped_column(ForeignKey("repositories.id",ondelete="CASCADE"),index=True)
    title: Mapped[str]=mapped_column(String(200)); description: Mapped[str]=mapped_column(Text,default="")
    patch: Mapped[str]=mapped_column(Text); status: Mapped[str]=mapped_column(String(30),default="draft")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

# Extended persistence entities. Sensitive GitHub credentials, if integrated by an
# OAuth/GitHub-App deployment, belong only in encrypted ciphertext fields.
class ConnectedGitHubAccount(Base):
    __tablename__="connected_github_accounts"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    github_user_id: Mapped[str]=mapped_column(String(80),index=True)
    login: Mapped[str]=mapped_column(String(120))
    token_ciphertext: Mapped[str|None]=mapped_column(Text,nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class RepositoryFile(Base):
    __tablename__="repository_files"
    id: Mapped[int]=mapped_column(primary_key=True)
    repository_id: Mapped[int]=mapped_column(ForeignKey("repositories.id",ondelete="CASCADE"),index=True)
    path: Mapped[str]=mapped_column(String(500)); sha: Mapped[str]=mapped_column(String(80),default="")
    language: Mapped[str|None]=mapped_column(String(80),nullable=True); size_bytes: Mapped[int]=mapped_column(Integer,default=0)
    indexed_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class RepositoryIssue(Base):
    __tablename__="repository_issues"
    id: Mapped[int]=mapped_column(primary_key=True)
    repository_id: Mapped[int]=mapped_column(ForeignKey("repositories.id",ondelete="CASCADE"),index=True)
    github_number: Mapped[int]=mapped_column(Integer); title: Mapped[str]=mapped_column(String(500))
    category: Mapped[str]=mapped_column(String(50),default="general"); priority: Mapped[str]=mapped_column(String(20),default="normal")
    evidence: Mapped[str]=mapped_column(Text,default=""); html_url: Mapped[str]=mapped_column(String(500))
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class EmbeddingMetadata(Base):
    __tablename__="embeddings_metadata"
    id: Mapped[int]=mapped_column(primary_key=True)
    repository_id: Mapped[int]=mapped_column(ForeignKey("repositories.id",ondelete="CASCADE"),index=True)
    file_path: Mapped[str]=mapped_column(String(500)); chunk_index: Mapped[int]=mapped_column(Integer)
    vector_store_id: Mapped[str]=mapped_column(String(200),index=True); content_sha: Mapped[str]=mapped_column(String(80))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class GeneratedTest(Base):
    __tablename__="generated_tests"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    repository_id: Mapped[int]=mapped_column(ForeignKey("repositories.id",ondelete="CASCADE"),index=True)
    source_path: Mapped[str]=mapped_column(String(500)); test_code: Mapped[str]=mapped_column(Text)
    status: Mapped[str]=mapped_column(String(30),default="generated_not_executed")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class AgentExecutionLog(Base):
    __tablename__="agent_execution_logs"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    repository_id: Mapped[int|None]=mapped_column(ForeignKey("repositories.id",ondelete="CASCADE"),nullable=True,index=True)
    agent_name: Mapped[str]=mapped_column(String(100)); status: Mapped[str]=mapped_column(String(30))
    trace_json: Mapped[str]=mapped_column(Text,default="{}"); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
