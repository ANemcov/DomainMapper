import asyncio
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from main import DNSServerWorker


class DNSConcurrencyTests(unittest.IsolatedAsyncioTestCase):
    async def test_workers_share_query_limit(self):
        active = 0
        peak = 0

        async def resolve(*args, **kwargs):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.001)
            active -= 1
            return [SimpleNamespace(address='192.0.2.1')]

        semaphore = asyncio.Semaphore(3)
        stats = {'total_domains_processed': 0, 'domain_errors': 0}
        workers = [DNSServerWorker(str(i), ['1.1.1.1'], 1000,
                                   query_semaphore=semaphore) for i in range(2)]
        for worker in workers:
            for i in range(10):
                await worker.add_domain(f'host{i}.example')
        with patch('dns.asyncresolver.Resolver.resolve', side_effect=resolve):
            await asyncio.gather(*(w.process_queue(stats) for w in workers))
        self.assertEqual(peak, 3)
        self.assertEqual(stats['total_domains_processed'], 20)
        self.assertEqual(stats['domain_errors'], 0)


if __name__ == '__main__':
    unittest.main()
