from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

def get_llm(config: dict):
    llm_config = config.get("llm", {})
    provider = llm_config.get("provider", "ollama")
    
    if provider == "ollama":
        return ChatOllama(
            model=llm_config.get("model", "llama3"),
            base_url=llm_config.get("base_url", "http://localhost:11434"),
            temperature=llm_config.get("temperature", 0.7)
        )
    elif provider == "openai":
        return ChatOpenAI(
            model=llm_config.get("model", "gpt-4"),
            temperature=llm_config.get("temperature", 0.7)
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")