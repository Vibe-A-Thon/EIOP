import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('EOIP-master-dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

p3 = text.find("type === 'cap'")
p4 = text.find("type === 'proc_unit'", p3)
print(text[p3:p4])
