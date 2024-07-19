from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# sentences = ["This is an example sentence", "Each sentence is converted"]
# embeddings = model.encode(sentences)
# print(embeddings)

corpus_of_documents = [
    "Take a leisurely walk in the park and enjoy the fresh air.",
    "Visit a local museum and discover something new.",
    "Attend a live music concert and feel the rhythm.",
    "Go for a hike and admire the natural scenery.",
    "Have a picnic with friends and share some laughs.",
    "Explore a new cuisine by dining at an ethnic restaurant.",
    "Take a yoga class and stretch your body and mind.",
    "Join a local sports league and enjoy some friendly competition.",
    "Attend a workshop or lecture on a topic you're interested in.",
    "Visit an amusement park and ride the roller coasters."
]

doc_embeddings = model.encode(corpus_of_documents)

query = "What's the best outside activity?"
query_embedding = model.encode([query])

similarities = cosine_similarity(query_embedding, doc_embeddings)

indexed = list(enumerate(similarities[0]))
sorted_index = sorted(indexed, key=lambda x: x[1], reverse=True)


recommended_documents = []
for value, score in sorted_index:
    formatted_score = "{:.2f}".format(score)
    print(f"{formatted_score} => {corpus_of_documents[value]}")
    if score > 0.3:
        recommended_documents.append(corpus_of_documents[value])


prompt = """
You are a bot that makes recommendations for activities. You answer in very short sentences and do not include extra information.
These are potential activities:
{recommended_activities}
The user's query is: {user_input}
Provide the user with 2 recommended activities based on their query.
"""
recommended_activities = "\n".join(recommended_documents)


user_input = "I like to hike"
full_prompt = prompt.format(user_input=user_input, recommended_activities=recommended_activities)



url = 'http://localhost:11434/api/generate'
data = {
    "model": "llama2",
    "prompt": full_prompt
}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)
full_response=[]
try:
    count = 0
    for line in response.iter_lines():
        #filter out keep-alive new lines
        # count += 1
        # if count % 5== 0:
        #     print(decoded_line['response']) # print every fifth token
        if line:
            decoded_line = json.loads(line.decode('utf-8'))
            
            full_response.append(decoded_line['response'])
finally:
    response.close()
print(''.join(full_response))