# Streaming-Events-Dead-Letter-Queue-Windowing
A streaming-style event processing project that replays JSONL event logs, validates incoming orders, removes duplicates, and routes invalid records to a dead-letter output. It groups valid transactions into five-minute event-time revenue windows with deterministic results. Includes tests and sample events; Kafka integration can be added separately.
