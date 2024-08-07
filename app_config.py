log = {
  "path": "logs/accountant.log",
  "format": "{time} | {level}\t| {file.path}:{line} '{message}'",
  "level": "INFO",
  "backtrace": True,
  "diagnose": True,
  "enqueue": True,
  "rotation": "1 day",
  "retention": "1 month",
  "compression": "zip",
}

database = {
  "scheme": "sqlite+aiosqlite",
  "path": "database/accountant.sqlite",
  "query": {"charset": "utf8mb4"},
  "echo": True,
  "autoflush": True,
  "expire_on_commit": False,
  "store_records_days": 100
}

telegram = {
  "timeout_sec": 10,
}


if __name__ == "__main__":
  pass
