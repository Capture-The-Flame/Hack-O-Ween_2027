#!/bin/sh
# macOS only: uses the built-in `say` command. Regenerates app/site/audio. VOICE=Whisper ./make_audio.sh for a creepier take.
cd "$(dirname "$0")/../app/site/audio" || exit 1
s() { say -v "${VOICE:-Fred}" -r 165 -o "$1" --file-format=WAVE --data-format=LEI16@22050 "$2"; }
s menu.wav "Thank you for calling Hollow Creek Haunted Trail. For hours and directions, press 1. For tickets, press 2. For group bookings, press 3. If you know your party's extension, you may dial it at any time."
s 1.wav "We are open Fridays and Saturdays in October, from dusk until eleven. Find us at the end of Ashgrove Road, past the second bridge. If you reach the third bridge, turn around. Goodbye."
s 2.wav "Tickets are sold at the gate only. Cash or card. No refunds, no exceptions, no matter what you saw. Goodbye."
s 3.wav "For group bookings of ten or more, leave a message after the tone, and someone will call you back. Eventually."
s 6.wav "Hey. It's Wren. If you're hearing this, you found the crew page, so you're probably one of us. The gate password this month is where I spend my days off. Just the two words, all lowercase, with an underscore between them. Then one more underscore, then the number of jack o lanterns that are lit on my porch. The photo's in the gallery. Count carefully. Don't write it down anywhere. See you at midnight."
s unavailable.wav "That extension is not available. Goodbye."
