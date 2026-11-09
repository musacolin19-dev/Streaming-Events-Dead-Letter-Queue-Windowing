import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from stream import process

class TestStream(unittest.TestCase):
    def test_aggregates_and_dlq(self):
        e={'event_id':'1','timestamp':'2026-01-01T12:01:00Z','category':'x','amount':'2.50'}
        rows, bad=process([e,e])
        self.assertEqual(rows[0]['revenue'],'2.50')
        self.assertEqual(len(bad),1)
