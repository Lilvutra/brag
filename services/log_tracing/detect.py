from collections import Counter
import time

def detect_abnormal_event_spikes(logs):
    topic_counts = Counter(log['topics'][0] for log in logs)
    for topic, count in topic_counts.items():
        if count > 1000:  # arbitrary threshold
            print(f"Unusual spike in event {topic}: {count} occurrences")

def detect_time_gaps(logs):
    timestamps = sorted(int(log['timeStamp'], 16) for log in logs)
    for i in range(1, len(timestamps)):
        if timestamps[i] - timestamps[i-1] > 3600:  # 1 hour gap
            print(f"Gap detected between blocks at {time.ctime(timestamps[i-1])}")
