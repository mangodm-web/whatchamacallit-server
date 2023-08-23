"""
단어 추론 모델에 관한 모듈
"""

from typing import List, Dict, Union

import numpy as np
from sentence_transformers import util

from app.model_instance import model_instance, corpus_embeddings, corpus_df


def get_predictions(query: str, top_k: int = 3) -> List[Dict[str, Union[str, int]]]:
    """
    사용자가 설명한 내용에 가장 가까운 단어 목록을 반환해준다.

    Args:
        query (str): 사용자의 설명
        top_k (int): 목록에 넣을 단어의 수

    Returns:
        List[Dict[str, Union[str, int]]]: 설명에 가장 가까운 단어들이 담긴 목록
    """

    if not query or top_k <= 0:
        return []

    query_embedding = model_instance.encode(query)

    similarities = util.cos_sim(query_embedding, corpus_embeddings)[0]

    top_k_sentences = []
    seen_labels = set()

    for index in np.argsort(-similarities):
        item_index = index.item()
        label = corpus_df.iloc[item_index]["correct_word"]

        if label not in seen_labels:
            seen_labels.add(label)
            top_k_sentences.append(
                {
                    "text": label,
                    "rank": len(top_k_sentences) + 1,
                }
            )

        if len(top_k_sentences) >= top_k:
            break

    return top_k_sentences
