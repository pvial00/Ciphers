class Hand:
    def tochars(self, nums):
        chars = []
        for n in nums:
            chars.append(chr(n + 65))
        return "".join(chars)

    def tonums(self, chars):
        nums = []
        for char in chars:
            nums.append((ord(char) - 65))
        return nums

    def encrypt(self, chars, key):
        k = self.tonums(key)
        nums = self.tonums(chars)
        charlen = len(chars)
        c = charlen % 26
        kl = len(key)
        for i in range(charlen):
            nums[i] = (nums[i] + k[c % kl] + c) % 26
            c += 1
        chars = self.tochars(nums)
        return chars

    def decrypt(self, chars, key):
        k = self.tonums(key)
        nums = self.tonums(chars)
        charlen = len(chars)
        c = charlen % 26
        kl = len(key)
        for i in range(charlen):
            nums[i] = (nums[i] - k[c % kl] - c) % 26
            c += 1
        chars = self.tochars(nums)
        return chars
