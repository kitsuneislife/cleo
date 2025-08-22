# Backup policy

- Snapshot vector DB daily; upload to `s3://{ARTIFACTS_S3_BUCKET}/backups/{date}`.
- Keep 30 days rolling snapshots and archive monthly snapshots for 1 year.
- Test restore quarterly.
