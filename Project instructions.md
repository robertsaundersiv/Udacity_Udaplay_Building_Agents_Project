# Project Instructions

## Part 1 - RAG Pipeline

* Set up a ChromaDB vector database
* Process and embed game data from JSON files
* Implement semantic search functionality
* Create a reusable vector store manager

## Part 2 - Agent Implementation

* Build an agent with three core tools:
  * retrieve_game: Search the vector database
  * evaluate_retrieval: Assess answer quality
  * game_web_search: Fall back to web search
* Implement a state machine for agent workflow
* Create a reporting system for clear output

## Connecting Part 1 and Part 2

Part 2 reuses the database you build in Part 1, so the two notebooks must agree:

* Run both notebooks from the `project/starter` folder.
* In Part 1, create the database with `chromadb.PersistentClient(path="chromadb")`
and a collection named `udaplay`. Part 2 loads exactly that path and that name.
* Use the embedding function from **Environment Setup** when you create the collection.
Don't delete the `chromadb/` folder that Part 1 creates. If you do, re-run Part
1 before Part 2.

If Part 2 finds no results, or says the collection udaplay does not exist, one
of these doesn't match.

## Submission Instructions

You will be presented with the opportunity to submit your workspace solution
during the final Submit Project step.

## How your project is evaluated

* **Submit both notebooks with their outputs.** Run every cell and save before
you submit. The reviewer reads the outputs, and a notebook without them can't
be assessed.
* **Run at least three example queries**, including at least one the local
dataset can answer and at least one it can't, so the web fallback runs. The
three queries already listed in the Part 2 notebook do this: two are in the
dataset, and *Mortal Kombat X* is not.
* **Make the process visible**. For each query, the output should show the steps
your agent took: retrieve from the vector database → evaluate the results →
search the web only when they aren't good enough → final answer.
* **Cite the source**. When an answer comes from the web, include the source URL.
* **Answers can vary between runs**. LLM output and web results change from run
to run. You won't fail because an answer is worded differently, or because one
query isn't answered perfectly, as long as the retrieve → evaluate → fall back
process is shown.
