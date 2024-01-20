import logging
import asyncio
from commands import main

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
