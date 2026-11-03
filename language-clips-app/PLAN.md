# Language Clips: MVP Plan

A mobile app where you learn a language by swiping through short AI-generated video scenes.

## Decisions so far
- **Format:** AI video scenes (about 10-20s each) with a voice and subtitles
- **Platform:** React Native with Expo (iOS + Android)
- **Audience:** English speakers learning one target language (language still to be chosen)

## Core loop
1. Vertical feed of clips. Each clip is a mini-scene (e.g. ordering coffee).
2. Subtitles in the target language, with tap-to-translate on each word.
3. After each clip, a 10-second check: 1-2 questions (pick the meaning, fill the blank).
4. Words you miss come back in later clips (spaced repetition).

## Architecture
```
Expo app  <->  Backend API (Supabase or small Node service)
                   |-- Content pipeline (offline, not at runtime)
                   |-- Postgres: clips, words, user progress
                   |-- Object storage + CDN: video files
```

**Key choice: generate clips ahead of time, not on demand.** Video generation is slow and costly,
so run a pipeline that builds a curated library, and serve it from a CDN. Review each clip before
it ships. This also keeps quality and language accuracy under control.

## Content pipeline (per clip)
1. **Script:** an LLM writes a short dialogue at a set CEFR level (A1 first) using a target
   vocabulary list, plus translation and word-level glosses (JSON output).
2. **Check:** a second LLM pass (and a native-speaker spot check) for grammar and naturalness.
3. **Voice:** text-to-speech in the target language, one voice per character.
4. **Video:** an image-to-video or text-to-video model renders the scene; lip-sync is optional
   for the MVP (use narration over scenes, or characters shown from behind or at a distance).
5. **Subtitles:** burn in or send as timed JSON so the app can make words tappable.
6. **Publish:** upload to storage, insert row in `clips`.

## Data model (sketch)
- `clips(id, level, topic, video_url, transcript_json, duration)`
- `words(id, lemma, translation, level)`
- `clip_words(clip_id, word_id)`
- `user_word_state(user_id, word_id, strength, next_review_at)`
- `attempts(user_id, clip_id, score, created_at)`

## Milestones
1. **Prototype (1 week):** 10 hand-picked clips, feed UI, tappable subtitles, no backend.
2. **Pipeline (1-2 weeks):** automated script, voice, video, review tool. Generate about 100 A1 clips.
3. **Learning loop (1-2 weeks):** quizzes, spaced repetition, accounts, progress.
4. **Beta:** TestFlight and Play internal testing, measure clips watched per session and day-7 retention.

## Main risks
- **Video cost and consistency:** characters can look different between clips. Start with
  one fixed cast and a consistent style.
- **Language errors:** AI can produce unnatural phrases, so keep a human review step.
- **Retention:** a feed is fun but may not teach. The quiz and review loop is what makes it a
  learning app, so build it early.

## Open questions
- Which target language first? (Spanish has the most content and learners; Japanese is a
  distinctive niche and fits the visual format.)
- Free vs subscription model?
- Which video model/vendor? (Evaluate cost per clip and character consistency.)
