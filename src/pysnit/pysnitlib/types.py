from typing import Dict, List, Union, Optional
from typing import NamedTuple
from typing_extensions import TypedDict


class SnippetType(NamedTuple):
    name: str
    prefix: str
    body: str
    description: Optional[str]


class ModuleSnippet(TypedDict):
    module: Dict[str, str]


InlineSnippet = Dict[str, Dict]


class SnippetData(NamedTuple):
    module: List[SnippetType]
    inline: InlineSnippet


class SnippetContent(TypedDict):
    prefix: str
    body: Union[str, List[str]]
    description: Optional[str]


SnippetDict = Dict[str, SnippetContent]
