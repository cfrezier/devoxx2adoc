# Devoxx2adoc

Generate your pre-filled notes in adoc and just add your notes during presentations !

## Requirements

```bash
pip3 install -r requirements.txt --user
```

## Usage

Get the cookie value of `PLAY_SESSION` in the `https://cfp.devoxx.fr` domain.

```bash
./generate.py
```

This will generate a folder `talks` with all talks, based on the template `template.adoc`.

Pick your favorites and add your notes !
