import json
from difflib import get_close_matches
import random

def load_knowledge_base(file_path: str) -> dict:
	with open(file_path, 'r') as file:
		data: dict = json.load(file)
	return data

def save_knowledge_base(file_path: str,data: dict):
	with open(file_path, 'w') as file:
		json.dump(data,file,indent=2)
#|
def find_best_match(user_questions: str, questions):
	matches: list = get_close_matches(user_questions,questions,n = 1 ,cutoff = 0.6)
	#print(f"matches: {matches}")
	return matches[0] if matches else None

def get_answer(question : str, knowledge_base: dict):
	for q in knowledge_base["Questoes"]:
		if q['Questao'] == question:
			respostas = q['resposta']
			index = random.randint(0, len(respostas) - 1)
			#print(index)
			return respostas[index]

