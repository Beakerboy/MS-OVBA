from ms_ovba.Models.Entities.license_info import LicenseInfo
from ms_ovba.Models.Entities.module_base import ModuleBase
from ms_ovba.Models.Entities.reference import Reference
from ms_dtyp.filetime import Filetime
from typing import TypeVar


T = TypeVar('T', bound='VbaProject')


class VbaProject:

    def __init__(self: T) -> None:

        self.endien = 'little'

        # Protected Instance Attributes
        self._codepage_name = 'cp1252'
        self._project_id = '{}'
        # The first byte of the protection byte string
        self._protection_state = 0
        self._password = b'\x00'
        self._visibility_state = b'\xFF'
        self._performance_cache = b''
        self._performance_cache_version = 0xFFFF

        # Lists
        # self.directories: list[] = []
        self.references: list[Reference] = []
        self.modules: list[ModuleBase] = []
        self._license_records: list[LicenseInfo] = []

        # Attributes and values
        self.attributes: dict[str, str] = {}

        self._project_cookie = 0xFFFF

        self._project_wm = False
        self._compat = False
        self._use_pw_hash = False
        self._default_date = Filetime.from_msfiletime(0x0000000000000000)
    # Getters and Setters

    @property
    def default_date(self: T) -> Filetime:
        return self._default_date

    @default_date.setter
    def default_date(self: T, date: Filetime) -> None:
        self._default_date = date

    @property
    def project_id(self: T) -> str:
        return self._project_id

    @project_id.setter
    def project_id(self: T, id: str) -> None:
        self._project_id = id

    @property
    def protection_state(self: T) -> bytes:
        return bytes([self._protection_state]) + b'\x00' * 3

    @property
    def visibility_state(self: T) -> bytes:
        return self._visibility_state

    @property
    def password(self: T) -> bytes:
        return self._password

    @password.setter
    def password(self: T, value: bytes) -> None:
        self._password = value

    @property
    def performance_cache(self: T) -> bytes:
        return self._performance_cache

    @performance_cache.setter
    def performance_cache(self: T, cache: bytes) -> None:
        self._performance_cache = cache

    @property
    def performance_cache_version(self: T) -> int:
        return self._performance_cache_version

    @performance_cache_version.setter
    def performance_cache_version(self: T, version: int) -> None:
        self._performance_cache_version = version

    @property
    def codepage_name(self: T) -> str:
        return self._codepage_name

    @codepage_name.setter
    def codepage_name(self: T, name: str) -> None:
        self._codepage_name = name

    @property
    def project_cookie(self: T) -> int:
        return self._project_cookie

    @project_cookie.setter
    def project_cookie(self: T, value: int) -> None:
        self._project_cookie = value

    def get_modules(self: T) -> list:
        return self.modules

    @property
    def projectwm(self: T) -> bool:
        return self._project_wm

    def include_projectwm(self: T) -> None:
        self._project_wm = True

    def exclude_projectwm(self: T) -> None:
        self._project_wm = False

    @property
    def compat(self: T) -> bool:
        return self._compat

    def include_compat(self: T) -> None:
        self._compat = True

    def exclude_compat(self: T) -> None:
        self._compat = False

    # Appenders
    def add_module(self: T, mod: ModuleBase) -> None:
        self.modules.append(mod)

    def add_reference(self: T, ref: Reference) -> None:
        self.references.append(ref)

    def add_attribute(self: T, name: str, value: str) -> None:
        self.attributes[name] = value

    def make_visible(self: T) -> None:
        self._visibility_state = b'\xff'

    def make_invisible(self: T) -> None:
        self._visibility_state = b'\x00'

    def user_protect(self: T) -> None:
        self._protection_state = self._protection_state | 128

    def user_unprotect(self: T) -> None:
        self._protection_state = self._protection_state & 127

    def host_protect(self: T) -> None:
        self._protection_state = self._protection_state | 64

    def host_unprotect(self: T) -> None:
        self._protection_state = self._protection_state & 191
    
    def vbe_protect(self: T) -> None:
        self._protection_state = self._protection_state | 32

    def vbe_unprotect(self: T) -> None:
        self._protection_state = self._protection_state & 223

    def use_password_hash(self: T) -> None:
        """
        Use the password hash data structure
        """
        self.use_pw_hash = True

    def use_plain_password(self: T) -> None:
        """
        Encrypt the plaintext password
        """
        self.use_pw_hash = False
