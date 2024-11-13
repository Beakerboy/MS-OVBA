from vbaproject_compiler.Models.Entities.module_base import ModuleBase
from vbaproject_compiler.Models.Entities.reference_record import (
    ReferenceRecord
)
from ms_dtyp.filetime import Filetime
from typing import TypeVar


T = TypeVar('T', bound='VbaProject')


class VbaProject:

    def __init__(self: T) -> None:

        self.endien = 'little'

        # Protected Instance Attributes
        self._codepage_name = 'cp1252'
        self._project_id = '{}'
        self._protection_state = b'\x00\x00\x00\x00'
        self._password = b'\x00'
        self._visibility_state = b'\xFF'
        self._performance_cache = b''
        self._performance_cache_version = 0xFFFF

        # A list of directories
        self.directories = []
        self.references = []
        self.modules = []

        self._project_cookie = 0xFFFF

        self._project_wm = False

    # Getters and Setters

    @property
    def default_date(self: T) -> Filetime:
        return self._default_date

    @default_date.setter
    def default_date(self: T, date: Filetime) -> None:
        self._default_date = date
        
    def set_project_id(self: T, id: str) -> None:
        self._project_id = id

    def get_project_id(self: T) -> str:
        return self._project_id

    def set_protection_state(self: T, state: int) -> None:
        self._protection_state = state

    def get_protection_state(self: T) -> int:
        return self._protection_state

    def set_visibility_state(self: T, state: int) -> None:
        """
        0   = not visible
        255 = visible
        """
        if state != 0 and state != 255:
            raise Exception("Bad visibility value.")
        self._visibility_state = state

    def get_visibility_state(self: T) -> bytes:
        return self._visibility_state

    def set_password(self: T, value: bytes) -> None:
        self._password = value

    def get_password(self: T) -> bytes:
        return self._password

    def set_performance_cache(self: T, cache: bytes) -> None:
        self._performance_cache = cache

    def get_performance_cache(self: T) -> None:
        return self._performance_cache

    def set_performance_cache_version(self: T, version: int) -> None:
        self._performance_cache_version = version

    def get_performance_cache_version(self: T) -> int:
        return self._performance_cache_version

    def get_codepage_name(self: T) -> str:
        return self._codepage_name

    def set_project_cookie(self: T, value: int) -> None:
        self._project_cookie = value

    def get_project_cookie(self: T) -> int:
        return self._project_cookie

    def get_modules(self: T) -> list:
        return self.modules

    def set_include_projectwm(self: T, value: bool) -> None:
        self._project_wm = value

    def get_include_projectwm(self: T) -> bool:
        return self._project_wm

    # Appenders
    def add_module(self: T, mod: ModuleBase) -> None:
        self.modules.append(mod)

    def add_reference(self: T, ref: ReferenceRecord) -> None:
        self.references.append(ref)
