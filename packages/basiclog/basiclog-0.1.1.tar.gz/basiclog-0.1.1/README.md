# Basic Log (basiclog)
## Example code:
```python
import traceback
import basiclog

logger = basiclog.log("debug", __file__)

# for slack error messages
logger.add_slack_handler(slack_api_toke, slack_channel)

logger.info("Script has been started")
try:
    main()
except KeyboardInterrupt:
    logger.info("Script has been stopped manually")
except:
    e = traceback.format_exc()
    logger.error(e)
```