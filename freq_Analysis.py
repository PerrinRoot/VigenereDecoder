frequency_of_letters = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getLetterCount(message):
    letter_count = {letter: 0 for letter in alphabet}
    for char in message.upper():
        if char in alphabet:
            letter_count[char] += 1
    return letter_count

def getFrequencyOrder(message):
    letter_to_freq = getLetterCount(message)
    freq_to_letters = {}
    for letter, freq in letter_to_freq.items():
        freq_to_letters.setdefault(freq, []).append(letter)
    for freq, letters in freq_to_letters.items():
        letters.sort(key=frequency_of_letters.find, reverse=True)
        freq_to_letters[freq] = ''.join(letters)
    freq_pairs = sorted(freq_to_letters.items(), reverse=True)
    freq_order = ''.join(letters for _, letters in freq_pairs)
    return freq_order

def englishFreqMatchScore(message):
    freq_order = getFrequencyOrder(message)
    match_score = sum(1 for letter in frequency_of_letters[:6] if letter in freq_order[:6]) \
                + sum(1 for letter in frequency_of_letters[-6:] if letter in freq_order[-6:])
    return match_score
