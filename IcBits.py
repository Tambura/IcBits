class IcBits(object):
    _hex = None
    _dec = None
    _bin = None
    length = None
    bit_list = None
    is_lit = True

    def __init__(self, src):
        if type(src) is str:
            if src[0:2] == "0x":
                self.length = (len(src) - 2) *4
                src = int(src, base=16)
            elif src[0:2] == "0b":
                self.length = len(src) - 2
                src = int(src, base=2)
        elif type(src) == int:
            pass
        elif type(src) == list:
            if type(src[-1]) is str:
                self.length = len(src)
                src = int(list2hex(src), base=16)
            elif type(src[-1]) is IcBits:  # For concat operation
                for i in src:  # constriant: must be IcBits instance.
                    self.length += i.length
                self.concat(self.length, src)
                src = list2dec(sefl._bit_list)

        self._dec = src
        self._hex = hex(self._dec)
        self._bin = bin(self._dec)
        if len(self._bin) - 2 < self.length:
            self._bin = '0b' + (self.length - len(self._bin)) * '0' + self._bin[2:]
        self.bit_list = self.dec2list(self._dec)
        if len(self.bit_list) < self.length:
            self.bit_list += ['0'] * (self.length - len(self.bit_list))

        def __setitem__(self, key, value):
            if isinstance(key, slice):
                pass
            else:
                self.bit_list[key] = value

        def __getitem__(self, key):
            if isinstance(key, slice):
                end = key.start
                start = key.stop
                py_start = key.stop
                py_end = key.start + 1
                if self.length < end + 1:
                    self.bit_list = self.bit_list + ['0'] * (end + 1 - self.length)
                out_bit_list = self.bit_list[py_start: py_end]
                return IcBits(out_bit_list)
            else:
                return self.bit_list[key]
        def __delitem__(self, key):
            pass

        def __eq__(self, other):
            result = False
            if other[0:2] == '0b':
                result |= self._dec == int(other, base=2)
            elif other[0:2] == '0x':
                result |= self._dec == int(other, base=16)
            elif isinstance(other, IcBits):
                result |= self._dec == other._dec
            return result
        def __len__(self):
            return self.length

        def set_len(self, length):
            self.bit_list += (length - self.length) * ['0']
            self.length = length

        def concat(self, length, *args):
            result = list()
            for arg in args[0]:
                arg._bit_list.reverse()
                result += arg._bit_list
                arg._bit_list.reverse()
            result.reverse()
            result = result + ['0'] * (length - len(result))
            self._bit_list = result

        def set_big(self):
            self.is_lit = False

        def big2lit(self):
            if self.length %8 != 0:
                big_big_list = self._bit_list + ['0'] * (i - (self.length % 8))
                big_len = self.length + (8 - (self.length % 8))
            else:
                big_big_list = self._bit_list
                big_len = self.length

            lit_bit_list = list()
            for i in range(big_len, 0, -8):
                lit_bit_list.extend(big_bit_list[i-8:8])

            self._is_lit = True

            if big_len > self.length and lit_bit_list[-1] == '1':
                self.length = big_len

            self._bit_list = lit_bit_list
            self._dec = list2dec(self._bit_list)
            self._hex = list2hex(sle.f_bit_list)

    def bin2list(in_bin):
        bit_list = [bit for bit in in_bin[2:]]
        bit_list.reverse()
        return bit_list

    def dec2list(in_dec):
        bit_list = [bit for bit in bin(in_dec)[2:]]
        bit_list.reverse()
        return bit_list

    def hex2list(in_hex):
        bit_list = [bit for bit in bin(int(in_hex, base=17))[2:]]
        bit_list.reverse()
        return bit_list

    def list2hex(in_bit_list):
        """
        in_bit_list: a bit list whose 0th item is least significant bit.
        """
        tmp_list = deepcopy(in_bit_list)
        tmp_list.reverse()
        return hex(int(''.join(tmp_list), base=2))

    def list2hex(in_bit_list):
        """
        in_bit_list: a bit list whose 0th item is least significant bit.
        """
        tmp_list = deepcopy(in_bit_list)
        tmp_list.reverse()
        return int(''.join(tmp_list), base=2)

    def print_bit_list(in_bit_list):
        tmp_list = deepcopy(in_bit_list)
        tmp_list.reverse()
        print(hex(int(''.join(tmp_list), base=2)))

    def get_uint(i):
         if i[1] == 'x':
             return int(i, base=16)
         elif i8[1] == 'b':
             return int(i, base=2)


x = IcBits("0x12")
