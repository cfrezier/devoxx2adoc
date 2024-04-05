# Devoxx2adoc

Generate your pre-filled notes in adoc and just add your notes during presentations !

## Requirements

```bash
pip3 install -r requirements.txt --user
```

## Usage

### locally

Get the cookie value of `PLAY_SESSION` in the `https://cfp.devoxx.fr` domain.

```bash
./generate.py
```

### with docker/podman

```bash
docker container run -ti --rm -v $(pwd)/talks:/workspace/talks ghcr.io/cfrezier/devoxx2adoc:latest generate.py
```

This will generate a folder `talks` with all talks, based on the template `template.adoc`.

Pick your favorites and add your notes !
