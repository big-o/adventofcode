import inspect
from pprint import pformat


class Biterator:
    def __init__(self, val: bytes, offset: int = 0):
        self._val = val
        self._offset = self._idx = offset

    def msb(self, n=1):
        msb = self._extract(n, self._idx)
        return msb

    def popmsb(self, n=1):
        msb = self.msb(n)
        self._idx += n
        return msb

    def consumed(self):
        print(self._offset, self._idx)
        return self._idx - self._offset

    def remainder(self):
        return self.__class__(self._val, self._idx)

    def remaining(self):
        return len(self) + self._offset - self._idx

    def _extract(self, n=1, start=0):
        shift = (8 * len(self._val)) - start - n
        mask = ((1 << n) - 1) << shift
        return (int.from_bytes(self._val, byteorder="big") & mask) >> shift

    def __bytes__(self):
        return self._val

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    def __str__(self):
        return bin(int.from_bytes(self._val, byteorder="big"))[2+self._idx:]

    def __len__(self):
        return (8 * len(self._val)) - self._offset


class BITS:
    def __init__(self, version, payload):
        self.version = version
        self._payload = payload
        self.parse_payload()

    def __repr__(self):
        attribs = inspect.getmembers(self, lambda at: not inspect.isroutine(at))
        overview = ", ".join([f"{k}={pformat(v)}" for k, v in attribs if not k.startswith("_")])
        return f"{self.__class__.__name__}({overview})"

    def __str__(self):
        return repr(self)

    @classmethod
    def parse_header(cls, bits):
        ver = bits.popmsb(3)
        typ = bits.popmsb(3)
        return ver, typ, bits.remainder()

    def parse_payload(self):
        raise NotImplementedError("Abstract method")

    def get_consumed(self):
        return self._payload.consumed()

    def get_remainder(self):
        return self._payload.remainder()


class BITSLiteral(BITS):
    def __init__(self, version, payload):
        super().__init__(version, payload)

    def parse_payload(self):
        value = 0
        data = self._payload
        while data.remaining():
            flag, num = self._payload.popmsb(), self._payload.popmsb(4)
            value <<= 4
            value |= num
            if not flag:
                break

        self.value = value

        return value


class BITSOperator(BITS):
    def __init__(self, version, payload):
        self.subpackets = []
        super().__init__(version, payload)

    def parse_payload(self):
        self.length_type = self._payload.popmsb()
        if self.length_type == 0:
            self.length = self._payload.popmsb(15)
        elif self.length_type == 1:
            self.length = self._payload.popmsb(11)
        else:
            raise ValueError(f"Unknown length type {self.length_type}")

        remaining = self.length
        remainder = self.get_remainder()
        print(remaining)
        while remaining:
            child = BITSParser.from_bits(remainder)
            print(child)
            self.subpackets.append(child)
            if self.length_type == 0:
                remaining -= child.get_consumed()
            else:
                remaining -= 1
            print(remaining)

            remainder = child.get_remainder()

            if remaining < 0:
                raise RuntimeError()


class BITSParser:
    _BITS_TYPE_LITERAL = 0x04

    @classmethod
    def from_hex(cls, data):
        return cls.from_bits(Biterator(bytes.fromhex(data)))

    @classmethod
    def from_bits(cls, payload):
        ver, typ, payload = BITS.parse_header(payload)
        if typ == cls._BITS_TYPE_LITERAL:
            return BITSLiteral(ver, payload)
        else:
            return BITSOperator(ver, payload)


def walk(root):
    yield root
    if not isinstance(root, BITSLiteral):
        for pkt in root.subpackets:
            yield from walk(pkt)

def main(fh):
    data = fh.read().strip()
    print(data)
    pkt = BITSParser.from_hex(data)
    print(pkt)

    versum = 0
    for p in walk(pkt):
        versum += p.version

    return versum


if __name__ == "__main__":
    from aocutils import run

    run(main)
