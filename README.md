# DAPI
Easy method to contact with DiscordAPI

## Disclaimer
**ENG**: This project is for educational and research purposes only.\
**RUS**: Данный проект был создан только в целях обучения.

## How to install
- MacOS & Linux:
  ```commandline
    git clone https://github.com/Mon4ik/DAPI.git
    cd DAPI
    . venv/bin/activate
    python3 main.py -h
  ```
- Windows:
  ```commandline
    git clone https://github.com/Mon4ik/DAPI.git
    cd DAPI
    venv/bin/activate.bat
    py main.py -h
  ```
## Docs
#### 🔑 - you're need your **authorization token**
### dm_nuke 🔑
#### Creates a lot of dm groups for nuke dm
### *Examples*
```commandline
  main.py dm_nuke -id 1 -id 2
```
```commandline
  main.py dm_nuke -id 1 -id 2 -c 5
```
### rpc
#### Create [Rich Presence](https://discord.com/developers/docs/rich-presence/best-practices)
### *Examples*
```commandline
  main.py rpc test
```
```commandline
  main.py rpc test_animation
```
[How to create your own rich presence](README-EXTRA.md#your-own-rpc)
### status_animation 🔑
#### Creates status animation
### *Examples*
```commandline
  main.py status_animation camera
```
[How to create your own status animation](README-EXTRA.md#your-own-status-animation)
### request 🔑
#### Make your custom request to DiscordAPI ([API docs](https://discord.com/developers/docs/intro))
#### P.s. All results save in dir `results`
### *Examples*
```commandline
  main.py request -m METHOD -j JSONPAYLOAD -v VERSION /path/to/method
```
```commandline
  main.py request /users/@me
```