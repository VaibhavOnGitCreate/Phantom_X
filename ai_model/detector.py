import generate_response as gr
import ast 


def fetch_risk_datasets(user_message : str):
    r_data_set = []
    dataset = str(gr.generate_ai_response(
        question = f"user_message is {user_message}",
        prompt = open("../Phantom_X/prompts/risk_dataset.txt" , "r").read(),
        model_ch=0
        )).strip()
    try:
        r_data_set = ast.literal_eval(dataset)
    except:
        r_data_set = [[],[],[],[],[],[]]
        print("empty dataset found!!")
    
    

    
    return r_data_set

# print(fetch_risk_datasets(user_message="""Dear Customer,

# We detected unusual activity in your account. For your security, your account will be temporarily suspended within 24 hours unless you verify your information immediately.

# Please click the secure link below to confirm your details:
# https://secure-bank-verify.example.com

# Failure to verify may result in permanent suspension of your account.

# Thank you,
# Security Team
# Your Trusted Bank
# """))

def fetch_risk_score(user_message : str):
    r_data_set = 0
    dataset = str(gr.generate_ai_response(
        question = f"user_message is {user_message}",
        prompt = open("../Phantom_X/prompts/risk_score.txt" , "r").read(),
        model_ch=0
        )).strip()
    try:
        r_data_set = ast.literal_eval(dataset)
    except:
        r_data_set = 0
        print("empty dataset found!!")

    return r_data_set

# print(fetch_risk_score(user_message="""Dear Customer,

# We detected unusual activity in your account. For your security, your account will be temporarily suspended within 24 hours unless you verify your information immediately.

# Please click the secure link below to confirm your details:
# https://secure-bank-verify.example.com

# Failure to verify may result in permanent suspension of your account.

# Thank you,
# Security Team
# Your Trusted Bank
# """))
    
def fetch_ai_insights(user_message : str):
    r_data_set = 0
    dataset = str(gr.generate_ai_response(
        question = f"user_message is {user_message}",
        prompt = open("../Phantom_X/prompts/risk_insights.txt" , "r").read(),
        model_ch=1
        )).strip()
    try:
        r_data_set = ast.literal_eval(dataset)
    except:
        r_data_set = ""

    return r_data_set

# print(fetch_ai_insights(user_message="""Dear Customer,

# We detected unusual activity in your account. For your security, your account will be temporarily suspended within 24 hours unless you verify your information immediately.

# Please click the secure link below to confirm your details:
# https://secure-bank-verify.example.com

# Failure to verify may result in permanent suspension of your account.

# Thank you,
# Security Team
# Your Trusted Bank
# """))

def fetch_ai_reponse(user_message : str):
    r_data_set = 0
    dataset = str(gr.generate_ai_response(
        question = f"user_message is {user_message}",
        prompt = open("../Phantom_X/prompts/risk_chatbot.txt" , "r").read(),
        model_ch=1
        )).strip()
    try:
        r_data_set = dataset
    except:
        r_data_set = ""

    return r_data_set

# print(fetch_ai_reponse(user_message="""Dear Customer,

# We detected unusual activity in your account. For your security, your account will be temporarily suspended within 24 hours unless you verify your information immediately.

# Please click the secure link below to confirm your details:
# https://secure-bank-verify.example.com

# Failure to verify may result in permanent suspension of your account.

# Thank you,
# Security Team
# Your Trusted Bank
# """))


