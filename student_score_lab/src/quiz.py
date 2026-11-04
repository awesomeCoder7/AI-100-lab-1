"""
quiz.py - checkpoint checker for the lab.

"""
import base64
import hashlib
import json

_DATA = json.loads(r"""{
 "P1": {
  "kind": "choice",
  "hint": "Look at which columns the pipeline printed as 'features used'. Is attendance there?",
  "explain": "c2VsZWN0X2R0eXBlcygnbnVtYmVyJykga2VlcHMgb25seSBudW1lcmljIGNvbHVtbnMuICc4NSUnIGlzIHRleHQsIHNvIGJvdGggYXR0ZW5kYW5jZSBjb2x1bW5zIHdlcmUgc2lsZW50bHkgbGVmdCBvdXQgLSBubyBlcnJvciwganVzdCBhIHdlYWtlciBtb2RlbC4gQWx3YXlzIHByaW50IHlvdXIgZmVhdHVyZSBsaXN0Lg==",
  "hash": "7db6587b2f68581c0c37dfc33176b4d0cf159c811fd373d154de7039d8b7c75a"
 },
 "P2": {
  "kind": "choice",
  "hint": "Where can a copy of the same student end up after a random split?",
  "explain": "NCBkdXBsaWNhdGVkIHN0dWRlbnRzIGhhZCBvbmUgY29weSBpbiB0cmFpbiBhbmQgb25lIGluIHRlc3QsIHNvIHBhcnQgb2YgdGhlIHRlc3Qgd2FzICdhbHJlYWR5IHNlZW4nLiBSZW1vdmluZyBkdXBsaWNhdGVzIG1ha2VzIHRoZSB0ZXN0IGhvbmVzdCAodGhlIHNwbGl0IGFsc28gcmVzaHVmZmxlcyBhIGJpdCkuIEFuIGhvbmVzdCBsb3dlciBzY29yZSBpcyBiZXR0ZXIgdGhhbiBhIGZsYXR0ZXJpbmcgd3Jvbmcgb25lLg==",
  "hash": "9e5b7b7e94c5e279dd60b1c3a35051024d2b91a53f0afbfe9ef9d109c61bc646"
 },
 "P3": {
  "kind": "number",
  "hint": "The code compares each status with exactly 'on time' (lower case, a space, no dash).",
  "explain": "Tm9uZSBvZiAnT24gdGltZScsICdvbi10aW1lJywgJ09OIFRJTUUnIGlzIGV4YWN0bHkgZXF1YWwgdG8gJ29uIHRpbWUnLCBzbyB0aGUgcmF0ZSBpcyAwIGZvciBhIHN0dWRlbnQgd2hvIHdhcyBhbHdheXMgb24gdGltZS4gVGhlIGNvbXB1dGVyIGNvbXBhcmVzIGNoYXJhY3RlcnMsIG5vdCBtZWFuaW5nLg==",
  "num": "MC4w",
  "tol": 1e-09
 },
 "P4": {
  "kind": "choice",
  "hint": "For which of the two blanks do we actually KNOW what the true value is?",
  "explain": "QSBibGFuayBob21ld29yayBzY29yZSBoYXMgYSBrbm93biBtZWFuaW5nOiBub3Qgc3VibWl0dGVkID0gMCBieSB0aGUgc3lsbGFidXMuIEEgYmxhbmsgYXR0ZW5kYW5jZSBpcyB1bmtub3duOyBmaWxsaW5nIDAgd291bGQgY2xhaW0gdGhlIHN0dWRlbnQgbmV2ZXIgY2FtZS4gVW5rbm93biB2YWx1ZXMgYXJlIGltcHV0ZWQgKG1lZGlhbiksIGtub3duLW1lYW5pbmcgYmxhbmtzIGZvbGxvdyB0aGUgcnVsZS4=",
  "hash": "13375ef37211656f8250064173a400a4fc036b7242cb837d4f23a480b999b244"
 },
 "P5": {
  "kind": "choice",
  "hint": "Least squares squares each error. What does squaring do to one very big error?",
  "explain": "VGhlIGVycm9yIG9uIGEgOTkgaXMgaHVnZSwgYW5kIHNxdWFyaW5nIGl0IG1ha2VzIGl0IGRvbWluYXRlIHRoZSB0b3RhbC4gTGVhc3Qgc3F1YXJlcyB0aGVuIGJlbmRzIHRoZSBsaW5lIHRvd2FyZCB0aGF0IG9uZSB3cm9uZyBwb2ludC4gQ2xlYW5pbmcgb3V0bGllcnMgcHJvdGVjdHMgdGhlIG9iamVjdGl2ZS4=",
  "hash": "32aa164465e8273f568e363ed69b8ff7a3307870ae4c1b6929d37fdfd6b56fdd"
 },
 "P6": {
  "kind": "choice",
  "hint": "With A=1, B=2, C=3, what does the model assume about B compared with A and C?",
  "explain": "QSBzaW5nbGUgbnVtYmVyIGNvbHVtbiB0ZWxscyBhIGxpbmVhciBtb2RlbCB0aGF0IHNlY3Rpb25zIGFyZSBvcmRlcmVkIGFuZCBldmVubHkgc3BhY2VkIChCIGlzIGhhbGZ3YXkgYmV0d2VlbiBBIGFuZCBDLCBDIGlzICdtb3JlJyB0aGFuIEEpLiBTZWN0aW9ucyBoYXZlIG5vIG9yZGVyLCBzbyBvbmUtaG90IGVuY29kaW5nIGdpdmVzIGVhY2ggaXRzIG93biAwLzEgY29sdW1uLg==",
  "hash": "9febdadd6fbc4220c5540d49039f4aee24dae417a8dde37c71fe76219de566b4"
 },
 "P7": {
  "kind": "choice",
  "hint": "When does a student's letter grade become known?",
  "explain": "bGV0dGVyX2dyYWRlIGlzIGNvbXB1dGVkIEZST00gZmluYWxfc2NvcmUsIHNvIGl0IGlzIG5vdCBhdmFpbGFibGUgd2hlbiB3ZSB3YW50IHRvIHByZWRpY3QuIFVzaW5nIGl0IGlzIHRhcmdldCBsZWFrYWdlOiBncmVhdCB0ZXN0IHNjb3JlLCB1c2VsZXNzIG1vZGVsLg==",
  "hash": "fbdd84c6afb9b4564e2e54b23f8255b7e3248be14e90d5a17875c7f7b9745f38"
 },
 "P8": {
  "kind": "choice",
  "hint": "What does the test set pretend to be?",
  "explain": "VGhlIHRlc3Qgc2V0IHBsYXlzIGZ1dHVyZSBzdHVkZW50cy4gQW55IG51bWJlciBjb21wdXRlZCB3aXRoIHRoZWlyIGRhdGEgKG1lZGlhbiwgbWVhbiwgc2NhbGVyKSBsZXRzIGluZm9ybWF0aW9uIGZyb20gdGhlICdmdXR1cmUnIGludG8gdHJhaW5pbmcgYW5kIG1ha2VzIHRoZSB0ZXN0IHNjb3JlIHRvbyBvcHRpbWlzdGljLiBGaXQgb24gdHJhaW4sIGFwcGx5IHRvIGJvdGgu",
  "hash": "8cfa5c0217014fc42780936b11d624725c5a610dbe3ee72e9b62267acecd7d62"
 },
 "P9": {
  "kind": "choice",
  "hint": "If hw_avg is divided by its standard deviation, what can the model do to its coefficient?",
  "explain": "U2NhbGluZyBhIGZlYXR1cmUgYnkgYSBjb25zdGFudCBqdXN0IHNjYWxlcyBpdHMgY29lZmZpY2llbnQgdGhlIG90aGVyIHdheTsgbGVhc3Qgc3F1YXJlcyByZWFjaGVzIGV4YWN0bHkgdGhlIHNhbWUgcHJlZGljdGlvbnMsIHNvIFIyIGRvZXMgbm90IGNoYW5nZS4gU2NhbGluZyBtYXR0ZXJzIGZvciBncmFkaWVudCBkZXNjZW50LCByZWd1bGFyaXphdGlvbiBhbmQgY29tcGFyaW5nIGNvZWZmaWNpZW50cyAtIHNlZSBub3RlYm9vayAwMy4=",
  "hash": "5e7ef5be7f892f8efe2c6e53bea1dce92dcd8924569ff44373531c7b3c24bcd2"
 },
 "O1": {
  "kind": "choice",
  "hint": "The method is literally called 'least ____'.",
  "explain": "T3JkaW5hcnkgbGVhc3Qgc3F1YXJlcyBwaWNrcyBiMC4uYmsgdG8gbWluaW1pemUgdGhlIG1lYW4gKG9yIHN1bSkgb2Ygc3F1YXJlZCBlcnJvcnMsIE1TRSA9IG1lYW4oKHkgLSB5X2hhdCleMiku",
  "hash": "443d50af2ab1774df1ce7f051d84303218fcb24437742c3bcf61979a6230f971"
 },
 "O2": {
  "kind": "number",
  "hint": "Errors are 5, -5, 0. Square them, add, divide by how many students.",
  "explain": "KDI1ICsgMjUgKyAwKSAvIDMgPSAxNi42Ny4gTm90ZSB0aGUgc2lnbiBvZiBhbiBlcnJvciBkaXNhcHBlYXJzIHdoZW4gc3F1YXJlZC4=",
  "num": "MTYuNjY2NjY2NjY2NjY2NjY4",
  "tol": 0.05
 },
 "O3": {
  "kind": "choice",
  "hint": "Run the gradient-descent cell with lr = 0.025 and look at the loss.",
  "explain": "RWFjaCBzdGVwIG92ZXJzaG9vdHMgdGhlIGJvdHRvbSBvZiB0aGUgYm93bCBieSBtb3JlIHRoYW4gaXQgc3RhcnRlZCwgc28gdGhlIGxvc3MgZ3Jvd3Mgd2l0aG91dCBsaW1pdCAoZGl2ZXJnZW5jZSkuIFRvbyBzbWFsbCBhIGxlYXJuaW5nIHJhdGUgaXMgc2FmZSBidXQgc2xvdy4=",
  "hash": "7f0da781af9476e9a510a63f6538ab551092d8922f537af3f610341b57b4a31f"
 },
 "O4": {
  "kind": "choice",
  "hint": "How many lowest points does a bowl have?",
  "explain": "VGhlIE1TRSBvZiBhIGxpbmVhciBtb2RlbCBpcyBjb252ZXggKGEgYm93bCk6IG9uZSBtaW5pbXVtLCBubyBmYWxzZSB2YWxsZXlzLiBBbnkgZG93bmhpbGwgcGF0aCwgbGlrZSBncmFkaWVudCBkZXNjZW50LCBlbmRzIGF0IHRoZSBzYW1lIGJlc3QgbGluZSBza2xlYXJuIGZpbmRzLg==",
  "hash": "6dad3db93efc787ce68d5b7314c16edf08d27c01ab5d1243423dd4fbacde79ce"
 },
 "O5": {
  "kind": "choice",
  "hint": "R2 compares the model with the 'always guess the average' baseline.",
  "explain": "UjIgPSAxIC0gU1NFX21vZGVsIC8gU1NFX2Jhc2VsaW5lLiAwLjg3IG1lYW5zIHRoZSBtb2RlbCByZW1vdmVzIDg3JSBvZiB0aGUgc3F1YXJlZCBlcnJvciB0aGF0IGd1ZXNzaW5nIHRoZSBjbGFzcyBhdmVyYWdlIHdvdWxkIG1ha2UuIEl0IGlzIG5vdCBhIHBlcmNlbnQgb2YgZXhhY3QgaGl0cy4=",
  "hash": "af7312987dc4c7019f9bf519c6cc27f8188cd0a29426ba640fdf27594930f9b1"
 },
 "O6": {
  "kind": "choice",
  "hint": "Coefficients in a multiple regression are read 'holding the other features fixed'.",
  "explain": "KzEgaG9tZXdvcmsgcG9pbnQgKG91dCBvZiAxMCkgLT4gYWJvdXQgKzMuNCBwcmVkaWN0ZWQgZmluYWwgcG9pbnRzLCB3aXRoIGF0dGVuZGFuY2UsIG9uLXRpbWUgcmF0ZSwgZXRjLiB1bmNoYW5nZWQuIFVuc2NhbGVkIGNvZWZmaWNpZW50cyBhcmUgaW4gcmVhbCB1bml0cyBhbmQgY2Fubm90IGJlIGNvbXBhcmVkIHdpdGggZWFjaCBvdGhlciBmb3IgaW1wb3J0YW5jZS4=",
  "hash": "caedaab21b1ed72339e793c76b511c52a915dd434aecb04783a052577223ed83"
 },
 "L1": {
  "kind": "choice",
  "hint": "Plug a very large and a very negative z into 1 / (1 + e^-z).",
  "explain": "c2lnbWEoeikgaXMgYWx3YXlzIHN0cmljdGx5IGJldHdlZW4gMCBhbmQgMSwgc28gaXQgY2FuIGJlIHJlYWQgYXMgYSBwcm9iYWJpbGl0eS4=",
  "hash": "ab38644d7809faf836f895a557359cf0e9aff56edbf5048efcc6fa0d9007dace"
 },
 "L2": {
  "kind": "number",
  "hint": "Log-loss for y = 1 is -ln(p). Use np.log.",
  "explain": "LWxuKDAuOCkgPSAwLjIyMy4gQSBjb25maWRlbnQsIGNvcnJlY3QgcHJlZGljdGlvbiBjb3N0cyBsaXR0bGUu",
  "num": "MC4yMjMx",
  "tol": 0.005
 },
 "L3": {
  "kind": "choice",
  "hint": "Compute -ln(probability given to the TRUE class) for each option.",
  "explain": "QyBnaXZlcyB0aGUgdHJ1ZSBjbGFzcyAocGFzcykgb25seSA1JTogLWxuKDAuMDUpID0gMy4wLiBBOiAwLjEwNSwgQjogLWxuKDAuNikgPSAwLjUxLCBEOiAtbG4oMC45KSA9IDAuMTA1LiBDb25maWRlbnQgYW5kIHdyb25nIGlzIHB1bmlzaGVkIGhhcmRlc3Qu",
  "hash": "cb37f8b50c192a91fd9c634c621d8a0ebe2a5d32eea7618e0f7e1cb811d7a37b"
 },
 "L4": {
  "kind": "choice",
  "hint": "Look at the ranges of hw_avg and the attendance columns before scaling.",
  "explain": "aHdfYXZnICgwLTEwKSBoYXMgbXVjaCBsYXJnZXIgZ3JhZGllbnRzIHRoYW4gYXR0ZW5kYW5jZSAoMC0xKS4gQSBsZWFybmluZyByYXRlIHNtYWxsIGVub3VnaCBmb3IgaHdfYXZnIGlzIGZhciB0b28gc21hbGwgZm9yIGF0dGVuZGFuY2UsIGFuZCBhIGxhcmdlciBvbmUgbWFrZXMgaHdfYXZnIGJvdW5jZS4gU2NhbGluZyBtYWtlcyB0aGUgbG9zcyBib3dsIHJvdW5kIHNvIG9uZSBsZWFybmluZyByYXRlIHdvcmtzIGZvciBldmVyeSBmZWF0dXJlLg==",
  "hash": "fd625a339bd4c3573660167a583565a60af79ade4bcec80dea305764dae8e97e"
 },
 "L5": {
  "kind": "choice",
  "hint": "Did we call .fit() again in the threshold table?",
  "explain": "VHJhaW5pbmcgbWluaW1pemVzIGxvZy1sb3NzIG9uY2UgYW5kIGZpeGVzIHRoZSBjb2VmZmljaWVudHMuIFRoZSB0aHJlc2hvbGQgaXMgYSBkZWNpc2lvbiBydWxlIGFwcGxpZWQgdG8gdGhlIHByb2JhYmlsaXRpZXMgYWZ0ZXJ3YXJkcywgc28gY2hhbmdpbmcgaXQgbmVlZHMgbm8gcmV0cmFpbmluZy4=",
  "hash": "67117f767f6ad4e64b30b3a0a5135de6f04fb081de1ad3607ee109452ce9febf"
 },
 "L6": {
  "kind": "choice",
  "hint": "What does accuracy do when you nudge a coefficient a tiny bit?",
  "explain": "QWNjdXJhY3kgb25seSBjaGFuZ2VzIHdoZW4gYSBwcmVkaWN0aW9uIGNyb3NzZXMgdGhlIHRocmVzaG9sZCwgc28gaXQgaXMgZmxhdCBhbG1vc3QgZXZlcnl3aGVyZTogbm8gc2xvcGUgZm9yIGdyYWRpZW50IGRlc2NlbnQgdG8gZm9sbG93LiBMb2ctbG9zcyBpcyBzbW9vdGggYW5kIGNvbnZleCBhbmQgc3RpbGwgcmV3YXJkcyBiZWNvbWluZyBtb3JlIGNvbmZpZGVudCBpbiB0aGUgcmlnaHQgYW5zd2VyLg==",
  "hash": "64403ffab64df677d574cc08bae9ef7adf7eaccd7d47a9a2cfb937b1272de078"
 }
}""")
_results = {}


def _h(qid, ans):
    return hashlib.sha256(f"ai100|{qid}|{ans}".encode()).hexdigest()


def _dec(s):
    return base64.b64decode(s).decode()


def check(qid, answer):
    """Check your answer to checkpoint question `qid`."""
    qid = qid.upper().strip()
    if qid not in _DATA:
        print(f"Unknown question id {qid!r}.")
        return
    q = _DATA[qid]
    if answer is None or (isinstance(answer, str) and answer.strip() in ("", "?")):
        print(f"[{qid}] Replace the ? with your answer, then run this cell again.")
        return
    if q["kind"] == "choice":
        ok = _h(qid, str(answer).strip().upper()) == q["hash"]
    else:
        try:
            ok = abs(float(answer) - float(_dec(q["num"]))) <= q["tol"]
        except (TypeError, ValueError):
            print(f"[{qid}] This question needs a number.")
            return
    _results[qid] = _results.get(qid, False) or ok
    if ok:
        print(f"[{qid}] Correct!\n  Why: {_dec(q['explain'])}")
    else:
        print(f"[{qid}] Not yet - try again.\n  Hint: {q['hint']}")


def summary(prefix=""):
    """Show which checkpoint questions you have answered correctly."""
    ids = [k for k in _DATA if k.startswith(prefix.upper())]
    right = [k for k in ids if _results.get(k)]
    todo = [k for k in ids if not _results.get(k)]
    print(f"Correct: {len(right)} / {len(ids)}   {' '.join(right)}")
    if todo:
        print(f"Still to do: {' '.join(todo)}")
