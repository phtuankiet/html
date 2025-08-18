import types, sys, random, marshal, importlib.util, struct, time, hashlib, ast

junk_names_list = [
    "\x7f[F@\r🔥☆\t🌈💥💢💫✨",
    "Đố\rEm\rTrai🔥Decompile💀👾🌀",
    "⚡🌟🚀💣💥💎\rĐỌC★HIỂU☆KHÔNG☆EM",
    "🖤💜💚💛💗\rTrình\rLà\rGì\rMà\rTrình\rAi\rChấm",
    "░▒▓█💥🌈🌋🔥💫🌠🌌\r☆\t♛",
    "☢☣⚠🚫\r🛑💣🔞🎯♻💌",
    "💀👹👻🤖\r🤡👺💩🗿🍉",
    "★彡[Loá Mắt Quá Kkk]彡★🔥\r✨",
    "🎆🎇✨⚡🌠\r🌟💫💥🔥",
    "╰☆☆ 𝓟𝓻𝓸 𝓞𝓫𝓯𝓾𝓼𝓬𝓪𝓽𝓸𝓻 ☆☆╮"
] + [f"💫🌟🔥{i}🌀💢💥" for i in range(50)]

def get_junk():
    return f'"{random.choice(junk_names_list)}"'

def makedocs():
    return "__docs__ = '''\n" + "\n".join(
        [f"🐔🐔 Địt Mẹ Mày\r☄️☄️ Đố Em Trai🔥Decompile💀👾🧩🧩" for i in range(100000)]
    ) + "\n'''\n"

def obff(co):
    processed_consts = []
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            processed_consts.append(obff(c))
        else:
            processed_consts.append(c)
    posonly = getattr(co, 'co_posonlyargcount', 0)
    total_args = co.co_argcount + posonly + co.co_kwonlyargcount
    if co.co_varnames:
        new_varnames_list = list(co.co_varnames)
        for i in range(total_args, len(new_varnames_list)):
            new_varnames_list[i] = random.choice(junk_names_list)
        new_varnames = tuple(new_varnames_list)
        return co.replace(co_consts=tuple(processed_consts), co_varnames=new_varnames)
    return co.replace(co_consts=tuple(processed_consts))

def serialize_code(co):
    consts_repr = []
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            consts_repr.append(serialize_code(c))
        else:
            consts_repr.append(repr(c))
    consts_str = "(" + ", ".join(consts_repr) + ",)"
    if sys.version_info >= (3, 11):
        return f"types.CodeType({co.co_argcount},{co.co_posonlyargcount},{co.co_kwonlyargcount},{co.co_nlocals},{co.co_stacksize},{co.co_flags},{repr(co.co_code)},{consts_str},{repr(co.co_names)},{repr(co.co_varnames)},{repr(co.co_filename)},{repr(co.co_name)},{repr(co.co_qualname)},{co.co_firstlineno},{repr(co.co_linetable)},{repr(co.co_exceptiontable)},{repr(co.co_freevars)},{repr(co.co_cellvars)})"
    elif sys.version_info >= (3, 10):
        return f"types.CodeType({co.co_argcount},{co.co_posonlyargcount},{co.co_kwonlyargcount},{co.co_nlocals},{co.co_stacksize},{co.co_flags},{repr(co.co_code)},{consts_str},{repr(co.co_names)},{repr(co.co_varnames)},{repr(co.co_filename)},{repr(co.co_name)},{co.co_firstlineno},{repr(co.co_linetable)},{repr(co.co_freevars)},{repr(co.co_cellvars)})"
    else:
        return f"types.CodeType({co.co_argcount},{co.co_posonlyargcount},{co.co_kwonlyargcount},{co.co_nlocals},{co.co_stacksize},{co.co_flags},{repr(co.co_code)},{consts_str},{repr(co.co_names)},{repr(co.co_varnames)},{repr(co.co_filename)},{co.co_firstlineno},{repr(co.co_lnotab)},{repr(co.co_freevars)},{repr(co.co_cellvars)})"

DECODER_TEMPLATE = """
def {b5}(a: str,b: str):
    return ([int(a[i:i+3]) for i in range(0,len(a),3)] if a else [],[ord(c)-48 for c in b] if b else [])
def {p4}(t: tuple):
    c,k=t; s=0
    for d in k: s=(s*131+d*17+79)%104729
    if not c: return (c,[])
    L=len(c); q=[]; u=(s*602+16)%104729
    for i in range(L): u=(u*337+(i*97+23))%104729; q.append((u^(u>>3)^(u<<1))&255)
    return (c,q)
def {l3}(p: tuple):
    c,q=p
    return [] if not c else [(c[i]-q[i])%256 for i in range(len(c))]
def {he2}(x: list): return bytes(x)
def {h1}(x: bytes): return x.decode("utf-8")
"""

def _rand_cn_name():
    base = ["氢","氦","锂","铍","硼","碳","氮","氧","氟","氖","钠","镁","铝","硅","磷","硫","氯","氩"]
    extra = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸","一","二","三","四","五","六","七","八","九"]
    return random.choice(base) + random.choice(extra) + str(random.randint(1,999))

def generate_decoder_variants(n: int = 3):
    variants = []
    src_parts = []
    for _ in range(max(1, n)):
        used = set()
        def uniq():
            name = _rand_cn_name()
            while name in used:
                name = _rand_cn_name()
            used.add(name)
            return name
        mapping = {
            'b5': uniq(),
            'p4': uniq(),
            'l3': uniq(),
            'he2': uniq(),
            'h1': uniq(),
        }
        variants.append(mapping)
        src_parts.append(DECODER_TEMPLATE.format(**mapping))
    return "\n".join(src_parts), variants

ANTI_HOOK_SRC = r'''
import sys as _sys, builtins as _bi, threading as _th, time as _ti

def _block_trace(*a,**k):
    raise RuntimeError('hooking blocked')
try:
    _sys.settrace(None); _sys.setprofile(None)
    _sys.settrace=_block_trace; _sys.setprofile=_block_trace
except Exception:
    pass

def _block_eval(*a,**k):
    raise RuntimeError('eval blocked')
def _block_compile(*a,**k):
    raise RuntimeError('compile blocked')
def _block_exec(*a,**k):
    raise RuntimeError('exec blocked')

try:
    _bi.eval=_block_eval; _bi.compile=_block_compile; _bi.exec=_block_exec
except Exception:
    pass

def _wd():
    while True:
        try:
            if _bi.eval is not _block_eval: _bi.eval=_block_eval
            if _bi.compile is not _block_compile: _bi.compile=_block_compile
            if _bi.exec is not _block_exec: _bi.exec=_block_exec
        except Exception:
            pass
        _ti.sleep(0.2)
try:
    _th.Thread(target=_wd, daemon=True).start()
except Exception:
    pass

if _sys.gettrace() is not None:
    raise SystemExit(1)
'''

class StringObfuscator(ast.NodeTransformer):
    def __init__(self, key_digits_length: int = 100, variants: list | None = None):
        self.key_digits_length = key_digits_length
        self.variants = variants or []

    @staticmethod
    def _keystream_from_key_digits(key_digits: str, length: int):
        seed = 0
        for ch in key_digits:
            d = ord(ch) - 48
            seed = (seed * 131 + d * 17 + 79) % 104729
        stream = []
        state = (seed * 602 + 16) % 104729
        for i in range(length):
            state = (state * 337 + (i * 97 + 23)) % 104729
            v = state ^ (state >> 3) ^ (state << 1)
            stream.append(v & 255)
        return stream

    def _encode_string(self, s: str):
        data = s.encode('utf-8')
        key_digits = ''.join(random.choice('0123456789') for _ in range(self.key_digits_length))
        ks = self._keystream_from_key_digits(key_digits, len(data))
        cipher_values = [(b + ks[i]) % 256 for i, b in enumerate(data)]
        cipher_digits = ''.join(f"{v:03d}" for v in cipher_values)
        return cipher_digits, key_digits

    def _make_nested_call_ast(self, cipher_digits: str, key_digits: str):
        if self.variants:
            m = random.choice(self.variants)
            n_b5 = m['b5']; n_p4 = m['p4']; n_l3 = m['l3']; n_he2 = m['he2']; n_h1 = m['h1']
        else:
            n_b5, n_p4, n_l3, n_he2, n_h1 = '硼5','铍4','锂3','氦2','氢1'
        call_b5 = ast.Call(func=ast.Name(id=n_b5, ctx=ast.Load()), args=[ast.Constant(cipher_digits), ast.Constant(key_digits)], keywords=[])
        call_p4 = ast.Call(func=ast.Name(id=n_p4, ctx=ast.Load()), args=[call_b5], keywords=[])
        call_l3 = ast.Call(func=ast.Name(id=n_l3, ctx=ast.Load()), args=[call_p4], keywords=[])
        node = ast.Call(func=ast.Name(id=n_he2, ctx=ast.Load()), args=[call_l3], keywords=[])
        if random.random() < 0.5:
            node = ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[], args=[ast.arg(arg='z')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=ast.Name('z', ast.Load())), args=[node], keywords=[])
        node = ast.Call(func=ast.Name(id=n_h1, ctx=ast.Load()), args=[node], keywords=[])
        if random.random() < 0.5:
            node = ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[], args=[ast.arg(arg='w')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=ast.Name('w', ast.Load())), args=[node], keywords=[])
        return node

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, str):
            cipher_digits, key_digits = self._encode_string(node.value)
            return self._make_nested_call_ast(cipher_digits, key_digits)
        return node


def buildcode(path):
    with open(path, "r", encoding="utf-8") as f:
        src_code = f.read()
    tree = ast.parse(src_code, filename=path, mode='exec')
    dec_src, variants = generate_decoder_variants(3)
    tree = StringObfuscator(key_digits_length=100, variants=variants).visit(tree)
    ast.fix_missing_locations(tree)

    docs_src = makedocs()
    docs_ast = ast.parse(docs_src, mode='exec')
    anti_ast = ast.parse(ANTI_HOOK_SRC, mode='exec')
    funcs_ast = ast.parse(dec_src, mode='exec')
    combined = ast.Module(body=[*anti_ast.body, *docs_ast.body, *funcs_ast.body, *tree.body], type_ignores=[])
    ast.fix_missing_locations(combined)
    try:
        with open("12345w.py", "w", encoding="utf-8") as f:
            f.write(ast.unparse(combined))
    except Exception as e:
        print("Không thể unparse AST:", e)

    return compile(combined, path, "exec")


def luufile(co, output_py, output_pyc):
    import zlib
    code_bytes = marshal.dumps(co)
    compressed_bytes = zlib.compress(code_bytes, level=9)

    with open(output_py, "w", encoding="utf-8") as f:
        f.write("import marshal, zlib, types, os, random\n")
        f.write(f"_orig=marshal.loads(zlib.decompress({repr(compressed_bytes)}))\n")
        f.write("def _chaos_bytes(b,lvl,seed):\n")
        f.write("    r=random.Random(seed)\n")
        f.write("    bb=bytearray(b)\n")
        f.write("    n=len(bb); k=max(1,int(n*lvl))\n")
        f.write("    for i in range(k):\n")
        f.write("        j=r.randrange(n); bb[j]^=r.randint(1,255)\n")
        f.write("    return bytes(bb)\n")
        f.write("def _mut_op(co,lvl,seed):\n")
        f.write("    c2=[]\n")
        f.write("    for c in co.co_consts:\n")
        f.write("        if isinstance(c,types.CodeType): c2.append(_mut_op(c,lvl,seed))\n")
        f.write("        else: c2.append(c)\n")
        f.write("    try:\n")
        f.write("        bc=co.co_code\n")
        f.write("        bc2=_chaos_bytes(bc,lvl,seed)\n")
        f.write("        return co.replace(co_code=bc2,co_consts=tuple(c2))\n")
        f.write("    except Exception:\n")
        f.write("        return co.replace(co_consts=tuple(c2))\n")
        f.write("def _run():\n")
        f.write("    lvl=float(os.environ.get('OPC_LEVEL','0.35'))\n")
        f.write("    seed=os.environ.get('OPC_SEED')\n")
        f.write("    seed=None if seed in (None,'',) else int(seed)\n")
        f.write("    try:\n")
        f.write("        m=_mut_op(_orig,lvl,seed)\n")
        f.write("        types.FunctionType(m,globals(),'x')()\n")
        f.write("    except Exception:\n")
        f.write("        types.FunctionType(_orig,globals(),'x')()\n")
        f.write("_run()\n")

    magic = importlib.util.MAGIC_NUMBER
    bitfield = 0
    timestamp = int(time.time())
    size = len(code_bytes)
    header = magic + struct.pack("<II", bitfield, timestamp) + struct.pack("<I", size)

    with open(output_pyc, "wb") as f:
        f.write(header)
        f.write(code_bytes)


if __name__ == "__main__":
    try:
        src = input("nhập file cần obfuscate: ")
    except KeyboardInterrupt:
        sys.exit(1)
    code_obj = buildcode(src)
    code_obj = obff(code_obj)
    luufile(code_obj, "1234.py", "1234.pyc")

