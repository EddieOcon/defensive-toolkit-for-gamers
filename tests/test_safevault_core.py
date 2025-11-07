from safevault.core import SafeVault, VaultEntry, VaultAuthError
import os
import tempfile

def test_vault_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "vault.bin")
        v = SafeVault(path)
        master = "TestMaster!123"
        v.create_new(master)
        v.add_entry(VaultEntry(name="steam", username="gamer", password="P@ssw0rd!"))
        v.save(master)

        v2 = SafeVault(path)
        v2.load(master)
        e = v2.get_entry("steam")
        assert e is not None
        assert e.username == "gamer"
        assert e.password == "P@ssw0rd!"

def test_wrong_master_raises():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "vault.bin")
        v = SafeVault(path)
        v.create_new("CorrectMaster123")
        v.save("CorrectMaster123")

        v2 = SafeVault(path)
        try:
            v2.load("WrongMaster")
            assert False, "Expected VaultAuthError"
        except VaultAuthError:
            pass
