import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

WINDOW_SECONDS = 300

def process(events):
    totals, rejected, seen = defaultdict(Decimal), [], set()
    for event in events:
        try:
            event_id = str(event['event_id'])
            if not event_id or event_id in seen:
                raise ValueError('missing or duplicate event id')
            ts = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
            if ts.tzinfo is None:
                raise ValueError('timestamp must specify timezone')
            amount = Decimal(str(event['amount']))
            if not amount.is_finite() or amount < 0:
                raise ValueError('amount must be finite and nonnegative')
            if not event.get('category'):
                raise ValueError('category required')
            seen.add(event_id)
            window_start = int(ts.astimezone(timezone.utc).timestamp()) // WINDOW_SECONDS * WINDOW_SECONDS
            totals[(window_start, str(event['category']))] += amount
        except (ValueError, TypeError, KeyError, InvalidOperation) as exc:
            rejected.append({'event': event, 'error': str(exc)})
    aggregates = [{'window_start_utc':datetime.fromtimestamp(start,timezone.utc).isoformat(),
                   'category':category,'revenue':str(value)}
                  for (start,category),value in sorted(totals.items())]
    return aggregates, rejected

def run(input_file, output_dir):
    events = [json.loads(x) for x in Path(input_file).read_text().splitlines() if x.strip()]
    agg, dlq = process(events)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for name, records in [('windows',agg),('dead_letter_queue',dlq)]:
        (Path(output_dir)/f'{name}.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records))
    return {'windows':len(agg),'rejected':len(dlq)}

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--output',default='output')
    a=p.parse_args()
    print(json.dumps(run(a.input,a.output)))
