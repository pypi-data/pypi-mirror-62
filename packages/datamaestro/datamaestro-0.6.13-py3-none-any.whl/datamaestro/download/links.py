import logging
import os
from datamaestro.download import Download
from datamaestro.utils import deprecated


class links(Download):
    def __init__(self, varname, **links):
        super().__init__(varname)
        self.links = links

    @property
    def path(self):
        return self.definition.datapath

    def prepare(self):
        return self.path

    def download(self, force=False):
        self.path.mkdir(exist_ok=True, parents=True)
        for key, value in self.links.items():
            value.download(force)

            path = value()
            dest = self.path / key

            if not dest.exists():
                if dest.is_symlink():
                    logging.info("Removing dandling symlink %s", dest)
                    dest.unlink()
                os.symlink(path, dest)


# Deprecated
Links = deprecated("Use @links instead of @Links", links)
