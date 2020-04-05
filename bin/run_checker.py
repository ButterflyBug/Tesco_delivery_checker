from time import sleep
from datetime import datetime, timedelta, timezone
import os
import prepare_syspath  # noqa: F401
from check import check


WAIT_TIME = int(os.environ.get("WAIT_TIME", "3600"))

while True:
    check()
    print(
        "Next check will be performed at: ",
        datetime.now(timezone(timedelta(hours=2))) + timedelta(seconds=WAIT_TIME),
    )
    sleep(WAIT_TIME)
