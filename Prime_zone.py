# language: Python, file: insta_check.py, target: Python 3.9+ / a-Shell
# توليد + فحص توفّر إنستا — بدون مكتبات خارجية (urllib فقط)
import random, re, urllib.request, urllib.error, time, sys

A = ["sky","neo","arc","zen","sol","vex","ray","ion","lux","orb","kai","nyx","rune","apex","dusk","echo","flux","jade","volt","ember"]
B = ["bit","core","line","wave","path","node","leaf","gate","mark","rift","stone","field","flow","spark","trace","drift","peak","vale","crest"]
C = ["x","io","hq","app","lab","pro","one","day","hub","net","go","now","box","kit","zap","run","fly","top","win"]
D = ["up","me","ly","er","ix","on","us","ax","oz","em","is","ar","en","ul","id","om","ur","ek","al","in"]
SEPS = ["", "_", "."]
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"


def gen(n=30, sep=None, digits=0, mode="34", seed=None):
    rng = random.Random(seed)
    out, seen, tries = [], set(), 0
    while len(out) < n and tries < n * 500:
        tries += 1
        parts = rng.randint(3, 4) if mode == "34" else (3 if mode == "3" else 4)
        words = [rng.choice(A), rng.choice(B), rng.choice(C)]
        if parts == 4:
            words.append(rng.choice(D))
        s = sep if sep is not None else rng.choice(SEPS)
        u = s.join(words)
        if digits:
            u += "".join(rng.choice("0123456789") for _ in range(digits))
        u = re.sub(r"[^a-z0-9._]", "", u.lower())
        if 3 <= len(u) <= 30 and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def check(user, delay=2.0):
    url = f"https://www.instagram.com/{user}/"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    time.sleep(delay * random.uniform(0.7, 1.5))
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            if r.status == 200:
                return "taken"
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "available"
        if e.code in (403, 429):
            return "blocked"
        return f"error:{e.code}"
    except Exception as e:
        return f"error:{type(e).__name__}"
    return "unknown"


if __name__ == "__main__":
    COUNT  = 20
    MODE   = "34"
    SEP    = None
    DIGITS = 0
    DELAY  = 3.0
    SCAN   = True

    users = gen(COUNT, SEP, DIGITS, MODE)
    print(f"[+] وُلّد {len(users)} يوزر\n")

    if not SCAN:
        for u in users:
            print(u)
        sys.exit(0)

    available, taken, blocked = [], [], []
    for i, u in enumerate(users, 1):
        status = check(u, DELAY)
        mark = {"available": "✅", "taken": "❌", "blocked": "🚫"}.get(status, "⚠️")
        print(f"[{i}/{len(users)}] {mark} {u} — {status}")
        if status == "available":
            available.append(u)
        elif status == "taken":
            taken.append(u)
        elif status == "blocked":
            blocked.append(u)
        if len(blocked) >= 5:
            print("\n[!] إنستا حظر الطلبات — توقف. انتظر ساعة أو استخدم بروكسي.")
            break

    print(f"\n{'='*40}")
    print(f"متاح:   {len(available)}")
    for u in available:
        print("   ✅", u)
    print(f"محجوز:  {len(taken)}")
    print(f"محظور:  {len(blocked)}")
    print(f"{'='*40}")
