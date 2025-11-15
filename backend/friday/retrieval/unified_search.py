"""
Unified Search Module for Friday

This module provides unified search across all knowledge bases,
implementing the priority-based search strategy:
1. Search ALL knowledge bases by default (when no files selected)
2. Search only selected files when explicitly chosen
3. Fallback to web search if no relevant results found

Author: Friday AI
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from loguru import logger

from friday.models.knowledge import Knowledges
from friday.models.memories import Memories
from friday.models.notes import Notes
from friday.models.prompts import Prompts
from friday.models.groups import Groups
from friday.utils.access_control import has_access
from friday.retrieval.utils import query_collection, query_collection_with_hybrid_search
from friday.retrieval.vector.factory import VECTOR_DB_CLIENT


@dataclass
class SearchResult:
    """Individual search result from a knowledge base"""

    content: str
    metadata: Dict[str, Any]
    score: float
    source: str  # knowledge base ID or collection name
    source_name: str  # human-readable name

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "content": self.content,
            "metadata": self.metadata,
            "score": self.score,
            "source": self.source,
            "source_name": self.source_name,
        }


@dataclass
class UnifiedSearchResult:
    """Aggregated search results from unified search"""

    results: List[SearchResult] = field(default_factory=list)
    total_count: int = 0
    max_score: float = 0.0
    sources: List[str] = field(default_factory=list)
    query: str = ""

    def __post_init__(self):
        """Calculate derived fields"""
        self.total_count = len(self.results)
        if self.results:
            self.max_score = max(r.score for r in self.results)
            self.sources = list(set(r.source for r in self.results))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "results": [r.to_dict() for r in self.results],
            "total_count": self.total_count,
            "max_score": self.max_score,
            "sources": self.sources,
            "query": self.query,
        }

    def is_relevant(self, threshold: float) -> bool:
        """Check if results meet relevance threshold"""
        return self.max_score >= threshold if self.results else False


async def get_all_user_collections(user_id: str, permission: str = "read") -> List[tuple]:
    """
    Get all collection IDs and names for a user's knowledge bases

    Args:
        user_id: User ID to get collections for
        permission: Permission level required (default: "read")

    Returns:
        List of tuples: [(collection_id, knowledge_base_name), ...]
    """
    try:
        logger.debug(f"Getting all knowledge bases for user {user_id}")

        # Get all knowledge bases the user has access to
        knowledge_bases = Knowledges.get_knowledge_bases_by_user_id(
            user_id=user_id,
            permission=permission
        )

        if not knowledge_bases:
            logger.info(f"No knowledge bases found for user {user_id}")
            return []

        # Each knowledge base ID IS the collection name
        collections = [
            (kb.id, kb.name)
            for kb in knowledge_bases
        ]

        logger.info(f"Found {len(collections)} collections for user {user_id}")
        return collections

    except Exception as e:
        logger.error(f"Error getting user collections: {e}")
        return []


async def get_collections_for_files(file_ids: List[str]) -> List[tuple]:
    """
    Get collection IDs for specific file IDs

    Args:
        file_ids: List of file IDs to get collections for

    Returns:
        List of tuples: [(collection_id, file_name), ...]
    """
    try:
        logger.debug(f"Getting collections for {len(file_ids)} files")

        collections = []

        # For individual files, the collection name is f"file-{file_id}"
        for file_id in file_ids:
            # Try modern format first
            collection_name = f"file-{file_id}"
            collections.append((collection_name, file_id))

        logger.info(f"Mapped {len(collections)} files to collections")
        return collections

    except Exception as e:
        logger.error(f"Error getting file collections: {e}")
        return []


async def search_collections(
    collection_names: List[str],
    query: str,
    embedding_function,
    k: int = 5,
    r: float = 0.0,
) -> List[Dict[str, Any]]:
    """
    Search across multiple collections using vector search

    Args:
        collection_names: List of collection IDs to search
        query: Search query text
        embedding_function: Function to generate embeddings
        k: Number of results per collection
        r: Relevance threshold

    Returns:
        List of search results with scores
    """
    try:
        if not collection_names:
            logger.warning("No collections provided for search")
            return []

        logger.debug(f"Searching {len(collection_names)} collections for: {query}")

        # Use existing query_collection function from retrieval/utils.py
        results = query_collection(
            collection_names=collection_names,
            queries=[query],
            embedding_function=embedding_function,
            k=k,
            r=r,
        )

        logger.info(f"Found {len(results)} raw results from collections")
        return results

    except Exception as e:
        logger.error(f"Error searching collections: {e}")
        return []


async def search_collections_hybrid(
    collection_names: List[str],
    query: str,
    embedding_function,
    k: int = 5,
    r: float = 0.0,
    bm25_weight: float = 0.5,
) -> List[Dict[str, Any]]:
    """
    Search across multiple collections using hybrid search (BM25 + vector)

    Args:
        collection_names: List of collection IDs to search
        query: Search query text
        embedding_function: Function to generate embeddings
        k: Number of results per collection
        r: Relevance threshold
        bm25_weight: Weight for BM25 scoring (0.0 = pure vector, 1.0 = pure BM25)

    Returns:
        List of search results with hybrid scores
    """
    try:
        if not collection_names:
            logger.warning("No collections provided for hybrid search")
            return []

        logger.debug(f"Hybrid searching {len(collection_names)} collections for: {query}")

        # Use existing hybrid search function
        results = query_collection_with_hybrid_search(
            collection_names=collection_names,
            queries=[query],
            embedding_function=embedding_function,
            k=k,
            r=r,
            hybrid_weight=bm25_weight,
        )

        logger.info(f"Found {len(results)} hybrid search results")
        return results

    except Exception as e:
        logger.error(f"Error in hybrid search: {e}")
        return []


async def search_memories(
    user_id: str,
    query: str,
    embedding_function,
    k: int = 3,
) -> List[SearchResult]:
    """
    Search user's memories using vector similarity

    Args:
        user_id: User ID to search memories for
        query: Search query text
        embedding_function: Function to generate embeddings
        k: Number of results to retrieve

    Returns:
        List of SearchResult objects from memories
    """
    try:
        collection_name = f"user-memory-{user_id}"

        # Check if user has any memories first
        memories = Memories.get_memories_by_user_id(user_id)
        if not memories:
            logger.debug(f"No memories found for user {user_id}")
            return []

        logger.debug(f"Searching memories for user {user_id}: {query}")

        # Perform vector search on memory collection
        query_embedding = embedding_function(query)

        results = VECTOR_DB_CLIENT.search(
            collection_name=collection_name,
            vectors=[query_embedding],
            limit=k,
        )

        search_results = []

        if results and hasattr(results, 'ids') and results.ids and len(results.ids) > 0:
            ids = results.ids[0]
            documents = results.documents[0]
            metadatas = results.metadatas[0]
            distances = results.distances[0]

            for i in range(len(ids)):
                # Vector DB returns distance, convert to similarity score
                # ChromaDB with cosine similarity: distance = 1 - cosine_similarity
                # So: similarity = 1 - distance
                # Clamp to [0, 1] range
                distance = distances[i]
                score = max(0.0, min(1.0, 1.0 - distance))

                search_results.append(SearchResult(
                    content=documents[i],
                    metadata=metadatas[i],
                    score=score,
                    source=collection_name,
                    source_name="Memories",
                ))

        if search_results:
            max_score = max(r.score for r in search_results)
            logger.info(f"Found {len(search_results)} memory results (max_score={max_score:.3f})")
        else:
            logger.info("Found 0 memory results")
        return search_results

    except Exception as e:
        logger.error(f"Error searching memories: {e}")
        return []


async def search_notes(
    user_id: str,
    query: str,
    k: int = 3,
) -> List[SearchResult]:
    """
    Search user's notes using text matching

    Args:
        user_id: User ID to search notes for
        query: Search query text
        k: Number of results to retrieve

    Returns:
        List of SearchResult objects from notes
    """
    try:
        logger.debug(f"Searching notes for user {user_id}: {query}")

        # Get notes the user has access to
        user_groups = Groups.get_groups_by_member_id(user_id)
        user_group_ids = {group.id for group in user_groups}
        notes = Notes.get_notes_by_permission(user_id, permission="read")

        if not notes:
            logger.debug(f"No notes found for user {user_id}")
            return []

        # Simple text matching on title and content
        query_lower = query.lower()
        scored_notes = []

        for note in notes:
            score = 0.0
            title = note.title.lower() if note.title else ""

            # Get content from note data
            content = ""
            if note.data and isinstance(note.data, dict):
                content_data = note.data.get("content", {})
                if isinstance(content_data, dict):
                    content = content_data.get("md", "") or content_data.get("text", "")
                elif isinstance(content_data, str):
                    content = content_data
            content_lower = content.lower()

            # Score based on exact match, word match, and contains
            if query_lower in title:
                score += 1.0
            elif any(word in title for word in query_lower.split()):
                score += 0.5

            if query_lower in content_lower:
                score += 0.7
            elif any(word in content_lower for word in query_lower.split()):
                score += 0.3

            if score > 0:
                # Include both title and snippet of content
                content_snippet = content[:500] if content else title
                full_text = f"{title}\n\n{content_snippet}" if content else title

                scored_notes.append((note, score, full_text))

        # Sort by score and take top k
        scored_notes.sort(key=lambda x: x[1], reverse=True)
        top_notes = scored_notes[:k]

        search_results = []
        for note, score, content_text in top_notes:
            search_results.append(SearchResult(
                content=content_text,
                metadata={
                    "note_id": note.id,
                    "title": note.title,
                    "created_at": note.created_at,
                },
                score=score,
                source=note.id,
                source_name=f"Note: {note.title}",
            ))

        logger.info(f"Found {len(search_results)} note results")
        return search_results

    except Exception as e:
        logger.error(f"Error searching notes: {e}")
        return []


async def search_prompts(
    user_id: str,
    query: str,
    k: int = 3,
) -> List[SearchResult]:
    """
    Search user's prompts using text matching

    Args:
        user_id: User ID to search prompts for
        query: Search query text
        k: Number of results to retrieve

    Returns:
        List of SearchResult objects from prompts
    """
    try:
        logger.debug(f"Searching prompts for user {user_id}: {query}")

        # Get prompts the user has access to
        prompts = Prompts.get_prompts_by_user_id(user_id, permission="read")

        if not prompts:
            logger.debug(f"No prompts found for user {user_id}")
            return []

        # Simple text matching on command, title, and content
        query_lower = query.lower()
        scored_prompts = []

        for prompt in prompts:
            score = 0.0
            command = prompt.command.lower() if prompt.command else ""
            title = prompt.title.lower() if prompt.title else ""
            content = prompt.content.lower() if prompt.content else ""

            # Score based on matches
            if query_lower in command:
                score += 1.0
            elif any(word in command for word in query_lower.split()):
                score += 0.6

            if query_lower in title:
                score += 0.8
            elif any(word in title for word in query_lower.split()):
                score += 0.4

            if query_lower in content:
                score += 0.6
            elif any(word in content for word in query_lower.split()):
                score += 0.2

            if score > 0:
                # Include command, title, and snippet of content
                content_snippet = prompt.content[:500] if prompt.content else ""
                full_text = f"/{prompt.command}: {prompt.title}\n\n{content_snippet}"

                scored_prompts.append((prompt, score, full_text))

        # Sort by score and take top k
        scored_prompts.sort(key=lambda x: x[1], reverse=True)
        top_prompts = scored_prompts[:k]

        search_results = []
        for prompt, score, content_text in top_prompts:
            search_results.append(SearchResult(
                content=content_text,
                metadata={
                    "command": prompt.command,
                    "title": prompt.title,
                    "created_at": prompt.timestamp,
                },
                score=score,
                source=prompt.command,
                source_name=f"Prompt: {prompt.title}",
            ))

        logger.info(f"Found {len(search_results)} prompt results")
        return search_results

    except Exception as e:
        logger.error(f"Error searching prompts: {e}")
        return []


async def unified_search(
    user_id: str,
    query: str,
    embedding_function,
    k: int = 5,
    threshold: float = 0.5,
    hybrid_search: bool = False,
    reranking_function = None,
    k_reranker: int = 3,
    r: float = 0.0,
    hybrid_bm25_weight: float = 0.5,
) -> UnifiedSearchResult:
    """
    Perform unified search across all user's knowledge sources

    This is the main function that implements the unified search strategy:
    - Retrieves all knowledge bases for the user
    - Performs vector/hybrid search across all collections
    - Searches user's memories using vector similarity
    - Searches user's notes using text matching
    - Searches user's prompts using text matching
    - Filters by relevance threshold
    - Optionally applies reranking

    Args:
        user_id: User ID to search knowledge bases for
        query: Search query text
        embedding_function: Function to generate embeddings
        k: Number of results to retrieve
        threshold: Minimum similarity score (0.0-1.0)
        hybrid_search: Use hybrid search (BM25 + vector)
        reranking_function: Optional reranking function
        k_reranker: Number of results for reranking
        r: Relevance threshold for initial filtering
        hybrid_bm25_weight: Weight for BM25 in hybrid search

    Returns:
        UnifiedSearchResult containing all results and metadata
    """
    try:
        logger.info(f"Starting unified search for user {user_id}: {query}")

        # Initialize search results list
        search_results = []

        # Get all user collections for knowledge base search
        collections_with_names = await get_all_user_collections(user_id)

        # Search knowledge bases if available
        if collections_with_names:
            collection_ids = [cid for cid, _ in collections_with_names]
            collection_names_map = {cid: name for cid, name in collections_with_names}

            # Perform search (vector or hybrid)
            if hybrid_search:
                raw_results = await search_collections_hybrid(
                    collection_names=collection_ids,
                    query=query,
                    embedding_function=embedding_function,
                    k=k,
                    r=r,
                    bm25_weight=hybrid_bm25_weight,
                )
            else:
                raw_results = await search_collections(
                    collection_names=collection_ids,
                    query=query,
                    embedding_function=embedding_function,
                    k=k,
                    r=r,
                )

            # Convert raw results to SearchResult objects
            if raw_results:
                for item in raw_results:
                    # Extract data from result format
                    # Results are tuples: (source_id, distance/score, document_dict)
                    if isinstance(item, tuple) and len(item) >= 3:
                        source_id = item[0]
                        score = float(item[1]) if isinstance(item[1], (int, float)) else 0.0
                        document = item[2] if len(item) > 2 else {}

                        # Get content and metadata
                        content = document.get("text", "") or document.get("content", "")
                        metadata = document.get("metadata", {})

                        # Get collection name
                        collection_id = metadata.get("collection_name", source_id)
                        collection_name = collection_names_map.get(collection_id, "Unknown")

                        search_results.append(SearchResult(
                            content=content,
                            metadata=metadata,
                            score=score,
                            source=collection_id,
                            source_name=collection_name,
                        ))
                    elif isinstance(item, dict):
                        # Alternative format: dict with score and document
                        score = float(item.get("score", 0.0))
                        content = item.get("content", "") or item.get("text", "")
                        metadata = item.get("metadata", {})
                        source_id = item.get("source", "")

                        collection_id = metadata.get("collection_name", source_id)
                        collection_name = collection_names_map.get(collection_id, "Unknown")

                        search_results.append(SearchResult(
                            content=content,
                            metadata=metadata,
                            score=score,
                            source=collection_id,
                            source_name=collection_name,
                        ))

        # Search memories
        try:
            memory_results = await search_memories(
                user_id=user_id,
                query=query,
                embedding_function=embedding_function,
                k=k,
            )
            search_results.extend(memory_results)
            logger.debug(f"Added {len(memory_results)} memory results")
        except Exception as e:
            logger.error(f"Error searching memories: {e}")

        # Search notes
        try:
            note_results = await search_notes(
                user_id=user_id,
                query=query,
                k=k,
            )
            search_results.extend(note_results)
            logger.debug(f"Added {len(note_results)} note results")
        except Exception as e:
            logger.error(f"Error searching notes: {e}")

        # Search prompts
        try:
            prompt_results = await search_prompts(
                user_id=user_id,
                query=query,
                k=k,
            )
            search_results.extend(prompt_results)
            logger.debug(f"Added {len(prompt_results)} prompt results")
        except Exception as e:
            logger.error(f"Error searching prompts: {e}")

        # If no results from any source, return empty result
        if not search_results:
            logger.info("No results found from any source")
            return UnifiedSearchResult(query=query)

        # Sort by score (descending)
        search_results.sort(key=lambda x: x.score, reverse=True)

        # Limit to k results (no threshold filtering - let middleware decide)
        final_results = search_results[:k]

        # Log result details
        max_score = max(r.score for r in final_results) if final_results else 0.0
        logger.info(
            f"Unified search complete: {len(final_results)} results "
            f"(max_score={max_score:.3f}, threshold={threshold})"
        )

        result = UnifiedSearchResult(
            results=final_results,
            query=query,
        )

        return result

    except Exception as e:
        logger.error(f"Error in unified search: {e}", exc_info=True)
        return UnifiedSearchResult(query=query)


async def get_search_context(
    unified_result: UnifiedSearchResult,
    max_context_length: int = 4000,
) -> str:
    """
    Convert unified search results into context string for LLM

    Args:
        unified_result: Unified search results
        max_context_length: Maximum length of context string

    Returns:
        Formatted context string with sources
    """
    if not unified_result.results:
        return ""

    context_parts = []
    current_length = 0

    for i, result in enumerate(unified_result.results, 1):
        # Format: [Source: Name] Content
        source_prefix = f"[Source: {result.source_name}] "
        result_text = f"{source_prefix}{result.content}\n\n"

        # Check if adding this would exceed limit
        if current_length + len(result_text) > max_context_length:
            break

        context_parts.append(result_text)
        current_length += len(result_text)

    context = "".join(context_parts).strip()

    logger.debug(f"Generated context of {len(context)} characters from {len(context_parts)} results")

    return context
