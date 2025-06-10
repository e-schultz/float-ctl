TITLE: Installing ChromaDB Client
DESCRIPTION: This snippet provides commands to install the `chromadb-client` package using different Node.js package managers: npm, pnpm, and yarn. It's the first step to setting up the client in your project.
SOURCE: https://github.com/chroma-core/chroma/blob/main/clients/js/packages/chromadb-client/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
# npm
npm install chromadb-client

# pnpm
pnpm add chromadb-client

# yarn
yarn add chromadb-client
```

----------------------------------------

TITLE: Running ChromaDB Server via Docker Container
DESCRIPTION: This command initiates a ChromaDB server within a Docker container, mapping host port 8000 to the container's port 8000 and persisting data to a local './chroma-data' directory. It uses the official 'chromadb/chroma' image with default settings.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/production/containers/docker.md#_snippet_0

LANGUAGE: terminal
CODE:
```
docker run -v ./chroma-data:/data -p 8000:8000 chromadb/chroma
```

----------------------------------------

TITLE: Adding Documents to a Collection (TypeScript)
DESCRIPTION: This TypeScript snippet demonstrates how to asynchronously add text documents and their unique IDs to a Chroma collection. Chroma automatically handles embedding and indexing these documents.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/overview/getting-started.md#_snippet_12

LANGUAGE: typescript
CODE:
```
await collection.add({
    documents: [
        "This is a document about pineapple",
        "This is a document about oranges",
    ],
    ids: ["id1", "id2"],
});
```

----------------------------------------

TITLE: Importing ChromaDB Client in Python
DESCRIPTION: Imports the necessary `chromadb` library, which is the first step to interact with a ChromaDB instance.
SOURCE: https://github.com/chroma-core/chroma/blob/main/examples/basic_functionality/where_filtering.ipynb#_snippet_0

LANGUAGE: python
CODE:
```
import chromadb
```

----------------------------------------

TITLE: Initializing ChromaDB Client in Python
DESCRIPTION: Initializes a ChromaDB client instance. This client is used to connect to and manage ChromaDB collections.
SOURCE: https://github.com/chroma-core/chroma/blob/main/examples/basic_functionality/where_filtering.ipynb#_snippet_1

LANGUAGE: python
CODE:
```
client = chromadb.Client()
```

----------------------------------------

TITLE: Initializing Persistent ChromaDB Client and Collection (Python)
DESCRIPTION: Initializes a `PersistentClient` for ChromaDB, specifying a directory ('db') for data persistence. It then gets or creates a collection named 'peristed_collection', ensuring that data can be stored and retrieved from this specific collection.
SOURCE: https://github.com/chroma-core/chroma/blob/main/examples/basic_functionality/local_persistence.ipynb#_snippet_1

LANGUAGE: python
CODE:
```
# Create a new Chroma client with persistence enabled. 
persist_directory = "db"

client = chromadb.PersistentClient(path=persist_directory)

# Create a new chroma collection
collection_name = "peristed_collection"
collection = client.get_or_create_collection(name=collection_name)
```

----------------------------------------

TITLE: Querying Chroma Collection by Texts (Python)
DESCRIPTION: This snippet shows how to query a Chroma collection using `query_texts`. Chroma will first embed each text, then perform the query. It supports `n_results`, `where` for metadata, and `where_document` for document content filtering.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_32

LANGUAGE: Python
CODE:
```
collection.query(
    query_texts=["doc10", "thus spake zarathustra", ...],
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains":"search_string"}
)
```

----------------------------------------

TITLE: Querying ChromaDB with New Text - TypeScript
DESCRIPTION: This TypeScript snippet demonstrates how to set up an in-memory ChromaDB client, get or create a collection, upsert documents, and perform a semantic search query. It shows how to query with a new text string ('This is a query document about florida') and retrieve a specified number of results, logging the output.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/overview/getting-started.md#_snippet_18

LANGUAGE: typescript
CODE:
```
import { ChromaClient } from "chromadb";
const client = new ChromaClient();

// switch `createCollection` to `getOrCreateCollection` to avoid creating a new collection every time
const collection = await client.getOrCreateCollection({
    name: "my_collection",
});

// switch `addRecords` to `upsertRecords` to avoid adding the same documents every time
await collection.upsert({
    documents: [
        "This is a document about pineapple",
        "This is a document about oranges",
    ],
    ids: ["id1", "id2"],
});

const results = await collection.query({
    queryTexts: "This is a query document about florida", // Chroma will embed this for you
    nResults: 2, // how many results to return
});

console.log(results);
```

----------------------------------------

TITLE: Querying Chroma Collections by Embeddings (Python)
DESCRIPTION: This snippet demonstrates how to query a Chroma collection using a list of `query_embeddings`. It allows specifying the number of results (`n_results`), applying metadata filters (`where`), document content filters (`where_document`), and filtering by specific document IDs (`ids`). The query returns the closest matches to each embedding.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/querying-collections/query-and-get.md#_snippet_0

LANGUAGE: python
CODE:
```
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains":"search_string"},
    ids=["id1", "id2", ...]
)
```

----------------------------------------

TITLE: Creating a Collection (Python)
DESCRIPTION: This Python snippet shows how to create a new collection within the Chroma database using the client object. Collections are named containers for embeddings, documents, and metadata.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/overview/getting-started.md#_snippet_9

LANGUAGE: python
CODE:
```
collection = chroma_client.create_collection(name="my_collection")
```

----------------------------------------

TITLE: Creating a ChromaDB Collection for SciQ Supports
DESCRIPTION: This Python snippet creates a new collection named "sciq_supports" within the initialized ChromaDB client. This collection will be used to store the supporting evidence from the SciQ dataset. By default, ChromaDB will use its built-in embedding function, eliminating the need for explicit specification.
SOURCE: https://github.com/chroma-core/chroma/blob/main/examples/basic_functionality/start_here.ipynb#_snippet_3

LANGUAGE: Python
CODE:
```
# Create a new Chroma collection to store the supporting evidence. We don't need to specify an embedding fuction, and the default will be used.
collection = client.create_collection("sciq_supports")
```

----------------------------------------

TITLE: Installing Dependencies and Running Chatbot Application
DESCRIPTION: This snippet provides the sequence of shell commands required to set up and run the document chatbot. It covers installing Python dependencies, loading the example documents into the Chroma vector database, and finally launching the main chatbot application.
SOURCE: https://github.com/chroma-core/chroma/blob/main/examples/chat_with_your_documents/README.md#_snippet_1

LANGUAGE: Bash
CODE:
```
pip install -r requirements.txt

python load_data.py

python main.py
```

----------------------------------------

TITLE: Building a RAG Pipeline with Chroma and Haystack
DESCRIPTION: This Python example illustrates how to construct a Retrieval-Augmented Generation (RAG) pipeline using `ChromaQueryRetriever` and Haystack components like `HuggingFaceTGIGenerator` and `PromptBuilder`. It defines a prompt template and connects components to perform a query against the Chroma document store.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/integrations/frameworks/haystack.md#_snippet_2

LANGUAGE: python
CODE:
```
from chroma_haystack.retriever import ChromaQueryRetriever
from haystack.components.generators import HuggingFaceTGIGenerator
from haystack.components.builders import PromptBuilder

prompt = """
Answer the query based on the provided context.
If the context does not contain the answer, say 'Answer not found'.
Context:
{% for doc in documents %}
  {{ doc.content }}
{% endfor %}
query: {{query}}
Answer:
"""
prompt_builder = PromptBuilder(template=prompt)

llm = HuggingFaceTGIGenerator(model="mistralai/Mixtral-8x7B-Instruct-v0.1", token='YOUR_HF_TOKEN')
llm.warm_up()
retriever = ChromaQueryRetriever(document_store)

querying = Pipeline()
querying.add_component("retriever", retriever)
querying.add_component("prompt_builder", prompt_builder)
querying.add_component("llm", llm)

querying.connect("retriever.documents", "prompt_builder.documents")
querying.connect("prompt_builder", "llm")

results = querying.run({"retriever": {"queries": [query], "top_k": 3},
                        "prompt_builder": {"query": query}})
```

----------------------------------------

TITLE: Adding Raw Documents to Chroma Collection (Python)
DESCRIPTION: This snippet demonstrates adding raw documents to a Chroma collection. Chroma automatically tokenizes and embeds these documents using the collection's embedding function. Each document requires a unique ID, and optional metadata can be provided for filtering.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_24

LANGUAGE: python
CODE:
```
collection.add(
    documents=["lorem ipsum...", "doc2", "doc3", ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    ids=["id1", "id2", "id3", ...]
)
```

----------------------------------------

TITLE: Upserting Embeddings in ChromaDB (Python)
DESCRIPTION: This function updates existing embeddings, metadatas, or documents, or creates them if they do not already exist, based on the provided IDs. Similar to 'update', embeddings can be computed from documents if not explicitly provided, leveraging the collection's 'embedding_function'.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/reference/python/collection.md#_snippet_8

LANGUAGE: python
CODE:
```
def upsert(ids: OneOrMany[ID],
           embeddings: Optional[OneOrMany[Embedding]] = None,
           metadatas: Optional[OneOrMany[Metadata]] = None,
           documents: Optional[OneOrMany[Document]] = None) -> None
```

----------------------------------------

TITLE: Querying ChromaDB with New Text - Python
DESCRIPTION: This Python snippet demonstrates how to set up an in-memory ChromaDB client, get or create a collection, upsert documents, and perform a semantic search query. It shows how to query with a new text string ('This is a query document about florida') and retrieve a specified number of results, printing the output.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/overview/getting-started.md#_snippet_17

LANGUAGE: python
CODE:
```
import chromadb
chroma_client = chromadb.Client()

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(name="my_collection")

# switch `add` to `upsert` to avoid adding the same documents every time
collection.upsert(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=["id1", "id2"]
)

results = collection.query(
    query_texts=["This is a query document about florida"], # Chroma will embed this for you
    n_results=2 # how many results to return
)

print(results)
```

----------------------------------------

TITLE: Upserting Records in Chroma Collection
DESCRIPTION: This snippet illustrates the `upsert` operation in Chroma, which acts as a combined update and add. If an `id` already exists in the collection, the corresponding item is updated. If an `id` is not found, a new item is created, similar to the `add` operation. This method is useful for ensuring data presence and currency.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/collections/update-data.md#_snippet_1

LANGUAGE: python
CODE:
```
collection.upsert(
    ids=["id1", "id2", "id3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    documents=["doc1", "doc2", "doc3", ...],
)
```

LANGUAGE: typescript
CODE:
```
await collection.upsert({
    ids: ["id1", "id2", "id3"],
    embeddings: [
        [1.1, 2.3, 3.2],
        [4.5, 6.9, 4.4],
        [1.1, 2.3, 3.2],
    ],
    metadatas: [
        { chapter: "3", verse: "16" },
        { chapter: "3", verse: "5" },
        { chapter: "29", verse: "11" },
    ],
    documents: ["doc1", "doc2", "doc3"],
});
```

----------------------------------------

TITLE: Installing ChromaDB Library (Bash)
DESCRIPTION: This Bash command installs the full `chromadb` library and its command-line interface (CLI) via pip. This installation is a prerequisite for running the Chroma server or utilizing the complete Chroma client functionalities.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_12

LANGUAGE: Bash
CODE:
```
pip install chromadb
```

----------------------------------------

TITLE: Installing ChromaDB (TypeScript/JavaScript - NPM)
DESCRIPTION: This snippet shows how to install `chromadb` and `chromadb-default-embed` using npm, the Node.js package manager. These packages are necessary for using Chroma in TypeScript or JavaScript projects.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/overview/getting-started.md#_snippet_2

LANGUAGE: terminal
CODE:
```
npm install --save chromadb chromadb-default-embed
```

----------------------------------------

TITLE: Importing ChromaDB Client - Python
DESCRIPTION: This snippet imports the `chromadb` library, which is the first step to interact with the Chroma vector database in Python.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_0

LANGUAGE: python
CODE:
```
import chromadb
```

----------------------------------------

TITLE: Querying Chroma Collection by Embeddings (Python)
DESCRIPTION: This snippet demonstrates how to query a Chroma collection using a list of `query_embeddings`. It retrieves the `n_results` closest matches and supports optional `where` and `where_document` filters for metadata and document content respectively. An exception is raised if embedding dimensions don't match.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_30

LANGUAGE: Python
CODE:
```
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains":"search_string"}
)
```

----------------------------------------

TITLE: Adding Documents to a Collection (Python)
DESCRIPTION: This Python snippet demonstrates how to add text documents and their unique IDs to a Chroma collection. Chroma automatically handles embedding and indexing these documents.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/overview/getting-started.md#_snippet_11

LANGUAGE: python
CODE:
```
collection.add(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=["id1", "id2"]
)
```

----------------------------------------

TITLE: Initializing ChromaDB Clients (Python)
DESCRIPTION: This snippet demonstrates various ways to initialize a ChromaDB client in Python for in-process usage. It shows how to create a default client, an ephemeral client for in-memory operations, or a persistent client for disk-based storage. These methods are applicable for direct Python integration.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/updates/migration.md#_snippet_0

LANGUAGE: Python
CODE:
```
import chromadb

client = chromadb.Client()
# or
client = chromadb.EphemeralClient()
# or
client = chromadb.PersistentClient()
```

----------------------------------------

TITLE: Adding Raw Documents to Chroma Collection (Javascript)
DESCRIPTION: This snippet shows how to add raw documents to a Chroma collection using `collection.add`. Chroma will automatically embed the documents. It requires unique IDs and allows optional metadata for additional information and filtering.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_25

LANGUAGE: javascript
CODE:
```
await collection.add({
    ids: ["id1", "id2", "id3", ...],
    metadatas: [{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    documents: ["lorem ipsum...", "doc2", "doc3", ...],
})
// input order
// ids - required
// embeddings - optional
// metadata - optional
// documents - optional
```

----------------------------------------

TITLE: Installing ChromaDB Client and Running Server
DESCRIPTION: This snippet provides commands for installing the ChromaDB client for Python using pip, and for JavaScript using npm. It also includes the command to run the ChromaDB server in client-server mode, specifying a path for database persistence.
SOURCE: https://github.com/chroma-core/chroma/blob/main/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
pip install chromadb # python client
# for javascript, npm install chromadb!
# for client-server mode, chroma run --path /chroma_db_path
```

----------------------------------------

TITLE: Updating Records in a Chroma Collection - Python
DESCRIPTION: This snippet shows how to update existing records in a ChromaDB collection using the `collection.update` method. It allows modification of IDs, embeddings, metadatas, and documents. If an ID is not found, the update for that ID is ignored.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_45

LANGUAGE: python
CODE:
```
collection.update(
    ids=["id1", "id2", "id3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    documents=["doc1", "doc2", "doc3", ...],
)
```

----------------------------------------

TITLE: Adding Embeddings to Collection in Python
DESCRIPTION: This function allows for the addition of new embeddings, along with their unique IDs, optional metadata, and associated documents, to the data store. It validates input lengths and ensures either embeddings or documents are provided, raising `ValueError` or `DuplicateIDError` on invalid or duplicate inputs.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/reference/python/collection.md#_snippet_2

LANGUAGE: python
CODE:
```
def add(ids: OneOrMany[ID],
        embeddings: Optional[OneOrMany[Embedding]] = None,
        metadatas: Optional[OneOrMany[Metadata]] = None,
        documents: Optional[OneOrMany[Document]] = None) -> None
```

----------------------------------------

TITLE: Adding Embeddings and Metadata to Chroma Collection (Python)
DESCRIPTION: This snippet shows how to add only pre-computed embeddings and associated metadata to a Chroma collection. Documents are stored externally, and `ids` are used to link the embeddings to those external documents. Unique IDs are required.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_28

LANGUAGE: python
CODE:
```
collection.add(
    ids=["id1", "id2", "id3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...]
)
```

----------------------------------------

TITLE: Creating and Getting Chroma Collections with Embedding Function
DESCRIPTION: This snippet demonstrates how to create and retrieve a Chroma collection using its name and an optional embedding function. The `embedding_function` must be supplied consistently when getting the collection if it was provided during creation.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/collections/create-get-delete.md#_snippet_0

LANGUAGE: python
CODE:
```
collection = client.create_collection(name="my_collection", embedding_function=emb_fn)
collection = client.get_collection(name="my_collection", embedding_function=emb_fn)
```

LANGUAGE: typescript
CODE:
```
let collection = await client.createCollection({
    name: "my_collection",
    embeddingFunction: emb_fn,
});

collection = await client.getCollection({
    name: "my_collection",
    embeddingFunction: emb_fn,
});
```

----------------------------------------

TITLE: Adding Documents with Embeddings to Chroma Collection (Python)
DESCRIPTION: This snippet illustrates adding documents along with pre-computed embeddings to a Chroma collection. Chroma stores the documents without re-embedding them. It requires unique IDs, and optional metadata can be included for filtering.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_26

LANGUAGE: python
CODE:
```
collection.add(
    documents=["doc1", "doc2", "doc3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    ids=["id1", "id2", "id3", ...]
)
```

----------------------------------------

TITLE: Installing ChromaDB Client
DESCRIPTION: Installs the `chromadb` or `chromadb-client` package using pip, which is necessary to interact with the ChromaDB server from Python applications.
SOURCE: https://github.com/chroma-core/chroma/blob/main/examples/basic_functionality/auth.ipynb#_snippet_0

LANGUAGE: bash
CODE:
```
pip install chromadb
```

LANGUAGE: bash
CODE:
```
pip install chromadb-client
```

----------------------------------------

TITLE: Upserting Records in a Chroma Collection - Python
DESCRIPTION: This snippet illustrates how to perform an upsert operation on a ChromaDB collection using `collection.upsert`. This method updates existing records if their IDs are found, or adds new records if their IDs do not exist.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_47

LANGUAGE: python
CODE:
```
collection.upsert(
    ids=["id1", "id2", "id3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    documents=["doc1", "doc2", "doc3", ...],
)
```

----------------------------------------

TITLE: Initializing ChromaDB Client
DESCRIPTION: This Python code imports the `chromadb` library and instantiates a default Chroma client. The default client is ephemeral, meaning any data stored will not persist to disk after the program terminates, making it suitable for temporary demonstrations or in-memory operations.
SOURCE: https://github.com/chroma-core/chroma/blob/main/examples/basic_functionality/start_here.ipynb#_snippet_2

LANGUAGE: Python
CODE:
```
# Import Chroma and instantiate a client. The default Chroma client is ephemeral, meaning it will not save to disk.
import chromadb

client = chromadb.Client()
```

----------------------------------------

TITLE: Starting ChromaDB Server with AuthN/AuthZ (Bash)
DESCRIPTION: This Bash command starts the ChromaDB server with persistent storage, enabling token-based authentication and simple RBAC authorization. It specifies the providers and configuration files for both authentication and authorization, along with standard Uvicorn server parameters for host, port, and logging.
SOURCE: https://github.com/chroma-core/chroma/blob/main/examples/basic_functionality/authz/README.md#_snippet_3

LANGUAGE: bash
CODE:
```
IS_PERSISTENT=1 \
CHROMA_SERVER_AUTHN_PROVIDER="chromadb.auth.token_authn.TokenAuthenticationServerProvider" \
CHROMA_SERVER_AUTHN_CREDENTIALS_FILE=examples/basic_functionality/authz/authz.yaml \
CHROMA_SERVER_AUTHZ_PROVIDER="chromadb.auth.simple_rbac_authz.SimpleRBACAuthorizationProvider" \
CHROMA_SERVER_AUTHZ_CONFIG_FILE=examples/basic_functionality/authz/authz.yaml \
uvicorn chromadb.app:app --workers 1 --host 0.0.0.0 --port 8000 --proxy-headers --log-config chromadb/log_config.yml --reload --timeout-keep-alive 30
```

----------------------------------------

TITLE: Initializing ChromaDB Client (JavaScript)
DESCRIPTION: This JavaScript snippet illustrates how to import and instantiate the `ChromaClient` for both CommonJS (`require`) and ECMAScript Modules (`import`) environments. The initialized client object is used to communicate with a running ChromaDB server.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_14

LANGUAGE: Javascript
CODE:
```
// CJS
const { ChromaClient } = require("chromadb");

// ESM
import { ChromaClient } from "chromadb";

const client = new ChromaClient();
```

----------------------------------------

TITLE: Retrieving, Creating, and Deleting Chroma Collections (Python)
DESCRIPTION: This snippet demonstrates how to interact with existing Chroma collections in Python. It shows `get_collection` for retrieving by name (raising an exception if not found), `get_or_create_collection` to retrieve or create if non-existent, and `delete_collection` for permanent removal of a collection and its data.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_18

LANGUAGE: python
CODE:
```
collection = client.get_collection(name="test") # Get a collection object from an existing collection, by name. Will raise an exception if it's not found.
collection = client.get_or_create_collection(name="test") # Get a collection object from an existing collection, by name. If it doesn't exist, create it.
client.delete_collection(name="my_collection") # Delete a collection and all associated embeddings, documents, and metadata. ⚠️ This is destructive and not reversible
```

----------------------------------------

TITLE: Combining Multiple Filters with Logical OR - Python
DESCRIPTION: This snippet demonstrates how to combine multiple metadata filters using the `$or` logical operator. Results will be returned if any of the specified conditions within the list are met.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_42

LANGUAGE: python
CODE:
```
{
    "$or": [
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        },
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        }
    ]
}
```

----------------------------------------

TITLE: Specifying Returned Data with Include Parameter (Python)
DESCRIPTION: This snippet illustrates using the `include` parameter with both `.get` and `.query` methods to control which data fields are returned. By default, `documents`, `metadatas`, and `distances` (for query) are returned, while `embeddings` are excluded for performance. `ids` are always returned.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/querying-collections/query-and-get.md#_snippet_6

LANGUAGE: python
CODE:
```
# Only get documents and ids
collection.get(
    include=["documents"]
)

collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
    include=["documents"]
)
```

----------------------------------------

TITLE: Adding Documents with Embeddings to Chroma Collection (Javascript)
DESCRIPTION: This snippet demonstrates adding documents with pre-computed embeddings to a Chroma collection. Chroma stores the provided documents and embeddings directly. Unique IDs are required, and optional metadata can be supplied for filtering.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_27

LANGUAGE: javascript
CODE:
```
await collection.add({
    ids: ["id1", "id2", "id3", ...],
    embeddings: [[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas: [{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    documents: ["lorem ipsum...", "doc2", "doc3", ...],
})
```

----------------------------------------

TITLE: Adding Items to Collection (TypeScript)
DESCRIPTION: This snippet demonstrates how to add new items to a collection using the `add` method. It requires providing IDs, embeddings, optional metadatas, and documents for the items to be added.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/reference/js/collection.md#_snippet_0

LANGUAGE: typescript
CODE:
```
const response = await collection.add({
  ids: ["id1", "id2"],
  embeddings: [[1, 2, 3], [4, 5, 6]],
  metadatas: [{ "key": "value" }, { "key": "value" }],
  documents: ["document1", "document2"]
});
```

----------------------------------------

TITLE: Deleting Items from Collection (TypeScript)
DESCRIPTION: This snippet shows how to remove items from a collection using the `delete` method. Items can be deleted by specific IDs, by matching metadata conditions using `where`, or by document content using `whereDocument`.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/reference/js/collection.md#_snippet_2

LANGUAGE: typescript
CODE:
```
const results = await collection.delete({
  ids: "some_id",
  where: {"name": {"$eq": "John Doe"}},
  whereDocument: {"$contains":"search_string"}
});
```

----------------------------------------

TITLE: Installing ChromaDB JavaScript/TypeScript Client
DESCRIPTION: These commands demonstrate how to install the `chromadb` and `chromadb-default-embed` client libraries for JavaScript and TypeScript projects using popular package managers like Yarn, npm, and pnpm. These clients are essential for connecting to and interacting with a Chroma server from web or Node.js applications.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/overview/introduction.md#_snippet_1

LANGUAGE: Terminal
CODE:
```
yarn add chromadb chromadb-default-embed
```

LANGUAGE: Terminal
CODE:
```
npm install --save chromadb chromadb-default-embed
```

LANGUAGE: Terminal
CODE:
```
pnpm install chromadb chromadb-default-embed
```

----------------------------------------

TITLE: Installing ChromaDB JavaScript Client
DESCRIPTION: This snippet demonstrates how to install the ChromaDB JavaScript client using popular package managers like npm, pnpm, and yarn. It provides the necessary commands for each, ensuring a straightforward setup process for integrating ChromaDB into your project.
SOURCE: https://github.com/chroma-core/chroma/blob/main/clients/js/packages/chromadb/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
# npm
npm install chromadb

# pnpm
pnpm add chromadb

# yarn
yarn add chromadb
```

----------------------------------------

TITLE: Creating and Getting Chroma Collections with Embedding Function (JavaScript)
DESCRIPTION: This snippet illustrates how to create and retrieve a Chroma collection in JavaScript using `createCollection` and `getCollection`. It emphasizes that if an `embeddingFunction` is provided during creation, it must also be supplied when retrieving the collection later.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_17

LANGUAGE: js
CODE:
```
let collection = await client.createCollection({
  name: "my_collection",
  embeddingFunction: emb_fn,
});
let collection2 = await client.getCollection({
  name: "my_collection",
  embeddingFunction: emb_fn,
});
```

----------------------------------------

TITLE: Importing Chroma Client - Javascript
DESCRIPTION: Demonstrates how to import the `ChromaClient` class in JavaScript, providing examples for both CommonJS (CJS) and ECMAScript Modules (ESM) environments.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/guides/usage-guide.md#_snippet_2

LANGUAGE: js
CODE:
```
// CJS
const { ChromaClient } = require("chromadb");

// ESM
import { ChromaClient } from "chromadb";
```

----------------------------------------

TITLE: Connecting to ChromaDB, Creating Collection, Adding, and Querying Data - JavaScript
DESCRIPTION: This snippet illustrates the fundamental steps for interacting with ChromaDB using its JavaScript client. It covers initializing the client, connecting to a local Chroma instance, creating a new collection, programmatically adding multiple documents with unique IDs, embeddings, and text, and finally, querying the collection based on embeddings and text. This example demonstrates a complete flow for basic data management within ChromaDB.
SOURCE: https://github.com/chroma-core/chroma/blob/main/clients/js/README.md#_snippet_0

LANGUAGE: JavaScript
CODE:
```
import { ChromaClient } from "chromadb"; // or "chromadb-client"
const chroma = new ChromaClient({ path: "http://localhost:8000" });
const collection = await chroma.createCollection({ name: "test-from-js" });
for (let i = 0; i < 20; i++) {
  await collection.add({
    ids: ["test-id-" + i.toString()],
    embeddings: [1, 2, 3, 4, 5],
    documents: ["test"]
  });
}
const queryData = await collection.query({
  queryEmbeddings: [1, 2, 3, 4, 5],
  queryTexts: ["test"]
});
```

----------------------------------------

TITLE: Retrieving and Deleting Chroma Collections
DESCRIPTION: This snippet demonstrates methods for retrieving and deleting Chroma collections. `get_collection` fetches an existing collection by name, raising an exception if not found. `get_or_create_collection` retrieves a collection if it exists, or creates it otherwise. `delete_collection` permanently removes a collection and all its associated data.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/collections/create-get-delete.md#_snippet_2

LANGUAGE: python
CODE:
```
collection = client.get_collection(name="test") # Get a collection object from an existing collection, by name. Will raise an exception if it's not found.
collection = client.get_or_create_collection(name="test") # Get a collection object from an existing collection, by name. If it doesn't exist, create it.
client.delete_collection(name="my_collection") # Delete a collection and all associated embeddings, documents, and metadata. ⚠️ This is destructive and not reversible
```

LANGUAGE: typescript
CODE:
```
const collection = await client.getCollection({ name: "test" }); // Get a collection object from an existing collection, by name. Will raise an exception of it's not found.
collection = await client.getOrCreateCollection({ name: "test" }); // Get a collection object from an existing collection, by name. If it doesn't exist, create it.
await client.deleteCollection(collection); // Delete a collection and all associated embeddings, documents, and metadata. ⚠️ This is destructive and not reversible
```

----------------------------------------

TITLE: Deleting Data from Chroma Collection (Python)
DESCRIPTION: This Python snippet demonstrates how to delete items from a Chroma collection using the `.delete` method. It supports deleting specific items by their `ids` and/or filtering items based on a `where` clause. If `ids` are provided, only those specific items are targeted; otherwise, all items matching the `where` filter are deleted.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/collections/delete-data.md#_snippet_0

LANGUAGE: python
CODE:
```
collection.delete(
    ids=["id1", "id2", "id3",...],
	where={"chapter": "20"}
)
```

----------------------------------------

TITLE: Deleting Data from Chroma Collection (TypeScript)
DESCRIPTION: This TypeScript snippet shows how to asynchronously delete items from a Chroma collection using the `.delete` method. Similar to the Python version, it allows specifying `ids` for direct deletion and/or a `where` filter to target items based on metadata. The operation is destructive and cannot be undone.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/collections/delete-data.md#_snippet_1

LANGUAGE: typescript
CODE:
```
await collection.delete({
    ids: ["id1", "id2", "id3",...], //ids
    where: {"chapter": "20"} //where
})
```

----------------------------------------

TITLE: Querying Nearest Neighbors in Python
DESCRIPTION: This method performs a nearest neighbor search based on provided `query_embeddings` or `query_texts`, returning the `n_results` closest embeddings. It supports filtering by metadata (`where`) and document content (`where_document`), and allows specifying which data to include in the `QueryResult` such as embeddings, metadatas, documents, and distances.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/reference/python/collection.md#_snippet_5

LANGUAGE: python
CODE:
```
def query(
        query_embeddings: Optional[OneOrMany[Embedding]] = None,
        query_texts: Optional[OneOrMany[Document]] = None,
        n_results: int = 10,
        where: Optional[Where] = None,
        where_document: Optional[WhereDocument] = None,
        include: Include = ["metadatas", "documents",
                            "distances"]) -> QueryResult
```

----------------------------------------

TITLE: Querying Chroma Collections by Texts (TypeScript)
DESCRIPTION: This snippet shows how to query a Chroma collection using a list of `queryTexts`. Chroma will first embed each text using the collection's embedding function, then perform the query. Parameters include `nResults`, `where` for metadata filtering, `whereDocument` for content filtering, and `ids` for pre-filtering by ID.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/querying-collections/query-and-get.md#_snippet_3

LANGUAGE: typescript
CODE:
```
await collection.query({
    queryTexts: ["doc10", "thus spake zarathustra", ...],
    nResults: 10,
    where: {"metadata_field": "is_equal_to_this"},
    whereDocument: {"$contains": "search_string"},
    ids: ["id1", "id2", ...]
})
```

----------------------------------------

TITLE: Inspecting Query Results - TypeScript
DESCRIPTION: This snippet displays the typical structure of query results returned by ChromaDB in TypeScript. It shows the 'documents', 'ids', and 'distances' fields, illustrating how semantic similarity (e.g., 'hawaii' to 'pineapple') is reflected in the distance values.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/overview/getting-started.md#_snippet_16

LANGUAGE: typescript
CODE:
```
{
    documents: [
        [
            'This is a document about pineapple', 
            'This is a document about oranges'
        ]
    ], 
    ids: [
        ['id1', 'id2']
    ], 
    distances: [[1.0404009819030762, 1.243080496788025]],
    uris: null,
    data: null,
    metadatas: [[null, null]],
    embeddings: null
}
```

----------------------------------------

TITLE: Initializing Default Embedding Function (Python)
DESCRIPTION: This snippet initializes the default embedding function in Python using `chromadb.utils.embedding_functions.DefaultEmbeddingFunction`. This function utilizes the `all-MiniLM-L6-v2` Sentence Transformers model locally, automatically downloading model files if necessary. It serves as Chroma's out-of-the-box embedding solution.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/embeddings/embedding-functions.md#_snippet_0

LANGUAGE: python
CODE:
```
from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()
```

----------------------------------------

TITLE: Starting Chroma Server - Terminal
DESCRIPTION: This command initiates the Chroma server process, making it available for client connections. The `--path` argument is crucial for specifying the persistent storage location for the database, ensuring data is saved across sessions.
SOURCE: https://github.com/chroma-core/chroma/blob/main/docs/docs.trychroma.com/markdoc/content/docs/run-chroma/client-server.md#_snippet_0

LANGUAGE: terminal
CODE:
```
chroma run --path /db_path
```