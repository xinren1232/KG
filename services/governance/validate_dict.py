import csv, sys, re, json

# 结合你的场景沉淀的类别枚举（后续可扩展，但请走变更记录）
CATS = {
  "异常现象","部件","流程","参数","测试","工具","材料","质量体系",
  "摄像头模组","显示相关","射频相关","电池","EMC","PCB","SMT","结构相关","软件相关"
}

def too_generic(term:str)->bool:
  term = term.strip()
  if len(term) <= 1: return True
  if re.fullmatch(r"[A-Za-z]{1,2}", term): return True
  return False

def load_rows(path):
  with open(path, newline='', encoding='utf-8') as f:
    return [r for r in csv.DictReader(f)]

def validate(rows):
  errs, warns = [], []
  seen_names = set()
  alias_to_main = {}

  for i, r in enumerate(rows, start=2):  # 表头为第1行
    name = (r.get("术语") or "").strip()
    aliases = [a.strip() for a in (r.get("别名") or "").split(";") if a.strip()]
    category = (r.get("类别") or "").strip()
    tags = [t.strip() for t in (r.get("多标签") or "").split(";") if t.strip()]

    if not name:
      errs.append((i, "术语为空"));  continue
    if name in seen_names:
      errs.append((i, f"术语重复: {name}"))
    seen_names.add(name)

    if category not in CATS:
      errs.append((i, f"类别非法: {category}；必须是{sorted(CATS)}"))

    if name in aliases:
      errs.append((i, f"别名包含主名本身: {name}"))

    for a in aliases:
      if a in alias_to_main and alias_to_main[a] != name:
        errs.append((i, f"别名冲突: {a} 已归 {alias_to_main[a]}，现又指向 {name}"))
      alias_to_main[a] = name

    if too_generic(name):
      warns.append((i, f"术语过短或过泛: {name}（建议用更具体业务词）"))

    if any(" " in t for t in tags):
      warns.append((i, f"标签包含空格（建议分号分隔且无空格）: {tags}"))

  return errs, warns

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("用法: python services/governance/validate_dict.py data/dicts/quality_terms.csv")
    sys.exit(2)
  rows = load_rows(sys.argv[1])
  errs, warns = validate(rows)
  for e in errs: print("ERROR line", e[0], e[1])
  for w in warns: print("WARN  line", w[0], w[1])
  print(json.dumps({"errors":len(errs), "warnings":len(warns)}, ensure_ascii=False))
  sys.exit(1 if errs else 0)
