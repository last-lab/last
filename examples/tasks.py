from datetime import date, timedelta

import httpx
from loguru import logger
from rearq import ReArq

from examples import settings
from examples.models import Sponsor

rearq = ReArq(
    db_url=settings.DATABASE_URL,
    redis_url=settings.REDIS_URL,
    keep_job_days=7,
)


# @rearq.task(bind=False, cron="0 0 * * *")
async def remove_invalid_sponsor():
    invalid_date = date.today() - timedelta(days=1)
    sponsors = await Sponsor.filter(invalid_date=invalid_date).only("username")
    org = "fastapi-admin"
    async with httpx.AsyncClient(
        headers={"accept": "application/vnd.github.v3+json"},
        auth=(settings.GITHUB_USERNAME, settings.GITHUB_TOKEN),
    ) as client:
        for sponsor in sponsors:
            username = sponsor.username
            url = f"https://api.github.com/orgs/{org}/outside_collaborators/{username}"
            res = await client.delete(url)
            logger.info(res.status_code)
    return len(sponsors)
