import os

from dotenv import load_dotenv

env = os.getenv("ENV", "")  # this tries to go to  the .env file to look for the "ENV' variable

print(env, "----")

# checks the value of th the env, if it's production then we don't need the load_dotenv library
if env != "production":
    # but if it's not production then we definitely need the  load_dotenv, to find our ".env" file and let our os load
    # it
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__name__)),
                               "{env}.env".format(env=env))  # THis just gets the .env path
    # so dotnv path == somthing like  like C:/Users/Romisagoat/projec/.env

    print(dotenv_path, "dotenv====")
    # this then loads this to our os letting it know that this is the env file it should read from
    load_dotenv(verbose=True, dotenv_path=dotenv_path)

secret_key = os.getenv('SECRET_KEY')
mongodb_url = os.getenv('MONGODB_URL')
mongodb_name = os.getenv('MONGODB_NAME')

"""
just get out
So basically locally we have to load our .env to the os, so it can read al our variables using the os.getenv()
"""