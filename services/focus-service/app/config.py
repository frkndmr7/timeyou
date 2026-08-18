import os


class ConfigurationError(RuntimeError):
    """Raised when required service configuration is missing."""


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url or not database_url.strip():
        raise ConfigurationError(
            "DATABASE_URL environment variable is required for Focus Service."
        )
    return database_url.strip()


def get_required_config(name: str) -> str:
    value = os.getenv(name)
    if not value or not value.strip():
        raise ConfigurationError(f"{name} environment variable is required.")
    return value.strip()


def get_cognito_region() -> str:
    return get_required_config("COGNITO_REGION")


def get_cognito_user_pool_id() -> str:
    return get_required_config("COGNITO_USER_POOL_ID")


def get_cognito_app_client_id() -> str:
    return get_required_config("COGNITO_APP_CLIENT_ID")


def get_cognito_issuer() -> str:
    return (
        f"https://cognito-idp.{get_cognito_region()}.amazonaws.com/"
        f"{get_cognito_user_pool_id()}"
    )


def get_internal_api_key() -> str:
    return get_required_config("FOCUS_INTERNAL_API_KEY")
