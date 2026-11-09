# Streaming Events, Dead Letter Queue & Windowing

A streaming-friendly event processor that validates order events, rejects duplicates, routes bad records to a dead-letter queue, and computes revenue by five-minute event-time windows. Includes deterministic JSONL replay and unit tests. It demonstrates a core streaming transformation independently of a broker, ready for a Kafka consumer adapter.

## Quick start

```bash
python stream.py --input samples/events.jsonl --output output
python -m unittest discover -s tests -v
```

## Architecture and scope

Replay adapter accepts JSONL events, organizes into five-minute event-time buckets, and reports invalid events. Real Kafka ingestion, watermark state management and checkpointing are deliberately out of scope.

**Portfolio note:** Original educational starter code, not a production deployment. Use only synthetic/public datasets, document your own extensions, and test integrations before claiming production experience.
