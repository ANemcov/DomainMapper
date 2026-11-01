import ipaddress
from pathlib import Path
import tempfile
import unittest

from merge_routes import merge_routes


class MergeRoutesTests(unittest.TestCase):
    def test_collapse_preserves_addresses_and_interfaces(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'routes.txt'
            source.write_text(
                'ip route 192.0.2.0/32 Wireguard1 auto !Openai\n'
                'ip route 192.0.2.1/32 Wireguard1 auto !Custom\n'
                'ip route 192.0.2.1/32 Wireguard1 auto !Duplicate\n'
                'ip route 192.0.2.4/32 Wireguard1 auto !Openai\n'
                'ip route 192.0.2.0/24 Wireguard2 auto !Other\n'
                'ip route 2001:db8::/128 Wireguard1 auto !IPv6\n'
                'ip route 2001:db8::1/128 Wireguard1 auto !IPv6\n',
                encoding='utf-8',
            )
            routes, counts = merge_routes([source])
            wireguard1 = [net for net, meta in routes if meta[0] == 'Wireguard1' and net.version == 4]
            self.assertEqual(wireguard1, [ipaddress.ip_network('192.0.2.0/31'),
                                          ipaddress.ip_network('192.0.2.4/32')])
            self.assertEqual({ip for net in wireguard1 for ip in net},
                             {ipaddress.ip_address(f'192.0.2.{i}') for i in (0, 1, 4)})
            self.assertIn((ipaddress.ip_network('192.0.2.0/24'),
                           ('Wireguard2', 'auto', '!Other')), routes)
            self.assertIn((ipaddress.ip_network('2001:db8::/127'),
                           ('Wireguard1', 'auto', '!IPv6')), routes)
            self.assertEqual(counts[0][1], 7)

    def test_missing_and_empty_inputs_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'routes.txt'
            with self.assertRaises(FileNotFoundError):
                merge_routes([source])
            source.write_text('invalid\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                merge_routes([source])


if __name__ == '__main__':
    unittest.main()
