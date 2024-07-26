import re

tx = "(1.О взыскании долга)"
print(re.sub(r"\(|\)", "", tx))