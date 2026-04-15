from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. API 키 및 핵심 설정
    openai_api_key: str
    
    # 2. 모델 관련 설정
    model_path: str = "./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf"
    n_ctx: int = 4096
    
    # 3. 서버 설정
    host: str = "0.0.0.0"
    port: int = 8000

    # .env 파일을 읽어오도록 설정
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()