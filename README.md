<a href="https://zerodha.tech"><img src="https://zerodha.tech/static/images/github-badge.svg" align="right" /></a>

## Frappe S3 Attachment

Frappe app that transparently uploads attachments to Amazon S3 and serves them back
from there. Fork of [zerodha/frappe-attachments-s3](https://github.com/zerodha/frappe-attachments-s3).

Compatible with Frappe `>=10.0.0,<17.0.0`.

#### Features

1. Uploads both public and private files to S3, then removes the local copy.
2. Private files are streamed through a redirect to a short-lived presigned URL,
   regenerated on every view. Public files get a `public-read` ACL and a direct
   S3 URL.
3. S3 credentials (AWS key, AWS secret, bucket, region, folder) are configured
   from the desk UI.
4. One-click migration of files already sitting in the site's `public/` and
   `private/` folders.
5. Optionally deletes the object from S3 when the File is deleted in the UI.
6. Objects are keyed categorically:
   `{folder_name}/{year}/{month}/{day}/{parent_doctype}/{random8}_{file_name}`
7. If the attached-to doctype declares an `image_field`, it is updated with the
   new file URL automatically.
8. AWS key/secret are optional — leave both blank to fall back to the ambient
   boto3 credential chain (IAM instance role, `~/.aws/credentials`, env vars).

#### Installation

```bash
bench get-app https://github.com/dsatsangi/frappe-attachments-s3.git
bench --site <site-name> install-app frappe_s3_attachment
```

#### Configuration

Open the single doctype **S3 File Attachment** and fill in:

| Field | Notes |
| --- | --- |
| Bucket Name | Target S3 bucket. |
| AWS Key / AWS Secret | Optional — omit both to use an IAM role or the ambient credential chain. |
| S3 Bucket Region Name | e.g. `ap-south-1`. |
| Folder Name | Key prefix for every upload. Optional; keys start at `{year}/` when blank. |
| Signed URL expiry time | Seconds a presigned URL stays valid. Field default `300`; falls back to `120` if left empty. |
| Delete file from cloud | Unchecked by default. When checked, deleting a File in the UI also deletes the S3 object. |
| Migrate Existing Files | Button. Uploads every File whose `file_url` is not already an S3 URL. Missing local files are skipped. |

#### Site config options

Set in `sites/<site>/site_config.json`:

```json
{
  "ignore_s3_upload_for_doctype": ["Data Import", "Report", "Prepared Report"]
}
```

Attachments whose `attached_to_doctype` is in this list stay on local disk.
When the key is absent, this fork defaults to:

```
Remittance Meta Data Import, Data Import, Report, Prepared Report,
WU Data Import, Western Union Data Import, User, Employee
```

Files with no parent doctype are treated as `File`.

#### Custom key naming

Override the generated S3 key from any app via the `s3_key_generator` hook:

```python
# hooks.py of your app
s3_key_generator = "my_app.s3.build_key"
```

```python
# my_app/s3.py
def build_key(file_name, parent_doctype, parent_name):
    return f"custom/{parent_doctype}/{parent_name}/{file_name}"
```

Return a falsy value (or raise) to fall back to the default key format.

#### API

| Method | Purpose |
| --- | --- |
| `frappe_s3_attachment.controller.generate_file` | Redirects to a presigned URL for a private object. Used as the `file_url` of private files. |
| `frappe_s3_attachment.controller.migrate_existing_files` | Migrates pre-existing local files to S3. |
| `frappe_s3_attachment.controller.ping` | Connectivity check, returns `pong`. |

#### Fork-specific changes

- Custom default `ignore_s3_upload_for_doctype` list (see above).
- `patches/fix_collections_import_error.py` — `collections.abc` import shim.
- `pyproject.toml` declaring the supported Frappe version range for bench v16.

#### License

MIT
