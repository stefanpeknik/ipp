s = "řetězec\032s\032lomítkem\032\092\032a\010novým\035řádkem"
decoded = s.encode('utf-8').decode('unicode_escape')
print(decoded)
