"""Decrypt secrets using Hiera's EYAML."""

import os
import re
import subprocess

from ansible.errors import AnsibleFilterError


def eyaml(encrypted, keys):
    os.environ['KEYBASE_PRIVKEY'] = slurp(keys['priv'])
    os.environ['KEYBASE_PUBKEY'] = slurp(keys['pub'])
    encrypted = re.sub(r'\s', '', encrypted, re.MULTILINE)
    cmd = ["eyaml", "decrypt",
           "--pkcs7-private-key-env-var=KEYBASE_PRIVKEY",
           "--pkcs7-public-key-env-var=KEYBASE_PUBKEY"]

    proc = subprocess.run(
        cmd + ["-s", encrypted],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=False)

    if proc.returncode != 0:
        raise AnsibleFilterError("Error (code %d) running %s: %s" %
                                 (proc.returncode,
                                  " ".join(cmd + ["-s", "..."]),
                                  proc.stderr))

    # What a nice surprise: eyaml doesn't manage its exit code correctly.
    output = proc.stdout

    if (not output) and " @ " in proc.stderr:
        raise AnsibleFilterError("Error running %s: %s" %
                                 (" ".join(cmd + ["-s", "..."]),
                                  proc.stderr))

    if "\n" not in output.rstrip():
        output = output.rstrip()

    return output


def slurp(path):
    if path.startswith('/keybase/'):
        # Thank you, https://github.com/keybase/client/issues/24636 ...
        kbfs_out = subprocess.check_output(['keybase', 'fs', 'read', path])
        if isinstance(kbfs_out, bytes):
            # (and additional thanks to Python for changing your mind about the return
            # type of a core API in between versions 2 and 3)
            return kbfs_out.decode("ascii")
        else:
            return kbfs_out
    else:
        return open(path).read()

class FilterModule(object):
    def filters(self):
        return {'eyaml': eyaml}
