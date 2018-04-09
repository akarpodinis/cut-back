## `cut-back`

Looking to save a couple of bucks for something?  Give this a shot.  This CLI utility does a variety of things to help you track toward your (small-time) financial goals and provides auditing for analyzing trend data.

Run with `./cut-back.p [arguments]`

## Commands

### Help
TK

### Save
```
:> save 5 on coffee for potatoes
Great!  You saved $5.00 for Potatoes when you skipped Coffee.
```

### Spend
```
:> spend 5 on potatoes
Hard work pays off!  You spent $5.00 on Potatoes.
```
### Maintenance
#### Transfer
```
>: transfer 5 from potatoes to coffee
You transferred $5.00 from Potatoes to Coffee.
```

#### Summarize
```
:> summarize
 Potatoes has $5.00 saved.
 Coffee has $5.00 saved.
```

#### Remove
```
:> remove potatoes
You removed $5.00 saved for Potatoes.
```

## Auditing
By default, `log.tsv` is used and all actions are logged.  The data is tab-separated and the columns are slightly different for each command.  Generally, they are:
```
datetime                    command amt from    to  
2018-04-09 14:51:18.447990  save    5.0 coffee	potatoes
```

The database is JSON-formatted to make editing to adjust easy.  By default, `saved.json` is used and is overwritten when the program is terminated.

## Program arguments
```
$ ./cut-back.py -h
usage: cut-back.py [-h] [-f FILE] [-s] [-a AUDIT_FILE] [--no_audit]

Track pocket change for budgeting!

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Database file location, in json format.
  -s, --summary         Print a summary and exit.
  -a AUDIT_FILE, --audit_file AUDIT_FILE
                        Audit log output file location, tab-separated. A file
                        will be created if none exists.
  --no_audit            Turns off auditing. Defaults to auditing on.
$
```