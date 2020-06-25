import pydantic


class Settings(pydantic.BaseSettings):
    datadir: str = pydantic.Field("data", env="SURFACESCAN_DATADIR")


current = Settings()
