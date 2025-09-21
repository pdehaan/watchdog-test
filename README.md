# watchdog-test

Playing w/ [watchdog](https://pypi.org/project/watchdog/) to monitor file changes on OS.

- Step 1: New MP3 is downloaded using async httpx streaming. (Question: does streaming work w/ watchdog, or will it try parsing an in-progress, chunked .mp3?)
- Step 2: Extract ID3 information from .mp3 while we wait for MacWhisper to async create transcript.
- Step 3: Update database w/ ID3 information based on MP3 filename (base filename is the episode's guid primary key).
- Step 4: Transcript complete from MacWhisper and it should create a .csv file w/ same base filename as .mp3.
- Step 5: Update database w/ transcript as a CSV (into a big TEXT column). Need a secondary column for speaker name map as JSON blob.
- Step 6: Delete the .MP3 and .CSV files.
- Step n: Find way to trigger another fetch of streaming .mp3 download to restart workflow. Do we fetch `n` files on a CRON? Or just a basic one-in-one-out queue?
