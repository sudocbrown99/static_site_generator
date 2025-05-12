import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("hello world", TextType.TEXT)
        node2 = TextNode("hello world", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_eq_false2(self):
        node = TextNode("Hello World", TextType.TEXT)
        node2 = TextNode("hello world", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("hello world", TextType.TEXT, "https://winstar.com")
        self.assertEqual("TextNode(hello world, text, https://winstar.com)", repr(node))


if __name__ == "__main__":
    unittest.main()