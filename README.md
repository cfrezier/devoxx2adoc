# Devoxx2adoc

Generate your pre-filled notes in adoc and just add your notes during presentations !

This script only generate the talks you marked as favorite in your planning : <https://cfp.devoxx.fr/2023/byday/wed>

## Usage

Get the cookie value of `PLAY_SESSION` in the `https://cfp.devoxx.fr` domain.

```bash
./favorite.py PLAY_SESSION_VALUE
```

This will generate a folder `wednesday`, `thursday` and `friday` with your favorite talks, based on the template `template.adoc`.
