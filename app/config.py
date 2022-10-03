from pydantic import BaseSettings 



class Settings(BaseSettings):
    """
    Here we are going to mention all the environment variables 
    This will check if there is any env variable with this name in System environment variables. 
    """
    database_hostname : str
    database_port : str 
    database_password : str
    database_name : str
    database_username : str
    secrete_key : str = "fs1df54f64wfdz15ew4g8fwe4651"
    algorithm : str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

print(settings.database_password) 