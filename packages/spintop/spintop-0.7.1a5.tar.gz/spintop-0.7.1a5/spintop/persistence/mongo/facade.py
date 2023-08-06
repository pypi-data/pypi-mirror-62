import os

from spintop.persistence import PersistenceFacade
from spintop.models import (
    SpintopTestRecord, 
    SpintopSerializedFlatTestRecord, 
    SpintopSerializedTestRecordCollection, 
    TestRecordSummary,
    Query, 
    serialized_get_test_uuid
)

from .operations import db_from_mongo_uri
from .mappers import create_mappers, simple_mongo_mapper_factory, TestRecordSummary, FeatureRecord


class MongoPersistenceFacade(PersistenceFacade):
    def __init__(self, mongo_db, serializer=None):
        self.mongo_db = mongo_db
        self.serializer = serializer
        mappers = create_mappers(mongo_db, serializer=serializer)
        self.feature_mapper = mappers[FeatureRecord]
        self._init(mappers)
        self.dc_serializer = self.feature_mapper.dc_serializer
    
    def _init(self, mappers):
        for _, mapper in mappers.items():
            mapper.init()

    @classmethod
    def from_mongo_uri(cls, mongo_uri, database_name):
        return cls(db_from_mongo_uri(mongo_uri, database_name))
    
    @classmethod
    def from_env(cls, mongo_uri_env_name='SPINTOP_MONGO_URI', database_name_env_name='SPINTOP_DATABASE_NAME'):
        return cls.from_mongo_uri(
            mongo_uri=os.environ[mongo_uri_env_name],
            database_name=os.environ[database_name_env_name]
        )

    def serialize_barrier(self, records):
        records = list(records)
        if records and isinstance(records[0], SpintopTestRecord):
            records = self.dc_serializer.serialize_many(records)

        if records and isinstance(records[0], dict):
            return [SpintopSerializedFlatTestRecord(**record) for record in records]
        else:
            return records
        
    def create(self, records):
        self._iter_op('create', records)
        
    def _iter_op(self, op_name, records):
        records = self.serialize_barrier(records)

        all_features = []
        for record in records:
            all_features += record.all_features

        self.logger.info('Processing {} of {} features.'.format(
                op_name, len(all_features)
            )
        )
        getattr(self.feature_mapper, op_name)(all_features)
        
        
    def retrieve(self, query=None, deserialize=True):
        """ Retrieve is responsible with returning the test_record (top level phase) associated
        with the matched features.
        """
        query = self._include_top_level_in_query(query)
        all_features = self.feature_mapper.retrieve(query)

        serialized_collection = SpintopSerializedTestRecordCollection(all_features)
        if deserialize:
            yield from serialized_collection.deserialize(self.dc_serializer.serializer)
        else:
            yield from (record for record in serialized_collection.records)
        
    def _include_top_level_in_query(self, query):
        if query is None:
            query = Query()
        return [query.create_top_level_query(), query]

    def update(self, records):
        self._iter_op('update', records)
    
    def delete(self, match_query):
        match_query = self._include_top_level_in_query(match_query)
        self.logger.info('Deleting flat records based on query: %s.' % repr(match_query))
        self.feature_mapper.delete(match_query)

    def create_mapper(self, name, **kwargs):
        return simple_mongo_mapper_factory(self.mongo_db, name, serializer=self.serializer, **kwargs)