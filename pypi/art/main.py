from art import art, artError

art_1 = art("coffee")
print(art_1)


art_2 = art("woman", number=2)
print(art_2)

print(art("coffee", number=3, space=5))

print(art("random"))
print(art("rand"))

try:
    art(22, number=1)
except artError as e:
    print(f"Caught expected error: {e}")