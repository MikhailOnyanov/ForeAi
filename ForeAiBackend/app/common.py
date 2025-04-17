import os

description = """
ForeAI API helps you do awesome stuff. 🚀
"""

def get_chroma_creds() -> dict:
    chroma_service_config = {
        "client_type": "http",
        "client_kwargs": {"host": "127.0.0.1", "port": 8000},
    }
    env_creds = get_all_env_creds_or_none(["CHROMA_HOST", "CHROMA_PORT"])
    if env_creds:
        chroma_service_config["client_kwargs"]["host"] = env_creds["CHROMA_HOST"]
        chroma_service_config["client_kwargs"]["port"] = env_creds["CHROMA_PORT"]
    return chroma_service_config

def get_all_env_creds_or_none(env_keys: list[str]) -> dict | None:
    """
    Reads environment variables and returns them as a dict. Returns None if any env key is missing
    """
    env_creds = {}
    for env_key in env_keys:
        env_creds[env_key] = os.getenv(env_key)
        if env_creds[env_key] is None:
            return None
    return env_creds