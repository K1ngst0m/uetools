import pytest

from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_list(capsys):

    main(args("plugin", "list"))
    capture = capsys.readouterr().out.splitlines()
    assert capture[0].startswith("No Plugins found inside")
