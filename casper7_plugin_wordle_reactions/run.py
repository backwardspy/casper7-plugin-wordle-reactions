"""
a casper7 plugin that reacts to wordle results

Usage:
    casper7-plugin-wordle-reactions [options] react [--] <args>
    casper7-plugin-wordle-reactions --listeners
    casper7-plugin-wordle-reactions --commands
    casper7-plugin-wordle-reactions --jobs
    casper7-plugin-wordle-reactions (-h | --help)
    casper7-plugin-wordle-reactions --version

Options:
    -g --guild GUILD_ID         Guild ID the message is coming from.
    -c --channel CHANNEL_ID     Channel ID the message is coming from.
    -u --user USER_ID           User ID the message is coming from.
    -m --message MESSAGE_ID     ID of the message that was sent.
    --listeners                 Get listener config JSON.
    --commands                  Get command config JSON.
    --jobs                      Get job config JSON.
    -h --help                   Show this screen.
    --version                   Show version.
"""
import json
import re
from importlib.metadata import version

from docopt import docopt

from casper7_plugin_wordle_reactions.settings import settings


def re_compile(pattern: str) -> re.Pattern:
    """Compile a regex pattern."""
    return re.compile(pattern, re.IGNORECASE | re.MULTILINE)


reactions = [
    (re_compile(r"wordle \d+ [1-6]/6"), "π§ "),
    (re_compile(r"wordle \d+ 1/6"), "1οΈβ£"),
    (re_compile(r"wordle \d+ 2/6"), "2οΈβ£"),
    (re_compile(r"wordle \d+ X/6"), "π"),
    (re_compile(r"daily duotrigordle #\d+\nguesses: \d+/37"), "π§ "),
    (re_compile(r"daily duotrigordle #\d+\nguesses: X/37"), "π"),
    (re_compile(r"scholardle \d+ [1-6]/6"), "π"),
    (re_compile(r"scholardle \d+ 1/6"), "1οΈβ£"),
    (re_compile(r"scholardle \d+ 2/6"), "2οΈβ£"),
    (re_compile(r"scholardle \d+ X/6"), "π"),
    (re_compile(r"worldle #\d+ [1-6]/6 \(100%\)"), "πΊοΈ"),
    (re_compile(r"worldle #\d+ X/6 \(\d+%\)"), "π"),
    (re_compile(r"waffle\d+ [0-5]/5"), "π§"),
    (re_compile(r"waffle\d+ 5/5"), "β­"),
    (re_compile(r"waffle\d+ X/5"), "π"),
    (re_compile(r"#wafflesilverteam"), "π₯"),
    (re_compile(r"#wafflegoldteam"), "π₯"),
    (re_compile(r"flowdle \d+ \[\d+ moves\]"), "π°"),
    (re_compile(r"flowdle \d+ \[failed\]"), "π"),
    (re_compile(r"jurassic wordle \(game #\d+\) - [1-8] / 8"), "π¦"),
    (re_compile(r"jurassic wordle \(game #\d+\) - X / 8"), "π"),
    (re_compile(r"jungdle \(game #\d+\) - [1-8] / 8"), "π¦"),
    (re_compile(r"jungdle \(game #\d+\) - X / 8"), "π"),
    (re_compile(r"dogsdle \(game #\d+\) - [1-8] / 8"), "πΆ"),
    (re_compile(r"dogsdle \(game #\d+\) - X / 8"), "π"),
    (re_compile(r"framed #\d+.*\n+.*π₯ [π₯β¬ ]*π©"), "π¬"),
    (re_compile(r"framed #\d+.*\n+.*π₯ [π₯β¬ ]+$"), "π"),
    (re_compile(r"moviedle #[\d-]+.*\n+.*π₯[π₯β¬β¬οΈ ]*π©"), "π¬"),
    (re_compile(r"moviedle #[\d-]+.*\n+.*π₯[π₯β¬β¬οΈ ]+$"), "π"),
    (re_compile(r"posterdle #[\d-]+.*\n+ β .*\n πΏ.+π©"), "π―"),
    (re_compile(r"posterdle #[\d-]+.*\n+ β 0οΈβ£ .*\n πΏ.+π©"), "0οΈβ£"),
    (re_compile(r"posterdle #[\d-]+.*\n+ β .*\n πΏ [β¬οΈπ₯β¬οΈ ]+$"), "π"),
    (re_compile(r"namethatride #[\d-]+.*\n+ β .*\n π.+π©"), "π"),
    (re_compile(r"namethatride #[\d-]+.*\n+ β .*\n π [β¬οΈπ₯β¬οΈ ]+$"), "π"),
    (re_compile(r"heardle #\d+.*\n+.*π©"), "π"),
    (re_compile(r"heardle #\d+.*\n+π"), "π"),
    (re_compile(r"flaggle .*\n+.*\d+ pts"), "β³"),
    (re_compile(r"flaggle .*\n+.*gave up"), "π"),
]


def print_listeners() -> None:
    """Print listener config JSON."""
    print(
        json.dumps(
            [
                {
                    "name": "react",
                }
            ]
        )
    )


def maybe_react(message: str, *, channel_id: str, message_id: str) -> None:
    """Check if a message contains any known patterns and emit add_reaction events."""
    if channel_id not in settings.wordle_channels:
        return

    events = []
    for pattern, emoji in reactions:
        if pattern.search(message):
            events.append(
                {
                    "type": "add_reaction",
                    "channel_id": channel_id,
                    "message_id": message_id,
                    "emoji": emoji,
                }
            )
    print(json.dumps(events))


def plugin() -> None:
    """Plugin entrypoint."""
    args = docopt(
        __doc__, version=f"casper7-plugin-wordle-reactions {version(__package__)}"
    )

    if args["<args>"]:
        args["<args>"] = json.loads(args["<args>"])

    channel_id = args["--channel"]
    message_id = args["--message"]

    match args:
        case {"--listeners": True}:
            print_listeners()
        case {"--commands": True}:
            print("[]")
        case {"--jobs": True}:
            print("[]")
        case {"react": True, "<args>": {"message": message}}:
            maybe_react(message, channel_id=channel_id, message_id=message_id)
