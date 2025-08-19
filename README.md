The backfolder Contains : Vector Database - Chroma and FastAPI Routes 
these are the only Routes i am able to implement : 
1. Create User
2. Get all Users
3. Delete User
4. Call LLM like ask Query and Get response 

Vectore Database is working , Fast API Routes are working But no integration Between them 

I am using Langchain CSV loader to To load the CSV and chunk and embeed it and store in Vector DB ~ Chroma

Frontend is in Streamlit :
In frontend i am using Streamlit to create a simple UI
and it is Integrted with AI, All we need to do is Drop the API key in the Streamlit.py and Then run the code 
I am using OpenAI API to get the response from the LLM


To run the Frontend
'''
streamlit run streamlit.py
'''

To run the Backend
'''
uvicorn app:app --reload
'''
