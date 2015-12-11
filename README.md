
## mh-ui-testing

Automated admin tasks and tests for DCE Matterhorn.

## Getting started

1. Create & activate a virtualenv. This is optional but recommended.

    `virtualenv venv && source venv/bin/activate`
    
2. Install the python package. If you skipped the virtualenv step you'll need to use `sudo` here.

    `pip install mh-ui-testing`
    
3. Sanity check the installation by looking at the usage output.

    * `mh --help` 
    
## Commands

The `mh` interface provides a few top-level commands as well as several more organized
into groups of sub-commands. For instance, `mh upload` is a top-level command, but
commands related to manipulating the MH recording inbox are grouped into an `inbox`
group, for example, `mh inbox list` and `mh inbox put`. Each command accepts one or
more options and arguments. `mh [cmd] --help` to display usage info.

Current command tree:

    * `mh inbox list`
    * `mh inbox put`
    * `mh inbox symlink`
    * `mh series create`
    * `mh upload`
    * `mh trim`
    * `mh gi list`
    * `mh gi exec`
    
### inbox commands

These tasks make use of the python [fabric](http://fabfile.org) library to execute
commands via ssh on the remote system. When running against an Opsworks cluster, it
is expected that your local user corresponds to a remote user so that ssh key auth 
can be utilized. In the case of the ansible-provisioned ec2 clusters you will need
to include the option `--user=ansible` and provide the ansbile user password
    
#### inbox list

    Usage: mh inbox list [OPTIONS] [MATCH]
    
      List the current contents of the inbox
    
    Options:
      -i, --inbox_path TEXT  alternate path to recording inbox
      -u, --user TEXT        The user to execute remote tasks as
      -H, --host TEXT        host/ip of remote admin node
      --help                 Show this message and exit.

#### inbox put

    Usage: mh inbox put [OPTIONS]
    
      Upload a recording file to the MH inbox
    
    Options:
      -f, --file TEXT
      -i, --inbox_path TEXT  alternate path to recording inbox
      -u, --user TEXT        The user to execute remote tasks as
      -H, --host TEXT        host/ip of remote admin node
      --help                 Show this message and exit.

**Note** that `-f/--file` allows the use of a url (eg, s3) and disallows local
uploads for files > 1G.

#### inbox symlink

    Usage: mh inbox symlink [OPTIONS]
    
      Create copies of an existing inbox file via symlinks
    
    Options:
      -f, --file TEXT
      -c, --count INTEGER
      -i, --inbox_path TEXT  alternate path to recording inbox
      -u, --user TEXT        The user to execute remote tasks as
      -H, --host TEXT        host/ip of remote admin node
      --help                 Show this message and exit.

### series create

    Usage: mh series create [OPTIONS]
    
    Options:
      -H, --host TEXT      host/ip of remote admin node
      -u, --username TEXT  MH admin login username
      -p, --password TEXT  MH admin login password
      --title TEXT         Title of the series
      --id TEXT            Series identifier. If not specified this will be
                           generated for you in the format '203501xxxxx' where
                           'xxxxx' is a random number sequence
      --help               Show this message and exit.

### upload

    Usage: mh upload [OPTIONS]
    
      Upload a recording from a local path or the inbox
    
    Options:
      --presenter TEXT     Presenter video
      --presentation TEXT  Presentation video
      --combined TEXT      Combined presenter/presentation video
      --series TEXT        Series title. Should match an existing series.
      --title TEXT         Recording title
      -i, --inbox          Use a MH inbox media file
      --live_stream
      -H, --host TEXT      host/ip of remote admin node
      -u, --username TEXT  MH admin login username
      -p, --password TEXT  MH admin login password
      --help               Show this message and exit.


### trim

    Usage: mh trim [OPTIONS]
    
      Execute trims on existing recording(s)
    
    Options:
      -f, --filter TEXT
      -c, --count INTEGER
      -H, --host TEXT      host/ip of remote admin node
      -u, --username TEXT  MH admin login username
      -p, --password TEXT  MH admin login password
      --help               Show this message and exit.


## Ghost Inspector test commands

Preliminary support for executing Ghost Inspector tests is provided via the 
`mh gi` command group. Options for these commands are simply passed along to
the `py.test` subprocess, so for now take a gander at the [pytest-ghostinspector](https://github.com/harvard-dce/pytest-ghostinspector)
docs to see what those options should be.

### gi list
 
### gi exec


## Example process

The following sequence of commands provides an example of how to upload a set of video files
to the Matterhorn inbox, create symlinks to populate the inbox selection menu
in the **Upload Recording** UI, and then execute a number of uploads

**Note**: This example uses separate presenter/presentation files. For a combined 
multitrack video file, you would execute the `put` and `symlink` commands per usual
but use the `--combined` option for the `upload` task instead of `--presenter/--presentation`.

#### 1. Upload the initial media to the inbox

Local files:

`mh inbox put -H [admin ip] -f path/to/presenter.mp4`

`mh inbox put -H [admin ip] -f path/to/presentation.mp4`

Or use an url for files > 1g:

`mh inbox put -H [admin ip] -f https://s3.amazonaws.com/my-bucket/presenter.mp4`

`mh inbox put -H [admin ip] -f https://s3.amazonaws.com/my-bucket/presentation.mp4`

#### 2. Create symlinks

This will create 10 inbox symlinks to each of the previously uploaded files, 
i.e., 10 identical presenter/presentation copies. Each copy will be named using
the sequence integer: `presenter_1.mp4`, `presenter_2.mp4`, etc.

`mh inbox symlink -H [admin ip] -f presenter.mp4 -c 10`

`mh inbox symlink -H [admin ip] -f presentation.mp4 -c 10`

#### 3. Check inbox contents (optional)

`mh inbox list -H [admin ip]`

#### 4. Run the upload tasks

The `uname` and `passwd` values here correspond to the Matterhorn admin interface 
login.

```
    for i in `seq 1 10`; do mh upload -u [uname] -p [passwd] --inbox --presenter presenter_${i}.mp4 --presentation presentation_${i}.mp4 [admin base_url] ; done
```

This *should* result in 10 processing workflows. The flakiness of Selenium + MH 
makes this not guaranteed.

#### 5. (later) execute the trim tasks

In a happy world you'll have a set of 10 of workflows that process their 
respective copies of the uploaded media and then pause/hold at the `editor` 
operation waiting for a human to intervene. We don't need stinking humans; we 
have Selenium!

`mh trim -u [uname] -p [passwd] [admin base_url]`


## Troubleshooting

### Known issues

#### UnexpectedAlertPresentException: Alert Text: Could not resume Workflow: error

Check that Matterhorn nodes, particularly admin, are not in maintenance state.

## Resources

* python selenium docs: https://selenium-python.readthedocs.org/index.html

