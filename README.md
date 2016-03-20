# SSLauncher
Build a Mac OSX app for launch ShadowSocksX with new configuration plist. It's worked for me.

thank for http://www.ishadowsocks.net


## Download
```bash
git clone https://github.com/leiyue/ss-launcher.git
cd ss-launcher
```

## Requirements
```bash
pip install -r requirements.txt
```
> Don't use `virtualenv`, because py2app don't like it.

## Install py2app
```bash
pip install py2app
```

## Build a app
```bash
python setup.py py2app
```

## Usage
```bash
open dist/SSLauncher.app
```

Use it as you like. I put it into Dock. :P

