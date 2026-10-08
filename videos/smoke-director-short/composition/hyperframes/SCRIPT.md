# Script — smoke-director-short

> Captions / reference only. Do **not** TTS — user voiceover is authoritative.

## Line (Frame 1)

    Recently Swiggy Burstrex అనే కొత్త feature launch చేసింది.

## Line (Frame 2)

    But within few days లోనే వాళ్ళు discontinue చేశారు.

## Line (Frame 3)

    Swiggy దీన్ని ఎందుకు discontinue చేశారో officiallyగా ఏమి చెప్పలేదు. And I am not saying this is the reason అని.

## Line (Frame 4)

    But ఈ feature liveలో ఉన్నప్పుడు we found a security issue.

## Line (Frame 5)

    ఏంటి అంటే ప్రతి Burstrexలో link చివర్లో మనకొక similar pattern కనిపిస్తుంది. Like ఒక random token లాగా.

## Line (Frame 6)

    normalగా చూసినప్పుడు మనకి ఇది just ఒక probably ఒక secured token అనిపించొచ్చు.

## Line (Frame 7)

    But మనం దీన్ని properగా analyze చేస్తే ఇది base64 encoding అని మనకు తెలుస్తుంది.

## Line (Frame 8)

    And base64 encoding అనేది any encryption technique కాదు. And దీన్ని మనం easyగా decode చేయగలం.

## Line (Frame 9)

    And surprisingly దీన్ని decode చేస్తే లోపల basically ఒక user ID and name ఉన్నాయి. Something like this.

## Line (Frame 10)

    So theoretically మనం దీన్ని decode చేసి values మార్చవచ్చు. And మళ్ళీ అదే formatలో encode చేయొచ్చు.

## Line (Frame 11)

    And that's exactly what we did. So కొత్త valuesతో ఒక token generate చేసి దాన్ని మేము test చేశాం.

## Line (Frame 12)

    And that link was still being accepted.

## Line (Frame 13)

    So immediateగా మేము ఏం చేశామంటే Swiggyకి ఈ issue కోసం report చేశాం. And దీని గురించి మనం detailedగా next partలో చూద్దాం.

## Line (Frame 14)

    And follow for more.
