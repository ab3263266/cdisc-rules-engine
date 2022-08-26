from typing import Type

from .cache_service_interface import CacheServiceInterface
from cdisc_rules_engine.services.cache.in_memory_cache_service import (
    InMemoryCacheService,
)
from cdisc_rules_engine.services.cache.redis_cache_service import RedisCacheService
from cdisc_rules_engine.services.factory_interface import FactoryInterface


class CacheServiceFactory(FactoryInterface):
    _service_map = {"redis": RedisCacheService, "in_memory": InMemoryCacheService}

    def __init__(self, config):
        self.config = config

    def get_cache_service(self):
        cache_service_type = self.config.getValue("CACHE_TYPE") or "in_memory"
        return self.get_service(cache_service_type, config=self.config)

    @classmethod
    def register_service(cls, name: str, service: Type[CacheServiceInterface]):
        if not name:
            raise ValueError("Service name must not be empty!")
        if not issubclass(service, CacheServiceInterface):
            raise TypeError("Implementation of CacheServiceInterface required!")
        cls._service_map[name] = service

    def get_service(self, name: str, **kwargs) -> CacheServiceInterface:
        if name in self._service_map:
            return self._service_map.get(name).get_instance(**kwargs)
        raise ValueError(f"Service name must be in  {list(self._service_map.keys())}")