import re

with open('test.md', 'r') as f:
    text = f.read()

def repair_latex(content):
    # Unescape common LaTeX characters
    content = content.replace('\\_', '_').replace('\\^', '^').replace('\\*', '*')
    
    # M*i -> M_i, R*i -> R_i
    content = re.sub(r'([A-Za-z])\*([a-z])', r'\1_\2', content)
    
    # Operators with subscripts
    # \sum*{...} -> \sum_{...}
    # \sum{...} -> \sum_{...}
    content = content.replace('\\sum*', '\\sum_')
    content = content.replace('\\int*', '\\int_')
    content = re.sub(r'\\sum(\{)', r'\\sum_\1', content)
    content = re.sub(r'\\int(\{)', r'\\int_\1', content)
    
    # t* -> t_
    content = content.replace('t*{\\text{epoch}}', 't_{\\text{epoch}}')
    content = content.replace('t*0', 't_0')
    
    # accumulated portfolio fix
    content = content.replace('B_accumulated(t)=b', 'B_{\\text{accumulated}}(t) = b')
    
    return content

def fix_blocks(match):
    # Both groups are capturing now
    prefix = match.group(1) or ""
    latex = match.group(2)
    repaired = repair_latex(latex)
    return f"{prefix}\n$$ {repaired.strip()} $$"

# Regex: Group 1 captures prettier-ignore, Group 2 captures the math content
text = re.sub(r'(<!-- prettier-ignore -->)?\s*\$\$\s*(.*?)\s*\$\$', fix_blocks, text, flags=re.DOTALL)

def fix_inline(match):
    content = match.group(1)
    return f"${repair_latex(content)}$"

text = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', fix_inline, text, flags=re.DOTALL)

with open('test.md', 'w') as f:
    f.write(text)

print("Fixed math syntax repair complete.")
