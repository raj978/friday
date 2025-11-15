import json
import logging
from typing import Optional
from fastapi import Request

from friday.utils.chat import generate_chat_completion
from friday.utils.task import get_task_model_id
from friday.models.memories import Memories
from friday.retrieval.vector.factory import VECTOR_DB_CLIENT

log = logging.getLogger(__name__)

# Memory extraction prompt template
MEMORY_EXTRACTION_PROMPT = """You are a memory extraction assistant. Analyze the conversation below and extract any important personal information, preferences, facts, or context about the user that should be remembered for future conversations.

Extract information such as:
- Personal facts (name, birthday, location, occupation, etc.)
- Preferences (likes, dislikes, favorites, etc.)
- Important dates or events
- Relationships and connections
- Goals and aspirations
- Any other relevant information the user shares about themselves

DO NOT extract:
- Greetings or pleasantries (hello, hi, how are you, etc.)
- Small talk or casual conversation
- Temporary or transient information
- Generic responses or acknowledgments
- Questions without answers
- Information that is not about the user specifically

Only extract meaningful, lasting information that would be valuable to remember in future conversations. Each memory should be self-contained and specific.

Return ONLY a JSON array of memory strings. If there is no new meaningful information to remember, return an empty array [].

Example output format:
["User's birthday is November 30, 2003 at 10:20am", "User prefers Python over JavaScript", "User is working on a chatbot project"]

Conversation:
{conversation}

Remember: Return ONLY the JSON array, nothing else."""


async def extract_memories_from_conversation(
    request: Request,
    messages: list[dict],
    user,
    model_id: str = None,
) -> list[str]:
    """
    Extract memories from a conversation using an LLM.

    Args:
        request: FastAPI request object
        messages: List of conversation messages
        user: User object
        model_id: Model ID to use for extraction (defaults to task model)

    Returns:
        List of extracted memory strings
    """
    try:
        # Get models
        if getattr(request.state, "direct", False) and hasattr(request.state, "model"):
            models = {
                request.state.model["id"]: request.state.model,
            }
        else:
            models = request.app.state.MODELS

        # Use provided model or get task model
        if not model_id:
            # Use the model from the last message or default task model
            conversation_model = messages[0].get("model") if messages else None
            if conversation_model and conversation_model in models:
                model_id = get_task_model_id(
                    conversation_model,
                    request.app.state.config.TASK_MODEL,
                    request.app.state.config.TASK_MODEL_EXTERNAL,
                    models,
                )
            else:
                # Fallback to any available model
                model_id = list(models.keys())[0] if models else None

        if not model_id or model_id not in models:
            log.warning("No valid model found for memory extraction")
            return []

        # Format conversation for the prompt
        conversation_text = ""
        for msg in messages[-10:]:  # Only use last 10 messages to keep context manageable
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, str):
                conversation_text += f"{role.capitalize()}: {content}\n\n"

        # Create the extraction prompt
        extraction_prompt = MEMORY_EXTRACTION_PROMPT.format(
            conversation=conversation_text.strip()
        )

        # Prepare payload for LLM
        max_tokens = (
            models[model_id].get("info", {}).get("params", {}).get("max_tokens", 1000)
        )

        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": extraction_prompt}],
            "stream": False,
            **(
                {"max_tokens": max_tokens}
                if models[model_id].get("owned_by") == "ollama"
                else {
                    "max_completion_tokens": max_tokens,
                }
            ),
            "metadata": {
                **(request.state.metadata if hasattr(request.state, "metadata") else {}),
                "task": "memory_extraction",
            },
        }

        # Call LLM to extract memories
        response = await generate_chat_completion(
            request, form_data=payload, user=user, bypass_filter=True
        )

        # Parse response
        if hasattr(response, "body_iterator"):
            # Streaming response (StreamingResponse)
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            response_text = body.decode("utf-8")

            # Try to parse as JSON response
            try:
                response_data = json.loads(response_text)
                if "choices" in response_data:
                    content = response_data["choices"][0]["message"]["content"]
                else:
                    content = response_text
            except json.JSONDecodeError:
                content = response_text
        elif hasattr(response, "body"):
            # JSONResponse - has body but not body_iterator
            response_body = response.body
            if isinstance(response_body, bytes):
                response_text = response_body.decode("utf-8")
            else:
                response_text = str(response_body)

            # Try to parse as JSON response
            try:
                response_data = json.loads(response_text)
                if "choices" in response_data:
                    content = response_data["choices"][0]["message"]["content"]
                else:
                    log.error(f"Unexpected JSONResponse format: {response_data}")
                    return []
            except json.JSONDecodeError as e:
                log.error(f"Failed to parse JSONResponse body as JSON: {e}, body: {response_text[:200]}")
                return []
        elif isinstance(response, dict):
            # Plain dict response
            if "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"]
            else:
                log.error(f"Unexpected dict response format: {response}")
                return []
        else:
            # Fallback to string conversion
            content = str(response)

        # Extract JSON array from the content
        # The LLM might wrap it in markdown or extra text
        try:
            # Ensure content is a string
            if not isinstance(content, str):
                log.error(f"Content is not a string, it's {type(content)}: {content}")
                return []

            # Find JSON array in the response
            start_idx = content.find("[")
            end_idx = content.rfind("]") + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                memories = json.loads(json_str)

                # Validate it's a list of strings
                if isinstance(memories, list):
                    memories = [str(m) for m in memories if m and str(m).strip()]
                    log.info(f"Extracted {len(memories)} memories from conversation")
                    return memories
                else:
                    log.warning(f"Extracted content is not a list: {type(memories)}")
                    return []
            else:
                log.warning("No JSON array found in response")
                return []

        except json.JSONDecodeError as e:
            log.error(f"Failed to parse extracted memories as JSON: {e}")
            return []
        except Exception as e:
            log.error(f"Error parsing memory extraction response: {e}")
            return []

    except Exception as e:
        log.error(f"Error extracting memories from conversation: {e}")
        return []


async def save_extracted_memories(
    request: Request,
    memories: list[str],
    user,
) -> int:
    """
    Save extracted memories to both SQL and vector DB.
    Checks for similar existing memories before saving to prevent duplicates.

    Args:
        request: FastAPI request object
        memories: List of memory strings to save
        user: User object

    Returns:
        Number of memories successfully saved
    """
    saved_count = 0
    SIMILARITY_THRESHOLD = 0.85  # Skip if 85% or more similar

    for memory_content in memories:
        if not memory_content or not memory_content.strip():
            continue

        try:
            collection_name = f"user-memory-{user.id}"
            memory_text = memory_content.strip()

            # Get embedding for new memory
            memory_embedding = request.app.state.EMBEDDING_FUNCTION(
                memory_text, user=user
            )

            # Check if similar memory already exists
            try:
                search_results = VECTOR_DB_CLIENT.search(
                    collection_name=collection_name,
                    vectors=[memory_embedding],
                    limit=1,  # Only need the most similar one
                )

                # Check if similar memory exists
                # SearchResult has nested lists: distances[0][i], documents[0][i]
                if (
                    search_results
                    and hasattr(search_results, "distances")
                    and search_results.distances
                    and len(search_results.distances[0]) > 0
                ):
                    # ChromaDB client already normalizes distances to 0-1 similarity scores
                    # 1.0 = perfect match, 0.0 = completely different
                    similarity = search_results.distances[0][0]
                    similar_text = search_results.documents[0][0]

                    if similarity >= SIMILARITY_THRESHOLD:
                        log.info(
                            f"Skipping duplicate memory (similarity: {similarity:.2f}): "
                            f"{memory_text[:50]}... "
                            f"(similar to: {similar_text[:50]}...)"
                        )
                        continue  # Skip this memory

            except Exception as e:
                # If search fails, log but continue with save (fail-safe)
                log.warning(f"Failed to check for similar memories: {e}. Proceeding with save.")

            # Save to SQL database
            memory = Memories.insert_new_memory(user.id, memory_text)

            # Save to vector database
            VECTOR_DB_CLIENT.upsert(
                collection_name=collection_name,
                items=[
                    {
                        "id": memory.id,
                        "text": memory.content,
                        "vector": memory_embedding,  # Reuse the embedding we already created
                        "metadata": {"created_at": memory.created_at},
                    }
                ],
            )

            saved_count += 1
            log.info(f"Saved memory for user {user.id}: {memory_text[:50]}...")

        except Exception as e:
            log.error(f"Failed to save memory '{memory_content[:50]}...': {e}")
            continue

    return saved_count


async def auto_extract_and_save_memories(
    request: Request,
    messages: list[dict],
    user,
    model_id: str = None,
) -> Optional[dict]:
    """
    Extract and save memories from conversation in one operation.

    Args:
        request: FastAPI request object
        messages: List of conversation messages
        user: User object
        model_id: Model ID to use for extraction

    Returns:
        Dict with extraction results: {"extracted": int, "saved": int, "memories": list}
    """
    try:
        # Extract memories
        memories = await extract_memories_from_conversation(
            request, messages, user, model_id
        )

        if not memories:
            return {"extracted": 0, "saved": 0, "memories": []}

        # Save memories
        saved_count = await save_extracted_memories(request, memories, user)

        return {
            "extracted": len(memories),
            "saved": saved_count,
            "memories": memories,
        }

    except Exception as e:
        log.error(f"Error in auto_extract_and_save_memories: {e}")
        return None
