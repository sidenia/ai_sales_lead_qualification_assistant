from app.core.config import async_openai_client


class LLMService:

    async def generate_response(self, message: str, context: str) -> str:
        """Generate a response using the LLM with context."""
        if not context.strip():
            context = "No relevant information available. If unsure, respond with 'I don't know'."

        system_prompt = f"""
            You are a helpful sales assistant. Use the following context to answer the user's question.

            Context:
            {context}

            User Question: {message}

            Answer clearly and objectively:
            """

        response = await async_openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()


llm_service = LLMService() # global instance