import itertools
from collections import Counter 
import re
import freq_Analysis

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_letters = letters + letters.lower() + ' \t\n'
maxlength= 16  
nonletters = re.compile('[^A-Z]')

def main():  
    ciphertext = """
    Lm oap btb rrvypqn. Tydi'a c cfqrmkt, sxi qv's r ktintyb dvg. I nrclgr zi ipg Edstzqr Yrcwtilv livcylco vhv Yxakgfwwa eodlco qvvu ipg svytvvh ylat vrlon zgaclomf tydi bje Irbip Edsxzg wrv pjquk wd nclc. Wwqu ij mjav aeripgr gdvm kn ylhbqrp, lhv'v ik? Zxtn tylh jg tyh tvf ow rjz eimlaqbakldv?
    """  # Put Encrpyed Message Here
    hackedMessage = hackVigenere(ciphertext)
    if hackedMessage != None:
        print(hackedMessage)
    else:
        print('Failed to decode')

def load_dictionary(filepath='words.txt'):
    with open(filepath) as dictionary_file:
        return {word.strip().upper(): None for word in dictionary_file}

words = load_dictionary()

def remove_non_letters(message):
    return ''.join(char for char in message if char.upper() in all_letters)

def get_english_count(message):
    possible_words = remove_non_letters(message.upper()).split()
    return sum(1 for word in possible_words if word in words) / len(possible_words) if possible_words else 0

def decryptMessage(key, message):
    decrypted = []
    keyIndex = 0
    key = key.upper()

    for symbol in message:
        num = letters.find(symbol.upper())
        if num != -1: 
            num -= letters.find(key[keyIndex])
            num %= len(letters) 
            if symbol.isupper():
                decrypted.append(letters[num])
            else:
                decrypted.append(letters[num].lower())

            keyIndex = (keyIndex + 1) % len(key) 
        else:
            decrypted.append(symbol)

    return ''.join(decrypted)

def isEnglish(message, wordPercentage=60, letterPercentage=85, minWords=1):
    words = message.split()
    wordPercentage = max(wordPercentage, 100 * minWords / len(words)) if words else 100
    wordsMatch = get_english_count(message) * 100 >= wordPercentage
    numLetters = len(remove_non_letters(message))
    lettersMatch = float(numLetters) / len(message) * 100 >= letterPercentage
    return wordsMatch and lettersMatch

def findRepeatSequencesSpacings(message):
    message = nonletters.sub('', message.upper())
    spacings = {}
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen + 1):
            seq = message[seqStart:seqStart + seqLen]
            for i in range(seqStart + seqLen, len(message) - seqLen + 1):
                if message[i:i + seqLen] == seq:
                    if seq not in spacings:
                        spacings[seq] = [i - seqStart]
                    else:
                        spacings[seq].append(i - seqStart)
    return spacings

def getUsefulFactors(num):
    factors = set()
    for i in range(2, min(num, maxlength) + 1):
        if num % i == 0:
            factors.add(i)
            factors.add(num // i)
    return list(factors & set(range(2, maxlength + 1)))


def getItemAtIndexOne(x):
    return x[1]

def getMostCommonFactors(seqFactors):
    allFactors = [factor for factors in seqFactors.values() for factor in factors]
    factorCounts = Counter(allFactors)
    return sorted([(factor, count) for factor, count in factorCounts.items() if factor <= maxlength], key=lambda x: x[1], reverse=True)

from collections import Counter

def kasiskiExamination(ciphertext):
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)
    allFactors = []
    for spacings in repeatedSeqSpacings.values():
        for spacing in spacings:
            allFactors.extend(getUsefulFactors(spacing))
    factorCounts = Counter(allFactors)
    mostCommonFactors = [factor for factor, count in factorCounts.most_common() if factor <= maxlength]
    return mostCommonFactors

def getNthSubkeysLetters(nth, keyLength, message):
    message = ''.join(char.upper() for char in message if char.isalpha())
    return ''.join(message[i] for i in range(nth - 1, len(message), keyLength))


def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    ciphertextUp = ciphertext.upper()
    allFreqScores = [
        sorted(
            [(letter, freq_Analysis.englishFreqMatchScore(decryptMessage(letter, getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp))))
             for letter in letters],
            key=lambda x: x[1], reverse=True)[:5]
        for nth in range(1, mostLikelyKeyLength + 1)
    ]

    for i, freqScores in enumerate(allFreqScores, start=1):
        print(f"Letters for letter {i} of the key: {' '.join(freqScore[0] for freqScore in freqScores)}")
    for indexes in itertools.product(range(5), repeat=mostLikelyKeyLength):
        possibleKey = ''.join(allFreqScores[i][index][0] for i, index in enumerate(indexes))
        print(f'Attempting with: {possibleKey}')

        decryptedText = decryptMessage(possibleKey, ciphertextUp)
        if isEnglish(decryptedText):
            decryptedText = ''.join(decryptedText[i].upper() if c.isupper() else decryptedText[i].lower() for i, c in enumerate(ciphertext))
            print(f'Possible encryption key: {possibleKey}. Possible orignal message:')
            return decryptedText 
    return None

def hackVigenere(ciphertext):
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    keyLengthStr = ' '.join(map(str, allLikelyKeyLengths))
    allKeyLengthsToTry = allLikelyKeyLengths + [k for k in range(1, maxlength + 1) if k not in allLikelyKeyLengths]
    for keyLength in allKeyLengthsToTry:
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage is not None:
            return hackedMessage
    return None

main()