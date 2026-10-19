import asyncio
import os
from datetime import datetime
from typing import Any

from common.base_job import BaseJob  # type: ignore
from database.base_database import BaseDatabase  # type: ignore
from database.postgres_database import PostgresDatabase  # type: ignore
from dotenv import load_dotenv  # type: ignore
from logger.logger import CustomLogger  # type: ignore

load_dotenv()


class LiveTickers(BaseJob):
  def __init__(
    self,
    job_name: str | None = None,
    job_payload: dict[str, Any] | None = None,
  ) -> None:
    super().__init__(job_name, job_payload)
    self._db: BaseDatabase | None = self._job_payload.get("db_instance") or None
    self._logger: CustomLogger | None = self._job_payload.get("logger_instance") or None
    if not self._logger:
      self._logger = CustomLogger()


async def main(job_sleep_mins: int = 30) -> None:

  logger: CustomLogger = CustomLogger()
  logger.info(
    f"{'=' * 80}\n"
    "Live tickers dump - scheduled execution\n"
    f"{'=' * 80}\n"
    f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    f"Running every {job_sleep_mins} minutes...\n"
    "Press Ctrl+C to stop\n"
    f"{'=' * 80}\n"
  )

  postgres_instance: PostgresDatabase = PostgresDatabase(os.getenv("POSTGRES_DATABASE_URI"))
  postgres_instance.initialize()

  print(postgres_instance)


if __name__ == "__main__":
  job_sleep_mins: int = 30
  try:
    asyncio.run(main(job_sleep_mins))
  except KeyboardInterrupt:
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Stopping scheduler... Goodbye!")
