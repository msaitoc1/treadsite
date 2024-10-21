from django.test import TestCase
from .models import coffeeShop, coffeeShopSearchDoc, GlobalInvertedIndex

class coffeeShopModel(TestCase):

    def setUp(self):
        """
        sets up data for testing
        """
        self.coffee_shop = coffeeShop.objects.create(
            name="Cozy Cafe",
            desc="A cozy place for coffee lovers.",
            location="123 Coffee St",
            hours="8am - 6pm"
        )
      
    
    def test_clean_word(self):
      word = "Coffee!"
      word2 = "Coffee2!"
      cleaned_word = self.coffee_shop.clean_word(word)
      self.assertEqual(cleaned_word, "coffee")
      self.assertEqual(self.coffee_shop.clean_word(word2), "coffee2")
    
    def test_word_freqs(self):
       words = self.coffee_shop.get_word_freqs()
       check = {}
       check["a"]= 1
       check["cozy"] = 2
       check["place"]= 1
       check["cafe"] =1 
       check["for"] = 1
       check["coffee"] = 1
       check["lovers"] =1
       self.assertEqual(check, words)
    
    def test_get_total_words(self):
       totalWords = self.coffee_shop.get_total_words()
       self.assertEqual(totalWords, 8)
    
    
class testCoffeeShopSearchDoc(TestCase):
    def setUp(self):
      """
      sets up data for testing
      """
      self.coffee_shop = coffeeShop.objects.create(
         name="Cozy Cafe",
         desc="A cozy place for coffee lovers.",
         location="123 Coffee St",
         hours="8am - 6pm"
      )
      self.search_doc = coffeeShopSearchDoc.objects.create(coffee_shop=self.coffee_shop)
    def test_get_freqs(self):
        """
        tests to see if the word frequencies list is made as expected
        """
        self.search_doc.wordFreqs()
        expected_freqs = {'cozy': 2/8, 'cafe': 1/8, 'a': 1/8, 'place': 1/8, 'for': 1/8, 'coffee': 1/8, 'lovers': 1/8}
        self.assertEqual(self.search_doc.freqs, expected_freqs)
    def test_term_frequency(self):
        """
        Test the term_frequency method to ensure it returns the correct frequency for a word.
        """
        self.search_doc.wordFreqs()  # Ensure frequencies are calculated
        freq = self.search_doc.term_frequency("coffee")
        self.assertEqual(freq, 1/8)
    def test_update_global_inverted_index(self):
        """
        Test if the global inverted index is updated correctly after saving the search document.
        """
        self.search_doc.save()
        index_entry = GlobalInvertedIndex.objects.get(term="coffee")
        self.assertIn(self.coffee_shop.id, index_entry.coffee_shop_ids)
    
    
    class testGlobalInvertedIndex(TestCase):
        def setUp(self):
            """
            sets up data for testing
            """
            self.coffee_shop = coffeeShop.objects.create(
                name="Cozy Cafe",
                desc="A cozy place for coffee lovers.",
                location="123 Coffee St",
                hours="8am - 6pm"
            )
            self.search_doc = coffeeShopSearchDoc.objects.create(coffee_shop=self.coffee_shop)
        def test_inverted_index_creation(self):
            """
            Test if the inverted index is created correctly.
            """
            index_entry = GlobalInvertedIndex.objects.get(term="coffee")
            self.assertEqual(index_entry.term, "coffee")

       
            self.assertIn(self.coffee_shop.id, index_entry.coffee_shop_ids)