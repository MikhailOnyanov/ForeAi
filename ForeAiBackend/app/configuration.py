from pydantic_settings import BaseSettings

class SecurityConfig(BaseSettings):
    """
    Represents the security configuration for basic authentication.

    This class loads the user and password credentials from environment variables or a .env file.
    """
    USER: str
    PASSWORD: str

    class Config:
        env_prefix = "BASIC_AUTH_"
        env_file = ".env"

def get_security_config() -> SecurityConfig:
    """
    Get the security configuration.
    
    This function retrieves the security configuration from environment variables
    or defaults defined in the SecurityConfig class.
    
    Returns:
        SecurityConfig: An instance of SecurityConfig with the loaded settings.
    """
    return SecurityConfig()
