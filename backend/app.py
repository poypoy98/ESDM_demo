from fastapi import FastAPI, Request
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for development (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read configuration from environment with sensible defaults
SPARQL_ENDPOINT = os.getenv("SPARQL_ENDPOINT", "http://ontop:8080/sparql")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")


def query_ollama(prompt):
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()
    return r.json().get("response", "")


@app.post("/query")
async def query(request: Request):
    body = await request.json()
    nl = body.get("query", "")
    session = body.get("session", "default")

    prompt = f"""You are a SPARQL expert. Translate the user's natural language question into a SPARQL query
based on the following ontology classes: Event, Interaction, Fulfillment.
Use PREFIX : <http://example.com/ontology#>.
Example mappings:
- "what is happening" -> query all Events
- "requests" or "fulfillment" -> query Fulfillment
- "interaction" -> query Interaction
User query: "{nl}"
Return only the SPARQL query.
"""

    sparql_query = query_ollama(prompt).strip()
    if "SELECT" not in sparql_query:
        sparql_query = """
        PREFIX : <http://example.com/ontology#>
        SELECT ?event ?id ?desc ?timestamp
        WHERE {
          ?event a :Event ;
                 :eventID ?id ;
                 :eventDescription ?desc ;
                 :eventTimestamp ?timestamp .
        }
        ORDER BY ?timestamp
        """

    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]

    return {
        "session": session,
        "sparql": sparql_query,
        "results": results,
    }
