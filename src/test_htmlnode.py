import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello world!",
            None,
            {"class": "greeting", "href" : "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"'
        )
    
    def test_to_html_props_2(self):
        node = HTMLNode(
            "p",
            "TOOL rocks",
            None,
            {"id": "body", "href": "https://tool.com"},
        )
        self.assertNotEqual(
            node.props_to_html(),
            'id="body" href="https://tool.com"'
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class" : "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag: p, value: What a strange world, children: None, props: {'class': 'primary'})"
        )
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me", {"href": "https://winstar.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://winstar.com">Click me</a>'
        )
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Howdy Jamie", None)
        self.assertEqual(
            node.to_html(),
            "Howdy Jamie"
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_child_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_tag_error(self):
        child_node = LeafNode("b", "hello")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()

    