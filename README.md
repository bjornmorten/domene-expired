# domene-expired

Fetch expired and soon-to-expire `.no` and `.se` domains from [domene.shop](https://domene.shop/expired).

## Usage

```sh
domene-expired [options]
```

## Options

| Option                   | Description                                 |
| ------------------------ | ------------------------------------------- |
| `-x, --only-expired`     | Show only expired domains                   |
| `-u, --expiring-soon`    | Show only domains that will expire soon     |
| `-s, --include-se`       | Include `.se` domains (default: `.no` only) |
| `-f, --filter REGEX`     | Filter domains by regex (repeatable)        |
| `-l, --max-len N`        | Filter by max domain length                 |
| `-d, --only-domains`     | Print only domain names (no dates)          |
| `-o, --output FILE`      | Write output to file (default: stdout)      |
| `-j, --json`             | Output JSON format                          |
| `-c, --csv`              | Output CSV format                           |
| `-y, --force`            | Overwrite output file if it already exists  |
| `-h, --help`             | Show help message and exit                  |

## Example output

### Default

```
2025-11-01  bjornmorten.no
2025-11-01	iku-toppene.no
2025-11-01	eksempel.no
```

### Only domains (`--only-domains`)

```
bjornmorten.no
iku-toppene.no
eksempel.no
```

### JSON (`--json`)

```json
[
  {
    "date": "2025-11-01",
    "domain": "bjornmorten.no"
  },
  {
    "date": "2025-11-01",
    "domain": "iku-toppene.no"
  },
  {
    "date": "2025-11-01",
    "domain": "eksempel.no"
  }
]
```

### CSV (`--csv`)

```
date,domain
2025-11-01,bjornmorten.no
2025-11-01,iku-toppene.no
2025-11-01,eksempel.no
```

## License

MIT License © 2025 [bjornmorten](https://github.com/bjornmorten)
