from collections import Counter

frequency_of_letters = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getLetterCount(message):
    return Counter(letter for letter in message.upper() if letter in letters)

def getFrequencyOrder(message):
    letterToFreq = getLetterCount(message)
    freqToLetter = {}
    for letter, freq in letterToFreq.items():
        freqToLetter.setdefault(freq, []).append(letter)
    for freq in freqToLetter:
        freqToLetter[freq].sort(key=frequency_of_letters.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])
    freqPairs = sorted(freqToLetter.items(), key=lambda x: x[0], reverse=True)
    freqOrder = ''.join(letters for freq, letters in freqPairs)
    return freqOrder

def englishFreqMatchScore(message):
    freqOrder = getFrequencyOrder(message)
    matchScore = sum(commonLetter in freqOrder[:6] for commonLetter in frequency_of_letters[:6]) + \
                 sum(uncommonLetter in freqOrder[-6:] for uncommonLetter in frequency_of_letters[-6:])

    return matchScore
