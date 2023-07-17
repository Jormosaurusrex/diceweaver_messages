#! python
"""Seed Translation Generator.

This utility takes in a path to the top directory of the messages tree, containing the JSON 
message files, and a target translation locale and generates a seed translation of the JSON
files using the Google Translation API.
"""

import argparse
import os
import json
import re
import sys

from datetime import datetime
from google.cloud import translate_v2


def generate_seed_translation(msg_top, target_language):
    """Generate a seed translation for a given language.

    Takes in the top of a directory tree with JSON message files and
    generates a set of machine translated JSON message files for the requested
    language written to a parallel output tree. The source messages must
    live in ${msg_top}/src/en-US and the output tranlslations will be
    written to ${msg_top}/translated/{$target_language}.

    msg_top: Top of the source message tree.
    target_language: requested translation language (as a localte string)
    """

    msg_src_top = os.path.join(msg_top, "src/en-US")
    msg_dest_top = os.path.join(msg_top, "translated", target_language)

    print(f"Creating seed translation for {target_language}")
    print(f"Reading source message files from {msg_src_top}")
    print(f"Writing output translations to {msg_dest_top}")

    if not os.path.exists(msg_src_top):
        print("ERROR: source message files not found")
        sys.exit(-1)

    if not os.path.exists(msg_dest_top):
        print("Creating message destination directory")
        os.mkdir(msg_dest_top)

    # Credentials and default project must be set via the gcloud utility.
    translate_client = translate_v2.Client()

    # Setup pattern matchers to map message arguments
    src_arg_tokens = re.compile("\$(?P<id>[0-9]+)")
    google_arg_tokens = re.compile("\__(?P<id>[0-9]+)__")

    for root, dirs, files in os.walk(msg_src_top, topdown=True):
        dest_root = root.replace(msg_src_top, msg_dest_top)

        # Create any intermediate directories within the destination directory
        for dir in dirs:
            dest_dir = os.path.join(dest_root, dir)
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)

        # Translate any files in this directory
        for file in files:
            msg_src_filename = os.path.join(root, file)
            msg_dest_filename = os.path.join(dest_root, file)

            with open(msg_src_filename, "r") as f_src:
                msgs_src = json.load(f_src)
                msgs_dest = {}

                # Move over expected metadata untouched
                msgs_dest["@metadata"] = msgs_src["@metadata"]
                msgs_dest["@metadata"]["locale"] = target_language
                msgs_dest["@metadata"]["last-updated"] = datetime.today().strftime(
                    "%Y-%m-%d"
                )
                msgs_dest["@metadata"][
                    "other-metadata"
                ] = f"{target_language} message file"

                for key in msgs_src:
                    # skip all keys starting with @
                    if key.startswith("@"):
                        continue

                    # machine translate message
                    try:
                        msg_txt = msgs_src[key]
                        msg_txt = src_arg_tokens.sub(r"__\g<id>__", msg_txt)
                        translated_txt = translate_client.translate(
                            msg_txt,
                            source_language="en_US",
                            target_language=target_language,
                        )
                        msg_translated = translated_txt["translatedText"]
                        msg_translated = google_arg_tokens.sub(
                            r"$\g<id>", msg_translated
                        )
                        msgs_dest[key] = msg_translated
                    except Exception as e:
                        print("Failed to translate {key}: ", e)

                with open(msg_dest_filename, "w", encoding="utf-8") as f_out:
                    json.dump(msgs_dest, f_out, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="seed_translation",
        description="Generate a seed translation of DiceWeaver's message files",
    )
    parser.add_argument(
        "--messages", default="messages", help="Source directory for message files"
    )
    parser.add_argument(
        "--language",
        required=True,
        help="Destination language (use Google Translate codes)",
    )

    args = parser.parse_args()
    generate_seed_translation(args.messages, args.language)
