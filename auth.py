import os
import keyring


class Auth:
    fred_key = keyring.get_password('fred', os.getlogin())
    os.environ['FRED_API_KEY'] = fred_key

