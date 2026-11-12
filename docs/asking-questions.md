# Asking Questions

Once knowledge has been added to Second Brain, you can ask questions about the information stored in the local knowledge base.

## Ask a question

Type your question in the input field at the bottom of the main window and select **Send**.

Second Brain searches the knowledge base for relevant information and uses the selected local language model to generate an answer.

While the answer is being generated, the application displays a thinking indicator.

## How answers are generated

Second Brain uses retrieval-augmented generation, or RAG.

In simple terms, this means that the application:

1. searches the local knowledge base for information related to your question
2. selects the most relevant entries
3. provides that information to the local language model
4. asks the model to answer using the retrieved information

The language model is instructed to base its answer on the available knowledge rather than inventing missing information.

## Sources

When an answer is based on stored knowledge, Second Brain displays source information together with the response.

The source indicator shows how many sources and knowledge entries were used.

Select the source indicator to inspect the information behind the answer.

This makes it possible to check where an answer came from and compare it with the original stored knowledge.

## Additional relevant sources

Second Brain may also identify information that is related to the question but was not used directly in the generated answer.

These sources can be inspected separately when available.

This can be useful when you want to explore related information or understand why certain knowledge was not included in the answer.

## When there is not enough information

If the knowledge base does not contain enough relevant information to answer a question, Second Brain will tell you that there is not enough information available.

In that case, you can:

- add more knowledge
- import another document or email
- rephrase the question
- review the stored information

## RAG settings

The retrieval process can be adjusted in **Settings**.

The available RAG settings include:

- **Top-K** — controls how many potentially relevant knowledge entries are retrieved
- **Similarity threshold** — controls how closely an entry must match the question to be considered relevant

The default settings are intended to provide a useful balance for normal use.

For more information, see [Settings](settings.md).

## Next steps

Continue with [Managing Knowledge](managing-knowledge.md) to learn how to search, edit and remove stored information.