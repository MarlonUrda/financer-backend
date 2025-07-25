from  sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s_%(referred_column_0_name)s"
}

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)