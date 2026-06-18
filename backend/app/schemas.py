from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

# --- Auth & User ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    refresh_token: str

# --- Message ---
class MessageBase(BaseModel):
    role: str
    content: str
    satire_level: int = 0

class MessageCreate(BaseModel):
    content: str
    satire_level: int = Field(default=0, ge=0, le=3)

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    tokens_prompt: int
    tokens_completion: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Conversation ---
class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

# --- Admin Dashboard Stats ---
class AdminUserDetail(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    created_at: datetime
    conversation_count: int

class AdminStatsDashboard(BaseModel):
    total_users: int
    active_users_24h: int
    total_conversations: int
    total_questions: int
    total_answers: int
    total_prompt_tokens: int
    total_completion_tokens: int
    model_name: str
