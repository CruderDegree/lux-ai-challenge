SIMPLEBOT = simple/main.py

test:
	lux-ai-2021 $(SIMPLEBOT) $(SIMPLEBOT) --out=replay.json

clean:
	rm -r -f errorlogs replays simple/__pycache__
	rm -f replay.json
	rm -f submission.tar.gz


submission: clean
	cd simple; tar -czf submission.tar.gz *;
	mv simple/submission.tar.gz .

