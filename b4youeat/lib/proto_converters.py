

import datetime
from typing import Final

from google.protobuf import timestamp_pb2
_SECONDS_PER_DAY: Final = 24 * 60 * 60
_NANOS_PER_MICROSECOND: Final = 1000

_EPOCH_NAIVE: Final = datetime.datetime(1970, 1, 1)
_EPOCH_AWARE: Final = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def datetime_to_timestamp(dt: datetime.datetime) -> timestamp_pb2.Timestamp:
    if dt.tzinfo is not None:
        td = dt - _EPOCH_AWARE
    else:
        td = dt - _EPOCH_NAIVE

    proto_ts = timestamp_pb2.Timestamp()
    proto_ts.seconds = _SECONDS_PER_DAY * td.days + td.seconds
    proto_ts.nanos = dt.microsecond * _NANOS_PER_MICROSECOND
    return proto_ts

def timestamp_to_datetime(ts: timestamp_pb2.Timestamp) -> datetime.datetime:
    return _EPOCH_NAIVE + datetime.timedelta(
        seconds=ts.seconds, microseconds= ts.nanos // _NANOS_PER_MICROSECOND
    )