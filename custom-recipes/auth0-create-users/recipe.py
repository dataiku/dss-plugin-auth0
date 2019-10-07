import dataiku
from dataiku.customrecipe import *
import requests, json, secrets
import pandas as pd
import dkuauth0

input_ds = dataiku.Dataset(get_input_names_for_role('main')[0])
output_ds = dataiku.Dataset(get_output_names_for_role('main')[0])
config = get_recipe_config()

s = dkuauth0.create_session(config["connection"])

results = []

for row in input_ds.iter_rows():
    row = dict(row)
    row["email_verified"] = True
    row["connection"] = "Username-Password-Authentication"
    row["password"] = secrets.token_hex(32) + "!"
    print(row)
    
    ret = s.post("https://dataiku.auth0.com/api/v2/users", data = json.dumps(row), headers={"Content-Type" : "application/json"})
    print("Ret is %s" % ret.text)
    
    results.append({"email" : row["email"], "http_code" : ret.status_code, "body" : ret.text})

output_ds.write_with_schema(pd.DataFrame(results))
