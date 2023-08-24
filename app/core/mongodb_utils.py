"""
MongoDB 관련 모듈
"""

import logging
from typing import Optional, Dict

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import pandas as pd

from app.settings.constants import MONGODB_URI, MONGODB_DB_NAME


def get_mongodb_client() -> Optional[MongoClient]:
    """
    MongoDB 데이터베이스와 연결할 수 있는 클라이언트를 반환한다.

    Returns:
        MongoClient 혹은 None: MongoDB 데이터베이스 연결이 성공적인 경우 MongoClient, 실패인 경우는 None
    """

    try:
        mongodb_client = MongoClient(MONGODB_URI)

        return mongodb_client
    except (ServerSelectionTimeoutError, ConnectionFailure) as exc:
        logging.error("Failed to connect to MongoDB")
        raise


def get_collection(
    client: MongoClient, collection_name: str, filters: Optional[Dict] = None
) -> Optional[pd.DataFrame]:
    """
    MongoDB 데이터베이스에서 데이터를 추출한다.

    Args:
        client (MongoClient): 데이터베이스와의 소통에 사용할 클라이언트
        collection_name (str): 데이터를 가져올 컬렉션 이름
        filters (dict, optional): 데이터 추출 시 적용할 필터, 기본값은 None

    Returns:
        pd.DataFrame 혹은 None: MongoDB 데이터베이스 연결이 성공적인 경우 MongoClient, 실패인 경우는 None
    """

    if not client:
        logging.warning("MongoDB client is None")
        return None

    try:
        db = client[MONGODB_DB_NAME]
        collection = db[collection_name]

        if filters:
            df = pd.DataFrame(list(collection.find(filters)))
        else:
            df = pd.DataFrame(list(collection.find()))

        return df
    except Exception:
        logging.error("An error occurred while fetching data from MongoDB")

        return None
