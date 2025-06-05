from enum import Enum


class StraicoRequest(Enum):
    USER_INFORMATION = "user_information"
    PROMPT_COMPLETION = "prompt_completion"
    MODELS_INFORMATION = "models_information"
    FILE_UPLOAD = "file_upload"
    IMAGE_GENERATION = "image_generation"
    CREATE_AGENT = "create_agent"
    ADD_RAG_TO_AGENT = "add_rag_to_agent"
    AGENT_DETAILS = "agent_details"
    LIST_OF_AGENTS = "list_of_agents"
    UPDATE_AGENT = "update_agent"
    AGENT_PROMPT_COMPLETION = "agent_prompt_completion"
    DELETE_AGENT = "delete_agent"
    CREATE_RAG = "create_rag"
    LIST_OF_RAGS = "list_of_RAGS"
    RAG_BY_ID = "rag_by_id"
    UPDATE_RAG = "update_rag"  # NOT exist
    DELETE_RAG = "delete_rag"
    RAG_PROMPT_COMPLETION = "rag_prompt_completion"
