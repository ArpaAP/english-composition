import json
import random
from difflib import SequenceMatcher

#################
# CONFIGURATIONS
#################

EXCEPTIONS = []
WITH_HINT = True

#################

with open('./data/2024_suneungttkgang.json', 'r', encoding='utf-8') as f:
    SENTENCES: list = json.load(f)['sentences']

print("""=======================================
ENGLISH COMPOSITION MEMORIZATION HELPER
=======================================
""")

menu = ''

print('\n1: 순서대로\n2: 랜덤으로\n3: 시작 범위 지정...\n4: 종료\n\n')

while not menu.isdecimal():
    menu = input('> ')

if menu == '4':
    exit()

else:
    sentences = SENTENCES.copy()
    start = 1

    if menu == '2':
        random.shuffle(sentences)
    elif menu == '3':
        start = int(input('시작 문항: '))
        sentences = SENTENCES[start - 1:]

    perfect = 0
    incorrect = 0
    skip = 0
    similarities = []

    print('\n', "=" * 20, '\n', sep='')

    for i, one in enumerate(sentences, start):
        if i in EXCEPTIONS:
            continue

        print(f'문제 {i}/{len(SENTENCES)}.\n\n')
        print(one['interpretation'], '\n')

        if WITH_HINT:
            words = one['content'].split()
            random.shuffle(words)

            print('[', ' / '.join(words), ']', '\n')

        ipt = input('> ')

        if ipt == 'pass' or not ipt:
            skip += 1

            print('\n')
            print('패스하고 넘어갑니다.')
            print(f"정답: {one['content']}")

        elif ipt.lower() == one['content'].lower():
            perfect += 1
            similarities.append(1)

            print('\n')
            print('완벽!')
        else:
            incorrect += 1
            sim = SequenceMatcher(None, ipt, one['content'])

            similarities.append(sim.ratio())

            print('\n')
            print(f"정답: {one['content']}")

            print(f'유사도: {round(sim.ratio() * 100, 3)}%')


        print('평균 유사도: {}%'.format(round(sum(similarities) / len(similarities) * 100, 3) if len(similarities) else 0))
        print('\n', "=" * 20, '\n', sep='')

    print(f'정확: {perfect}, 틀림: {incorrect}, 건너뜀: {skip}')
    print('최종 정확도: {}'.format(round(sum(similarities) / len(similarities) * 100, 3) if len(similarities) else 0))

