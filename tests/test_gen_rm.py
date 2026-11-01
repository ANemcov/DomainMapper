import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'gen_rm.sh'


class RemovalCommandsTests(unittest.TestCase):
    def run_script(self, *arguments, ssh_status='0'):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            table = root / 'routes'
            table.write_text(
                'Destination Gateway Interface F Metric\n'
                '0.0.0.0/0 0.0.0.0 Wireguard1 U 0\n'
                '1.1.1.1/32 0.0.0.0 Wireguard1 U 0\n'
                '8.8.8.8/32 0.0.0.0 Wireguard1 U 0\n'
                '10.40.0.0/24 0.0.0.0 Wireguard1 U 0\n'
                '8.47.69.0/32 0.0.0.0 Wireguard1 U 0\n'
                '8.47.69.0/32 0.0.0.0 Wireguard1 U 0\n'
                '81.1.1.10/32 0.0.0.0 Wireguard1 U 0\n'
                '192.168.33.0/24 0.0.0.0 Home U 0\n'
                '192.0.2.1/32 0.0.0.0 Wireguard10 U 0\n'
                '192.0.2.2/32 192.0.2.254 Wireguard1 U 0\n'
                '198.51.100.1/32 0.0.0.0 IKE0 U 0\n',
                encoding='utf-8',
            )
            ssh = root / 'ssh'
            ssh.write_text('#!/bin/sh\ncat "$MOCK_ROUTES"\nexit "$MOCK_SSH_STATUS"\n')
            ssh.chmod(0o755)
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ['PATH'],
                       MOCK_ROUTES=str(table), MOCK_SSH_STATUS=ssh_status)
            return subprocess.run(['bash', str(SCRIPT), *arguments], env=env,
                                  capture_output=True, text=True, check=False)

    def test_exact_interface_and_protected_routes(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.splitlines(), [
            'no ip route 8.47.69.0/32 Wireguard1',
            'no ip route 81.1.1.10/32 Wireguard1',
        ])

    def test_explicit_interface(self):
        result = self.run_script('IKE0')
        self.assertEqual(result.stdout, 'no ip route 198.51.100.1/32 IKE0\n')

    def test_ssh_failure_produces_no_commands(self):
        result = self.run_script(ssh_status='255')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
