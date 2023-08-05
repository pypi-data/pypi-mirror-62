# Telegram Infobot for Raspberry Pi

This is a bot for the Telegram chat platform. It will report useful information to the user, such as IP address, to make it easier to find and login to the new Pi.

It's intended to be installed early on in the SD card setup process for a Raspberry Pi, from the mounted partition on the machine where you originally flashed the image.

## Commands

* `/chatinfo` - This will give the Telegram chat ID for the current chat / room. It allows you to configure on which chat(s) this bot will announce itself.

* `/showip` - This will lookup all of the network interfaces on the system and report interface name, MAC address, and IPv4 address.

## Configuration

At a minimum you'll need the token granted by *@botfather* when you setup the new bot. If you have a chat ID (by running this command in a local virtualenv or something) then you can also have the bot announce itself when the system boots or shuts down.

By default, the configuration file is in: `$HOME/.config/rpi.infobot/config.yaml`. The format looks pretty simple:

```
token: SOME_TOKEN_HERE
chats:
  - 1234567
  - -3456789
```

## Startup

The `rpi.infobot.service` file in the root of this repository should be added to the `/etc/systemd/system` directory. It will need to be enabled, which is a process I'm still working on, trying to avoid a chroot situation.

Ideally, this can be automated using something like Ansible as part of a post-flash step before the new SD card is ready for use. Other things like the config.txt, wpa_supplicant.conf, and the SSH enable marker file are also candidates for this post-process phase.
