import unittest

from src.blocks import check_if_markdown_heading, check_if_markdown_code, check_if_markdown_quote, \
    check_if_markdown_unordered_list, check_if_markdown_ordered_list, block_to_block_type, TypeBlock


class TestBlocks(unittest.TestCase):
    def test_check_if_markdown_heading_true(self):
        markdown_block1 = '# Test1'
        markdown_block2 = '### 3'
        markdown_block3 = '###### Test6 ABC'
        markdown_heading1 = check_if_markdown_heading(markdown_block1)
        markdown_heading2 = check_if_markdown_heading(markdown_block2)
        markdown_heading3 = check_if_markdown_heading(markdown_block3)
        self.assertEqual(markdown_heading1, True)
        self.assertEqual(markdown_heading2, True)
        self.assertEqual(markdown_heading3, True)

    def test_check_if_markdown_heading_false(self):
        markdown_block1 = '#Test1'
        markdown_block2 = '######## 3'
        markdown_block3 = 'CC'
        markdown_block4 = 'A ###'
        markdown_heading1 = check_if_markdown_heading(markdown_block1)
        markdown_heading2 = check_if_markdown_heading(markdown_block2)
        markdown_heading3 = check_if_markdown_heading(markdown_block3)
        markdown_heading4 = check_if_markdown_heading(markdown_block4)
        self.assertEqual(markdown_heading1, False)
        self.assertEqual(markdown_heading2, False)
        self.assertEqual(markdown_heading3, False)
        self.assertEqual(markdown_heading4, False)

    def test_check_if_markdown_code_true(self):
        markdown_block1 = '``` Test1 ```'
        markdown_block2 = '```3```'
        markdown_block3 = '```### ABC```'
        markdown_code1 = check_if_markdown_code(markdown_block1)
        markdown_code2 = check_if_markdown_code(markdown_block2)
        markdown_code3 = check_if_markdown_code(markdown_block3)
        self.assertEqual(markdown_code1, True)
        self.assertEqual(markdown_code2, True)
        self.assertEqual(markdown_code3, True)

    def test_check_if_markdown_code_false(self):
        markdown_block1 = '``` Test1'
        markdown_block2 = 'Test1```'
        markdown_block3 = '``CC``'
        markdown_block4 = '```A ###``'
        markdown_code1 = check_if_markdown_code(markdown_block1)
        markdown_code2 = check_if_markdown_code(markdown_block2)
        markdown_code3 = check_if_markdown_code(markdown_block3)
        markdown_code4 = check_if_markdown_code(markdown_block4)
        self.assertEqual(markdown_code1, False)
        self.assertEqual(markdown_code2, False)
        self.assertEqual(markdown_code3, False)
        self.assertEqual(markdown_code4, False)

    def test_check_if_markdown_quote_true(self):
        markdown_block1 = '>Test1'
        markdown_block2 = '>Test1\n>Test2\n>Test3'
        markdown_block3 = '> Test Test Test >Test \n>>test'
        markdown_quote1 = check_if_markdown_quote(markdown_block1)
        markdown_quote2 = check_if_markdown_quote(markdown_block2)
        markdown_quote3 = check_if_markdown_quote(markdown_block3)
        self.assertEqual(markdown_quote1, True)
        self.assertEqual(markdown_quote2, True)
        self.assertEqual(markdown_quote3, True)

    def test_check_if_markdown_quote_false(self):
        markdown_block1 = 'test \n>test'
        markdown_block2 = 'test \n> test'
        markdown_block3 = '>>>test\n>>>test\ntest'
        markdown_block4 = '#>test\n>test'
        markdown_quote1 = check_if_markdown_quote(markdown_block1)
        markdown_quote2 = check_if_markdown_quote(markdown_block2)
        markdown_quote3 = check_if_markdown_quote(markdown_block3)
        markdown_quote4 = check_if_markdown_quote(markdown_block4)
        self.assertEqual(markdown_quote1, False)
        self.assertEqual(markdown_quote2, False)
        self.assertEqual(markdown_quote3, False)
        self.assertEqual(markdown_quote4, False)

    def test_check_if_markdown_unordered_list_true(self):
        markdown_block1 = '- Test1'
        markdown_block2 = '- Test1\n- Test2\n- Test3'
        markdown_block3 = '- Test Test Test -Test \n- -test'
        markdown_unordered_list1 = check_if_markdown_unordered_list(markdown_block1)
        markdown_unordered_list2 = check_if_markdown_unordered_list(markdown_block2)
        markdown_unordered_list3 = check_if_markdown_unordered_list(markdown_block3)
        self.assertEqual(markdown_unordered_list1, True)
        self.assertEqual(markdown_unordered_list2, True)
        self.assertEqual(markdown_unordered_list3, True)

    def test_check_if_markdown_unordered_list_false(self):
        markdown_block1 = 'test \n- test'
        markdown_block2 = '- test\n-test'
        markdown_block3 = '---test\n---test\n---test'
        markdown_block4 = '>- test'
        markdown_unordered_list1 = check_if_markdown_unordered_list(markdown_block1)
        markdown_unordered_list2 = check_if_markdown_unordered_list(markdown_block2)
        markdown_unordered_list3 = check_if_markdown_unordered_list(markdown_block3)
        markdown_unordered_list4 = check_if_markdown_unordered_list(markdown_block4)
        self.assertEqual(markdown_unordered_list1, False)
        self.assertEqual(markdown_unordered_list2, False)
        self.assertEqual(markdown_unordered_list3, False)
        self.assertEqual(markdown_unordered_list4, False)

    def test_check_if_markdown_ordered_list_true(self):
        markdown_block1 = '1. Test1'
        markdown_block2 = '1. Test1\n2. Test2\n3. Test3'
        markdown_block3 = '1. 2. Test Test Test -Test \n2. 2.test'
        markdown_ordered_list1 = check_if_markdown_ordered_list(markdown_block1)
        markdown_ordered_list2 = check_if_markdown_ordered_list(markdown_block2)
        markdown_ordered_list3 = check_if_markdown_ordered_list(markdown_block3)
        self.assertEqual(markdown_ordered_list1, True)
        self.assertEqual(markdown_ordered_list2, True)
        self.assertEqual(markdown_ordered_list3, True)

    def test_check_if_markdown_ordered_list_false(self):
        markdown_block1 = '1. test \n2.test'
        markdown_block2 = '1.test\n2. test'
        markdown_block3 = '1. test\n2. test\n2. test'
        markdown_block4 = '1.. test'
        markdown_ordered_list1 = check_if_markdown_ordered_list(markdown_block1)
        markdown_ordered_list2 = check_if_markdown_ordered_list(markdown_block2)
        markdown_ordered_list3 = check_if_markdown_ordered_list(markdown_block3)
        markdown_ordered_list4 = check_if_markdown_ordered_list(markdown_block4)
        self.assertEqual(markdown_ordered_list1, False)
        self.assertEqual(markdown_ordered_list2, False)
        self.assertEqual(markdown_ordered_list3, False)
        self.assertEqual(markdown_ordered_list4, False)

    def test_block_to_block_type(self):
        markdown_heading = '### Test\nTest'
        markdown_code = '```Test\nTest```'
        markdown_quote = '>Test\n>Test\n> Test'
        markdown_unordered_list = '- Test\n- Test\n- Test'
        markdown_ordered_list = '1. Test\n2. Test\n3. Test'
        markdown_paragraph = 'Test\nTest\nTest'

        block_heading = block_to_block_type(markdown_heading)
        block_code = block_to_block_type(markdown_code)
        block_quote = block_to_block_type(markdown_quote)
        block_unordered_list = block_to_block_type(markdown_unordered_list)
        block_ordered_list = block_to_block_type(markdown_ordered_list)
        block_paragraph = block_to_block_type(markdown_paragraph)

        self.assertEqual(block_heading, TypeBlock.HEADING)
        self.assertEqual(block_code, TypeBlock.CODE)
        self.assertEqual(block_quote, TypeBlock.QUOTE)
        self.assertEqual(block_unordered_list, TypeBlock.UNORDERED_LIST)
        self.assertEqual(block_ordered_list, TypeBlock.ORDERED_LIST)
        self.assertEqual(block_paragraph, TypeBlock.PARAGRAPH)
