from typing import Optional


from pydantic import BaseModel, Field, field_validator




class LlmConfig(BaseModel):
    provider: str = Field(description="Provider of the LLM (e.g., 'ollama', 'openai')", default="openai")
    config: Optional[dict] = Field(description="Configuration for the specific LLM", default={})


    @field_validator("config")
    def validate_config(cls, v, values):
        provider = values.data.get("provider")
        # Imported lazily (and looked up at validation time) to avoid an
        # import cycle with mem0.utils.factory, and so that providers
        # registered via LlmFactory.register_provider are accepted.
        from mem0.utils.factory import LlmFactory

        if provider in LlmFactory.get_supported_providers():
            return v
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
