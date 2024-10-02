import json
# TELEGRAM_TOKEN = '7185545350:AAGtOuW_ZTTCHXNiN2oI1cGxxC_1wD0vQKw'
API_TOKEN = '7288098737:AAEssWaZUuv5F0-bCRBfscJ6jGHAnd-Rg-w' # 法

def obj_to_json(obj) ->str:
    return json.dumps(obj.__dict__, indent=4)