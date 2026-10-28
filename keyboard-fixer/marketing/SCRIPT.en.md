# KeyFlip promo (English version, 9:16, 30 s)

File: `out/keyflip-promo-en-9x16.mp4` (1080×1920, 30 fps) – English captions, narration, SFX and music.
Fits TikTok, YouTube Shorts and Instagram Reels.

## Narration (as spoken in the video)
| Seconds | Line |
|---|---|
| 0.0–3.2 | Typed a whole sentence in the wrong language? |
| 3.2–7.0 | Total gibberish. Now delete it all and retype. |
| 7.0–11.5 | Meet KeyFlip, a free tool that fixes it instantly. |
| 11.5–16.0 | Keep typing. At the end of each word, it spots the mistake and fixes it. |
| 16.0–20.5 | It works both ways: Hebrew to English, and English to Hebrew. |
| 20.5–25.0 | It runs on your computer, sends nothing anywhere, and never touches passwords. |
| 25.0–30.0 | Chrome extension and Windows app. Open source and free. Link in the description! |

Subtitles for upload: `narration.en.srt` (the captions are also burned into the video).

## Voice
Generated offline with [Piper](https://github.com/OHF-Voice/piper1-gpl) using the `en_US-lessac-medium` voice. It is a synthetic voice:
- Check the voice model license and the platform rules for AI-generated audio labelling (TikTok / YouTube) before publishing (needs verification against the official terms).
- To use a human voice instead: record the lines above and run `./add_voice.sh voice.mp3` on the no-voice build (`./build.sh he` produces the Hebrew no-voice base; adapt `promo.html?lang=en` for an English no-voice base).

## Post copy
**Title:** Typed in the wrong keyboard language? KeyFlip fixes it for you
**Description:**
Wrote a whole sentence before noticing your keyboard was on the wrong language? KeyFlip automatically fixes Hebrew <-> English typing mistakes.
- Chrome extension + Windows app
- Free and open source (Apache-2.0)
- Runs locally, sends no data, never touches password fields
Download: [link – https://github.com/diamondrubinny/diamondrubinny/releases, or the keyflip repo once it exists]
Note: preview release; Windows may warn because the app is not code-signed yet.
**Hashtags:** #productivity #chromeextension #windows #opensource #hebrew #typing #keyflip

Do not claim 100% accuracy; detection recovered about 96-97% of wrongly typed words in our tests.

## Rebuild
```bash
pip install piper-tts      # plus a Piper voice: en_US-lessac-medium.onnx and .onnx.json
PIPER_MODEL=/path/to/en_US-lessac-medium.onnx ./build.sh en
```
