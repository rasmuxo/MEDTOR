# MEDTOR is a code-based self diagnostic tool. Due to the scope of the project, the database is currently limited to a small range of
# symptoms and pulmonary illnesses. MEDTOR diagnoses a user by asking yes or no questions about their symptoms. Each symptom is weighted
# on a severity scale of 1-3, with 1 being the least severe and 3 being the most severe. Each illness is pre-defined with a list of
# symptoms. The program adds the weights of the 'yes' symptoms and uses a modified Jaccard Similarity calculator to create a similarity
# score between the weights of the 'yes' symptoms and the weights of the symptoms in each illness. Whichever 'yes' symptom - illness
# match has the highest similarity score is diagnosed as the illness. Additionally, MEDTOR offers information about the diagnosed
# illness after each diagnoses to make sure the user is informed and educated.

import random

class Character:
    def __init__(self, name, traits):
        self.name = name
        self.traits = traits

# ANSI escape code for red text
RED_TEXT = "\033[91m"

# ANSI escape code for lime green text
LIME_GREEN_TEXT = "\033[92m"

# ANSI escape code to reset text color
RESET_TEXT_COLOR = "\033[0m"

# List of all symptoms
all_symptoms = [
    "shortness of breath", "cough", "wheezing", "chest tightness", "fatigue",
    "sputum production", "abnormal breath sounds", "abnormal pulmonary function test",
    "increased mucus production", "chest discomfort", "fever", "cyanosis",
    "clubbing of fingers", "hemoptysis", "weight loss", "abnormal chest x-ray",
    "night sweats", "loss of appetite", "dizziness", "fast heart rate",
    "leg swelling", "anxiety", "sweating", "skin rash", "joint pain",
    "swollen lymph nodes", "enlarged spleen", "eye redness", "reduced chest expansion",
    "decreased breath sounds", "hypoxia", "pink frothy sputum", "chest palpitations",
    "rapid breathing", "confusion", "low blood pressure", "failure to thrive",
    "low blood oxygen", "abdominal pain", "enlarged abdomen"
]

# This section defines symptom weights (higher values indicate higher severity of the symptom)
symptom_weights = {
    "shortness of breath": 1,
    "cough": 1,
    "wheezing": 2,
    "chest tightness": 2,
    "fatigue": 1,
    "sputum production": 1,
    "abnormal breath sounds": 1,
    "abnormal pulmonary function test": 2,
    "increased mucus production": 1,
    "chest discomfort": 1,
    "fever": 2,
    "cyanosis": 3,
    "clubbing of fingers": 2,
    "hemoptysis": 2,
    "weight loss": 1,
    "abnormal chest x-ray": 2,
    "night sweats": 1,
    "loss of appetite": 1,
    "dizziness": 1,
    "fast heart rate": 1,
    "leg swelling": 2,
    "anxiety": 1,
    "sweating": 1,
    "skin rash": 2,
    "joint pain": 2,
    "swollen lymph nodes": 1,
    "enlarged spleen": 1,
    "eye redness": 1,
    "reduced chest expansion": 1,
    "decreased breath sounds": 1,
    "hypoxia": 2,
    "pink frothy sputum": 2,
    "chest palpitations": 1,
    "rapid breathing": 1,
    "confusion": 1,
    "low blood pressure": 1,
    "failure to thrive": 1,
    "low blood oxygen": 2,
    "abdominal pain": 1,
    "enlarged abdomen": 1,
    "chest pain": 2,
    "swelling in ankles and legs": 2,
    "fainting": 1,
    # Add weights for other symptoms here as needed
}

# Database of illness descriptions
illness_description = {
    "Asthma": "Asthma is a chronic respiratory condition characterized by recurrent episodes of shortness of breath, coughing, wheezing, chest tightness, and increased mucus production. It often worsens in response to triggers like allergens or irritants.",
    "Chronic Bronchitis": "Chronic bronchitis is a type of chronic obstructive pulmonary disease (COPD) that involves persistent cough, increased mucus production, chest discomfort, fever, shortness of breath, and can lead to complications like cyanosis and clubbing of fingers.",
    "Emphysema": "Emphysema is a progressive lung disease that damages the air sacs in the lungs, leading to difficulty in exhaling, shortness of breath, coughing, and chest tightness. It is often associated with long-term smoking.",
    "Pneumonia": "Pneumonia is a lung infection that can cause symptoms such as shortness of breath, cough, chest pain, fever, fatigue, and production of yellow or green sputum. It can be caused by bacteria, viruses, or other pathogens.",
    "Tuberculosis": "Tuberculosis (TB) is a bacterial infection that primarily affects the lungs. It can lead to symptoms like cough, fever, fatigue, weight loss, and coughing up blood. TB is contagious and requires treatment with antibiotics.",
    "Lung Cancer": "Lung cancer is a malignancy that often presents with symptoms like shortness of breath, cough, chest pain, fatigue, and coughing up blood. It can occur due to smoking or exposure to carcinogens.",
    "Pulmonary Hypertension": "Pulmonary hypertension is a condition characterized by high blood pressure in the arteries of the lungs. Symptoms include shortness of breath, chest pain, fatigue, and cyanosis.",
    "Pulmonary Fibrosis": "Pulmonary fibrosis is a lung disease that causes scarring of the lung tissue, leading to shortness of breath, cough, chest pain, fatigue, and weight loss. It is a progressive condition with limited treatment options.",
    "Bronchiectasis": "Bronchiectasis is a chronic lung condition where the bronchial tubes are damaged and widened. It results in symptoms like chronic cough, increased mucus production, chest discomfort, and shortness of breath.",
    "Pleural Effusion": "Pleural effusion is the accumulation of fluid in the pleural cavity surrounding the lungs. It can cause symptoms such as shortness of breath, chest pain, fever, and fatigue.",
    "Pulmonary Embolism": "Pulmonary embolism is a blockage in the pulmonary artery, typically caused by a blood clot. Symptoms include sudden shortness of breath, cough, chest pain, fever, and sometimes hemoptysis.",
    "Sarcoidosis": "Sarcoidosis is an inflammatory disease that can affect various organs, including the lungs. Pulmonary symptoms may include cough, fever, fatigue, weight loss, and abnormal chest X-rays.",
    "COPD (Chronic Obstructive Pulmonary Disease)": "COPD is a progressive lung disease that includes conditions like chronic bronchitis and emphysema. It leads to symptoms such as shortness of breath, chronic cough, wheezing, and chest tightness.",
    "Interstitial Lung Disease": "Interstitial lung disease refers to a group of disorders that cause inflammation and scarring of the lung tissue. Symptoms often include shortness of breath, cough, chest pain, and abnormal pulmonary function tests.",
    "Atelectasis": "Atelectasis is the collapse or closure of a part of the lung. It can lead to symptoms like shortness of breath, cough, chest pain, fever, and reduced breath sounds on examination.",
    "Pulmonary Edema": "Pulmonary edema is the accumulation of fluid in the air sacs of the lungs. It can cause symptoms such as shortness of breath, cough, chest pain, and pink frothy sputum.",
    "Pleural Mesothelioma": "Pleural mesothelioma is a rare cancer that affects the lining of the lungs. It can cause symptoms like shortness of breath, cough, chest pain, weight loss, and clubbing of fingers.",
    "Respiratory Distress Syndrome (ARDS)": "ARDS is a severe lung condition that leads to symptoms such as shortness of breath, cough, chest pain, fever, rapid breathing, and low blood pressure.",
    "Pulmonary Alveolar Proteinosis": "Pulmonary alveolar proteinosis is a rare lung disease where a protein substance accumulates in the air sacs, causing symptoms like shortness of breath, cough, fever, and weight loss.",
    "Pulmonary Hypoplasia": "Pulmonary hypoplasia is a condition where the lungs do not develop properly, leading to symptoms like shortness of breath, rapid breathing, and cyanosis.",
    "Pulmonary Sarcoidosis": "Pulmonary sarcoidosis is a form of sarcoidosis that primarily affects the lungs, leading to symptoms like cough, fever, fatigue, weight loss, and skin rashes.",
    "Pulmonary Lymphangioleiomyomatosis (LAM)": "LAM is a rare lung disease that primarily affects women. It causes symptoms such as shortness of breath, cough, chest pain, fatigue, and abnormal chest X-rays.",
    "Pulmonary Arterial Hypertension (PAH)": "PAH is a type of pulmonary hypertension characterized by high blood pressure in the arteries of the lungs. Symptoms include shortness of breath, chest pain, fatigue, and swelling in the ankles and legs.",
    "Pulmonary Alveolar Microlithiasis": "Pulmonary alveolar microlithiasis is a rare lung disease where small calcium deposits accumulate in the air sacs, causing symptoms like shortness of breath, cough, and chest pain.",
    "Pulmonary Sequestration": "Pulmonary sequestration is a congenital condition where lung tissue doesn't connect to the normal airways. It can cause symptoms like shortness of breath, cough, chest pain, and abdominal pain.",
    "Pulmonary Hypertension due to Left Heart Disease": "Pulmonary hypertension due to left heart disease occurs when heart conditions affect the lungs. Symptoms include shortness of breath, chest pain, fatigue, and swelling in the ankles and legs.",
    "Pulmonary Hypertension due to Lung Disease": "Pulmonary hypertension due to lung disease results from lung conditions affecting the blood vessels in the lungs, leading to symptoms like shortness of breath and fatigue.",
    "Pulmonary Hypertension due to Chronic Blood Clots": "Pulmonary hypertension due to chronic blood clots is caused by recurrent clotting in the pulmonary arteries. Symptoms include shortness of breath, chest pain, fatigue, and swelling in the ankles and legs.",
}

def calculate_similarity(user_traits, illness_traits):
    # Program uses Jaccard Similarity to create a similarity score between the inputted symptoms and the symptoms of each illness. A higher similarity score means more aligning symptoms.
    intersection = sum(symptom_weights[symptom] for symptom in user_traits if symptom in illness_traits)
    user_weight_sum = sum(symptom_weights[symptom] for symptom in user_traits)
    illness_weight_sum = sum(symptom_weights[symptom] for symptom in illness_traits)
    
    return intersection / (user_weight_sum + illness_weight_sum - intersection) if user_weight_sum > 0 else 0

def validate_yes_no_input(input_string):
    """
    Validates user input to ensure it's either 'yes' or 'no'.
    """
    while True:
        user_input = input(input_string).strip().lower()
        if user_input == 'yes' or user_input == 'no':
            return user_input
        else:
            print("Sorry! I didn't quite catch that... Could you please respond with a 'yes' or 'no'?")

def ask_user_for_symptoms():
    user_symptoms = []
    print("Welcome to MEDTOR!")
    print("I will guess your illness based on your symptoms.")
    print("Answer with 'yes' or 'no' to the following questions.")

    for i, symptom in enumerate(all_symptoms):
        if i % 5 == 0 and i > 0:
            more_questions = validate_yes_no_input("Do you want to answer more questions? (yes/no) ")
            if more_questions != "yes":
                break

        answer = validate_yes_no_input(f"Are you experiencing {symptom}? ")
        
        if answer == "yes":
            user_symptoms.append(symptom)

    return user_symptoms

def diagnose_illness(user_symptoms):
    characters = [
    Character("Asthma", ["shortness of breath", "cough", "wheezing", "chest tightness", "fatigue", "sputum production", "abnormal breath sounds", "abnormal pulmonary function test"]),
    Character("Chronic Bronchitis", ["cough", "increased mucus production", "chest discomfort", "fever", "shortness of breath", "wheezing", "cyanosis", "clubbing of fingers", "hemoptysis", "weight loss", "abnormal breath sounds", "abnormal chest x-ray", "abnormal pulmonary function test", "chest tightness", "night sweats", "loss of appetite"]),
    Character("Emphysema", ["shortness of breath", "cough", "wheezing", "chest tightness", "fatigue", "sputum production", "abnormal breath sounds", "abnormal pulmonary function test"]),
    Character("Pneumonia", ["shortness of breath", "cough", "chest pain", "fever", "fatigue", "sputum production", "cyanosis", "clubbing of fingers", "hemoptysis", "weight loss", "abnormal breath sounds", "abnormal chest x-ray", "abnormal pulmonary function test", "chest tightness", "night sweats", "loss of appetite"]),
    Character("Tuberculosis", ["shortness of breath", "cough", "fever", "fatigue", "sputum production", "cyanosis", "clubbing of fingers", "hemoptysis", "weight loss", "abnormal breath sounds", "abnormal chest x-ray", "abnormal pulmonary function test", "loss of appetite"]),
    Character("Lung Cancer", ["shortness of breath", "cough", "chest pain", "fatigue", "sputum production", "clubbing of fingers", "hemoptysis", "weight loss", "abnormal breath sounds", "abnormal chest x-ray", "abnormal pulmonary function test", "loss of appetite"]),
    Character("Pulmonary Hypertension", ["shortness of breath", "chest pain", "fatigue", "cyanosis", "abnormal breath sounds", "abnormal chest x-ray"]),
    Character("Pulmonary Fibrosis", ["shortness of breath", "cough", "chest pain", "fatigue", "sputum production", "cyanosis", "clubbing of fingers", "hemoptysis", "weight loss", "abnormal breath sounds", "abnormal chest x-ray", "abnormal pulmonary function test", "loss of appetite"]),
    Character("Bronchiectasis", ["cough", "increased mucus production", "chest discomfort", "shortness of breath", "wheezing", "hemoptysis", "abnormal breath sounds", "loss of appetite"]),
    Character("Pleural Effusion", ["shortness of breath", "chest pain", "fever", "fatigue", "cyanosis", "abnormal breath sounds", "chest tightness", "night sweats", "loss of appetite"]),
    Character("Pulmonary Embolism", ["shortness of breath", "cough", "chest pain", "fever", "cyanosis", "hemoptysis", "dizziness", "fast heart rate", "leg swelling", "chest tightness", "anxiety", "sweating"]),
    Character("Sarcoidosis", ["cough", "fever", "fatigue", "weight loss", "skin rash", "joint pain", "swollen lymph nodes", "enlarged spleen", "eye redness", "abnormal breath sounds", "abnormal chest x-ray", "loss of appetite"]),
    Character("COPD (Chronic Obstructive Pulmonary Disease)", ["shortness of breath", "cough", "wheezing", "chest tightness", "fatigue", "sputum production", "abnormal breath sounds", "abnormal pulmonary function test"]),
    Character("Interstitial Lung Disease", ["shortness of breath", "cough", "chest pain", "fatigue", "sputum production", "cyanosis", "clubbing of fingers", "weight loss", "abnormal breath sounds", "abnormal chest x-ray", "abnormal pulmonary function test"]),
    Character("Atelectasis", ["shortness of breath", "cough", "chest pain", "fever", "cyanosis", "decreased breath sounds", "reduced chest expansion", "hypoxia"]),
    Character("Pulmonary Edema", ["shortness of breath", "cough", "chest pain", "wheezing", "fatigue", "pink frothy sputum", "rapid breathing", "anxiety", "leg swelling", "hypoxia"]),
    Character("Pleural Mesothelioma", ["shortness of breath", "cough", "chest pain", "fever", "fatigue", "sputum production", "weight loss", "cyanosis", "clubbing of fingers", "hemoptysis", "loss of appetite"]),
    Character("Respiratory Distress Syndrome (ARDS)", ["shortness of breath", "cough", "chest pain", "fever", "rapid breathing", "hypoxia", "low blood pressure", "confusion", "fatigue"]),
    Character("Pulmonary Alveolar Proteinosis", ["shortness of breath", "cough", "fever", "fatigue", "weight loss", "cyanosis", "chest pain", "wheezing", "night sweats"]),
    Character("Pulmonary Hypoplasia", ["shortness of breath", "cough", "rapid breathing", "cyanosis", "wheezing", "fatigue", "failure to thrive", "low blood oxygen"]),
    Character("Pulmonary Sarcoidosis", ["cough", "fever", "fatigue", "weight loss", "skin rash", "joint pain", "swollen lymph nodes", "enlarged spleen", "eye redness", "abnormal breath sounds", "abnormal chest x-ray", "loss of appetite"]),
    Character("Pulmonary Lymphangioleiomyomatosis (LAM)", ["shortness of breath", "cough", "chest pain", "fatigue", "wheezing", "cyanosis", "abnormal breath sounds", "abnormal chest x-ray", "hemoptysis", "loss of appetite"]),
    Character("Pulmonary Arterial Hypertension (PAH)", ["shortness of breath", "chest pain", "fatigue", "cyanosis", "abnormal breath sounds", "abnormal chest x-ray", "swelling in ankles and legs", "dizziness", "fainting", "chest palpitations"]),
    Character("Pulmonary Alveolar Microlithiasis", ["shortness of breath", "cough", "chest pain", "fatigue", "cyanosis", "abnormal breath sounds", "abnormal chest x-ray", "chest tightness", "hemoptysis", "loss of appetite"]),
    Character("Pulmonary Sequestration", ["shortness of breath", "cough", "chest pain", "cyanosis", "hemoptysis", "fever", "wheezing", "abnormal chest x-ray", "abdominal pain", "enlarged abdomen"]),
    Character("Pulmonary Hypertension Due to Left Heart Disease", ["shortness of breath", "cough", "chest pain", "fatigue", "cyanosis", "abnormal breath sounds", "abnormal chest x-ray", "swelling in ankles and legs", "dizziness", "fainting"]),
    Character("Pulmonary Hypertension Due to Lung Disease", ["shortness of breath", "cough", "chest pain", "fatigue", "cyanosis", "abnormal breath sounds", "abnormal chest x-ray", "swelling in ankles and legs", "dizziness", "fainting"]),
    Character("Pulmonary Hypertension Due to Chronic Blood Clots", ["shortness of breath", "cough", "chest pain", "fatigue", "cyanosis", "abnormal breath sounds", "abnormal chest x-ray", "swelling in ankles and legs", "dizziness", "fainting"]),
    Character("No Illness", [])
]

    best_match = None
    best_similarity = 0

    for character in characters:
        similarity = calculate_similarity(user_symptoms, character.traits)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = character

    return best_match

def main():
    # Display the ASCII art in green
    medtor_ascii_art = """\033[92m
    ooo        ooooo oooooooooooo oooooooooo.   ooooooooooooo   .oooooo.   ooooooooo.   
    `88.       .888' `888'     `8 `888'   `Y8b  8'   888   `8  d8P'  `Y8b  `888   `Y88.  ™
     888b     d'888   888          888      888      888      888      888  888   .d88' 
     8 Y88. .P  888   888oooo8     888      888      888      888      888  888ooo88P'  
     8  `888'   888   888    "     888      888      888      888      888  888`88b.    
     8    Y     888   888       o  888     d88'      888      `88b    d88'  888  `88b.  
    o8o        o888o o888ooooood8 o888bood8P'       o888o      `Y8bood8P'  o888o  o888o
    \033[0m"""
    print(medtor_ascii_art)

    user_symptoms = ask_user_for_symptoms()

    if not user_symptoms:
        healthy_message = f"{LIME_GREEN_TEXT}You seem pretty healthy to me! Congratulations!{RESET_TEXT_COLOR}"
        print(healthy_message)
        return

    best_match = diagnose_illness(user_symptoms)

    if best_match:
        diagnosis_illness = best_match.name
        diagnosis = f"{RED_TEXT}I diagnose you with {diagnosis_illness}!{RESET_TEXT_COLOR}"
        print(diagnosis)

        more_info = input("Would you like more information about this illness? (yes/no) ").lower()
        if more_info == "yes" and diagnosis_illness in illness_description:
            print(illness_description[diagnosis_illness])
        else:
            print("Thanks for letting me diagnose you!")
    else:
        print("Hmm... I'm stumped, let's start over!")

if __name__ == "__main__":
    while True:
        main()
        restart = input("Would you like to start over? (yes/no) ").lower()
        if restart != "yes":
            print("Alright. Have a wonderful day!")
            break
