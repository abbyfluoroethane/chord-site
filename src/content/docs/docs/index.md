---
draft: true
title: Chord docs
description: How to use Chord, find an XMPP server, and host your own.
---

Chord is a chat client for XMPP. It shows spaces, channels, and DMs in a layout like other chat apps.

## Start here

- [Getting started](getting-started/): install Chord and sign in.
- [Find a server](find-a-server/): pick a public XMPP server for your account.
- [Self-host](self-host/): run your own XMPP server for your spaces.

## Names in Chord

Chord uses one name for each thing.

| Chord says | XMPP term |
| --- | --- |
| space | a space ([XEP-0503](https://xmpp.org/extensions/xep-0503.html)): a PubSub node that groups channels |
| channel | a MUC room ([XEP-0045](https://xmpp.org/extensions/xep-0045.html)) |
| DM | a one-to-one chat |
| server | the XMPP server that hosts an account |
| address | a JID, for example `you@yourserver.org` |

## How spaces work

A space is an XMPP space, as defined in [XEP-0503: Server-side spaces](https://xmpp.org/extensions/xep-0503.html). A space is a PubSub node on a server. The node lists the channels (MUC rooms) that belong to the space.

Because a space is an ordinary PubSub node, any user can make a space. The server admin does not need to set it up. Other XMPP clients that support spaces show the same spaces.

:::caution
XEP-0503 is an experimental XEP. The protocol can change before it becomes a standard. Chord follows the current version of the XEP.
:::
