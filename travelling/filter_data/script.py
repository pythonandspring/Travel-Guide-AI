import os
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd


# Choose your database
DATABASES = {
    # "sqlite": "sqlite:///db.sqlite3",
    "mysql": "mysql+pymysql://root:Iqbal@1234@localhost:3306/travel",

    # "postgresql": "postgresql+psycopg2://username:password@localhost/your_database_name",
}


db_type = "mysql"  # Change to "mysql" or "postgresql" if needed
engine = create_engine(DATABASES[db_type])
result_list = []


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT country, state, city, name FROM guide_place"))
        result_list = list(result)
except Exception as err:
    print(f"Error: {err}")


data = pd.DataFrame(result_list)

data.to_csv('./travelling/filter_data/place_info.csv', index=False)


