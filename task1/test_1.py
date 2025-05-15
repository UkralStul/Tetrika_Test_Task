import unittest
from solution import strict

class TestStrictDecorator(unittest.TestCase):

    def test_1(self):
        @strict
        def func(a: int, b: str):
            return f"{a}{b}"

        self.assertEqual(func(1, "test"), "1test")

    def test_2(self):
        @strict
        def func(a: int, b: str):
            return f"{a}{b}"

        self.assertEqual(func(a=1, b="test"), "1test")

    def test_3(self):
        @strict
        def func(a: int, b: str, c: bool):
            return f"{a}{b}{c}"

        self.assertEqual(func(1, b="test", c=True), "1testTrue")

    def test_4(self):
        @strict
        def func(a: int, b: int):
            return a + b

        with self.assertRaisesRegex(TypeError, "Аргумент 'b' имеет некорректный тип: ожидался int, получен str"):
            func(1, "2")

    def test_5(self):
        @strict
        def func(a: int, b: str):
            return f"{a}{b}"

        with self.assertRaisesRegex(TypeError, "Аргумент 'b' имеет некорректный тип: ожидался str, получен int"):
            func(a=1, b=2)

    def test_6(self):
        @strict
        def func(flag: bool):
            return flag

        self.assertTrue(func(True))
        with self.assertRaisesRegex(TypeError, "Аргумент 'flag' имеет некорректный тип: ожидался bool, получен int"):
            func(1)

    def test_7(self):
        @strict
        def func(val: int):
            return val

        self.assertEqual(func(10), 10)
        with self.assertRaisesRegex(TypeError, "Аргумент 'val' имеет некорректный тип: ожидался int, получен bool"):
            func(True)

    def test_8(self):
        @strict
        def func(a: int, b: int):
            return a + b

        with self.assertRaisesRegex(TypeError, "Ошибка вызова функции: missing a required argument: 'b'"):
            func(a=1)

    def test_9(self):
        @strict
        def func(a: int):
            return a

        with self.assertRaisesRegex(TypeError, "Ошибка вызова функции: too many positional arguments"):
            func(1, 2)

    def test_10(self):
        @strict
        def func(a: int):
            return a

        with self.assertRaisesRegex(TypeError, "Ошибка вызова функции: got an unexpected keyword argument 'b'"):
            func(a=1, b=2)

    def test_11(self):
        @strict
        def func_no_annotations(a, b):
            return a + b

        self.assertEqual(func_no_annotations(1, 2), 3)
        self.assertEqual(func_no_annotations("a", "b"), "ab")

    def test_12(self):
        @strict
        def func_return_only(a, b) -> str:
            return str(a) + str(b)

        self.assertEqual(func_return_only(1, 2), "12")