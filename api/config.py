from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv



class Settings(BaseSettings):
    input_licenses_csv: str = "data/licenses.csv"
    output_licenses_csv: str = "data/classified_licenses.csv"
    open_api_key: str

    model_config = SettingsConfigDict(
        env_file=find_dotenv()
        )
