# Check this build yourself

PROSOCHĒ interrupts you, so you should be able to look inside it. This page shows you how to check three things with tools that already ship with your Mac:

1. The file you downloaded is the file described here.
2. That file contains exactly the readable source published next to it.
3. Nothing in it fetches anything from the internet.

Run every command from the top folder of this repository, the one that holds `README.md`.

## What you need

A Mac. `shasum`, `plutil`, `openssl`, `aea` and `aa` all come with macOS. `python3` comes with Apple's Command Line Tools, which macOS offers to install the first time you run it.

## The fingerprint

This prints the fingerprint of the signed file and of the readable source.

```bash
shasum -a 256 release/PROSOCHĒ.shortcut source/PROSOCHE.xml
```

You should see exactly these two lines:

```text
fa107e2974025c38ed80ee3cdc8f4122523ebc4e607dfe7d42704fa0ec1cba99  release/PROSOCHĒ.shortcut
18b6ce8a1db283a4697db85a070db821bb1a0878d3f9dfbdaa604df101dd19ca  source/PROSOCHE.xml
```

If the first line differs, you are not looking at the release described in the README.

## The signed file contains exactly this source

A signed shortcut is an Apple Encrypted Archive. The commands below open it using the certificate stored inside it, pull out the list of actions it really contains, and compare that list with the published XML.

```bash
SIGNED="release/PROSOCHĒ.shortcut"; XML="source/PROSOCHE.xml"; W=$(mktemp -d)
/usr/bin/python3 -c 'import struct,plistlib,sys; d=open(sys.argv[1],"rb").read(); n=struct.unpack_from("<I",d,8)[0]; open(sys.argv[2],"wb").write(plistlib.loads(d[12:12+n])["SigningCertificateChain"][0])' "$SIGNED" "$W/leaf.der"
/usr/bin/openssl x509 -inform DER -in "$W/leaf.der" -noout -pubkey > "$W/pub.pem"
aea decrypt -i "$SIGNED" -o "$W/payload.aa" -sign-pub "$W/pub.pem"
mkdir "$W/un" && aa extract -i "$W/payload.aa" -d "$W/un"
plutil -convert xml1 -o "$W/signed.xml" "$W/un/Shortcut.wflow"
/usr/bin/python3 -c 'import plistlib,sys; a=plistlib.load(open(sys.argv[1],"rb")); b=plistlib.load(open(sys.argv[2],"rb")); print("identical actions:", a["WFWorkflowActions"]==b["WFWorkflowActions"], len(a["WFWorkflowActions"]))' "$W/signed.xml" "$XML"
rm -rf "$W"
```

You should see:

```text
identical actions: True 2769
```

The certificate inside the archive is issued by Apple and names no person and no email address. Apart from the list of actions, the top-level settings of the two files differ only where Apple's signer changes them: the client version string, an added empty list of quick-action surfaces, and the shortcut's display name, which signing removes. That is why the file name becomes the shortcut's name when you import it.

## Nothing in it fetches anything from the internet

This counts the actions that download a web page, request a web address, or call a model.

```bash
grep -cE 'is\.workflow\.actions\.(downloadurl|geturl|getcontentsofurl|askllm)' source/PROSOCHE.xml
```

You should see:

```text
0
```

The only actions that reach outside the shortcut hand you off to an app you choose: one Open URL, one Search Web, one Search Maps and nine Open App. They run only when you pick a way out.

## What it is made of

This lists every kind of action in the build and how many of each there are, most common first.

```bash
/usr/bin/python3 -c 'import plistlib,collections,sys; p=plistlib.load(open(sys.argv[1],"rb")); [print(v,k) for k,v in collections.Counter(a["WFWorkflowActionIdentifier"] for a in p["WFWorkflowActions"]).most_common()]' source/PROSOCHE.xml
```

Each line is a count followed by the name Apple uses for that action.

## One random number

This counts the actions that pick a random number.

```bash
grep -c 'is\.workflow\.actions\.number\.random' source/PROSOCHE.xml
```

You should see:

```text
1
```

That single random number only labels a session so two sessions never share a name. Every response follows counters, so the same history gets the same response.

## Reading the XML

The XML is produced by a private tool, so `source/PROSOCHE.xml` is the readable form of exactly what you install, not something you are expected to edit. The variable names inside it use the design's working names, which differ from the words you see on screen.
