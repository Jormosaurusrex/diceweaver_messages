# Diceweaver Messages

Message Files for Diceweaver

# Messages

The `messages` directory is set up to hold both the source and translated message files.

The original messages are stored in the `messages/src/en-US/` subdirectory:

* 'client' files are for the website
* 'server' files are sent by the node backend.

Where you see numbered parameters ($1, $2, etc.) these are arguments passed to the string.  

Translated message files are stored in the `messages/translated/` directory in a locale subdirectory. Use the full locale for
the directory (ie. en-US, de-DE) with a dash as the separator between the language and country code. A seed translation (100% machine translated) can be generated for a new language using the `seed_translation.py` tool

Due to limitations in the tooling, for now, the `-en.json` suffix should be used on the corresponding translated files, despite the
local mismatch.

Create a pull request for changes.  Changes are merged into the mainline periodically, so will not become immediately visible.

## Tools Directory

The tools directory contains scripts and utilities for working with the Diceweaver messages files.

### Google Cloud SDK and APIs

The seed translation tool depends on the [Google Cloud SDK](https://cloud.google.com/sdk) gCloud CLI. Installation instructions for the gCloud CLI can be found [here](https://cloud.google.com/sdk/docs/install). You must also configure an application-default project with the Google Cloud Translate API enable.

### Python Tools

Python tools require Python version 3 and a virtaul environment to run. The Python tools share a `requirements.txt` to manage
package dependencies.

To create a virtual environment, execute the following commands:

```shell
python3 -m venv .venv
```

To activate the virtual environemnt, source the activation script:

```shell
source .venv/bin/activate
```

To deactivate the virtual environment, run the command:

```shell
deactivate
```

### Tools

| Tool                | Purpose                                                          |
| ------------------- | ---------------------------------------------------------------- |
| seed_translation.py | Generate a machine translation of the message files for a locale |
